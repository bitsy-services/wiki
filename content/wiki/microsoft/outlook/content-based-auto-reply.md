---
title: "Content-Based Auto-Reply"
weight: 20
---

A content-based auto-reply reads each incoming email and sends back a reply whose wording depends on *what the message says* — routing a refund request one way, a password problem another, and leaving anything unrecognized for a human. Where a vacation responder answers everything identically, this is a small event-driven program on top of [Microsoft Graph](/wiki/microsoft/outlook/api): wait to be told a message arrived, fetch it, decide from its content, and reply.

The examples are JavaScript running on [Cloudflare Workers](https://developers.cloudflare.com/workers/). Graph pushes notifications over HTTPS, so this program is a public web endpoint that must be up whenever mail might arrive — which is what a Worker is, without a server to keep alive. The platform also supplies the three other pieces the job needs: [Cron Triggers](https://developers.cloudflare.com/workers/configuration/cron-triggers/) to renew the subscription, [Workers KV](https://developers.cloudflare.com/kv/) for the small amount of state, and [Queues](https://developers.cloudflare.com/queues/) to move the slow work off the webhook. There is no SDK to install: token acquisition and every Graph call are plain `fetch`.

Because no human is signed in, the app authenticates with **application permissions** via the client-credentials flow described on the [API page](/wiki/microsoft/outlook/api#authentication-entra-id-and-oauth-20). Two are enough: `Mail.Read` to subscribe and read, and `Mail.Send` to reply. The `reply` action sends rather than edits, so it needs no write access to the mailbox — do not reach for `Mail.ReadWrite` out of habit.

## The shape of the problem

Four things have to happen, in order:

```text
new email lands in Inbox
        │
        ▼
Graph matches your subscription
        │  HTTPS POST (notification: message id, no body)
        ▼
Worker fetch handler  ──►  GET the message (subject + body)
        │
        ▼
decide from content  ──►  reply?  ──no──►  leave for a human
        │ yes
        ▼
POST /messages/{id}/reply   (Graph composes and sends)
```

Graph does not stream mail. The program registers interest and Graph calls *it* when something changes, so this is not a loop polling for work — it is an HTTPS endpoint that sits idle, costing nothing, until Graph knocks.

## Configuration and bindings

A Worker gets its settings from `env`, the second argument handed to every handler. Non-secret values go in `vars` in the Wrangler config; secrets are set out-of-band with `wrangler secret put` and merely *declared* here, so a deploy fails loudly if one is missing rather than at the first Graph call. Everything else the responder needs — a KV namespace for state, a cron schedule — is a binding in the same file.

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "outlook-autoresponder",
  "main": "src/index.js",
  "compatibility_date": "2026-08-14",
  "observability": { "enabled": true },

  "vars": {
    "TENANT_ID": "...",                              // your Entra ID tenant
    "CLIENT_ID": "...",                              // from the app registration
    "MAILBOX": "support@contoso.com",                // the mailbox this service watches
    "PUBLIC_URL": "https://autoresponder.contoso.com"
  },

  // Set with: wrangler secret put CLIENT_SECRET
  "secrets": { "required": ["CLIENT_SECRET", "SUBSCRIPTION_SECRET"] },

  // Token cache, subscription id, and the set of messages already answered.
  "kv_namespaces": [{ "binding": "STATE", "id": "<namespace-id>" }],

  // Renew the Graph subscription every six hours; see below for why.
  "triggers": { "crons": ["0 */6 * * *"] }
}
```

`SUBSCRIPTION_SECRET` is not a Microsoft credential — it is any hard-to-guess string you invent, and Step 1 explains what it is for.

## The Graph helper

Every call needs a bearer token and the same base URL, so wrap that once and reuse it. A Worker has no long-lived process to hold a cached token in, and module-level state is unreliable — isolates are created and discarded at the platform's discretion — so cache the token in KV instead, expiring your copy a few minutes early so you never present one that has already lapsed.

```js
const GRAPH = "https://graph.microsoft.com/v1.0";

async function accessToken(env) {
  const cached = await env.STATE.get("graph:token");
  if (cached) return cached;

  const resp = await fetch(
    `https://login.microsoftonline.com/${env.TENANT_ID}/oauth2/v2.0/token`,
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: env.CLIENT_ID,
        client_secret: env.CLIENT_SECRET,
        scope: "https://graph.microsoft.com/.default",
        grant_type: "client_credentials",
      }),
    },
  );
  if (!resp.ok) throw new Error(`token request failed: ${resp.status}`);

  const { access_token, expires_in } = await resp.json();
  await env.STATE.put("graph:token", access_token, {
    expirationTtl: Math.max(60, expires_in - 300),
  });
  return access_token;
}
```

The wrapper itself attaches the token, throws on failure, and copes with the fact that some Graph actions answer `202` with no body at all. It also singles out `429` and `5xx` as *retryable*, carrying the server's `Retry-After` along on the error — [the queue consumer](#move-the-work-onto-a-queue) below is where that gets acted on.

```js
async function graph(env, method, path, body) {
  const resp = await fetch(`${GRAPH}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${await accessToken(env)}`,
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const text = await resp.text();
  if (!resp.ok) {
    const err = new Error(`${method} ${path} → ${resp.status} ${text}`);
    err.retryable = resp.status === 429 || resp.status >= 500;
    err.retryAfter = Number(resp.headers.get("Retry-After")) || 30;
    throw err;
  }
  return text ? JSON.parse(text) : null;   // reply returns 202 with an empty body
}
```

## Step 1: Subscribe to the inbox

A **subscription** tells Graph "POST to my URL whenever a message is *created* in this mailbox's inbox." The `clientState` is the secret you chose; Graph echoes it back in every notification so you can confirm the call really came from your subscription and not a stranger who found your URL.

Subscriptions to messages expire in under three days, so this is not a one-time setup step — something has to keep recreating it, forever. A Worker has no startup hook to hang that on; a [Cron Trigger](https://developers.cloudflare.com/workers/configuration/cron-triggers/) invokes the `scheduled` handler on a schedule instead, and one function can both create the subscription the first time and renew it every time after.

```js
// Graph caps message subscriptions just under three days; two is a safe cushion.
const EXPIRY_MS = 2 * 24 * 60 * 60 * 1000;

const expiry = () => new Date(Date.now() + EXPIRY_MS).toISOString();

async function ensureSubscription(env) {
  const id = await env.STATE.get("subscription:id");
  if (id) {
    try {
      await graph(env, "PATCH", `/subscriptions/${id}`, {
        expirationDateTime: expiry(),
      });
      return id;
    } catch {
      // Renewal failed — it expired or was deleted. Fall through and make a
      // new one rather than going quietly deaf.
    }
  }

  const created = await graph(env, "POST", "/subscriptions", {
    changeType: "created",
    notificationUrl: `${env.PUBLIC_URL}/notifications`,
    resource: `users/${env.MAILBOX}/mailFolders('inbox')/messages`,
    expirationDateTime: expiry(),
    clientState: env.SUBSCRIPTION_SECRET,
  });
  await env.STATE.put("subscription:id", created.id);
  return created.id;
}
```

### The validation handshake

The moment you call `POST /subscriptions`, Graph makes a test call *back* to your `notificationUrl` with a `validationToken` query parameter, and expects you to echo that token as plain text, with a `200`, within **10 seconds**. If your endpoint isn't live and correct, the subscription is never created. That fixes the deployment order: the Worker has to be deployed and reachable at `PUBLIC_URL` before the first cron tick can subscribe.

This is the first half of the Worker's `fetch` handler — the notification half arrives in Step 2, and both are assembled into a single working file under [Putting it together](#putting-it-together):

```js
// excerpt — the opening of fetch()
const url = new URL(request.url);
if (request.method !== "POST" || url.pathname !== "/notifications") {
  return new Response("Not found", { status: 404 });
}

const validationToken = url.searchParams.get("validationToken");
if (validationToken !== null) {
  // Subscription setup ping — echo the token back verbatim, as plain text.
  return new Response(validationToken, {
    headers: { "Content-Type": "text/plain" },
  });
}
```

## Step 2: Receive the notification

A real notification is a JSON body with a `value` array — one entry per change.

**Check `clientState`** and drop anything that doesn't match. Compare it with `crypto.subtle.timingSafeEqual` rather than `===`: a plain string comparison returns as soon as two bytes differ, and the time that takes leaks how much of the secret an attacker has guessed. Workers exposes the primitive, but it throws on mismatched lengths, so the usual wrapper compares a value against *itself* and negates the result rather than returning early:

```js
const encoder = new TextEncoder();

function timingSafeEqual(a, b) {
  const aBytes = encoder.encode(a);
  const bBytes = encoder.encode(b);
  if (aBytes.byteLength !== bBytes.byteLength) {
    return !crypto.subtle.timingSafeEqual(aBytes, aBytes);
  }
  return crypto.subtle.timingSafeEqual(aBytes, bBytes);
}
```

**Answer fast**: return `202 Accepted` immediately and do the slow work (fetching, deciding, replying) after the response, because Graph retries any notification it does not see acknowledged within a few seconds. `ctx.waitUntil` is the built-in way to do that — it keeps the invocation alive for work that outlives the response. Note that `ctx` is passed, not destructured; pulling `waitUntil` off it loses its binding and throws at runtime.

```js
// excerpt — the rest of fetch(), where Step 1 left off
const payload = await request.json();
for (const change of payload.value ?? []) {
  if (!timingSafeEqual(change.clientState ?? "", env.SUBSCRIPTION_SECRET)) {
    continue;   // not from our subscription — ignore
  }
  ctx.waitUntil(handleMessage(env, change.resourceData.id));
}
return new Response(null, { status: 202 });
```

`waitUntil` gets you a correct responder; it does not get you a durable one, because work dropped by an error or a 30-second overrun is simply gone. [Moving to a Queue](#move-the-work-onto-a-queue) below fixes that: one line here changes, and a `queue` handler joins the export.

The notification carries an id and little else — not the message body — so the content the decision runs on has to be fetched.

## Step 3: Read the message

Fetch just the fields the decision needs. `body` and `bodyPreview` give you the text; `from` and `internetMessageHeaders` are what keep you out of a [reply loop](#dont-create-a-reply-loop) later.

```js
function fetchMessage(env, messageId) {
  const select = "subject,bodyPreview,body,from,internetMessageHeaders";
  return graph(
    env, "GET", `/users/${env.MAILBOX}/messages/${messageId}?$select=${select}`,
  );
}
```

## Step 4: Decide the reply from its content

The starter version is a keyword matcher; returning `null` means "no confident match — don't reply," which is the safe default.

```js
function composeReply(message) {
  const text = `${message.subject} ${message.bodyPreview}`.toLowerCase();
  if (text.includes("refund")) {
    return "Thanks for reaching out — I've flagged your refund request for " +
           "our billing team, who will follow up within one business day.";
  }
  if (text.includes("password") || text.includes("can't log in")) {
    return "It sounds like a sign-in problem. You can reset your password at " +
           "https://contoso.com/reset — reply here if that doesn't fix it.";
  }
  return null;   // nothing matched; leave it for a human
}
```

Keyword matching is brittle — "I was *not* charged twice" trips the same rule as a real refund. The clean upgrade is to replace the body of `composeReply` with a call to a [large language model](/wiki/ai/llm) that reads the message, classifies its intent, and either drafts a reply or declines. The surrounding machinery — subscribe, fetch, reply — does not change; only the decision does. Keep the "when unsure, return `null`" discipline regardless of how the decision is made: a wrong automated answer costs more than a slightly delayed human one.

## Step 5: Send the reply

The `reply` action composes the response *and sends it*, quoting the original beneath your text and preserving the subject and threading — so you only supply the new body.

```js
function sendReply(env, messageId, text) {
  return graph(env, "POST", `/users/${env.MAILBOX}/messages/${messageId}/reply`, {
    message: { body: { contentType: "Text", content: text } },
  });
}
```

## Putting it together

`handleMessage` is the whole pipeline, and it is where the loop-prevention and de-duplication guards from the next section live:

```js
const REPLIED_TTL = 60 * 60 * 24 * 30;   // remember for 30 days

async function handleMessage(env, messageId) {
  // Graph is at-least-once; see the dedup note below.
  if (await env.STATE.get(`replied:${messageId}`)) return;

  const message = await fetchMessage(env, messageId);
  if (isAutoOrSelf(env, message)) return;   // never answer an auto-message or ourselves

  const reply = composeReply(message);
  if (reply === null) return;

  await sendReply(env, messageId, reply);
  // Remember it, so a redelivery can't reply twice.
  await env.STATE.put(`replied:${messageId}`, "1", { expirationTtl: REPLIED_TTL });
}
```

The default export is where the two excerpts from Steps 1 and 2 join up, and it is the whole of the Worker's public surface — one webhook, one cron:

```js
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (request.method !== "POST" || url.pathname !== "/notifications") {
      return new Response("Not found", { status: 404 });
    }

    const validationToken = url.searchParams.get("validationToken");
    if (validationToken !== null) {
      // Subscription setup ping — echo the token back verbatim, as plain text.
      return new Response(validationToken, {
        headers: { "Content-Type": "text/plain" },
      });
    }

    const payload = await request.json();
    for (const change of payload.value ?? []) {
      if (!timingSafeEqual(change.clientState ?? "", env.SUBSCRIPTION_SECRET)) {
        continue;   // not from our subscription — ignore
      }
      ctx.waitUntil(handleMessage(env, change.resourceData.id));
    }
    return new Response(null, { status: 202 });
  },

  async scheduled(controller, env, ctx) {
    await ensureSubscription(env);
  },
};
```

That is the complete responder. One wrinkle on first run: `wrangler deploy` does *not* subscribe — the `scheduled` handler does, and `"0 */6 * * *"` next fires at 00:00, 06:00, 12:00, or 18:00 UTC. Until then the Worker is deployed, healthy, and receiving nothing, with no error anywhere to explain it. Exercise the handler locally before you go looking for a bug:

```sh
npx wrangler dev --test-scheduled
curl "http://localhost:8787/cdn-cgi/handler/scheduled"
```

## Getting it right in production

### Scope the app to the mailboxes it needs

Do this before the app sees real mail. An application permission like `Mail.Read` grants access to **every mailbox in the tenant** by default, so a leaked `CLIENT_SECRET` reads the whole organization's email — every inbox, not just the one this service watches.

Exchange Online contains it with **RBAC (role-based access control) for Applications**: register a pointer to the app's service principal, define a scope naming the mailboxes it may touch, and assign a role across that scope.

```powershell
New-ServicePrincipal -AppId <client-id> -ObjectId <service-principal-object-id> `
  -DisplayName "Outlook auto-responder"

New-ManagementScope -Name "Autoresponder mailboxes" `
  -RecipientRestrictionFilter "MemberOfGroup -eq '<group-distinguished-name>'"

New-ManagementRoleAssignment -App <service-principal-object-id> `
  -Role "Application Mail.Read" -CustomResourceScope "Autoresponder mailboxes"
New-ManagementRoleAssignment -App <service-principal-object-id> `
  -Role "Application Mail.Send" -CustomResourceScope "Autoresponder mailboxes"
```

**RBAC grants are additive to the tenant-wide consent in Entra ID, not a replacement for it.** Leave `Mail.Read` consented in Entra and the app's effective access is the union of the two — unscoped, exactly as it was before the scope was defined. Remove the Entra consent, verify with `Test-ServicePrincipalAuthorization -Identity <app> -Resource <mailbox>`, and expect up to two hours for permission changes to clear the cache.

The older mechanism, `New-ApplicationAccessPolicy` with a mail-enabled security group, still works and still constrains Entra-granted permissions — which RBAC does not. But Microsoft states RBAC for Applications replaces it, so new work belongs above.

### Don't create a reply loop

A responder that answers a message which was *itself* automated — another auto-responder, a mailing list, a bounce — volleys with it at machine speed until something breaks: a flooded mailbox, a throttled domain, a listing on a blocklist. Guard on the way *in*, before you ever reply:

```js
function isAutoOrSelf(env, message) {
  const sender = message.from?.emailAddress?.address?.toLowerCase() ?? "";
  if (sender === env.MAILBOX.toLowerCase()) return true;   // our own sent copy

  const headers = new Map(
    (message.internetMessageHeaders ?? []).map((h) => [h.name.toLowerCase(), h.value]),
  );
  // RFC 3834: automated mail marks itself so responders can stand down.
  if ((headers.get("auto-submitted") ?? "no").toLowerCase().startsWith("auto")) {
    return true;
  }
  return headers.has("x-auto-response-suppress");
}
```

Skip your own outgoing mail, skip anything already marked automated, and — belt and braces — never reply twice to the same thread. Being a well-behaved responder also means marking your *own* replies as automated so the system on the other end stands down; you can add a custom `x-` header for that purpose to the reply's `internetMessageHeaders`.

### Never let the subscription lapse

A message subscription lives under three days and then goes silent — no error, just no more notifications, and mail that arrives in the gap is never seen again. `ensureSubscription` handles both halves of that, but the cadence matters: cron changes take up to fifteen minutes to propagate across Cloudflare's network, and a tick that fails takes the next interval to come around again. Renewing every six hours against a two-day expiry means seven consecutive failures before anything is missed.

Cron invocations are billed and logged separately from requests; **Cron Events** in the dashboard shows each tick and whether the handler threw, which is the first place to look when notifications stop arriving.

### Move the work onto a Queue

`ctx.waitUntil` runs the pipeline after the response, but nothing catches it if it fails — a transient Graph error means that email is silently never answered. [Queues](https://developers.cloudflare.com/queues/) supply retries, a delay knob, and a dead-letter queue for the ones that never succeed. Add both ends of the queue to the Wrangler config:

```jsonc
  "queues": {
    "producers": [{ "binding": "MAIL_QUEUE", "queue": "inbound-mail" }],
    "consumers": [{
      "queue": "inbound-mail",
      "max_batch_size": 10,
      "max_retries": 5,
      "dead_letter_queue": "inbound-mail-dlq"
    }]
  }
```

The webhook now only enqueues, and a `queue` handler does the work. Because a failed message can be handed back for another attempt, this is also the natural home for the `Retry-After` the Graph helper captured:

```js
  // in fetch(), replacing the ctx.waitUntil call:
  await env.MAIL_QUEUE.send({ messageId: change.resourceData.id });

  // and alongside it in the default export:
  async queue(batch, env, ctx) {
    for (const message of batch.messages) {
      try {
        await handleMessage(env, message.body.messageId);
        message.ack();
      } catch (err) {
        console.error(JSON.stringify({
          event: "handle_failed", id: message.body.messageId, error: String(err),
        }));
        // Throttled: wait exactly as long as Graph asked. Anything else: back
        // off, and let max_retries carry it to the dead-letter queue.
        message.retry({ delaySeconds: err.retryable ? err.retryAfter : 60 });
      }
    }
  },
```

Acknowledge and retry per message rather than letting an exception escape the loop — an uncaught throw leaves the *rest* of the batch unacknowledged, so one poisonous message drags nine healthy ones through the retry cycle with it.

### Expect duplicate and repeated notifications

Graph aims for at-least-once delivery, not exactly-once: the same `created` event can arrive more than once, and a retry after a slow response will redeliver. Queues are at-least-once too, so adding one gives you a second source of duplicates rather than fewer. Without a guard, that means replying twice — which is what the `replied:` key in `handleMessage` is for.

KV is the pragmatic store for that marker. Writes are visible immediately in the location that made them and within about sixty seconds everywhere else, so KV reliably stops a *redelivery minutes later* and does not stop two copies of the same notification landing in two cities at once. If a double reply is genuinely unacceptable rather than merely embarrassing, move the marker to a [Durable Object](https://developers.cloudflare.com/durable-objects/) keyed by message id, or to a D1 row with a unique constraint — both give you a single serialization point that KV, by design, does not.

### Honor throttling

Under load Graph returns `429 Too Many Requests` with a `Retry-After` header, as noted on the [API page](/wiki/microsoft/outlook/api#throttling). Treat it as routine: wait the stated interval and retry rather than hammering, or a burst of inbound mail will turn into a burst of failures.

A Worker is the wrong place to wait out that interval — there is no sleep worth paying for, and holding an invocation open burns wall-clock time against the limits. Hand the waiting to the platform instead: `message.retry({ delaySeconds })` above puts the message back with the delay Graph asked for and costs nothing in between. Cap the consumer's `max_concurrency` if a large inbound batch keeps tripping the limit in the first place.

## External references

- [Microsoft Graph change notifications overview](https://learn.microsoft.com/en-us/graph/change-notifications-overview)
- [Create subscription (Microsoft Graph API)](https://learn.microsoft.com/en-us/graph/api/subscription-post-subscriptions)
- [message: reply (Microsoft Graph API)](https://learn.microsoft.com/en-us/graph/api/message-reply)
- [RBAC for Applications in Exchange Online](https://learn.microsoft.com/en-us/exchange/permissions-exo/application-rbac) — scoping app permissions to specific mailboxes
- [RFC 3834 — Recommendations for Automatic Responses to Electronic Mail](https://www.rfc-editor.org/rfc/rfc3834)
- [Cloudflare Workers best practices](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/)
- [Wrangler configuration reference](https://developers.cloudflare.com/workers/wrangler/configuration/)
- [`timingSafeEqual` in the Workers Web Crypto API](https://developers.cloudflare.com/workers/runtime-apis/web-crypto/#timingsafeequal)

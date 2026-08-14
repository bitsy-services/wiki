---
title: "Content-Based Auto-Reply"
weight: 20
---

A common request: when an email arrives, read it, and send back a reply whose wording depends on *what the message says* — route a refund request one way, a password problem another, and leave anything unrecognized for a human. This is more than a vacation responder, which answers everything identically. It is a small event-driven program on top of [Microsoft Graph](/wiki/microsoft/outlook/api): wait to be told a message arrived, fetch it, decide from its content, and reply. This page builds that program end to end and then covers the ways it bites you in production.

The examples are Python, using [`msal`](https://learn.microsoft.com/en-us/entra/msal/python/) for tokens, [`httpx`](https://www.python-httpx.org/) for HTTP, and [FastAPI](https://fastapi.tiangolo.com/) for the webhook. Because no human is signed in, the app authenticates with **application permissions** (`Mail.ReadWrite` and `Mail.Send`) via the client-credentials flow described on the [API page](/wiki/microsoft/outlook/api#authentication-entra-id-and-oauth-20).

## The shape of the problem

Four things have to happen, in order:

```text
new email lands in Inbox
        │
        ▼
Graph matches your subscription
        │  HTTPS POST (notification: message id, no body)
        ▼
your webhook  ──►  GET the message (subject + body)
        │
        ▼
decide from content  ──►  reply?  ──no──►  leave for a human
        │ yes
        ▼
POST /messages/{id}/reply   (Graph composes and sends)
```

The one non-obvious step is the first: Graph does not stream you mail. You register interest, and it calls *you* when something changes. So the program is a web server that waits for Graph to knock.

## The Graph helper

Every call needs a bearer token and the same base URL, so wrap that once and reuse it. `msal` caches tokens internally, so calling `acquire_token_for_client` per request is cheap — it only hits the network when the cached token is near expiry.

```python
import msal
import httpx

TENANT_ID = "..."                     # your Entra ID tenant
CLIENT_ID = "..."                     # from the app registration
CLIENT_SECRET = "..."                 # a secret or, better, a certificate
MAILBOX = "support@contoso.com"       # the mailbox this service watches
SUBSCRIPTION_SECRET = "..."           # any hard-to-guess string; see below

_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET,
)

def _token() -> str:
    result = _app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    return result["access_token"]

def graph(method: str, path: str, **kwargs) -> httpx.Response:
    resp = httpx.request(
        method,
        f"https://graph.microsoft.com/v1.0{path}",
        headers={"Authorization": f"Bearer {_token()}"},
        **kwargs,
    )
    resp.raise_for_status()
    return resp
```

## Step 1: Subscribe to the inbox

A **subscription** tells Graph "POST to my URL whenever a message is *created* in this mailbox's inbox." The `clientState` is a secret you choose; Graph echoes it back in every notification so you can confirm the call really came from your subscription and not a stranger who found your URL.

```python
from datetime import datetime, timedelta, timezone

def subscribe() -> dict:
    body = {
        "changeType": "created",
        "notificationUrl": "https://autoresponder.contoso.com/notifications",
        "resource": f"users/{MAILBOX}/mailFolders('inbox')/messages",
        # Message subscriptions max out under 3 days; two is a safe cushion.
        "expirationDateTime":
            (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        "clientState": SUBSCRIPTION_SECRET,
    }
    return graph("POST", "/subscriptions", json=body).json()
```

### The validation handshake

The moment you call `POST /subscriptions`, Graph makes a test call *back* to your `notificationUrl` with a `validationToken` query parameter, and expects you to echo that token as plain text, with a `200`, within **10 seconds**. If your endpoint isn't live and correct, the subscription is never created. So the webhook has to handle validation before it can handle notifications:

```python
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.post("/notifications")
async def notifications(request: Request):
    validation_token = request.query_params.get("validationToken")
    if validation_token is not None:
        # Subscription setup ping — echo the token back verbatim.
        return Response(content=validation_token, media_type="text/plain")
    # ...otherwise it's a real notification; handled in Step 2.
```

## Step 2: Receive the notification

A real notification is a JSON body with a `value` array — one entry per change. Two rules matter here. First, **check `clientState`** and drop anything that doesn't match. Second, **answer fast**: return `202 Accepted` immediately and do the slow work (fetching, deciding, replying) elsewhere, because Graph times out and retries if you dawdle. In a real deployment you would hand each message id to a queue; the inline call below keeps the example readable.

```python
    payload = await request.json()
    for change in payload.get("value", []):
        if change.get("clientState") != SUBSCRIPTION_SECRET:
            continue  # not from our subscription — ignore
        message_id = change["resourceData"]["id"]
        handle_message(message_id)   # offload to a queue in production
    return Response(status_code=202)
```

Notice what the notification does *not* contain: the message body. It carries an id and little else, so the content you need for the decision has to be fetched.

## Step 3: Read the message

Fetch just the fields the decision needs. `body` and `bodyPreview` give you the text; `from` and `internetMessageHeaders` are what keep you out of a [reply loop](#dont-create-a-reply-loop) later.

```python
def fetch(message_id: str) -> dict:
    fields = "subject,bodyPreview,body,from,internetMessageHeaders"
    return graph(
        "GET", f"/users/{MAILBOX}/messages/{message_id}?$select={fields}"
    ).json()
```

## Step 4: Decide the reply from its content

This is the part that makes the responder *content-based*. The starter version is a keyword matcher; returning `None` means "no confident match — don't reply," which is the safe default.

```python
def compose_reply(message: dict) -> str | None:
    text = f"{message['subject']} {message['bodyPreview']}".lower()
    if "refund" in text:
        return ("Thanks for reaching out — I've flagged your refund request "
                "for our billing team, who will follow up within one business day.")
    if "password" in text or "can't log in" in text:
        return ("It sounds like a sign-in problem. You can reset your password "
                "at https://contoso.com/reset — reply here if that doesn't fix it.")
    return None  # nothing matched; leave it for a human
```

Keyword matching is brittle — "I was *not* charged twice" trips the same rule as a real refund. The clean upgrade is to replace the body of `compose_reply` with a call to a [large language model](/wiki/ai/llm) that reads the message, classifies its intent, and either drafts a reply or declines. The surrounding machinery — subscribe, fetch, reply — does not change; only the decision does. Keep the "when unsure, return `None`" discipline regardless of how the decision is made: a wrong automated answer costs more than a slightly delayed human one.

## Step 5: Send the reply

The `reply` action composes the response *and sends it*, quoting the original beneath your text and preserving the subject and threading — so you only supply the new body.

```python
def send_reply(message_id: str, text: str) -> None:
    body = {"message": {"body": {"contentType": "Text", "content": text}}}
    graph("POST", f"/users/{MAILBOX}/messages/{message_id}/reply", json=body)
```

## Putting it together

`handle_message` is the whole pipeline, and it is where the loop-prevention and de-duplication guards from the next section live:

```python
def handle_message(message_id: str) -> None:
    if already_replied(message_id):  # Graph is at-least-once; see the dedup note below
        return
    message = fetch(message_id)
    if is_auto_or_self(message):     # never answer an auto-message or ourselves
        return
    reply = compose_reply(message)
    if reply is not None:
        send_reply(message_id, reply)
        record_reply(message_id)     # remember it, so a redelivery can't reply twice
```

That is the complete responder: `subscribe()` once at startup, then the webhook drives `handle_message` for each new mail. What is left is everything that turns a demo into something you can leave running.

## Getting it right in production

### Don't create a reply loop

This is the failure that does real damage. If your responder answers a message that was *itself* automated — another auto-responder, a mailing list, a bounce — the two systems can volley forever, and you can flood a mailbox, get your domain throttled, or land on a blocklist. Guard on the way *in*, before you ever reply:

```python
def is_auto_or_self(message: dict) -> bool:
    sender = message["from"]["emailAddress"]["address"].lower()
    if sender == MAILBOX.lower():
        return True   # our own sent copy — never reply to ourselves
    headers = {h["name"].lower(): h["value"]
               for h in message.get("internetMessageHeaders", [])}
    # RFC 3834: automated mail marks itself so responders can stand down.
    if headers.get("auto-submitted", "no").lower().startswith("auto"):
        return True
    if "x-auto-response-suppress" in headers:
        return True
    return False
```

Skip your own outgoing mail, skip anything already marked automated, and — belt and braces — never reply twice to the same thread. Being a well-behaved responder also means marking your *own* replies as automated so the system on the other end stands down; you can add a custom `x-` header for that purpose to the reply's `internetMessageHeaders`.

### Scope the app to the mailboxes it needs

An application permission like `Mail.ReadWrite` grants access to **every mailbox in the tenant** by default — far more than an auto-responder for one support address should hold. Contain it with an **Application Access Policy** in Exchange Online PowerShell, tying the app to a mail-enabled security group that contains only the mailboxes it may touch:

```powershell
New-ApplicationAccessPolicy -AppId <client-id> `
  -PolicyScopeGroupId autoresponder-mailboxes@contoso.com `
  -AccessRight RestrictAccess `
  -Description "Auto-responder: support mailbox only"
```

Now a leaked secret exposes one mailbox instead of the whole organization. This is the single most important hardening step, so do it before the app sees real mail.

### Renew subscriptions before they expire

A message subscription lives under three days and then goes silent — no error, just no more notifications. Run a timer that `PATCH`es a fresh expiry well before the deadline, and recreate the subscription if a renewal ever fails, since a lapse means missed mail during the gap.

```python
def renew(subscription_id: str) -> None:
    body = {"expirationDateTime":
            (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()}
    graph("PATCH", f"/subscriptions/{subscription_id}", json=body)
```

### Expect duplicate and repeated notifications

Graph aims for at-least-once delivery, not exactly-once: the same `created` event can arrive more than once, and a retry after a slow response will redeliver. Without a guard, that means replying twice. This is what the `already_replied` / `record_reply` pair in `handle_message` above is for — back them with a persistent store (a database row, a Redis set) keyed by message id, so that once a reply has gone out, any redelivery short-circuits before it can send another. An in-memory set is not enough; a restart would forget every id and re-reply to whatever redelivers.

### Honor throttling

Under load Graph returns `429 Too Many Requests` with a `Retry-After` header, as noted on the [API page](/wiki/microsoft/outlook/api#throttling). Treat it as routine: wait the stated interval and retry rather than hammering, or a burst of inbound mail will turn into a burst of failures.

## External references

- [Microsoft Graph change notifications overview](https://learn.microsoft.com/en-us/graph/change-notifications-overview)
- [Create subscription (Microsoft Graph API)](https://learn.microsoft.com/en-us/graph/api/subscription-post-subscriptions)
- [message: reply (Microsoft Graph API)](https://learn.microsoft.com/en-us/graph/api/message-reply)
- [Limit application permissions to specific mailboxes](https://learn.microsoft.com/en-us/graph/auth-limit-mailbox-access)
- [RFC 3834 — Recommendations for Automatic Responses to Electronic Mail](https://www.rfc-editor.org/rfc/rfc3834)

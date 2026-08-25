---
title: "The Outlook Mail API"
weight: 10
---

Programmatic access to an Outlook mailbox — reading mail, sending mail, watching for new messages, managing the calendar — goes through **Microsoft Graph**, a single REST API over HTTPS that fronts all of Microsoft 365. A handful of older interfaces still exist for narrow jobs, but Graph is the only one that reaches every mailbox resource and the only one still gaining features, so the rest of this section assumes it.

## Microsoft Graph, in one endpoint

Every Graph call is an HTTPS request to `https://graph.microsoft.com`, versioned by a path segment (`/v1.0` for production, `/beta` for preview features). The mailbox resources from the [overview](/wiki/microsoft/outlook) hang off a user:

```http
GET https://graph.microsoft.com/v1.0/users/{id}/messages
GET https://graph.microsoft.com/v1.0/users/{id}/mailFolders('inbox')/messages
GET https://graph.microsoft.com/v1.0/users/{id}/events
```

`{id}` is a user's object ID or their user principal name (usually their email address, like `alex@contoso.com`). When a real person is signed in and your code is acting *as them*, the shorthand `/me` stands in for `/users/{their-id}` — but a background service with no signed-in user must name the mailbox explicitly with `/users/{id}`. Which of the two applies is decided by how the app authenticates.

Responses are JSON shaped by the [OData](https://www.odata.org/) conventions Graph follows: `$select` to choose fields, `$filter` to narrow results, `$top` to page. A message carries its entire `body`, so a listing without `$select` transfers every message in full just to decide which one is worth reading:

```http
GET /v1.0/users/alex@contoso.com/messages?$select=subject,from,receivedDateTime&$top=25
```

Microsoft publishes **SDKs** (C#, Python, JavaScript/TypeScript, Java, Go, PHP) that wrap these calls in typed methods, plus a browser-based [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) for trying requests against a sandbox tenant. The SDKs are thin over the REST surface above, so the raw calls are what any of them reduce to.

## Authentication: Entra ID and OAuth 2.0

Graph does not have its own logins. It trusts **Microsoft Entra ID** (the identity service formerly called Azure Active Directory), and access is granted through [OAuth 2.0](https://oauth.net/2/): your code obtains a short-lived **access token** from Entra ID and sends it on every request as `Authorization: Bearer <token>`.

Before any of that, the application must be **registered** in Entra ID, which yields a client ID (and, for confidential apps, a client secret or certificate). Registration is also where the app declares which **permissions** it needs, in one of two kinds:

- **Delegated permissions** — the app acts *on behalf of a signed-in user* and can only touch what that user can. A user signs in interactively and consents. Use this for apps a person drives (a desktop tool, a web app with a login).
- **Application permissions** — the app acts *as itself*, with no user present, using the [OAuth client-credentials flow](https://oauth.net/2/grant-types/client-credentials/). A tenant administrator consents once. Use this for daemons, cron jobs, and webhook processors — anything that runs unattended. By default an app permission grants access to *every* mailbox in the tenant, so a leaked client secret reads the whole organization's mail (see [least privilege](/wiki/microsoft/outlook/content-based-auto-reply#scope-the-app-to-the-mailboxes-it-needs) in the walkthrough).

Either way, the specific rights are named **scopes**. The ones this section uses:

| Scope | Grants |
|-------|--------|
| `Mail.Read` | Read messages |
| `Mail.ReadWrite` | Read, create, update, delete messages and drafts |
| `Mail.Send` | Send mail as the mailbox |
| `MailboxSettings.Read` | Read automatic-reply and other mailbox settings |

Delegated scopes take a "least of the two" rule — the effective access is the intersection of what the app was granted and what the user themselves can do.

Unattended apps name the same rights differently. The client-credentials flow does not request these scopes one at a time; it asks for the single resource scope `https://graph.microsoft.com/.default`, which means "every application permission an administrator has already consented to for this app." The specific rights — `Mail.Read`, `Mail.Send` — are still chosen at registration and consented there; `.default` is how the token request names that whole pre-approved set at once, and why the [walkthrough](/wiki/microsoft/outlook/content-based-auto-reply) requests it rather than the named scopes above.

## The six calls mail automation needs

Everything in the [auto-reply walkthrough](/wiki/microsoft/outlook/content-based-auto-reply) is built from these:

| Goal | Request |
|------|---------|
| List inbox messages | `GET /users/{id}/mailFolders('inbox')/messages` |
| Read one message | `GET /users/{id}/messages/{messageId}` |
| Send a new message | `POST /users/{id}/sendMail` |
| Reply to a message | `POST /users/{id}/messages/{messageId}/reply` |
| Draft a reply (send later) | `POST /users/{id}/messages/{messageId}/createReply` |
| Watch for changes | `POST /subscriptions` |

`reply` composes *and sends* in one call, quoting the original beneath the new text. `createReply` instead returns a draft to edit and send separately — useful when the reply body is assembled in stages. Both fill in the original message's subject, recipients, and quoted history.

## Reacting to new mail: notifications vs. polling

Automation usually needs to *act when something arrives*, and Graph offers two ways to learn that it did:

- **Change notifications (webhooks)** — you create a **subscription** to a resource (say, the inbox), and Graph sends an HTTPS POST to your endpoint whenever a matching change happens. Push-based, near-real-time, and the basis of the [auto-reply walkthrough](/wiki/microsoft/outlook/content-based-auto-reply). The catch is that your endpoint must be publicly reachable and subscriptions expire and must be renewed.
- **Delta queries** — you call `GET /users/{id}/mailFolders('inbox')/messages/delta`, and Graph returns a token; presenting that token on the next call returns only what changed since. Pull-based, no public endpoint required, at the cost of polling latency and running the loop yourself.

Push for responsiveness, poll for simplicity. The walkthrough uses push.

## The older paths, and when they still fit

Graph is the default, but three predecessors survive:

- **Exchange Web Services (EWS)** — the previous-generation SOAP API. Microsoft is **retiring EWS for Exchange Online on 1 October 2026** and has stopped adding features to it, so new work should not start here; it remains relevant only for on-premises Exchange Server, which Graph does not cover.
- **The Outlook desktop object model (COM/VBA/VSTO)** — automates the *classic* Outlook application installed on a Windows machine, in-process. It is the right tool for a macro that manipulates what the user sees in their running client, and the wrong tool for anything server-side. Note that the new Outlook for Windows drops COM support in favor of web add-ins.
- **IMAP, POP, and SMTP** — the open standards. Exchange Online still speaks them (now requiring OAuth, since Basic authentication was disabled), which is handy for cross-platform mail libraries, but they only see mail — no calendar, contacts, or change notifications. Reach for them for portability, not capability.

## Throttling

Graph enforces per-app, per-mailbox rate limits and answers a request that exceeds them with `429 Too Many Requests` and a `Retry-After` header. Treat `429` (and transient `503`/`504`) as expected, not exceptional: honor `Retry-After`, back off exponentially, and design batch jobs to spread load rather than burst it.

## External references

- [Microsoft Graph REST API reference](https://learn.microsoft.com/en-us/graph/api/overview) — the authoritative endpoint documentation
- [Working with Outlook mail in Microsoft Graph](https://learn.microsoft.com/en-us/graph/outlook-mail-concept-overview)
- [Register an application with the Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)
- [Microsoft identity platform and OAuth 2.0](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
- [Set up notifications for changes in resource data](https://learn.microsoft.com/en-us/graph/change-notifications-overview)
- [Retirement of Exchange Web Services in Exchange Online](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/exchange-web-services/retirement-of-exchange-web-services-in-exchange-online)

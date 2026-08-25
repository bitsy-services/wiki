---
title: "Outlook"
weight: 10
bookCollapseSection: true
---

Outlook is Microsoft's email, calendar, and contacts client — and, for the purposes of these pages, the front end to a **mailbox** hosted in Microsoft 365. Automating Outlook almost never means automating the app sitting on someone's desktop; it means talking to the mailbox behind it over a web API. Every copy of Outlook — the Windows program, the website, the phone app — is another view of that same server-side data, so a program that reads and sends mail works no matter which Outlook the human happens to be looking at, or whether one is open at all.

This section covers that programmatic access: the [API surface](/wiki/microsoft/outlook/api) Microsoft exposes for a mailbox, and worked patterns built on top of it — beginning with [replying to incoming mail based on what it says](/wiki/microsoft/outlook/content-based-auto-reply).

## "Outlook" names several different things

The name covers several products, and only one of them can be automated in-process:

- **Classic Outlook for Windows** — the long-standing desktop application. It is the only Outlook with the COM/VBA object model, so it is what people mean by "automating Outlook with a macro."
- **New Outlook for Windows** and **Outlook on the web** (OWA) — web applications. They have no COM model; they extend through web add-ins and call the same web API your own code would.
- **Outlook mobile** — the iOS and Android apps.
- **Outlook.com** — the free consumer mail service (personal Microsoft accounts), as opposed to a Microsoft 365 organizational mailbox.

All of them are windows onto a mailbox that lives in **Exchange Online** (the mail server inside Microsoft 365) or, for some organizations, an on-premises Exchange Server. The client is interchangeable; the mailbox is what automation targets.

## What lives in a mailbox

Beyond the inbox, a mailbox holds four categories of item that code can address:

- **Messages** — individual emails, each in a **mail folder** (`Inbox`, `Sent Items`, `Drafts`, and any user-created folders).
- **Calendar events** — with attendees, times, and recurrence.
- **Contacts** — people and their details.
- **Tasks and notes** — lighter-weight items.

Each is a resource the API can list, read, create, and change, and each can raise a notification when it changes.

## Talking to it in code

Modern access goes through one REST API — **Microsoft Graph** — with older, narrower paths (Exchange Web Services, the desktop COM model, standard IMAP/SMTP) still around for specific jobs. The [API page](/wiki/microsoft/outlook/api) covers the Graph surface, how authentication works, and where those older paths still fit; the [auto-reply walkthrough](/wiki/microsoft/outlook/content-based-auto-reply) puts Graph to work on a concrete, event-driven task.

## Wiki Pages

{{< section >}}

---
title: "Getting a Message's Raw Source"
weight: 30
---

## What "raw" means in Outlook

An email on the wire is one text document: a block of headers, a blank line,
and a body, laid out as RFC 5322 plus Multipurpose Internet Mail Extensions
(MIME) for anything beyond plain 7-bit text. Neither classic
[Outlook](/wiki/microsoft/outlook) for Windows nor the Exchange mailbox behind
it (Exchange is Microsoft's mail server, Exchange Online in Microsoft 365)
stores a message that way. Exchange converts the incoming MIME on arrival
into a set of **Messaging Application Programming Interface (MAPI)**
properties — one for the subject, one for the HTML body, one per attachment,
and one holding the original header block verbatim — and discards the wire
bytes. Outlook's local cache holds the same properties. So the client can show
the headers exactly as received, and a body it regenerates from the stored
properties, but never the original file. That is why classic Outlook has three
separate places to look instead of one *view source* command, and why the full
MIME view lives in the web client, new Outlook and the API rather than in
classic Outlook.

| You want | Where it is |
| --- | --- |
| The header block (`Received:` chain, authentication results, `Message-ID:`) | File > Properties, *Internet headers* box |
| The body's HTML | Actions > Other Actions > View Source |
| A complete copy of the item | File > Save As, `.msg` |
| A real MIME file (`.eml`) | New Outlook, Outlook on the web, or Microsoft Graph |

## The headers: the Properties dialog

1. Open the message in its own window by double-clicking it in the list.
2. Choose **File > Properties**. From the reading pane, the same dialog opens
   from the small arrow in the bottom-right corner of the **Tags** group on the
   **Message** tab.
3. The **Internet headers** box at the bottom of the dialog holds the header
   block. Click into it, then Ctrl+A and Ctrl+C.

The box is a few lines tall and cannot be resized, but the copy takes the whole
block. It is the header block as Exchange received it, which is what a delivery
or spam investigation needs: every `Received:` hop, the
`Authentication-Results:` line carrying the sender-authentication verdicts,
DomainKeys Identified Mail (DKIM) among them, and the `Message-ID:`. Microsoft's
[Message Header Analyzer](https://mha.azurewebsites.net/) parses a pasted block
into a hop-by-hop table with per-hop delays, and the
[add-in of the same name](https://appsource.microsoft.com/en-us/product/office/WA104005406)
puts that table on a ribbon button inside Outlook so the copy-and-paste step
disappears.

Items in *Sent Items* and *Drafts* have an empty box. The Sent Items copy is
written at submission, before the message reaches transport, so nothing has
been stamped on it yet.

## The body: View Source

For an HTML-formatted message, **Message > Actions > Other Actions > View
Source** opens the body's HTML in Notepad, or in whatever program Windows has
registered for editing HTML. In the simplified ribbon, *Actions* sits behind
the **⋯** at the ribbon's right end. The command is greyed out for plain-text
messages, and it shows the body alone with no headers.

This is the view for the questions the rendered message hides: the real `href`
behind a link's display text, a one-pixel tracking image, `cid:` references to
inline attachments, and remote content Outlook declined to download.

## The whole item: Save As

**File > Save As** on an open message offers six formats:

| Format | What the file contains |
| --- | --- |
| Outlook Message Format – Unicode (`.msg`) | Every MAPI property of the item, header block and attachments included, in a binary compound-file container documented as `[MS-OXMSG]` |
| Outlook Message Format (`.msg`) | The same, with strings in the legacy code page rather than Unicode |
| Outlook Template (`.oft`) | The same container with a template message class, for opening as the starting point of a new message |
| HTML (`.htm`) | The rendered body, with images written to a sidecar folder |
| MHT files (`.mht`) | The rendered body and its images as one MIME HTML file |
| Text Only (`.txt`) | The plain-text body under a From/Sent/To/Subject block. Not the internet headers |

Dragging a message from the list onto a Windows Explorer folder writes the same
Unicode `.msg`.

There is no `.eml` option. The `.msg` is the closest thing to a complete copy,
and the header block is inside it as the `PidTagTransportMessageHeaders`
property, but the file is not MIME and nothing outside Outlook opens it without
a converter. The Perl `msgconvert` script writes one out as an `.eml`, and
Python's `extract-msg` library re-serializes one as a standard email message
object.

## The MIME stream: new Outlook, the web client, or Graph

New Outlook for Windows and Outlook on the web work directly against the
mailbox, and Exchange will generate MIME on request:

- Open the message and choose **⋯ (More actions) > View > View message
  source**. The dialog shows the header block and the MIME body together, and
  the text can be copied.
- **⋯ > View > View message details** shows the header block alone.
- **⋯ > Save as** in new Outlook, or **Download** in the web client, writes an
  `.eml` file.

The same stream is one call away in code. On the
[Graph mail API](/wiki/microsoft/outlook/api), appending `/$value` to a message
URL returns it as MIME, and `$select=internetMessageHeaders` returns the header
block already parsed into name/value pairs. Both need `Mail.Read`.

```text
GET https://graph.microsoft.com/v1.0/users/{user}/messages/{id}/$value
```

Every one of these paths returns a regeneration, not the sender's bytes. The
header block is verbatim, but the body is re-encoded from the stored
properties, so multipart boundary strings and transfer encodings differ from
what left the sender, and a DKIM signature that covers the body will usually
fail to verify against it. Wire-exact bytes exist only on a system that held the
message before Exchange ingested it: the sending mail server's copy, or a
third-party gateway in front of the tenant.

## Further reading

- [Get MIME content of a message](https://learn.microsoft.com/en-us/graph/outlook-get-mime-message) — the Graph `$value` endpoint
- [View internet message headers in Outlook](https://support.microsoft.com/en-us/office/view-internet-message-headers-in-outlook-cd039382-dc6e-4264-ac74-c048563d212c) — Microsoft's own walkthrough of the Properties dialog
- [`[MS-OXMSG]`: Outlook Item (.msg) File Format](https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxmsg/b046868c-9fbf-41ae-9ffb-8de2bd4eec82)
- [Content conversion in Exchange](https://learn.microsoft.com/en-us/exchange/mail-flow/content-conversion/content-conversion) — how MIME becomes MAPI and back

---
title: "Nostr"
weight: 30
---

Nostr is a protocol for publishing signed messages through relays. Each user is a key pair on secp256k1, the elliptic curve Bitcoin uses, and each message is an **event**: a small JSON object carrying the author's public key, a timestamp, a numeric kind, a list of tags, a text body, and a signature over all of them. A client signs events with the user's private key and sends them over WebSockets to **relays**, servers that store events and forward them to clients whose subscriptions match. The base protocol defines no messages between relays. Clients check signatures themselves, so a relay can refuse, drop or withhold an event but cannot alter one or forge one under another key.

The name stands for "Notes and Other Stuff Transmitted by Relays". The developer fiatjaf described it in November 2020 as the basis for a censorship-resistant social network, and most of what runs on it is social: profiles, posts, follows and replies. The base protocol knows nothing about any of that. It is specified in short numbered documents called Nostr Implementation Possibilities (NIPs). NIP-01 defines events, relays and the messages between clients and relays. Every other NIP is optional, and the index of the NIPs repository says so plainly: "Nothing forces any software to implement any NIP."

## An event

A complete event, signed with a key generated for this page:

```json
{
  "id": "cd0156048449a56ea2147abf34c2df3200838b70ae068d53f15abe074072fd0d",
  "pubkey": "343bef815181036a6523e2a76b9be8a06d34aeaddcf09e5252ea1b3ff7278d85",
  "created_at": 1790380800,
  "kind": 1,
  "tags": [["t", "networking"]],
  "content": "Signed once, readable from any relay.",
  "sig": "4b57a466d33ed1287ff7a3024d27e6070deada34bf26fce58b021c73edee3a5fa3e5194ba816e6136da94b5798fcfd0a229b355b171d6a241bcb3f22bc07d31f"
}
```

- `pubkey` is the author's public key: 32 bytes, the x-coordinate of the curve point alone, written in lowercase hex. That encoding comes from BIP-340, the Bitcoin Improvement Proposal that also defines the signature scheme.
- `created_at` is a Unix time in seconds, chosen by the author. Nothing checks it except relays that decide to reject implausible values.
- `kind` is an integer from 0 to 65535 that says how to read the rest. Kind 1 is a short text note, the equivalent of a post, and kind 0 is the author's profile.
- `tags` are arrays of strings whose first element is the tag's name. Relays index tags with single-letter names, so a client can ask for every event whose `t` tag is `networking`. Only the first value after the name is indexed.
- `content` is an arbitrary string.
- `id` is the SHA-256 hash of the array `[0, pubkey, created_at, kind, tags, content]`, serialized as JSON with no whitespace.
- `sig` is a 64-byte Schnorr signature, as specified in BIP-340, over the `id`.

The id is a hash of a serialization, so two implementations must turn the same event into the same bytes. NIP-01 fixes the rules: UTF-8, no whitespace, and seven characters in `content` escaped (line feed, double quote, backslash, carriage return, tab, backspace and form feed), with "all other characters" included verbatim. JavaScript's `JSON.stringify` escapes the remaining control characters as well, writing U+0001 as `\u0001`. An event whose content contains one of them therefore hashes to a different id under the two rules, and a verifier using the other rule rejects its signature. It is the disagreement at the root of every [canonicalization attack](/wiki/cs/canonicalization-attack), in a mild form: the two sides reject rather than accept.

## Keys are the accounts

There is no registration. A user's identity is the public key, and whoever holds the private key is that user on every relay at once. Clients display keys in bech32 (NIP-19), a checksummed text encoding whose prefix says what the string is: `npub1…` for a public key, `nsec1…` for a private key, `note1…` for an event id. The prefixes exist so that a person copying a string can tell the one to share from the one to keep. The protocol itself uses only hex.

Three consequences follow.

- **Changing relays keeps the identity.** Followers follow a key, not a server, so a user who moves loses no followers and needs no operator's cooperation. What the move does not carry over is reach: followers' clients still have to learn where the user now publishes, the problem covered under [finding someone's events](#finding-someones-events). fiatjaf's original note sets this against Mastodon, where "user identities are attached to domain names controlled by third-parties" and migration "can only be accomplished if servers cooperate."
- **A lost private key is a lost identity**, and no one can restore it. A leaked one is worse: anyone holding it can sign as the user on every relay, and no NIP in the repository defines a way to revoke a key or move an identity to a new one.
- **Clients try not to hold the key.** NIP-07 defines `window.nostr`, an object a browser extension adds to web pages, which signs events on request so the page never sees the private key. NIP-46 moves signing to a separate program, a remote signer "also known as 'bunker'", and the client asks it for signatures by exchanging encrypted events through a relay.

## Talking to a relay

A client opens one WebSocket to each relay it uses and sends JSON arrays whose first element names the message.

| Direction | Message | Meaning |
|---|---|---|
| client → relay | `["EVENT", event]` | publish an event |
| client → relay | `["REQ", subId, filter, …]` | send stored events that match any of the filters, then keep sending new ones |
| client → relay | `["CLOSE", subId]` | end a subscription |
| relay → client | `["EVENT", subId, event]` | an event matching subscription `subId` |
| relay → client | `["EOSE", subId]` | end of stored events; everything after this is live |
| relay → client | `["OK", id, true or false, message]` | whether a published event was accepted |
| relay → client | `["CLOSED", subId, message]` | the relay refused or ended a subscription |
| relay → client | `["NOTICE", message]` | a human-readable message |

A filter is an object that can constrain `ids`, `authors`, `kinds`, `#` followed by a single-letter tag name, `since`, `until`, and `limit`, the number of stored events to return. Every condition in one filter must match, and an event matching any one of a request's filters is sent. Fetching the example author's recent notes looks like this:

```text
client → ["REQ", "feed", {"authors": ["343bef815181036a6523e2a76b9be8a06d34aeaddcf09e5252ea1b3ff7278d85"], "kinds": [1], "limit": 20}]
relay  → ["EVENT", "feed", {…}]    up to 20 stored events, newest first
relay  → ["EOSE", "feed"]          end of stored events
relay  → ["EVENT", "feed", {…}]    each new matching event, as it arrives
client → ["CLOSE", "feed"]
```

An `OK` carries `true` if the relay accepted the event and `false` if it did not. A rejection's message starts with a machine-readable word, which NIP-01 standardizes as `duplicate:`, `pow:`, `blocked:`, `rate-limited:`, `invalid:`, `restricted:`, `mute:` or `error:`. NIP-42 adds `auth-required:`.

## What a relay keeps

The kind decides whether a relay stores an event at all. NIP-01 divides the range into four classes:

| Kinds | Class | What a relay does with it |
|---|---|---|
| 1, 2, 4–44, 1000–9999 | regular | stores every one |
| 0, 3, 10000–19999 | replaceable | must keep the latest per author and kind; may discard older ones |
| 20000–29999 | ephemeral | not expected to store it; delivers it to the subscriptions open at that moment |
| 30000–39999 | addressable | must keep the latest per author, kind and `d` tag; may discard older ones |

Replaceable kinds carry state. Kind 0 is the profile and kind 3 the follow list, and publishing a new one supersedes the old, although a relay is allowed to keep the old one and only asked to return the latest. Addressable kinds work the same way per value of the event's `d` tag, an identifier the author chooses, so one author can keep many, such as one per article. Ephemeral kinds carry messages that only matter live, and a client that subscribes a second too late never sees them. Among NIP-01's examples of rejection messages is a relay answering an ephemeral event with `mute: no one was listening to your ephemeral event and it wasn't handled in any way, it was ignored`. The classes are conventions, and NIP-01 ends the list by saying that "relay implementations may differ."

## What a relay can and cannot do

A relay cannot change an event, because the id would no longer match the fields and the signature covers the id. It cannot create an event under someone else's key without that key. Everything else is its operator's choice.

- **What to accept.** A relay can require payment, proof of work, or authentication. Proof of work (NIP-13) means the author varies a `nonce` tag until the event's id starts with a required number of zero bits. Authentication (NIP-42) means the client signs a challenge the relay sent, as an event of kind 22242. A relay states its rules in an information document (NIP-11), a JSON file served from the relay's own URL: the NIPs it supports, and limits such as `max_message_length`, `auth_required` and `payment_required`.
- **What to keep and return.** A relay can delete any event, stop serving it, or answer a query with some matching events and not others. A client cannot tell an omitted event from one that does not exist.
- **What to observe.** Every WebSocket arrives from an IP address, and every subscription says what the client is looking for. NIP-44's list of its own limitations includes "IP address leak: user IP may be seen by relays and all intermediaries between user and relay."

Resistance to censorship therefore comes from redundancy, not from any single relay. A client publishes to several relays and reads from several, so a relay that bans a user removes that user only from its own copy.

Deletion runs into the same structure. NIP-09 defines a deletion request, an event of kind 5 listing the ids to delete, and relays "SHOULD delete or stop publishing" the listed events that were signed by the same key as the request. NIP-09 also lets clients tell users that deletion is not guaranteed, "because it is impossible to delete events from all relays and clients." NIP-40's expiration tag carries the same warning: "don't consider expiring messages as a security feature." A published event is safest treated as permanent.

## Finding someone's events

There is no directory. A client that wants a user's posts has to know which relays hold them, and the protocol's README calls that "the hardest part". It notes that "multiple heuristics" are in use. Several NIPs carry hints, such as a relay URL inside the `e` and `p` tags an event uses to point at another event or user, or inside a shareable NIP-19 identifier, and the most complete scheme is NIP-65: each user publishes a replaceable event of kind 10002 listing relays marked `write`, where the user publishes, and `read`, where the user wants to receive mentions. A client fetches a user's events from that user's write relays, and publishes an event that mentions someone to that person's read relays as well as to its own write relays. NIP-65 asks clients to keep each list to two to four relays, and to spread the kind 10002 event itself as widely as possible, since a client has to find that event before it can find anything else.

A client following many people therefore holds many connections, one to every relay that any of them writes to.

## Private messages

Every event can be read by anyone who can query a relay that holds it, so a private message is an encrypted event. The first scheme, NIP-04, is deprecated; its own security warning says it "leaks metadata in the events". Its replacement, NIP-17, nests the message three deep:

1. The message itself, a kind 14 event, is left unsigned. The NIP calls it a *rumor*, and a leaked copy cannot be proven genuine.
2. It is encrypted to the recipient and placed in a kind 13 *seal*, signed by the sender. The seal names no recipient.
3. The seal is encrypted again and placed in a kind 1059 *gift wrap*, signed by a key generated for that one message and tagged with the recipient's public key so that relays can deliver it.

NIP-17 says clients should set the seal's and the gift wrap's timestamps to random times up to two days in the past. A relay then sees that a key received a gift wrap, but not who sent it or when it was written. NIP-44, the encryption, lists its own limits. Among them: it has no forward secrecy or post-compromise security, so a stolen key decrypts every earlier message and every later one; relays see the user's IP address; and padding only partly hides a message's size. NIP-44 advises that in high-risk situations users should talk in dedicated end-to-end encrypted messengers and use Nostr only to exchange contacts.

## Relays as a public message bus

fiatjaf's note says the design "does not rely on P2P techniques, therefore it works". Clients never connect to each other peer-to-peer. Each one connects out to servers with public addresses, so none of the [NAT traversal](/wiki/networking/nat-traversal) problems arise. That property, together with ephemeral kinds and tag filters, makes public relays usable as a general publish–subscribe service between clients that share nothing but a string. Two clients subscribe to ephemeral events tagged with an agreed value, and whatever either publishes reaches the other and is not kept.

Several NIPs use relays this way. NIP-46 remote signing exchanges its requests as kind 24133 events, and NIP-47 connects a client to a wallet with kinds 23194 and 23195. Outside the NIPs, [Trystero](/wiki/networking/trystero) uses public relays to pass [WebRTC](/wiki/networking/webrtc) connection offers between browsers, so that a protocol built to avoid peer-to-peer connections ends up setting them up.

The load lands on whoever runs the relay. In August 2026 the operator of `x.kojira.io`, a relay on Trystero's default list, reported that it had gone down under "roughly 4,000 events/second" of ephemeral events, 93% of them in Trystero's format. Not keeping an event is not free. The report lists what each one still costs the relay, from signature verification and "a transient DB write" to deletion by a cleanup job, and sums it up: "Only the final state is 'not stored'; all the work still happens." That relay's cleanup job was deleting 160,000 to 400,000 ephemeral events per run and saturating its processor. Every Trystero client was announcing itself every 5.333 seconds to five relays, for as long as its tab stayed connected to its peers. Trystero 0.25.4 cut that to once a minute and made clients back off when a relay answers `rate-limited:`. The operator's reply after the fix: "I have no objection to Nostr relays being used for peer bootstrapping — it's a genuinely good fit for the protocol. My concern was only ever the volume."

## Check

Ask a relay for its rules:

```bash
curl -H 'Accept: application/nostr+json' https://relay.damus.io
```

The reply is the relay's NIP-11 document. `supported_nips` lists the extensions it implements, and `limitation` holds its limits. A relay that requires payment or authentication says so there, before a client has sent anything.

Verify an event without trusting the relay that served it. This script recomputes the id from the fields and checks the signature against the public key:

```javascript
// verify.mjs — npm install @noble/secp256k1@3
import {schnorr} from '@noble/secp256k1'
import {createHash} from 'node:crypto'

const event = JSON.parse(process.argv[2])

// NIP-01: the id is the SHA-256 of this exact array, serialized with no whitespace.
// JSON.stringify matches NIP-01 except on control characters in content other
// than \n \" \\ \r \t \b \f, which it escapes and NIP-01 writes verbatim.
const serialized = JSON.stringify([
  0, event.pubkey, event.created_at, event.kind, event.tags, event.content,
])
const id = createHash('sha256').update(serialized).digest('hex')

const fromHex = h => Uint8Array.from(Buffer.from(h, 'hex'))
console.log('id matches:', id === event.id)
console.log('signature valid:',
  await schnorr.verifyAsync(fromHex(event.sig), fromHex(id), fromHex(event.pubkey)))
```

Save the example event above as `event.json` and run `node verify.mjs "$(cat event.json)"`. Both lines print `true`. Change one character of `content` and both print `false`: the id no longer matches the fields, and the signature, which covers the id, no longer verifies. That check is the reason a client does not have to trust a relay.

## Sources

- [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md): Basic protocol flow description — events, kinds, filters and the relay messages
- [The NIPs repository](https://github.com/nostr-protocol/nips), whose index lists every NIP and registered kind
- [NIP-19](https://github.com/nostr-protocol/nips/blob/master/19.md) (bech32 encodings), [NIP-07](https://github.com/nostr-protocol/nips/blob/master/07.md) (`window.nostr`), [NIP-46](https://github.com/nostr-protocol/nips/blob/master/46.md) (remote signing)
- [NIP-09](https://github.com/nostr-protocol/nips/blob/master/09.md) (deletion requests), [NIP-40](https://github.com/nostr-protocol/nips/blob/master/40.md) (expiration)
- [NIP-11](https://github.com/nostr-protocol/nips/blob/master/11.md) (relay information document), [NIP-13](https://github.com/nostr-protocol/nips/blob/master/13.md) (proof of work), [NIP-42](https://github.com/nostr-protocol/nips/blob/master/42.md) (authentication)
- [NIP-65](https://github.com/nostr-protocol/nips/blob/master/65.md): Relay List Metadata
- [NIP-04](https://github.com/nostr-protocol/nips/blob/master/04.md), [NIP-17](https://github.com/nostr-protocol/nips/blob/master/17.md), [NIP-44](https://github.com/nostr-protocol/nips/blob/master/44.md) and [NIP-59](https://github.com/nostr-protocol/nips/blob/master/59.md): encrypted messages, sealing and gift wrapping
- [NIP-47](https://github.com/nostr-protocol/nips/blob/master/47.md): Nostr Wallet Connect
- [BIP-340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki): Schnorr Signatures for secp256k1
- fiatjaf, [nostr - Notes and Other Stuff Transmitted by Relays](https://fiatjaf.com/nostr.html) (November 2020), and the [protocol README](https://github.com/nostr-protocol/nostr)
- [Trystero issue #192](https://github.com/dmotz/trystero/issues/192): the relay operator's report and the maintainer's fix

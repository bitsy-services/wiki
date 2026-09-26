---
title: "Trystero"
weight: 40
---

Trystero is a JavaScript library that connects browsers directly over [WebRTC](/wiki/networking/webrtc) without a signalling server of the application's own. Before two browsers can open a WebRTC connection they have to swap session descriptions, written in the Session Description Protocol (SDP), and the candidate addresses that [ICE](/wiki/networking/nat-traversal/ice) finds for each of them. WebRTC leaves the channel for that swap to the application. Trystero sends it through services that other people already run in public: by default [Nostr](/wiki/networking/nostr) relays, servers that forward signed messages between any clients that ask, and in other packages BitTorrent trackers, public brokers for MQTT (a publish–subscribe protocol for small devices) or a hosted database. Browsers that join the same **room** find each other there, exchange encrypted offers and answers, and end up with a direct WebRTC connection. After that, application data no longer passes through the relays.

The library is by Dan Motzenbecker, MIT-licensed, and has not reached 1.0. This page describes version 0.25.4, published on npm on 30 August 2026, and the behaviour it describes is read from that version's published code.

## A room in code

```javascript
import {joinRoom} from 'trystero' // the Nostr strategy

const room = joinRoom({appId: 'example-game-7f3a'}, roomId, {
  onJoinError: ({peerId, error}) => console.warn(peerId, error),
})

const move = room.makeAction('move')
move.onMessage = (data, {peerId}) => applyMove(peerId, data)

room.onPeerJoin = peerId => console.log(`${peerId} joined`)
room.onPeerLeave = peerId => console.log(`${peerId} left`)

move.send({x: 3, y: 4})                       // to every peer in the room
move.send({x: 3, y: 4}, {target: somePeerId}) // to one peer
```

`appId` names the application and `roomId` a group of peers within it, and two browsers meet only if both match. An *action* is a named message type. Trystero serializes whatever is sent through it, whether a JSON-compatible value, a string or binary data, splits large payloads into chunks, and hands the result to the matching `onMessage` on each receiving peer. Where `roomId` should come from is a security question, answered [below](#what-is-encrypted-and-what-a-relay-sees).

The other signalling media are separate packages exporting the same `joinRoom`: `@trystero-p2p/torrent`, `@trystero-p2p/mqtt`, `@trystero-p2p/supabase`, `@trystero-p2p/firebase`, `@trystero-p2p/ipfs` and `@trystero-p2p/ws-relay`. Older import paths such as `trystero/torrent` now throw an error naming the package to install instead.

## How peers find each other

Every peer in a room works from two strings:

- the **room topic**, a SHA-1 hash of `Trystero@<appId>@<roomId>`;
- its **own topic**, a SHA-1 hash of `Trystero@<appId>@<roomId>@<selfId>`, where `selfId` is a random 20-character ID the library generates on each page load.

Joining a room starts this sequence on every relay in use:

1. Subscribe to the room topic and to the peer's own topic.
2. Announce `{"peerId": selfId}` on the room topic. The first four announcements go out within about two seconds, and after that the Nostr strategy announces once a minute for as long as the room is open. The README describes this as "a short startup announcement burst followed by a 60-second steady interval".
3. On hearing another peer's announcement, compare the two IDs as strings. The peer whose ID sorts first sends an **offer** to the other peer's own topic. The peer whose ID sorts second sends only an announcement there, which makes the first one offer. Normally only one side of a pair offers. When both do, the offer from the ID that sorts first wins and the other is dropped, which resolves the collision the [WebRTC page](/wiki/networking/webrtc#setting-up-a-connection) calls glare.
4. The other peer replies with an **answer** on the offerer's own topic, and both send their ICE candidates to each other's topic as they are gathered.
5. When the WebRTC data channel opens, the peer is added to the room and `onPeerJoin` fires.

```text
  peer 3kQ…                    relays                    peer Qx9…
     |--- announce, room topic --------------------------->|
     |<--------------------------- announce, room topic ---|
     |     "3kQ…" sorts first, so it offers                |
     |--- offer (encrypted), to Qx9…'s topic ------------->|
     |<------------- answer (encrypted), to 3kQ…'s topic --|
     |<-- candidates (encrypted), to each other's topic -->|
     |                                                     |
     |================= WebRTC data channel ===============|
```

Offers are made in advance. On joining, Trystero creates a pool of 20 `RTCPeerConnection` objects with an offer ready in each, so that answering an announcement costs no setup time. Creating an offer starts candidate gathering, so a join sends a burst of [STUN](/wiki/networking/nat-traversal/stun) requests to the configured servers. If a [TURN](/wiki/networking/nat-traversal/turn) server is configured, each of the 20 also asks it for a relay address. TURN is the relay that carries traffic for pairs with no direct path.

On a Nostr relay each of these messages is an ephemeral event, the class of event a relay forwards to open subscriptions and is not expected to store. Its `x` tag holds the topic, its kind is a number in the ephemeral range 20000–29999 derived from the topic, and it is signed with a Nostr key pair generated on each page load. The subscription filters on that kind and tag, with `since` set to the moment of subscribing. An announcement made before a peer arrived therefore never reaches it. A late peer is found through its own announcements instead, which the peers already in the room receive.

Unless the application passes its own list, the Nostr strategy uses five of the 28 relays built into the release, chosen by shuffling the list with a seed computed from `appId`. Every copy of one application picks the same five, which is what lets them meet.

## What is encrypted, and what a relay sees

Offers, answers and candidates are encrypted with AES-GCM, the Advanced Encryption Standard in Galois/Counter Mode, which also detects tampering. The key is the SHA-256 hash of `<password>:<appId>:<roomId>`, where the password is an optional setting that defaults to an empty string. Announcements are not encrypted.

What a Nostr relay forwards, anyone subscribed to it can read. A subscription that filters on the ephemeral kinds alone, with no tag, receives every Trystero event passing through the relay. The author of issue #192 measured the ephemeral traffic exactly that way, on the 37 reachable relays among the 47 then on Trystero's default list. So a relay, and any subscriber to it, sees:

- the room topic of every room using the relay, and so which peers share a room;
- each peer's `selfId`, in its announcements;
- the size and timing of every message.

The relay's operator also sees the IP address of every browser connected to it. No one on the relay sees the session descriptions or any application data, which travels over WebRTC encrypted with Datagram Transport Layer Security (DTLS), as described under [what runs over the path](/wiki/networking/webrtc#what-runs-over-the-path). The announcements continue once a minute after the peers have connected, so the relay goes on seeing who is in each room and for how long.

`appId` ships inside the application's JavaScript, where anyone can read it. Without a password, the room ID is the only secret input to both the topic and the key. Anyone who knows or guesses it can find the room on any relay, decrypt the session descriptions, which list each peer's candidate addresses including its public IP address, and join. The README says as much: without a password, "a relay strategy operator can reverse engineer the key using the room and app IDs." Guessing does not even need a relay of one's own. Any subscriber sees the topic of every room on that relay, and SHA-1 is fast to compute, so a room called `lobby`, or one named by a six-digit code, falls to trying candidates against the topics seen.

The key protects more than privacy. WebRTC authenticates the other browser by a certificate fingerprint carried inside the session description, and RFC 8827 notes that this rests on "minimal trust in the signaling service not to perform a man-in-the-middle attack." With Trystero the signalling service is a set of strangers' relays, and the key is what stops one of them from reading or rewriting the descriptions. Whoever holds the key holds the position RFC 8827 trusts the signalling service not to abuse.

A room ID drawn from 128 random bits cannot be guessed, although it does not keep out peers the user meets in other rooms of the same app, for the reason under [rooms of one app share connections](#rooms-of-one-app-share-connections). Carried in a link's fragment, the part after `#`, it is not sent to the web server that serves the page:

```javascript
const bytes = crypto.getRandomValues(new Uint8Array(16)) // 128 bits
const roomId = btoa(String.fromCharCode(...bytes))
  .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
const inviteLink = `${location.origin}${location.pathname}#${roomId}`
```

A password protects the descriptions without hiding the room. The topic does not include it, so relays still see which peers share a room. When two peers' passwords differ, whichever of them receives the offer cannot decrypt it and gets `onJoinError` with `incorrect room password when decrypting offer`, and that can be the peer holding the right password. A password is worth setting when it travels separately from the link, so that a leaked link alone is not enough to join. Sent inside the same link as a random room ID, it adds nothing. Either secret works like a bearer token: anyone who has it can join, and the only way to revoke it is to move everyone to a new room. To decide who may join by anything else, the application supplies `onPeerHandshake`, which runs over the new connection before the peer is admitted and can reject it.

## Rooms of one app share connections

Trystero 0.25.4 keeps one `RTCPeerConnection` to each remote peer per `appId`, and every room the two browsers are both in runs over it, with each message tagged by room. The connection outlives the rooms. After the last shared room is left it stays open for about two minutes in case another room needs it, and `room.getPeers()` returns that same object in every room.

Rooms are announced over these connections regardless of which came first, the room or the connection. Joining a room sends a token for it to every peer the browser is connected to in the app, from any room, and a newly formed connection is sent the tokens of every room the browser is already in. The token is the SHA-256 hash of `Trystero:<appId>:<roomId>`, which does not include the password. A peer that sends the same token back is attached to the room over the existing connection, with no signalling and no session key involved. An unmodified client sends back only the tokens of rooms it has joined itself, but a modified one can send back any token it was given. When a password is set, the challenge that runs on this path is checked by only one of the two peers, the one whose ID sorts first, and each peer chooses its own ID.

Read from the 0.25.4 code, and not tested here, that means a private room under the same `appId` as a public one is open to a modified client run by anyone the user has met in the public one. A room given an `appId` of its own, for example the application's name with the room ID appended, shares connections with nothing else. Peers still find each other only on two conditions:

- **Every `joinRoom` call passes the same explicit `relayConfig.urls`.** A page picks its relays once, from the configuration of the first room it joins, and picks again only after it has left every room. The default pick is seeded by `appId`. Without a fixed list, a user who is still in another room signals on that room's relays, while a newcomer opening the private room's link on a fresh page uses relays seeded by the private room's `appId`, and the two may share none. Trystero connects to every relay in the list, so a short one is kinder to the relays than the full default set.
- **The strategy lets `appId` vary.** Supabase does not, because its `appId` must be the project's URL. Firebase does only when the application passes its initialized app as `relayConfig.firebaseApp`.

Checking the room ID inside one `appId`, with an `onPeerHandshake` in which each side proves it knows it, is harder than it looks. Peer IDs are only claims, and the handshake callback is not given the connection it runs on, so a proof cannot be bound to that connection. A peer connected to two members of the room who are not yet connected to each other can then pass one member's challenges and answers to the other under borrowed IDs. The separate `appId` avoids the problem rather than defending against it.

## When two peers cannot connect

By default Trystero configures four STUN servers, `stun.l.google.com`, `stun1.l.google.com` and `stun2.l.google.com` on port 19302 and `stun.cloudflare.com` on port 3478, and no TURN server. The `turnConfig` setting adds TURN servers to those defaults, and `rtcConfig.iceServers` replaces the whole list.

A pair of peers with no direct path between them therefore finds each other, exchanges descriptions, and never connects. Trystero reports it through `onJoinError` with the message `could not connect to peer <id> after exchanging SDP; configure TURN servers with turnConfig or rtcConfig.iceServers`. The report comes about 23 seconds after the descriptions are exchanged, or sooner if the browser gives up on the connection first. Which pairs those are, and roughly how many, is the subject of [Running without TURN](/wiki/networking/nat-traversal/without-turn).

Adding TURN runs into the reason for using Trystero. A TURN server needs credentials. A fixed username and password placed in a public web page can be read by anyone, who can then relay their own traffic at the server owner's expense. The alternative is short-lived credentials minted for each user by the application's server, the [scheme on the TURN page](/wiki/networking/nat-traversal/turn#credentials), which means running a server after all. An application with no server of its own is left with four options: accept that some pairs never connect, let users enter their own TURN server, publish credentials anyone can reuse, or, with three or more players, forward a disconnected pair's messages through a peer both of them can reach.

## One data channel

Trystero opens one data channel to each peer, labelled `data` and created with default options, which makes it reliable and ordered. Every action shares it, and every room of the app too, since the channel belongs to the shared connection. Messages are split into chunks of 16 KiB including a 36-byte header, and before sending each chunk Trystero waits until less than 64 KiB is queued on the channel. Concurrent sends therefore take turns chunk by chunk, but every message still waits behind whatever is already queued, up to about 80 KiB. A lost packet stalls every later message on the channel until it is retransmitted. For a game sending position updates many times a second, that is the head-of-line blocking described under [A relay changes the game's timing](/wiki/networking/nat-traversal/without-turn#a-relay-changes-the-games-timing).

`room.getPeers()` returns the `RTCPeerConnection` behind each peer, and a second channel can be opened on it for traffic that should be unordered and unreliable. It has to be *negotiated*: created on both sides with `negotiated: true` and the same `id`, instead of being announced to the other side over the connection. On the answering side, Trystero 0.25.4 installs an `ondatachannel` handler that adopts any channel announced that way as its own. Trystero's messages then go out on the new channel, and closing that channel counts as the peer leaving.

```javascript
// One channel per connection, in a map shared by the whole page. The
// connection is shared by every room of the app and outlives a room by about
// two minutes, so onPeerJoin can fire again for a connection that already has
// the channel. Never close the channel: a closed one is only replaced at the
// next onPeerJoin, which for a connected peer may never come.
const stateChannels = new WeakMap()

function stateChannel(pc, peerId) {
  let state = stateChannels.get(pc)
  if (state && state.readyState !== 'closed') return state
  state = pc.createDataChannel('state', {
    negotiated: true, // created on both sides; never reaches ondatachannel
    id: 42,           // the same number on both sides
    ordered: false,
    maxRetransmits: 0,
  })
  // Set once, here. Messages on this channel carry no room tag, so an app in
  // several rooms at once must add one and route on it.
  state.onmessage = e => applyState(peerId, e.data)
  stateChannels.set(pc, state)
  return state
}

// In every room:
room.onPeerJoin = peerId => stateChannel(room.getPeers()[peerId], peerId)
```

`onPeerJoin` fires on both sides, so both create the channel. The `id` is the number of the stream that carries the channel inside the Stream Control Transmission Protocol (SCTP) association all data channels share. RFC 8831 leaves it to the application to pick one that is not in use, and creating a channel on a taken id fails. That is why the code keeps one channel per connection in a page-wide map and sets its handler only when it creates it: a map per room would create id 42 twice on a shared connection, and a handler set per room would leave only the last room receiving. Trystero opens only one channel of its own, and the browser gives it a low number, so an id such as 42 is clear of it.

## Public relays are other people's servers

The default relays are volunteers' machines, and the list changes between releases. Release 0.25.4 dropped a relay that Trystero's announcements had overloaded, an incident described on the [Nostr page](/wiki/networking/nostr#relays-as-a-public-message-bus). Each release shuffles its own list with the same seed, so two builds of one application on different Trystero versions can pick different relays, and two peers with no relay in common never meet. An application can pass its own list as `relayConfig.urls`, and Trystero then uses every relay in it.

Trystero also acts on what relays tell it. After a relay answers any event with `rate-limited:`, Trystero sends it no announcements for a minute, then two, doubling up to fifteen minutes, and the delay resets once the relay accepts an announcement. A relay that closes a subscription, or rejects an event for any other reason except a duplicate, is dropped for as long as the page stays open.

## Choosing a strategy

The README recommends Nostr as the default for its redundancy, "hundreds of active relays", and ranks the other public options "in the order of MQTT, BitTorrent, and IPFS, based on robustness."

| Package | Signalling medium | Run by | Notes |
|---|---|---|---|
| `trystero`, which is `@trystero-p2p/nostr` | public Nostr relays | volunteers | the default |
| `@trystero-p2p/mqtt` | public MQTT brokers | the brokers' operators, as free test services | ranked second by the README |
| `@trystero-p2p/torrent` | WebTorrent trackers, the servers browser BitTorrent clients use to find each other | volunteers | the author knows of "only 4 public webtorrent trackers" and says "all of them have spotty reliability" |
| `@trystero-p2p/ipfs` | the Waku network | Waku node operators | the author says the strategy "rarely works" |
| `@trystero-p2p/supabase`, `@trystero-p2p/firebase` | a database in the developer's own hosted project | the developer, on a hosted service | needs the project's key or database URL |
| `@trystero-p2p/ws-relay` | a small WebSocket server | the developer | no public default |

The package called `ipfs` does not use [IPFS](/wiki/cs/ipfs). It uses Waku, a separate network built on the same libp2p networking library. The author explains that the strategy originally did use IPFS and was switched to Waku when that stopped working.

Running two strategies at once, so that the application survives one medium failing, gives two independent rooms. Each keeps its own peers and connections, so every peer that both find is connected twice. A feature request to merge strategies into one room (issue #100) is open.

## Rough edges

- **The API is still moving.** The `@trystero-p2p` packages first appeared on npm in March 2026 at 0.23, when the strategies were split out, and the restructuring broke the torrent strategy until 0.23.1 (issue #165). Pin an exact version.
- **`selfId` is not an identity.** It is 20 characters drawn from `Math.random` on each page load, so a reload produces a new one, and it arrives in plaintext announcements that nothing authenticates. Anything that must know who a peer is belongs in `onPeerHandshake`, within the limit described under [rooms of one app share connections](#rooms-of-one-app-share-connections): a proof made there cannot be tied to the connection it arrives on.
- **A room is a full mesh.** Every peer connects to every other, which is *N*(*N* − 1)/2 connections for *N* peers, and the README warns that "browsers can only handle a limited amount of WebRTC connections at a time." A room of three or more can also end up partly connected. A user reports two peers each connected to a third but not to each other (issue #161, open). Why one missing pair matters is covered under [the topology multiplies the risk](/wiki/networking/nat-traversal/without-turn#the-topology-multiplies-the-risk).

## Check

List the relays a page is actually connected to:

```javascript
import {getRelaySockets} from 'trystero'

const open = Object.entries(getRelaySockets())
  .filter(([, ws]) => ws.readyState === WebSocket.OPEN)
  .map(([url]) => url)
console.log(`${open.length} relays open`, open)
```

Two peers can meet only through a relay that is open on both sides. An application that passes its own list can show this count to the user, since zero means no one can join.

In Chrome, `chrome://webrtc-internals` lists every `RTCPeerConnection` on the page. Joining a room adds about twenty at once, which is the offer pool. Each connected peer has one connection there, taken from the pool if this browser made the offer or created new if it answered, and its selected candidate pair shows whether the path is direct or relayed, as described in the [WebRTC check](/wiki/networking/webrtc#check). The script in [Running without TURN](/wiki/networking/nat-traversal/without-turn#check) reads the same thing from a connection passed to it; pass it `room.getPeers()[peerId]`.

## Sources

- Trystero [README](https://github.com/dmotz/trystero) and the published code of version 0.25.4 on npm: [`@trystero-p2p/core`](https://www.npmjs.com/package/@trystero-p2p/core) (`strategy.mjs`, `signal-handler.mjs`, `shared-peer.mjs`, `handshake.mjs`, `room.mjs`, `crypto.mjs`, `peer.mjs`, `offer-pool.mjs`, `action-wire.mjs`) and [`@trystero-p2p/nostr`](https://www.npmjs.com/package/@trystero-p2p/nostr); release dates from the npm registry
- Trystero issues [#100](https://github.com/dmotz/trystero/issues/100) (multiple strategies), [#161](https://github.com/dmotz/trystero/issues/161) (partial meshes), [#165](https://github.com/dmotz/trystero/issues/165) (torrent regression, public trackers), [#175](https://github.com/dmotz/trystero/issues/175) (Waku), [#192](https://github.com/dmotz/trystero/issues/192) (relay overload)
- [RFC 8827](https://www.rfc-editor.org/rfc/rfc8827): WebRTC Security Architecture
- [RFC 8831](https://www.rfc-editor.org/rfc/rfc8831): WebRTC Data Channels, Section 6.5 on out-of-band negotiation
- [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md): the Nostr event kinds and subscription filters Trystero uses

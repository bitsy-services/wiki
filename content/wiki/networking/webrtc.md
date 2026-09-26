---
title: "WebRTC"
weight: 20
---

WebRTC is the browser's built-in facility for sending audio, video and arbitrary data directly to another browser, or to a server that speaks the same protocols, with encryption that cannot be switched off. It has two halves. The W3C defines the JavaScript API, whose central object is `RTCPeerConnection`. The IETF defines the protocols underneath: [ICE](/wiki/networking/nat-traversal/ice) to find a network path, Datagram Transport Layer Security (DTLS) to authenticate the two ends and agree keys, Secure Real-time Transport Protocol (SRTP) for media, and Stream Control Transmission Protocol (SCTP) for data channels. RFC 8825 is the overview.

Most of the work in setting up a call is [NAT traversal](/wiki/networking/nat-traversal), because two browsers are usually both behind network address translation (NAT) devices, and neither can accept a connection the way a web server can. WebRTC runs the full procedure on every connection: [STUN](/wiki/networking/nat-traversal/stun) for public addresses, [hole punching](/wiki/networking/nat-traversal/hole-punching) through ICE's connectivity checks, and a [TURN](/wiki/networking/nat-traversal/turn) relay when nothing direct works.

## What WebRTC leaves to the application

Before two browsers can exchange a packet, they have to exchange a description of the session: which media and data they will send, which codecs they support, their ICE candidates and credentials, and a fingerprint of the certificate each will present. WebRTC produces and consumes those descriptions but does not carry them. RFC 9429, which defines the JavaScript Session Establishment Protocol (JSEP) behind the API, states that it "does not specify a particular signaling model," and leaves the transport of descriptions "including addressing, retransmission, forking, and glare handling" to the application.

That channel is called **signalling**, and it is a server the application runs, reached for example over a WebSocket or HTTPS, which are the two transports RFC 8827's worked example names. It also decides who can call whom, which is an application concern rather than a protocol one.

The descriptions are Session Description Protocol (SDP) text, exchanged as an **offer** and an **answer**. The caller creates an offer describing what it wants, the callee replies with an answer describing what it accepts, and each side applies both. ICE candidates travel the same channel, usually one at a time as they are found ([trickle ICE](/wiki/networking/nat-traversal/ice#trickle-ice)).

## Setting up a connection

The configuration below names the STUN and TURN servers. The TURN credentials are short-lived ones minted by the application server for this user, in the [scheme described on the TURN page](/wiki/networking/nat-traversal/turn#credentials):

```javascript
const pc = new RTCPeerConnection({
  iceServers: [
    { urls: "stun:stun.example.org:3478" },
    {
      urls: [
        "turn:turn.example.org:3478?transport=udp",
        // TURN over TLS, for networks that block outbound UDP
        "turns:turn.example.org:5349?transport=tcp",
      ],
      username: "1790371886:alice",
      credential: "SNMs3SVnqKzt5Of+Ay7f6xY0A8o=",
    },
  ],
});

const signaling = new WebSocket("wss://app.example.org/signal");

// Trickle ICE: forward each candidate as soon as it is gathered. A candidate
// whose .candidate string is empty marks end-of-candidates; forward it too,
// since the peer's connection cannot reach "failed" without it.
pc.onicecandidate = ({ candidate }) => {
  if (candidate) signaling.send(JSON.stringify({ candidate }));
};

signaling.onmessage = async ({ data }) => {
  const msg = JSON.parse(data);
  if (msg.description) {
    await pc.setRemoteDescription(msg.description);
    if (msg.description.type === "offer") {
      await pc.setLocalDescription(); // with no argument, creates the answer
      signaling.send(JSON.stringify({ description: pc.localDescription }));
    }
  } else if (msg.candidate) {
    await pc.addIceCandidate(msg.candidate);
  }
};

// The caller adds what it wants to send, then makes the offer.
async function call() {
  pc.createDataChannel("chat");
  await pc.setLocalDescription(); // with no argument, creates the offer
  signaling.send(JSON.stringify({ description: pc.localDescription }));
}
```

Setting the local description starts candidate gathering, and each candidate surfaces through `onicecandidate`. Once both descriptions are applied, ICE pairs the candidates and runs its checks. The rest of the connection happens without the application: DTLS, then media or data.

The TURN server in the configuration is optional. What leaving it out costs, for a game in particular, is on [Running without TURN](/wiki/networking/nat-traversal/without-turn).

This sketch leaves out what a production application has to handle. If both sides make an offer at once (*glare*), the collision has to be resolved, and a changing network needs an ICE restart through `restartIce()`.

## What runs over the path

ICE selects one candidate pair, one local address and port and one remote. Everything else in the session shares that single path:

```text
   audio / video               data channels
   -------------               -------------
       SRTP                        SCTP
        |                           |
        |   keys  <-------------   DTLS
        |                           |
   ------------------------------------------------
   one ICE-selected path (STUN checks and keepalives share it)
   UDP, directly or through a TURN relay; TCP as a fallback
```

- **DTLS** runs first, as a handshake over the selected path. Each browser presents a certificate it generated itself, which no authority has signed. The other side checks it against the fingerprint that came in the SDP. The link between the two is what authenticates the peer, so unless the application uses RFC 8827's optional identity-provider mechanism, WebRTC's security rests on the signalling channel delivering the fingerprint intact. RFC 8827 calls that "minimal trust in the signaling service not to perform a man-in-the-middle attack."
- **SRTP** carries audio and video. Its keys are exported from the DTLS handshake, a combination called DTLS-SRTP. RFC 8827 forbids sending media unencrypted and forbids negotiating a null cipher. There is no unencrypted WebRTC.
- **SCTP** carries data channels, and it runs *inside* DTLS. Each data channel can be reliable or unreliable, and ordered or unordered. That choice is the reason to use a data channel for game state or telemetry rather than a WebSocket, which is always reliable and ordered.

All of these arrive on the same local port. The receiver sorts packets by their first byte, using ranges defined in RFC 7983:

| First byte | Protocol |
|---|---|
| 0–3 | STUN |
| 20–63 | DTLS |
| 64–79 | TURN ChannelData |
| 128–191 | SRTP and its control packets |

## Transport requirements

RFC 8835 sets what a browser must support, and most of it is about reaching peers from hostile networks:

- STUN and TURN, configurable both by the application and by the browser.
- TURN over TCP and TURN over TLS, for networks that block outbound UDP entirely.
- ICE-TCP candidates, which let a browser reach a peer with a public address over TCP without a relay.
- TURN for IPv6, so an IPv4-only peer and an IPv6-only peer can still be connected through a relay.

Browsers must also verify reachability with ICE before sending anything else to an address (RFC 8827). A web page therefore cannot use WebRTC to send media at an arbitrary host. The destination has to answer a STUN check authenticated with credentials from the page's own session description, and [consent checks](/wiki/networking/nat-traversal/ice#after-a-pair-is-selected) stop the flow within 30 seconds if it stops answering.

## Local addresses and privacy

ICE works best when each agent offers its private interface addresses as host candidates, because two peers on the same network can then connect directly. But a list of private addresses, handed to any web page that asks, is a stable fingerprint of the user's machine and network. An IETF draft whose authors include engineers at Apple and Google specifies the fix. Each private address is replaced in the candidate with a random name, a version 4 universally unique identifier followed by `.local`, and the browser answers multicast DNS queries for that name on the local network only. A peer on the same network can resolve the name, and a web page on the internet learns nothing. A candidate line with a `.local` address is this mechanism at work.

Server-reflexive candidates still reveal the user's public address, to the page and to the peer. A page that must keep peers from exchanging packets with the user directly can set `iceTransportPolicy: "relay"`, which uses only relayed candidates, so that every packet passes through the TURN server.

## More than two people

A connection is between two endpoints. For a call among *N* people there are two basic arrangements.

- **Mesh.** Every participant opens a connection to every other and sends its media *N* − 1 times. Upload bandwidth and encoding work grow with the number of participants, which limits a mesh to small calls.
- **Selective forwarding unit (SFU).** Every participant opens one connection to a server and sends its media once. The server forwards each stream to the participants that should receive it, choosing among quality layers when the sender provides several. RFC 7667 calls this a *Selective Forwarding Middlebox*. To each browser the SFU is simply the other peer. It has a public address, so it can run [ICE-lite](/wiki/networking/nat-traversal/ice#ice-lite), the reduced ICE that only answers checks, and RFC 8827 requires such servers to implement at least that.

The SFU terminates each participant's DTLS session, so it holds the SRTP keys and can read the media it forwards. Encryption between participants across an SFU needs a second layer applied to the media inside the browser, on top of what WebRTC does by default.

## Check

Chrome's `chrome://webrtc-internals` and Firefox's `about:webrtc` show every candidate a page gathered, every candidate pair, the state of each check, and which pair was selected. They are the quickest way to answer "did this call go through TURN." A call relayed through TURN shows a selected pair whose local or remote candidate type is `relay`. Local means this browser's relay, and remote means the peer's. The peer's relay can also appear here as `prflx`, when its checks arrived before its candidate did, so the reliable reading is each browser's own local type.

## Sources

- [RFC 8825](https://www.rfc-editor.org/rfc/rfc8825): Overview of WebRTC
- [RFC 9429](https://www.rfc-editor.org/rfc/rfc9429): JavaScript Session Establishment Protocol (JSEP), which replaced RFC 8829
- [RFC 8827](https://www.rfc-editor.org/rfc/rfc8827): WebRTC Security Architecture
- [RFC 8835](https://www.rfc-editor.org/rfc/rfc8835): Transports for WebRTC
- [RFC 8831](https://www.rfc-editor.org/rfc/rfc8831): WebRTC Data Channels
- [RFC 7983](https://www.rfc-editor.org/rfc/rfc7983): multiplexing STUN, DTLS, TURN and SRTP on one port
- [RFC 7667](https://www.rfc-editor.org/rfc/rfc7667): Real-time Transport Protocol topologies, including the selective forwarding middlebox
- [draft-ietf-mmusic-mdns-ice-candidates](https://datatracker.ietf.org/doc/draft-ietf-mmusic-mdns-ice-candidates/): Using Multicast DNS to protect privacy when exposing ICE candidates
- W3C, [WebRTC: Real-Time Communication in Browsers](https://www.w3.org/TR/webrtc/)

---
title: "Running Without TURN"
weight: 55
---

An application runs without TURN when it gives its [ICE](/wiki/networking/nat-traversal/ice) agent STUN servers but no [TURN](/wiki/networking/nat-traversal/turn) server, the relay that forwards packets between peers that cannot reach each other. ICE is the procedure that gathers each peer's candidate addresses and tests every pairing. Without TURN it tests only direct paths, between three of its four kinds of candidate: *host* candidates, the machine's own addresses; *server-reflexive* (`srflx`) candidates, the public address a [STUN](/wiki/networking/nat-traversal/stun) server reports; and *peer-reflexive* (`prflx`) candidates, addresses discovered during the tests themselves. The fourth kind, *relayed* (`relay`), exists only when a TURN server is configured. For any pair of peers with no direct path between them, every test fails and the two never exchange a packet. There is no degraded mode, no slower path and no partial connection: the pair does not connect at all.

Which pairs have no direct path is set out in the table under [When TURN is required](/wiki/networking/nat-traversal/turn#when-turn-is-required). This page covers what the gap costs an application, using a peer-to-peer browser game as the worked case.

## What the failure looks like

While the connectivity checks run, the connection's `connectionState` is `"connecting"`. When every check has failed it becomes `"disconnected"`, which the W3C specification calls transient, not a verdict. It becomes `"failed"` only when three things hold:

- every candidate pair has failed its checks;
- the peer has signalled that it has no more candidates to send, which arrives as an ICE candidate whose candidate string is empty and has to be forwarded by the application like any other;
- a minimum waiting period has passed, unless the browser gathered no candidates at all.

The waiting period is RFC 8863's *PAC timer* ("Patiently Awaiting Connectivity"). It exists so that a late peer-reflexive candidate still gets a chance, and its recommended length is 39.5 seconds. At that length, a pair that can never connect keeps two players waiting about forty seconds before the browser gives up. If the end-of-candidates signal is never sent or is lost, `"failed"` never comes at all.

When `"failed"` does arrive, the application learns nothing more specific. It cannot tell a pair of incompatible network address translation (NAT) devices from a firewall that blocks UDP or a peer whose network dropped.

Retrying does not help. An [ICE restart](/wiki/networking/nat-traversal/ice#after-a-pair-is-selected) gathers the same candidates on the same networks and runs the same tests, so the same pair fails again until one of the players changes network. The failure is a property of the pair, and it recurs every time those two players meet.

## How often a pair has no direct path

One large public measurement exists, and it is old. callstats.io, which monitored WebRTC sessions for its customers' services, published aggregate figures on webrtcHacks in April 2016 covering January 2015 to February 2016 and "billions of minutes":

- 12% of sessions, one in eight, were never set up, and 85% of those failures came from "the inability of an endpoint to traverse NATs or firewalls."
- 22% of conferences "need some kind of TURN relay server," and about 9% needed TCP.
- The authors note that not all of their customers had deployed TURN over TCP or TLS, so the failure rate "may still be indicative" of relays that were missing.

ICE ranks relayed paths last, so a session that ended up on TURN is one where the direct tests did not succeed. The 22% figure counts conferences, not pairs of browsers, and it mixes two kinds of session. Some were peer-to-peer. Others connected a customer's browser "through a WebRTC gateway", a server with a public address, which needs a relay only when the customer's network blocks UDP or forces a proxy. So the figure bounds the browser-to-browser rate in neither direction. In 2020 an engineer at Tailscale estimated that STUN and [hole punching](/wiki/networking/nat-traversal/hole-punching) give a direct connection "over 90% of the time", with relays covering the rest. That is an estimate, not a measurement.

Neither source gives a number for any particular application. They agree on the shape: most pairs connect directly, and a minority large enough to matter do not.

## Who it hits

The failures are not spread evenly across users. They follow networks, so they land on the same people every time.

- **Office and cloud networks.** An *easy* NAT uses one public port for all of a socket's traffic, and a *hard* NAT picks a new port for each destination, as described under [NAT mapping](/wiki/networking/nat-traversal/mapping-and-filtering#mapping-does-the-public-port-depend-on-the-destination). Tailscale's experience is that "home routers tend to be easy NATs, and hard NATs tend to be office routers or cloud NAT gateways." A player on a hard NAT can still connect to an opponent whose NAT [filters](/wiki/networking/nat-traversal/mapping-and-filtering#filtering-who-may-send-in) loosely, admitting any port on an address it has sent to. It cannot connect to the many NATs that admit only the exact address and port.
- **Networks that block UDP.** Tailscale reports a university guest Wi-Fi network that blocked all outbound UDP except DNS. Without TURN over TCP or TLS, a player there can connect only to a peer with a public address that accepts TCP.
- **Browsers in a restricted address mode.** RFC 8828 numbers four modes for how much a browser reveals. A browser may use the stricter ones when the user asks for them. In Mode 3 it withholds private addresses, and in Mode 4 it also forces all traffic through an HTTP proxy. In Mode 4, a relay is the only route out.
- **Neighbours behind the same [carrier-grade NAT](/wiki/networking/nat-traversal/mapping-and-filtering#carrier-grade-nat)**, the internet service provider's shared NAT, when it does not [hairpin](/wiki/networking/nat-traversal/mapping-and-filtering#hairpinning) their traffic back inside.

To the team building the application, this looks like a product that works for them and for most testers, and never works for a few players who report it repeatedly. The bug cannot be reproduced from a home network, because home routers are usually easy.

## In a peer-to-peer browser game

A browser game that sends moves or state between players over WebRTC data channels, as described on the [WebRTC](/wiki/networking/webrtc) page, meets every consequence above. Four more are specific to it.

### The topology multiplies the risk

In a **full mesh**, where every player connects to every other, a game of *N* players needs *N*(*N* − 1)/2 connections, and all of them must succeed. Four players need 6 and eight players need 28. One player on a strict network can fail against most of the others, and a mesh with a missing link is broken for everyone: the players on either side of it cannot see each other's moves.

In a **star**, where one player hosts and the rest connect only to the host, the game needs *N* − 1 connections, and everything depends on the host's network. A host with a public address, or with an easy NAT that filters loosely, can accept players that could never connect to each other. A host on a hard NAT is the worst choice, because every player behind a strict filter fails against it. A browser cannot measure its own NAT's filtering, but the game can record which players' connections have succeeded directly in the past and prefer them as hosts. When the host leaves, promoting a new one can strand players who could reach the old host but not the new one.

### Every opponent learns your address

On a direct path each player receives the others' packets from their real public addresses. The server-reflexive candidates state the addresses outright, in the [signalling](/wiki/networking/webrtc#what-webrtc-leaves-to-the-application) messages the game's server passes between players to set up each connection. RFC 8828 adds a case: when the browser gathers addresses from every network interface, which it should do only once the user has granted something like camera or microphone permission, WebRTC can reveal "the ISP public address over which the VPN is running." That applies to a user on a split-tunnel virtual private network (VPN), one that sends only some traffic through the tunnel. A game with voice chat asks for exactly that permission. In a game that matches strangers, a hostile opponent who has a player's address can flood it with traffic.

A TURN server is the fix, and it is a benefit that has nothing to do with NATs. With `iceTransportPolicy: "relay"`, every packet passes through the relay and opponents see only the relay's address. One pair of fields still needs care. Under RFC 8839, a relayed candidate's related address and port, `raddr` and `rport`, carry the player's public address. RFC 8839 lets an agent withhold them "for privacy reasons" by setting the address to `0.0.0.0` for IPv4 or `::` for IPv6, and the port to `9`. The game's signalling server forwards every candidate, so it can make that rewrite itself. It has to apply it in two places: to each candidate sent on its own, and to the `a=candidate` lines inside every session description it forwards, because a renegotiated offer or answer, such as the one that adds voice chat mid-match, repeats every candidate gathered so far. Browsers may already blank the fields; check what your target browsers send, since the rewrite costs nothing either way. Without a TURN server, none of this is possible.

### A relay changes the game's timing

A relayed path detours through the server. Tailscale's assessment is that if the relay is "near enough" to the direct path, there will be "a bit more latency, maybe less bandwidth." Whether that matters depends on how fast the game is.

Over TURN on TCP, which is the only relay that works from a network blocking UDP, an unreliable, unordered data channel stops behaving like one. TCP delivers in order and retransmits losses, so one lost packet on the leg to the relay stalls everything behind it until the retransmission arrives. That is head-of-line blocking. RFC 8828 warns that sending media over TCP "will result in reduced media quality." The game sees a stutter where it expected a dropped update. The player still gets a connection, which is the alternative to not playing at all.

### A relay is cheap for game traffic

The usual objection to TURN is bandwidth cost, and that objection is sized for video. Game traffic is small. Take a client that sends 20 updates a second at 200 bytes each, headers included:

```text
20 × 200 bytes      = 4,000 bytes per second
4,000 × 3,600 s     = 14.4 MB per hour
```

A relayed player receiving that stream from one opponent costs the relay 14.4 MB of outbound traffic per hour. Cloudflare's published rate for its TURN service, as of September 2026, is $0.05 per GB of egress, with the first 1,000 GB a month free and shared with its media server product. At that rate one relayed stream costs $0.00072 per hour, and the free allowance covers about 69,000 such stream-hours a month. For comparison, a 1.5-megabit-per-second video stream is 675 MB an hour, 47 times as much.

Running a TURN server yourself changes the price but not the proportion: the bill scales with the bytes relayed, and a game relays very few.

## If you ship without it anyway

- **Measure it.** Record for every pair whether it connected, and over which kind of path, so the failure rate is a number rather than a guess. The script in the Check section below reads the path type. A game without TURN learns only which pairs failed; a game with TURN also learns which pairs used it.
- **Detect restricted browsers.** RFC 8828 advises checking for host candidates: "If no host candidates are present, Mode 3 or 4 is in use." A game can warn that player before a match starts.
- **Run your own timer.** Start a timer when setup begins and treat its expiry as failure, alongside `"failed"`, which comes no sooner than the PAC timer and never if an end-of-candidates signal is lost or never sent. RFC 8863 itself says that "the application is in the best position to determine what is reasonable for its scenario." Then tell both players the connection could not be made, and offer something other than waiting.
- **Relay through your own server.** The signalling server already has a connection to every player, and forwarding game messages over it is a relay by another name. It runs over TCP, with the head-of-line blocking described above. Unlike a TURN server, which only ever carries WebRTC's encrypted packets, it also sees the game traffic unless the game encrypts it separately. That fallback is still better than no connection.
- **Choose hosts by track record** in a star topology, as above.

## Check

Two browser-side checks cover most of this.

To reproduce an incompatible pair, have the signalling server rewrite every candidate's address to `192.0.2.1`, a documentation address that routes nowhere (RFC 5737). Rewrite both the candidates sent one at a time and the `a=candidate` lines inside session descriptions, since one real address slipping through lets the pair connect. The browsers then send checks that all time out, as they would between two incompatible NATs.

- Forward end-of-candidates as usual, and the connection should reach `"failed"` once the PAC timer has run.
- Have the server also drop the end-of-candidates messages, and `"failed"` can never come. That tests the game's own timer.

To see which kind of path a live connection is using, read it from the statistics API:

```javascript
// Returns this side's candidate type for the path in use: "host", "srflx", "prflx" or "relay".
async function localPathType(pc) {
  const stats = await pc.getStats();
  let pair;
  for (const s of stats.values()) {
    if (s.type === "transport" && s.selectedCandidatePairId) {
      pair = stats.get(s.selectedCandidatePairId);
    }
  }
  if (!pair) {
    // Fallback for browsers that omit the transport's selected pair.
    for (const s of stats.values()) {
      if (s.type === "candidate-pair" && s.nominated && s.state === "succeeded") pair = s;
    }
  }
  if (!pair) return null;
  return stats.get(pair.localCandidateId).candidateType;
}
```

Each player should report its own local type, and a pair counts as relayed if either report is `relay`. The remote type is not reliable for this. With [trickle ICE](/wiki/networking/nat-traversal/ice#trickle-ice), where candidates are sent one at a time as they are found, a relayed address can reach the other side as a connectivity check before its candidate arrives through signalling, and that side then records it as `prflx` (RFC 8838). A pair with no `relay` on either side connected directly. A pair with `relay` on either side used TURN, which does not by itself prove that no direct path existed. ICE may settle on a relayed pair before a slower direct check succeeds, and switch later, which fires a `selectedcandidatepairchange` event on the ICE transport. Take the reading once the connection has settled, and again on that event.

## Sources

- Lasse Lumiaho and Varun Singh, [The Big Churn – learning from real usage stats](https://webrtchacks.com/usage-stats/) (webrtcHacks, April 2016) — the callstats.io figures
- [RFC 8828](https://www.rfc-editor.org/rfc/rfc8828): WebRTC IP Address Handling Requirements — the address modes and the advice to deploy TURN over UDP and TCP
- [RFC 8835](https://www.rfc-editor.org/rfc/rfc8835): Transports for WebRTC
- [RFC 8839](https://www.rfc-editor.org/rfc/rfc8839): Session Description Protocol (SDP) offer/answer procedures for ICE, including the related-address field
- [RFC 4787](https://www.rfc-editor.org/rfc/rfc4787): NAT Behavioral Requirements for Unicast UDP
- [RFC 8838](https://www.rfc-editor.org/rfc/rfc8838): Trickle ICE, Section 11 on candidates first seen as peer-reflexive
- [RFC 8863](https://www.rfc-editor.org/rfc/rfc8863): ICE Patiently Awaiting Connectivity (the PAC timer)
- [RFC 5737](https://www.rfc-editor.org/rfc/rfc5737): IPv4 address blocks reserved for documentation
- David Anderson, [How NAT traversal works](https://tailscale.com/blog/how-nat-traversal-works) (Tailscale, 2020)
- Cloudflare, [Realtime pricing](https://developers.cloudflare.com/realtime/sfu/platform/pricing/) and [TURN service](https://developers.cloudflare.com/realtime/turn/)
- W3C, [WebRTC: Real-Time Communication in Browsers](https://www.w3.org/TR/webrtc/) — the `"failed"` state and end-of-candidates
- W3C, [Identifiers for WebRTC's Statistics API](https://www.w3.org/TR/webrtc-stats/)

---
title: "Hole Punching"
weight: 30
---

Hole punching is a technique for opening a direct path between two hosts that are each behind a [network address translation (NAT)](/wiki/networking/nat-traversal) device. Each host sends packets to the other's public address at about the same time. A filtering NAT forwards an inbound packet only if the host behind it has already sent to that sender, so each host's outbound packet "punches a hole" in its own NAT's filter. The other side's packets then arrive through that hole. Nothing on the path is reconfigured. The hosts create, with ordinary outbound traffic, the NAT state that a reply would have found.

## The steps

Hole punching needs a **rendezvous server** that both hosts can already reach. The server's only job is to pass each host the other's addresses. In Ford, Srisuresh and Kegel's description, each host registers with the server, and the server records two addresses for it. One is the host's *private endpoint*, the address and port it believes it is using, which it reports itself. The other is its *public endpoint*, the source address the registration actually arrived from. The public endpoint is exactly what a [STUN](/wiki/networking/nat-traversal/stun) server reports, and in modern systems a STUN server usually supplies it.

```text
  A      private 10.0.0.1:4321     public (NAT A) 155.99.25.11:62000
  B      private 10.1.1.3:4321     public (NAT B) 138.76.29.7:31000

  1.  A --> 138.76.29.7:31000     passes NAT A   (NAT A now has state for B)
                                  dropped at NAT B (no state for A yet)

  2.  B --> 155.99.25.11:62000    passes NAT B   (NAT B now has state for A)
                                  admitted at NAT A (matches step 1)

  3.  A --> 138.76.29.7:31000     admitted at NAT B (matches step 2)
```

1. A sends to B's public endpoint. The packet passes out through NAT A, which records a mapping and a filter entry for B's address. It arrives at NAT B before B has sent anything to A, so NAT B has no matching entry and drops it.
2. B sends to A's public endpoint. NAT B now has an entry for A. At NAT A, the packet matches the entry that A's first packet created, so it is admitted.
3. From here both NATs have state for the flow, and packets pass in both directions.

The first packet is expected to be lost, so both hosts keep sending until something arrives. The addresses in the diagram are the ones Ford et al. use in their Figure 5.

Both hosts also try each other's private endpoint. If the two are behind the same NAT, that path works without the NAT's help. If they are on different networks, a private address such as `10.0.0.1` may belong to some unrelated machine on the local network. For that reason the paper insists that peers **authenticate** whatever answers before trusting it.

## What it requires of the NAT

The technique rests on one property: the public port a NAT uses for traffic to the peer must be the port the rendezvous server saw. That is **endpoint-independent mapping**, defined on the [mapping and filtering](/wiki/networking/nat-traversal/mapping-and-filtering) page. If a NAT assigns a fresh public port for each destination, A's packets to B leave from a port that B was never told about, and B's packets to the advertised port are dropped. The connection can then form only if B's NAT admits A's packet from the unexpected port, which it does if it filters by address alone or not at all. B can then reply to the port the packet actually came from. If B's NAT filters by address and port, which Tailscale reports is overwhelmingly the case in the wild, A's packet is dropped too, and retrying the same addresses never fixes it.

Between two easy NATs, filtering costs one packet and no more. Every filtering variant admits a packet from an address the inside host has already sent to, and step 1 is A sending to exactly the address that B's packet in step 2 comes from.

In the 2005 survey by Ford et al., 310 of 380 reports (82%) showed NATs compatible with UDP hole punching. The reports came from volunteers rather than a random sample, which the authors say limits how far the number generalises.

## TCP

TCP hole punching works the same way at the protocol level, with two complications.

- **Sockets.** Each host has to listen for an incoming connection and make outgoing ones from the same local port it used to reach the rendezvous server. That needs the `SO_REUSEADDR` socket option, plus `SO_REUSEPORT` on systems that separate the two. A UDP host uses one socket for everything.
- **Rejection.** A NAT that answers an unsolicited incoming SYN with a TCP reset (RST), rather than silently dropping it, aborts the peer's connection attempt. Ford et al. call this "not necessarily fatal": the peer retries after a short delay, and a later attempt gets through once the other side's hole is open. It makes hole punching slower. Their survey counted a NAT that sent resets as incompatible.

Which socket ends up holding the connection depends on the operating system. On systems derived from the Berkeley Software Distribution (BSD), the outgoing `connect()` usually succeeds. On Linux and Windows the stream more often arrives through `accept()` on the listen socket, and the `connect()` fails. The application has to take the stream from whichever one produces it, which is why the listen socket is needed. If both SYNs cross their own NATs before reaching the other, the hosts see a *simultaneous open*, a case the TCP state machine already defines. Ford et al. found 184 of 286 reports (64%) compatible with TCP hole punching.

## When one side is hard

When one NAT has endpoint-dependent mapping and the other filters by address and port, the easy side knows the hard side's public address but not the port the hard side will use toward it. It can guess. Tailscale's 2020 write-up works through a birthday-paradox version of the guess. The hard side opens 256 sockets and sends from all of them to the easy side, creating 256 mappings on unknown ports. The easy side then sends probes to random ports on the hard side's address. A probe that lands on any of the 256 open mappings gets through.

| Random probes from the easy side | Chance of a hit |
|---|---|
| 174 | 50% |
| 256 | 64% |
| 1,024 | 98% |
| 2,048 | 99.9% |

At 100 probes per second, that is a 50% chance within two seconds and near-certainty within about 20.

With **both** sides hard, the search is over pairs of ports rather than one port. The same write-up puts 99.9% success at 170,000 probes from each side, about 28 minutes at 100 packets per second. It also notes that each probe consumes a NAT session: a Juniper SRX 300 allows 64,000 active sessions, and one attempt would exhaust it. Two hard NATs means a [relay](/wiki/networking/nat-traversal/turn).

## Keeping the hole open

The NAT state that hole punching creates is ordinary mapping state, and it expires the same way. RFC 4787 requires NATs to keep an idle UDP mapping for at least two minutes. Stateful firewalls often use shorter timers; Tailscale cites 30 seconds as a common value for UDP. An idle peer-to-peer flow therefore sends keepalives from both sides. If the hole closes anyway, the hosts must punch it again, which needs the rendezvous server again.

## Where it runs

Most deployments do not implement hole punching by hand. [ICE](/wiki/networking/nat-traversal/ice) builds it in: its connectivity checks are STUN requests sent directly between the two peers' candidate addresses, from both sides and at the same time, which is hole punching with a test attached to each attempt. [WebRTC](/wiki/networking/webrtc) uses ICE, so every browser video call punches holes. Tailscale's write-up calls ICE "a stunningly elegant algorithm" and describes its own approach as that algorithm with deviations "here and there", with the birthday trick as an optional extra step.

## Sources

- Ford, Srisuresh & Kegel, [Peer-to-Peer Communication Across Network Address Translators](https://bford.info/pub/net/p2pnat/) (USENIX 2005) — Sections 3 and 4 for the procedure, Section 6 for the measurements
- [RFC 5128](https://www.rfc-editor.org/rfc/rfc5128): State of Peer-to-Peer Communication across NATs
- David Anderson, [How NAT traversal works](https://tailscale.com/blog/how-nat-traversal-works) (Tailscale, 2020) — the birthday-paradox figures

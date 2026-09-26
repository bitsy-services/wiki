---
title: "NAT Traversal"
weight: 10
bookCollapseSection: true
---

NAT traversal is the set of techniques that let two hosts exchange packets when each of them sits behind a network address translation (NAT) device. A NAT forwards a packet from outside only if something inside sent a packet out first. Two hosts behind NATs can therefore each reach a server, but neither can reach the other until something arranges for both to send first, or for a third machine to carry the traffic between them.

## Why a NAT blocks the first packet

A NAT shares one public IPv4 address among the hosts on a private network. When an inside host sends a packet out, the NAT rewrites the packet's source address and port to its own public address and a port it chooses, and records the pairing in a table. That table entry is a **mapping**. A reply arriving at the public port is looked up in the table and rewritten back to the inside host.

A packet that arrives at a public port with no mapping has no inside destination, so the NAT drops it. A port that does have a mapping is not open to everyone either. NATs usually also **filter**, forwarding a packet only if it comes from an address the inside host has itself sent to. For a client talking to a server, neither rule matters, because the client always sends first. For two peers, both matter on the first packet. Whichever peer sends first meets either no mapping or a filter that has never seen its address, and the other side's NAT drops the packet.

Two layers of NAT are now common. An internet service provider (ISP) short of IPv4 addresses runs its own [carrier-grade NAT (CGNAT)](/wiki/networking/nat-traversal/mapping-and-filtering#carrier-grade-nat) in front of the customer's home router, and the customer's traffic is translated twice.

## Why IPv6 does not end it

IPv6 has enough addresses that every host can have a public one, and the translation goes away. The first-packet problem does not. A stateful firewall, on a home router, in a corporate network or on the host itself, typically admits inbound packets only on flows an inside host started. That is the same filtering a NAT applies, and it drops the first packet the same way. The techniques on these pages that deal with filtering still apply on IPv6, and the ones that exist only to discover a translated address do not.

## The pieces

Each page is one mechanism. They are listed in reading order, which is also roughly the order an implementation tries them.

| Mechanism | What it does | Page |
|---|---|---|
| Mapping and filtering | the two NAT behaviours that decide which of the techniques below can work | [NAT mapping and filtering](/wiki/networking/nat-traversal/mapping-and-filtering) |
| Address discovery | asks a server on the public internet which address and port a packet arrived from | [STUN](/wiki/networking/nat-traversal/stun) |
| Simultaneous send | both peers send to each other's public address so that each NAT sees an outbound packet first | [Hole punching](/wiki/networking/nat-traversal/hole-punching) |
| Relay | a server with a public address forwards packets between peers that cannot reach each other | [TURN](/wiki/networking/nat-traversal/turn) |
| Orchestration | gathers every candidate address, tests every pairing, and selects the best one that works | [ICE](/wiki/networking/nat-traversal/ice) |
| Explicit request | asks the NAT itself to open a port, where the NAT supports it | [Port mapping protocols](/wiki/networking/nat-traversal/port-mapping) |

One page is not a mechanism. [Running without TURN](/wiki/networking/nat-traversal/without-turn) covers what an application gives up by configuring STUN and no relay: which pairs of users then never connect, who they tend to be, and what it means for a peer-to-peer browser game. It sits after ICE because it assumes it.

Two things sit outside the table because the protocols do not supply them. The peers need a **signalling channel**, usually a server both already have a connection to, to exchange addresses before any of the techniques can start. They also need something to run, and for most readers that is [WebRTC](/wiki/networking/webrtc), which runs STUN, hole punching, TURN and ICE in every browser.

## How often a direct path exists

In 2005 Ford, Srisuresh and Kegel collected 380 reports from volunteers running a test tool behind NATs from 68 vendors. They found that 82% supported UDP hole punching, and that 64% of the 286 reports covering TCP supported it for TCP. The sample was self-selected, which the authors say limits it. In 2020 an engineer at Tailscale, a company that links devices into private networks over direct peer-to-peer connections, estimated that STUN plus hole punching yields a direct connection "over 90% of the time", with relays covering the rest. The article offers that as the author's estimate, not a measurement.

What the numbers agree on is that a direct path is the common case and a relay is still needed. Any system that has to connect every pair of users carries a relay, and the other techniques exist to use it as rarely as possible.

## Sources

- Ford, Srisuresh & Kegel, [Peer-to-Peer Communication Across Network Address Translators](https://bford.info/pub/net/p2pnat/) (USENIX 2005)
- David Anderson, [How NAT traversal works](https://tailscale.com/blog/how-nat-traversal-works) (Tailscale, 2020) — the clearest long-form explanation, written by someone shipping it
- [RFC 5128](https://www.rfc-editor.org/rfc/rfc5128): State of Peer-to-Peer Communication across NATs

## Wiki Pages

{{< section >}}

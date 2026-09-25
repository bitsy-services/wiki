---
title: "NAT Mapping and Filtering"
weight: 10
---

A network address translation (NAT) device handles a flow of UDP packets according to two separate rules. The **mapping** rule decides which public address and port the NAT assigns when an inside host sends a packet out. The **filtering** rule decides which packets arriving at that public port are forwarded back in. RFC 4787 names three variants of each, and the variant a NAT implements decides which [NAT traversal](/wiki/networking/nat-traversal) techniques can get through it.

The notation below is RFC 4787's. `X:x` is the inside host's private address and port, `X':x'` is the public address and port the NAT maps it to, and `Y:y` is a remote host on the internet.

## Mapping: does the public port depend on the destination?

When `X:x` sends to `Y1:y1`, the NAT creates a mapping to some `X':x'`. The question is what happens when the same `X:x` then sends to a different destination, `Y2:y2`.

- **Endpoint-independent mapping.** The NAT reuses `X':x'` for every destination. One inside socket has one public address and port.
- **Address-dependent mapping.** The NAT reuses `X':x'` for any port on the same remote address `Y1`, and creates a new mapping for a different address `Y2`.
- **Address- and port-dependent mapping.** The NAT creates a new mapping for every distinct `Y:y`.

This is the property that decides whether a peer-to-peer connection is cheap. A host learns its public address by sending a packet to a [STUN](/wiki/networking/nat-traversal/stun) server and asking what source address it arrived from. Under endpoint-independent mapping, the answer is also the address a peer will see, so the host can publish it and the peer can use it. Under either dependent variant, a packet sent to the peer leaves from a different public port than the one STUN reported, so the published address is wrong for the peer.

RFC 4787 makes endpoint-independent mapping a requirement (`REQ-1`), with the justification that a NAT failing it "will force the use of a UDP relay." The same document narrows that claim later, when it gets to filtering, as the next section describes. An engineering write-up from Tailscale, a company that links devices over direct peer-to-peer connections, calls endpoint-independent NATs *easy* and the rest *hard*, and argues that this split is the only one a traversal implementation needs to care about.

## Filtering: who may send in?

Once the mapping `X:x` ⇄ `X':x'` exists, the filtering rule decides which inbound packets to `X':x'` reach `X:x`.

- **Endpoint-independent filtering.** Any remote host may send to `X':x'`.
- **Address-dependent filtering.** Only remote addresses that `X:x` has already sent to, from any of their ports.
- **Address- and port-dependent filtering.** Only the exact `Y:y` that `X:x` has already sent to.

Every variant admits a packet from `Y:y` once `X:x` has sent a packet to `Y:y`. Filtering is therefore satisfied by sending first, which is the whole basis of [hole punching](/wiki/networking/nat-traversal/hole-punching). Between two easy NATs, filtering on its own never defeats it.

The two rules interact when one side is hard. The hard NAT sends to the peer from a public port the peer was never told about, so the outcome depends on the peer's filter. If the peer's NAT filters by address only, or not at all, the packet is admitted, and the peer can reply to the port it actually came from. If the peer's NAT filters by address and port, the packet is dropped. RFC 4787 spells this out in its justification for `REQ-8`. When the endpoints use [ICE](/wiki/networking/nat-traversal/ice), the procedure that finds and tests paths between two peers, and the peer's NAT uses address- and port-dependent filtering, "connectivity will require a UDP relay," but with endpoint-independent or address-dependent filtering "ICE will ultimately find connectivity without requiring a UDP relay." How often each case occurs is a separate question. Tailscale reports that in the wild "we're overwhelmingly dealing only with IP-and-port endpoint-dependent firewalls," and concludes that one hard NAT anywhere on the path is enough to break plain hole punching.

RFC 4787 does not require one filtering variant. `REQ-8` recommends endpoint-independent filtering where application transparency matters most, and address-dependent filtering where stricter filtering matters most.

## The old names: cone and symmetric

The first STUN specification, RFC 3489 (2003), classified NATs into four types, and the names are still printed by diagnostic tools and quoted in forum posts. Each is a fixed pairing of a mapping rule with a filtering rule:

| RFC 3489 name | Mapping | Filtering |
|---|---|---|
| Full cone | endpoint-independent | endpoint-independent |
| Restricted cone | endpoint-independent | address-dependent |
| Port restricted cone | endpoint-independent | address- and port-dependent |
| Symmetric | address- and port-dependent | address- and port-dependent |

Four names cover four of the nine combinations. A NAT with address-dependent mapping has no name at all in this scheme, and a test that assumes one of the four will misreport it. RFC 4787 dropped the terms because the terminology "has proven inadequate at describing real-life NAT behavior." The useful reading of the old names is the table's middle column: *symmetric* means dependent mapping, which means hard, and all three kinds of *cone* mean endpoint-independent mapping, which means easy.

## How long a mapping lasts

A NAT deletes a UDP mapping after a period with no packets, because UDP has no connection teardown to tell it the flow has ended. RFC 4787 requires that this timer not expire in less than two minutes (`REQ-5`), with an exception for specific well-known destination ports, and recommends five minutes or more. It also observes that "there is great variation in the values used by different NATs." Stateful firewalls apply their own timers, and Tailscale gives 30 seconds as a common value for UDP.

When the mapping expires, the peer's next packet arrives at a public port with no mapping and is dropped. The connection is not reset, since UDP has no reset, and the peer sees only silence. An application holding a UDP path open therefore sends keepalives from the inside more often than the shortest timer on the path. RFC 4787 requires outbound packets to refresh the timer (`REQ-6`) and only permits inbound ones to. ICE sends a STUN keepalive on each path it is sending data over, whenever it has sent nothing on that path for 15 seconds.

## Hairpinning

Two hosts behind the same NAT may learn each other's public addresses and try to use them. A packet from `X1:x1` addressed to `X2':x2'`, which is another inside host's public mapping on the same NAT, has to be turned around at the NAT and delivered back inside. That turnaround is **hairpinning**. RFC 4787 requires it (`REQ-9`), and requires the hairpinned packet to carry the sender's public address rather than its private one.

Support has historically been poor. In the 2005 survey by Ford, Srisuresh and Kegel, 80 of 335 reports (24%) showed UDP hairpinning and 37 of 286 (13%) showed it for TCP, though the authors warn that their hairpin test "may yield unnecessarily pessimistic results." The standard workaround is to try the private addresses first: two hosts on the same network can reach each other directly without the NAT involved, and ICE ranks those addresses highest for that reason.

## Carrier-grade NAT

A carrier-grade NAT (CGNAT) is a NAT operated by the internet service provider (ISP), shared by many customers, and placed in front of each customer's own router. RFC 6598 reserves `100.64.0.0/10` as shared address space for the network between the two. A home router whose WAN address falls in that range is behind a CGNAT. One whose WAN address is in a private range may be as well, since not every ISP uses the reserved block.

A second layer of NAT changes three things:

- STUN reports the mapping on the **outermost** NAT, which is the one a peer on the internet has to reach. The home router's mapping never appears.
- Two customers behind the same CGNAT cannot use their private addresses, because their home networks are different. They reach each other directly only if the CGNAT hairpins, or if one home router grants a [port mapping](/wiki/networking/nat-traversal/port-mapping), whose address sits on the ISP's inside network where the other customer can reach it. Tailscale's summary: "If both hairpinning and port mapping protocols fail, you're stuck with relaying."
- Port mapping protocols talk to the nearest NAT, which is the home router. For a peer elsewhere on the internet, the CGNAT keeps filtering regardless of what the home router was asked to do.

## Check

The combined mapping behaviour of every NAT on the path can be observed from one socket. Send a STUN request to two different servers from the same local port and compare the public ports they report. The Python script on the [STUN page](/wiki/networking/nat-traversal/stun#check) does exactly this. If both servers report the same public port, the path maps endpoint-independently, which requires every NAT on it to. If they report different ports, at least one NAT on the path has a dependent mapping, and the connection will usually need a [relay](/wiki/networking/nat-traversal/turn).

Filtering cannot be observed this way. Each reply comes from the address and port the client has just sent to, which is the one sender every filtering variant admits, so it reveals nothing about the rest. Testing filtering needs a server that can answer from a second address and port, which is what the experimental RFC 5780 defines.

## Sources

- [RFC 4787](https://www.rfc-editor.org/rfc/rfc4787): Network Address Translation (NAT) Behavioral Requirements for Unicast UDP — the source of the mapping and filtering terms, and of every `REQ` number above
- [RFC 3489](https://www.rfc-editor.org/rfc/rfc3489), Section 5 — the original cone and symmetric definitions
- [RFC 6598](https://www.rfc-editor.org/rfc/rfc6598): IANA-Reserved IPv4 Prefix for Shared Address Space
- [RFC 5780](https://www.rfc-editor.org/rfc/rfc5780): NAT Behavior Discovery Using STUN (Experimental)
- Ford, Srisuresh & Kegel, [Peer-to-Peer Communication Across Network Address Translators](https://bford.info/pub/net/p2pnat/) (2005), Table 1
- David Anderson, [How NAT traversal works](https://tailscale.com/blog/how-nat-traversal-works) (Tailscale, 2020)

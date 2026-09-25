---
title: "Port Mapping Protocols"
weight: 60
---

A port mapping protocol lets a host ask the network address translation (NAT) device in front of it to create a mapping on request. The host names its own address and port, the NAT forwards a public port to it for a stated lifetime, and packets arriving at that public port are admitted whoever sends them. The request is a port forward that software makes, rather than one a person types into a router's admin page. Three such protocols are deployed: Universal Plug and Play Internet Gateway Device (UPnP IGD), NAT Port Mapping Protocol (NAT-PMP), and Port Control Protocol (PCP). Stripped of detail, all three do the same exchange. The host says "forward a public port to this private address and port," and the NAT answers with the public address and port it allocated.

Where one works, the NAT stops being a problem. The host learns a public address that any peer can reach, with no [hole punching](/wiki/networking/nat-traversal/hole-punching) and no dependence on the NAT's [mapping behaviour](/wiki/networking/nat-traversal/mapping-and-filtering). The catch is that it works only on the NAT nearest the host, and only when that NAT has the feature switched on.

## UPnP IGD

UPnP is a family of protocols from the UPnP Forum for devices on a home network to discover and control each other. IGD is the part that controls a router. Discovery uses the Simple Service Discovery Protocol (SSDP), which is HTTP-formatted messages sent over multicast UDP, and control uses SOAP requests with XML bodies. It dates from the late 1990s, and many routers still ship with it.

The authors of NAT-PMP, writing in RFC 6886, count "360 pages of specification spread over 13 separate documents," not including SSDP and XML. They argue that IGD is shaped for a person configuring a gateway, who expects a port mapping to stay until they delete it, and not for software, which should have to prove it is still running by renewing the mapping.

*How NAT traversal works*, an engineering write-up from Tailscale, a company that links devices over direct peer-to-peer connections, notes that UPnP "suffered from a number of high-profile vulnerabilities," and that disabling it by policy is common as a result. Many routers put all three protocols behind a single *UPnP* checkbox, so switching off UPnP switches off the other two as well.

## NAT-PMP

NAT-PMP is Apple's answer, shipped from 2005 in Mac OS X, Bonjour for Windows and AirPort base stations, and published in 2013 as RFC 6886. It does port mapping and nothing else.

- The client sends a small UDP packet to port 5351 of its **default gateway**. It does not search for the router, since the gateway is by definition the device that forwards its traffic, and on a home network that is the NAT.
- One request returns the NAT's public IPv4 address. Another creates a mapping for a given internal port and protocol, and the response gives the public port and the lifetime granted.
- Mappings expire. The recommended lifetime is 7,200 seconds (two hours), and a client that wants to keep one renews it. A client that crashes leaves nothing permanent behind.
- When the NAT's public address changes, it announces the new one by multicast to `224.0.0.1` on port 5350, so clients do not have to poll.

NAT-PMP covers only IPv4.

## PCP

PCP, RFC 6887, is the Standards Track successor to NAT-PMP, published the same month. It keeps ports 5350 and 5351 and a compatible packet format, distinguished by a version number of 2 where NAT-PMP uses 0. It adds IPv6, control of firewall rules as well as NAT mappings, NATs with a pool of public addresses, and an extension mechanism. Two operations carry most of the work:

- **`MAP`** creates an inbound mapping: forward this public port to me. This is what NAT-PMP did.
- **`PEER`** manages an outbound mapping toward one remote peer. It can create that mapping, or extend the lifetime of one the host's own traffic already created, and it tells the host the mapping's public address and port. An application that would otherwise send frequent keepalives to hold a mapping open can learn, and influence, how long the mapping will actually last, which RFC 6887 notes saves battery on mobile devices.

PCP was designed to work with a [carrier-grade NAT](/wiki/networking/nat-traversal/mapping-and-filtering#carrier-grade-nat), a second NAT that the internet service provider runs in front of its customers' routers, as well as with a home router. A client uses a PCP server configured for it, for example through DHCP, and falls back to its default router otherwise. An ISP that runs a PCP server on its carrier-grade NAT and advertises it lets customers map ports on the NAT that matters.

## What they cannot reach

All three talk to one NAT, the nearest. Behind a carrier-grade NAT, a mapping on the home router yields a "public" address that is really in the ISP's shared address space. No peer on the internet can reach it, though another customer behind the same carrier-grade NAT can. A home-router mapping is therefore one of the two ways such neighbours connect directly. The other is the carrier-grade NAT [hairpinning](/wiki/networking/nat-traversal/mapping-and-filtering#hairpinning) their traffic back inside. The protocols give the client no way to find the next NAT up and repeat the request there. The exception is a PCP server the ISP has deliberately configured.

A traversal implementation therefore treats a port mapping as one more [candidate](/wiki/networking/nat-traversal/ice#candidates): useful when present, never relied on. Tailscale queries all three protocols on the default gateway and uses a mapping if one is granted, alongside everything else.

## Is a port mapping a security hole?

One common view is that a NAT protects the hosts behind it by blocking inbound connections, and that a protocol letting any program open a port undermines the protection. The authors of RFC 6886 answer it directly:

> Some people view the property of NATs blocking inbound connections as a security benefit that is undermined by this protocol. The authors of this document have a different point of view.

Their argument is that a NAT exists to share an address, and its refusal of inbound traffic is a side effect of that, not a policy anyone chose. "Blocking of certain connections should occur only as a result of explicit and intentional firewall policy, not as an accidental side effect of some other technology." They also dismiss the threat of rogue local software opening ports for other hosts: such software "could attack such unsuspecting hosts directly itself." On that view the risk is in the service listening on the mapped port, and a host that should not accept connections should not be listening.

The protocols do share a real weakness: they trust the local network. NAT-PMP identifies a client by nothing more than its source address. RFC 6886 notes that a host spoofing that address can create or delete another host's mappings, and that forged address-change announcements make the protocol "unsuitable for use on LANs with large numbers of hosts where one or more of the hosts may be untrustworthy."

## Sources

- [RFC 6886](https://www.rfc-editor.org/rfc/rfc6886): NAT Port Mapping Protocol (NAT-PMP) — Section 5 for security, Section 9 for the comparison with UPnP IGD
- [RFC 6887](https://www.rfc-editor.org/rfc/rfc6887): Port Control Protocol (PCP)
- David Anderson, [How NAT traversal works](https://tailscale.com/blog/how-nat-traversal-works) (Tailscale, 2020) — the sections on port mapping protocols and on double NAT

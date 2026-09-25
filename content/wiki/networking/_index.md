---
title: "Networking"
weight: 23
bookCollapseSection: true
---

How packets get from one host to another: the addresses they carry, the boxes along the path that rewrite those addresses or refuse to forward them, and the protocols two endpoints use to find a path that works anyway.

The first subsection is [NAT traversal](/wiki/networking/nat-traversal). Most hosts on the internet sit behind a network address translation (NAT) device that lets them reach out but not be reached, and two such hosts cannot talk directly without help. The section covers the [property of a NAT](/wiki/networking/nat-traversal/mapping-and-filtering) that decides whether help is possible, and then the tools, in the order they are usually tried. A [STUN](/wiki/networking/nat-traversal/stun) server reports a host's public address. The two hosts [punch holes](/wiki/networking/nat-traversal/hole-punching) in their NATs by sending to each other at the same time. A [TURN](/wiki/networking/nat-traversal/turn) server relays the traffic when that fails, and [ICE](/wiki/networking/nat-traversal/ice) tries every combination and keeps the best one that works.

[WebRTC](/wiki/networking/webrtc) puts those tools in every browser. It is the browser stack for audio, video and data sent directly between two users, and every call it places runs the whole NAT traversal procedure before the first frame of media is sent.

## Where the boundaries fall

[Web](/wiki/web) is about publishing: building a document and serving it to a browser that asked for it. The browser always opens that connection to a server with a public address, so none of the problems in this section arise there. A browser talking to *another browser* is the point where they begin, which is why WebRTC is here rather than there.

The durable ideas in [Computer Science](/wiki/cs) are not about the wire. [IPFS](/wiki/cs/ipfs) runs over a peer-to-peer network that has to traverse NATs like anything else, but it sits in Computer Science because its subject is content addressing, not connectivity.

[Security](/wiki/security) handles keys and credentials on a developer machine. The credentials a relay server issues are covered here, with the relay, because they only make sense next to the protocol that checks them.

## Wiki Pages

{{< section >}}

---
title: "STUN"
weight: 20
---

Session Traversal Utilities for NAT (STUN) is a request/response protocol whose central job is to tell a host what its own address looks like from the far side of a network address translation (NAT) device. The host sends a small UDP packet, a **Binding request**, to a STUN server on the public internet. The server copies the source address and port the packet arrived from into its response. That address is the host's **server-reflexive address**: the public mapping that the outermost NAT created for the socket that sent the request.

The current specification is RFC 8489 (2020). STUN also defines the message format that [TURN](/wiki/networking/nat-traversal/turn) and [ICE](/wiki/networking/nat-traversal/ice) are built from, so most of the packets in a [NAT traversal](/wiki/networking/nat-traversal) exchange are STUN messages whether or not a STUN server is involved.

## What a message contains

Every STUN message is a 20-byte header followed by zero or more attributes.

| Field | Size | Content |
|---|---|---|
| Leading bits | 2 bits | always `00` |
| Message type | 14 bits | method and class; a Binding request is `0x0001`, a Binding success response `0x0101` |
| Message length | 16 bits | length of the attributes in bytes, excluding the header |
| Magic cookie | 32 bits | always `0x2112A442` |
| Transaction ID | 96 bits | random, chosen by the client and echoed in the response |

Each attribute is a type, a length and a value, padded to a multiple of four bytes. A Binding request needs none. The success response carries one that matters, `XOR-MAPPED-ADDRESS`, which holds the reflexive address.

The client matches a response to its request by the transaction ID. There is no connection and no session: the server answers each request from the packet alone, which RFC 8489 notes makes it hard to exhaust a STUN server by flooding it with requests.

## Why the address is XORed

`XOR-MAPPED-ADDRESS` does not hold the address in plain binary. The port is XORed with the top 16 bits of the magic cookie, and an IPv4 address is XORed with the whole cookie. An IPv6 address is XORed with the cookie followed by the transaction ID. The client reverses the operation.

The original specification sent the address in the clear, in an attribute called `MAPPED-ADDRESS`. Deployment found NATs that scanned packet payloads for four bytes matching their own public IP address and rewrote them, which RFC 8489 describes as "the well-meaning but misguided attempt to provide a generic Application Layer Gateway (ALG) function." An application layer gateway (ALG) is NAT code that edits application protocols in transit. It rewrote the one field STUN existed to report, and broke the message's integrity check too. XOR makes the bytes on the wire stop looking like an address, so the NAT leaves them alone.

## Ports and retries

STUN servers listen on port 3478 for UDP and TCP, and on 5349 for STUN over TLS and over Datagram Transport Layer Security (DTLS), the UDP counterpart of TLS.

Over UDP the client retransmits. With the default initial retransmission timeout (RTO) of 500 ms, doubling each time, the client sends up to seven requests: at 0, 0.5, 1.5, 3.5, 7.5, 15.5 and 31.5 seconds. With no answer 39.5 seconds after the first send, the transaction has failed. Over TCP there is no retransmission, since TCP handles it, and the client gives up after the same 39.5 seconds.

## What STUN cannot tell you

The reflexive address is the mapping the NAT created **for traffic to the STUN server**. Whether a peer can use it depends on the NAT's [mapping rule](/wiki/networking/nat-traversal/mapping-and-filtering#mapping-does-the-public-port-depend-on-the-destination). If the mapping is endpoint-independent, a packet from the same socket to the peer leaves through the same public port, and the address is good. If the mapping is endpoint-dependent, the NAT assigns a new port for the peer, and the address STUN reported leads nowhere.

A single reflexive address cannot tell which case applies, and the protocol's history is the record of discovering that. The first version, RFC 3489 (2003), was called *Simple Traversal of UDP Through NATs*. It presented itself as a complete solution: classify the NAT into one of four types, then use the discovered address directly in the application protocol. RFC 5389 (2008) replaced it after experience showed that "classic STUN simply does not work sufficiently well to be a deployable solution." The address was sometimes usable and sometimes not, with no way to find out which, and "many NATs did not fit cleanly into the types defined there." The replacement kept the acronym, changed the name to *Session Traversal Utilities for NAT*, and removed NAT type detection. It recast STUN as a tool that a complete solution uses. [ICE](/wiki/networking/nat-traversal/ice) is that solution: it treats the reflexive address as one candidate among several and tests it rather than trusting it.

## The other jobs STUN does

The Binding method and the message format are reused for everything below. A single UDP port can then carry STUN alongside media: the two zero bits, the magic cookie, and an optional `FINGERPRINT` attribute let a receiver pick STUN packets out of the stream. `FINGERPRINT` is a CRC-32 of the message XORed with `0x5354554e`, the ASCII for "STUN", so that a packet carrying the application's own CRC-32 is not mistaken for STUN.

- **Keepalives.** A Binding *indication* is a one-way STUN message that expects no answer. Sent from the inside, it refreshes the NAT mapping without the overhead of a transaction.
- **Connectivity checks.** ICE tests each candidate path by sending Binding requests directly between the two peers. Each peer authenticates its requests with a short-term credential, a username and password exchanged beforehand through the signalling channel, a path both peers can already reach, usually the application's own server. The `MESSAGE-INTEGRITY` attribute carries an HMAC of the message keyed with that password, using SHA-1, or SHA-256 in the newer `MESSAGE-INTEGRITY-SHA256`.
- **Relaying.** [TURN](/wiki/networking/nat-traversal/turn) is an extension of STUN: it adds methods for allocating a relay address and installing permissions on it, and authenticates them with STUN's long-term credential mechanism.

## Public servers

A STUN server answers each request with one packet and keeps no state, so running one is cheap and public ones exist. Google's `stun.l.google.com:19302` and Cloudflare's `stun.cloudflare.com:3478` both answer the check below. A [TURN](/wiki/networking/nat-traversal/turn) server carries every byte of the traffic it relays, and Tailscale's explanation of why it built its own relay protocol notes that there are "no open TURN servers on the internet."

A public STUN server learns the public address of every client that uses it and nothing more. It never sees the traffic that follows.

## Check

The script below sends a Binding request from one UDP socket to two public STUN servers and decodes the `XOR-MAPPED-ADDRESS` in each response. It needs only the Python standard library.

```python
import os
import socket
import struct

MAGIC = 0x2112A442


def binding(sock, server):
    txid = os.urandom(12)
    sock.sendto(struct.pack("!HHI", 0x0001, 0, MAGIC) + txid, server)
    data, _ = sock.recvfrom(2048)
    msg_type, length, cookie = struct.unpack("!HHI", data[:8])
    assert msg_type == 0x0101 and cookie == MAGIC and data[8:20] == txid
    pos = 20
    while pos < 20 + length:
        attr, alen = struct.unpack("!HH", data[pos:pos + 4])
        value = data[pos + 4:pos + 4 + alen]
        if attr == 0x0020 and value[1] == 0x01:  # XOR-MAPPED-ADDRESS, IPv4
            port = struct.unpack("!H", value[2:4])[0] ^ (MAGIC >> 16)
            addr = struct.unpack("!I", value[4:8])[0] ^ MAGIC
            return socket.inet_ntoa(struct.pack("!I", addr)), port
        pos += 4 + alen + (-alen % 4)  # attributes are padded to 4 bytes


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(3)
sock.bind(("0.0.0.0", 0))
print("local port".ljust(20), sock.getsockname()[1])
for host, port in [("stun.l.google.com", 19302), ("stun.cloudflare.com", 3478)]:
    server = (socket.gethostbyname(host), port)
    print(host.ljust(20), binding(sock, server))
```

Output from behind a home router looks like this, with your own public address in place of the documentation address:

```text
local port           45256
stun.l.google.com    ('198.51.100.7', 61580)
stun.cloudflare.com  ('198.51.100.7', 61580)
```

Read three things from it:

- The public address differs from the machine's own, so there is at least one NAT on the path.
- The public port (61580) differs from the local port (45256), so the NAT does not preserve ports. RFC 4787 allows that, and it is why a host cannot guess its reflexive address without asking.
- Both servers report the **same** public port for the same local socket, so every NAT on the path maps endpoint-independently, and [hole punching](/wiki/networking/nat-traversal/hole-punching) from this network should work with any peer whose NAT is also easy. Two different ports would mean that at least one NAT on the path has a dependent mapping, the "hard" case described on the [mapping and filtering](/wiki/networking/nat-traversal/mapping-and-filtering) page.

## Sources

- [RFC 8489](https://www.rfc-editor.org/rfc/rfc8489): Session Traversal Utilities for NAT (STUN) — Section 5 for the header, 6.2.1 for retransmission, 14.2 for the XOR rationale
- [RFC 5389](https://www.rfc-editor.org/rfc/rfc5389), Section 2 — why classic STUN was abandoned
- [RFC 3489](https://www.rfc-editor.org/rfc/rfc3489): the original "Simple Traversal of UDP Through NATs"
- David Anderson, [How NAT traversal works](https://tailscale.com/blog/how-nat-traversal-works) (Tailscale, 2020)

---
title: "TURN"
weight: 40
---

Traversal Using Relays around NAT (TURN) is a protocol in which a client asks a server on the public internet for a **relayed transport address**, an IP address and port on the server itself, and the server forwards packets between that address and the client. A peer sends to the relayed address as if it were the client. The server wraps each packet and passes it down the client's own connection to the server, and passes the client's packets back out the same way. Both hosts only ever send *to* the server, so the path works through any network address translation (NAT) device and any firewall that allows the client to reach the server at all.

TURN is an extension of [STUN](/wiki/networking/nat-traversal/stun), and most TURN messages are STUN messages with added methods. The current specification is RFC 8656 (2020), which replaced RFC 5766 (2010). It is the fallback in [NAT traversal](/wiki/networking/nat-traversal): the thing that works when [hole punching](/wiki/networking/nat-traversal/hole-punching) cannot. The next section lists exactly when that is.

## When TURN is required

STUN reports an address and never carries a packet. So STUN is enough whenever a direct path exists between the two peers, and TURN is required exactly when none does. Whether a direct path exists depends on both peers' networks together. A player on a strict network may connect directly to one opponent and need a relay for the next, so the useful question is not "does this user need TURN" but "does this pair."

Two NAT behaviours decide most cases, both defined on the [mapping and filtering](/wiki/networking/nat-traversal/mapping-and-filtering) page. A NAT with endpoint-independent **mapping**, called *easy*, uses the same public port for every destination, so the address STUN reported is the address the peer will see. A *hard* NAT, with endpoint-dependent mapping, picks a new public port for each destination. A NAT's **filtering** decides which inbound packets it admits: from anyone, from any port on an address the inside host has sent to, or only from the exact address and port.

| The pair | Direct path? | Why |
|---|---|---|
| On the same local network | Yes, without STUN | each can reach the other's private address |
| One has a public address that accepts inbound UDP | Yes | the other sends first, and nothing filters it |
| Both NATs easy | Yes, with STUN | hole punching works whatever the filtering |
| One hard, the other filtering by address only or not at all | Yes, with STUN | the easy side admits the packet from the unexpected port and replies to it; RFC 4787 says [ICE](/wiki/networking/nat-traversal/ice), the procedure that tests candidate address pairs, "will ultimately find connectivity" here |
| One hard, the other filtering by address and port | **No** | the hard side's packets arrive from a port the other side never sent to, and are dropped |
| Both hard | **No** | neither side can know the port the other will use |
| Outbound UDP blocked on either side | **No**, unless the other peer has a public address that accepts TCP | only TCP leaves the network: TURN over TCP or TLS, or a direct TCP connection to a peer with a public address |
| A browser required to send everything through an HTTP proxy | **No** | the proxy carries TCP only, so TURN over TCP or TLS is the only route (RFC 8828, "Mode 4") |
| One peer IPv4-only, the other IPv6-only | **No** | the two have no address family in common; a TURN server with both relays between them (RFC 8835) |
| Both behind the same [carrier-grade NAT](/wiki/networking/nat-traversal/mapping-and-filtering#carrier-grade-nat), the internet provider's shared NAT, which does not [hairpin](/wiki/networking/nat-traversal/mapping-and-filtering#hairpinning) their traffic back inside | **No** in a browser | the one other remedy, a port mapping on a home router, is not available to a web page |

Outside a browser, two of the **No** rows can sometimes be rescued. An application with its own sockets can use the birthday-paradox port guessing on the [hole punching](/wiki/networking/nat-traversal/hole-punching#when-one-side-is-hard) page for one hard NAT, and a [port mapping protocol](/wiki/networking/nat-traversal/port-mapping) for a cooperative home router. A web page can do neither. The browser's ICE agent gathers one host candidate per local address and makes no attempt to guess ports. The WebRTC API gives the page no socket of its own and no port mapping call. In a browser, every **No** in the table except the UDP-blocked row is final without a relay.

Most rows cannot be detected in advance. Filtering is invisible to a STUN test, so the only way to learn whether a given pair can connect directly is to let ICE try. RFC 8828, which sets how browsers expose addresses, puts its advice to applications plainly: they "SHOULD deploy a TURN server with support for both UDP and TCP connections to the server." What an application loses by not doing so, and what it looks like to its users, is on [Running without TURN](/wiki/networking/nat-traversal/without-turn).

## The allocation

The client sends an **Allocate** request. The server authenticates it, reserves a UDP port, and answers with the relayed address in an `XOR-RELAYED-ADDRESS` attribute. The same response also carries the client's server-reflexive address, the public address and port the client's NAT assigned it, so one TURN exchange also does a STUN server's job. The relayed address, together with its permissions and timers, is the **allocation**.

An allocation lasts 10 minutes unless the client refreshes it with a **Refresh** request. The client can ask for a longer lifetime, and RFC 8656 recommends that servers cap it at an hour. A Refresh with a lifetime of zero deletes the allocation at once. A client that disappears without deleting leaves a relay port reserved until the timer runs out.

The relayed side is always UDP. The client can reach the server over UDP, TCP, TLS over TCP, or Datagram Transport Layer Security (DTLS) over UDP, and the server converts between that and UDP toward the peer. An extension, RFC 6062, adds TCP on the relayed side. The transport rules for [WebRTC](/wiki/networking/webrtc), the browser's peer-to-peer media stack, do not require it (RFC 8835), because two peers that both need TCP can each reach their own TURN server over TCP and relay UDP between the servers.

## Who may send to it

A relayed address that forwarded anything from anyone would let any host on the internet send into a network through its TURN server. TURN prevents this with **permissions**. Each permission names one peer IP address, and the server discards any packet arriving at the relayed address from an IP that has no permission. The port is ignored. RFC 8656 says the design "mimic[s] the address-restricted filtering mechanism of NATs," so a TURN server lets in the same traffic that an [address-dependent filtering](/wiki/networking/nat-traversal/mapping-and-filtering#filtering-who-may-send-in) NAT would.

The client installs permissions with a **CreatePermission** request, which can carry several peer addresses at once. A permission expires after five minutes unless refreshed, and there is no way to delete one early. Only authenticated requests can install permissions. The data-carrying messages below cannot, so an outsider cannot open a hole for themselves.

## How data travels

There are two ways to carry a packet between the client and the server.

- **Send and Data indications** are STUN messages that wrap the payload with the peer's address. RFC 8656 puts their overhead at 36 bytes per packet, which it calls substantial for applications such as voice over IP.
- **ChannelData** messages replace that with a 4-byte header. The client first sends a **ChannelBind** request that binds a channel number, in the range `0x4000` to `0x4FFF`, to a peer's address. After that, the number stands in for the address. A channel binding lasts 10 minutes, longer than a permission, and refreshing it refreshes the permission too.

## What it costs

Every byte of a relayed session passes through the server twice, once in and once out, so the operator pays for the entire bandwidth of every session it carries. RFC 8656 is direct about it: relaying "comes at a high cost to the provider of the TURN server," so a TURN server is best used "only when a direct communication path cannot be found." [ICE](/wiki/networking/nat-traversal/ice) encodes that preference numerically. RFC 8445's recommended type preference for relayed candidates is 0, the lowest possible, which means "used as a last resort."

The cost is one reason TURN servers demand credentials when public STUN servers do not. A service that needs a relay runs its own or buys relay capacity, and issues credentials so that only its own users can allocate.

The relay does not weaken end-to-end encryption. It forwards packets without interpreting them, so an application that encrypts end to end, as WebRTC is required to, exposes only ciphertext and metadata to the relay: who talked to whom, when, and how much.

## Getting through a hostile network

Some networks block outbound UDP entirely. Tailscale reports a university guest Wi-Fi network that blocked all outbound UDP except DNS. TURN over TCP, or over TLS, reaches the server anyway, and WebRTC browsers are required to support both (RFC 8835).

The default ports are 3478 for UDP and TCP and 5349 for TLS and DTLS, the same as STUN. Nothing stops a server from also listening on 443, the port HTTPS uses, which any network that lets browsers reach HTTPS sites directly has to leave open. To a firewall that checks only the port, TURN over TLS there is indistinguishable from HTTPS. The example server list in the TURN REST draft includes a TURN-over-TLS address on 443.

## Credentials

Allocations are authenticated with STUN's **long-term credential mechanism**: a username and password shared between client and server, and a challenge from the server with a realm and a nonce. The client proves it knows the password by keying an HMAC over each request.

A static password cannot be handed to a browser, because anyone can read it out of the page. One answer is ephemeral credentials, as described in *A REST API for Access to TURN Services*, a 2013 Internet-Draft that expired without becoming an RFC and that the open-source coturn server, configured below, implements anyway. The application server and the TURN server share a secret. The application server mints a username and password for each user on demand:

- **username**: an expiry time as a Unix timestamp, a colon, and the user's identifier, for example `1790371886:alice`
- **password**: `base64(HMAC(secret, username))`, with HMAC over SHA-1 as the example algorithm the draft names

The TURN server recomputes the password from the username and the shared secret, then checks that the timestamp has not passed. It needs no user database and no call back to the application.

```python
import base64
import hashlib
import hmac
import time


def turn_credentials(secret: str, user: str, ttl: int = 3600) -> tuple[str, str]:
    username = f"{int(time.time()) + ttl}:{user}"
    mac = hmac.new(secret.encode(), username.encode(), hashlib.sha1).digest()
    return username, base64.b64encode(mac).decode()
```

Only the application server calls this, and only for a user it has already authenticated. A leaked pair works until its timestamp, not forever. RFC 7635 standardises an alternative based on OAuth access tokens.

## Running one: coturn

coturn is an open-source TURN server, and it implements the credential scheme above. A minimal configuration for a server on a cloud virtual machine (VM) that is itself behind the provider's NAT:

```text
listening-port=3478
tls-listening-port=5349
realm=turn.example.org
use-auth-secret
static-auth-secret=replace-with-a-long-random-string
external-ip=203.0.113.10/10.0.0.5
min-port=49152
max-port=65535
cert=/etc/ssl/turn.example.org/fullchain.pem
pkey=/etc/ssl/turn.example.org/privkey.pem
no-multicast-peers
no-tcp-relay
denied-peer-ip=10.0.0.0-10.255.255.255
denied-peer-ip=172.16.0.0-172.31.255.255
denied-peer-ip=192.168.0.0-192.168.255.255
denied-peer-ip=100.64.0.0-100.127.255.255
denied-peer-ip=169.254.0.0-169.254.255.255
denied-peer-ip=0.0.0.0-0.255.255.255
denied-peer-ip=fc00::-fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
denied-peer-ip=fe80::-febf:ffff:ffff:ffff:ffff:ffff:ffff:ffff
denied-peer-ip=64:ff9b::-64:ff9b:1:ffff:ffff:ffff:ffff:ffff
denied-peer-ip=::ffff:0:0-::ffff:ffff:ffff
```

- `use-auth-secret` and `static-auth-secret` turn on the ephemeral-credential scheme above. coturn's own configuration notes say to use it or `lt-cred-mech` with static users, never both.
- `external-ip` maps the VM's private address to its public one. Without it, the server hands clients a relayed address on the private network, which no peer can reach.
- `min-port` and `max-port` are the range relayed addresses are drawn from. The values shown are coturn's defaults. The firewall in front of the server has to admit UDP on the whole range, and both UDP and TCP on 3478 and 5349, since TURN over TCP and over TLS arrive on the TCP side.
- `no-tcp-relay` turns off the RFC 6062 extension, which coturn enables by default. RFC 8835 makes it optional for WebRTC, which does not need it, and leaving it on lets anyone with credentials open TCP connections from the server to any address the deny list does not cover.
- The `denied-peer-ip` lines deserve the most attention. A client chooses which peer addresses to install permissions for, and the server relays to them from inside its own network. Without these lines, any user who can get credentials can reach machines that sit next to the TURN server and are otherwise unreachable from the internet. That is the use case coturn's documentation gives for the option. The IPv4 ranges above are the private blocks, the carrier-grade NAT block, the "this network" block, and the link-local block, which on the major clouds holds the instance metadata service at `169.254.169.254`. The IPv6 lines are needed as well: with no `relay-ip` set, coturn relays from the address of the socket the client came in on, so a server reachable over IPv6 hands out IPv6 relays. They cover unique local addresses (`fc00::/7`) and link-local ones (`fe80::/10`). They also cover the prefixes most likely to embed an IPv4 address and so lead back to the private IPv4 ranges: IPv4-mapped addresses (`::ffff:0:0/96`), and the IPv6-to-IPv4 translation prefixes, which a cloud network may route to a translator. Those are the well-known `64:ff9b::/96` and the local-use `64:ff9b:1::/48` of RFC 8215, which is the one meant for private IPv4 addresses. Add any internal ranges specific to the deployment, and any public addresses whose access rules trust the TURN server. coturn already refuses loopback peers unless `allow-loopback-peers` is set, and `no-multicast-peers` refuses multicast and broadcast addresses.
- One address escapes the deny list: the TURN host's own private address. The two-part form of `external-ip` adds its private half, `10.0.0.5` here, to coturn's allow list, so that clients relayed by the same server can reach each other. coturn checks the allow list before the deny list, and an address on both is allowed. Any UDP service on the TURN host that listens on that address, or on all addresses, is therefore reachable through the relay. Bind other services on the host to loopback, or drop relayed traffic to them with a host firewall rule.

## Check

To confirm a TURN server works, force a browser to use it. Create a peer connection with `iceTransportPolicy: "relay"`, which discards every candidate except relayed ones, and see whether a connection forms. The WebRTC project's *Trickle ICE* sample page takes a server URL, username and password and lists the candidates gathered. A `relay` candidate in that list means the allocation succeeded. No `relay` candidate means the credentials, the ports or the TLS certificate are wrong. A `relay` candidate whose address is private, such as `10.0.0.5`, means `external-ip` is missing or wrong: the allocation worked, but no peer can reach the address it produced.

## Sources

- [RFC 8656](https://www.rfc-editor.org/rfc/rfc8656): Traversal Using Relays around NAT (TURN) — Section 3 is a readable overview of allocations, permissions and channels; Section 21 covers security
- [RFC 8835](https://www.rfc-editor.org/rfc/rfc8835), Section 3.4 — what WebRTC requires of TURN
- [draft-uberti-behave-turn-rest-00](https://datatracker.ietf.org/doc/html/draft-uberti-behave-turn-rest-00): A REST API for Access to TURN Services
- [RFC 7635](https://www.rfc-editor.org/rfc/rfc7635): OAuth-based credentials for STUN and TURN
- [coturn](https://github.com/coturn/coturn) and its annotated [`turnserver.conf`](https://github.com/coturn/coturn/blob/master/examples/etc/turnserver.conf)
- [Trickle ICE](https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice/) sample page
- David Anderson, [How NAT traversal works](https://tailscale.com/blog/how-nat-traversal-works) (Tailscale, 2020)

---
title: "ICE"
weight: 50
---

Interactive Connectivity Establishment (ICE) is the procedure two hosts use to find a working network path between them when either may be behind a [network address translation (NAT)](/wiki/networking/nat-traversal) device. Each host, called an **agent**, gathers every address at which it might be reachable, called its **candidates**. The two agents exchange their candidate lists through a **signalling channel**, a path both can already reach, usually the application's own server. Each then pairs its own candidates with the other's and tests every pair by sending [STUN](/wiki/networking/nat-traversal/stun) requests directly to the peer. STUN is a small request/response protocol whose reply reports the address the request arrived from. The highest-priority pair that succeeds in both directions carries the traffic.

ICE does not guess which technique will work. It tries direct addresses, NAT-translated addresses and relayed addresses in the same pass, ranks them, and lets the tests decide. It is defined in RFC 8445 (2018), which replaced RFC 5245, and [WebRTC](/wiki/networking/webrtc) requires it.

## Candidates

A candidate is a transport address, an IP address and a port, plus its type. There are four types, which differ in where the address came from:

| Type | Keyword | Where it comes from |
|---|---|---|
| Host | `host` | an address on one of the agent's own network interfaces |
| Server-reflexive | `srflx` | the public mapping a NAT created, as reported by a [STUN](/wiki/networking/nat-traversal/stun) server |
| Relayed | `relay` | an address allocated on a [TURN](/wiki/networking/nat-traversal/turn) server |
| Peer-reflexive | `prflx` | an address discovered during the tests themselves, described below |

Gathering is the first phase. The agent lists its interfaces for host candidates. It then sends a STUN Binding request from each host candidate to each configured STUN server, and a TURN Allocate request to each TURN server. The Allocate response carries both a relayed address and a server-reflexive one, so a TURN server supplies both types. Every candidate has a **base**, the address its packets are actually sent from. A server-reflexive candidate's base is the host candidate it was obtained from, since the public address is only the NAT's translation of that local socket. A relayed candidate is its own base, because its packets leave from the TURN server.

A peer-reflexive candidate is never gathered. It appears when a test packet from the peer arrives from an address the agent was not told about, which happens when a NAT between the two peers assigns a [mapping that no STUN server saw](/wiki/networking/nat-traversal/mapping-and-filtering#mapping-does-the-public-port-depend-on-the-destination).

## How candidates are written down

ICE does not define a wire format for the exchange. The format commonly used is Session Description Protocol (SDP), the text format for describing a media session. Each candidate is one `a=candidate` line. These two are from the example in RFC 8839:

```text
a=candidate:1 1 UDP 2130706431 203.0.113.141 8998 typ host
a=candidate:2 1 UDP 1694498815 192.0.2.3 45664 typ srflx raddr 203.0.113.141 rport 8998
```

Read left to right, the fields are the **foundation**, the component, the transport, the priority, the address and the port, and the type. Two candidates share a foundation when they have the same type and transport, their bases have the same IP address, and, if reflexive or relayed, they were obtained from the same server. The component is 1 for a single flow, and a media stream that needs two flows numbers the second one 2. For a reflexive or relayed candidate, `raddr` and `rport` give the related address, which for the `srflx` line is the host candidate behind it. The same session description carries the agent's **username fragment** and **password** (`a=ice-ufrag`, `a=ice-pwd`), which authenticate the tests.

## Priority

Every candidate gets a 32-bit priority. RFC 8445's recommended formula is:

```text
priority = 2^24 × type preference
         + 2^8  × local preference
         + (256 − component ID)
```

The recommended type preferences are 126 for host, 110 for peer-reflexive, 100 for server-reflexive and 0 for relayed. Local preference ranks the agent's own interfaces, from 0 to 65535, and is 65535 when there is only one. So for component 1 on a host with a single interface:

| Type | Priority |
|---|---|
| Host | 2,130,706,431 |
| Peer-reflexive | 1,862,270,975 |
| Server-reflexive | 1,694,498,815 |
| Relayed | 16,777,215 |

The first and third match the two `a=candidate` lines above. The ordering is the whole policy: a direct path on the local network beats a path through a NAT, and both beat a relay. The specification says a type preference of 0 means the type "will only be used as a last resort."

Each agent pairs every local candidate with every remote candidate of the same component and address family, and gives each pair a priority computed from both sides:

```text
pair priority = 2^32 × MIN(G, D) + 2 × MAX(G, D) + (G > D ? 1 : 0)
```

`G` is the priority of the candidate supplied by the controlling agent, the one that makes the final choice of pair, and `D` that of the other, controlled, agent. The roles are described below. Because the formula uses both candidates in a fixed arrangement, both agents compute the same number for the same pair and work through their lists in the same order.

## The tests

The sorted list of pairs is the **checklist**. Every pair is in one of five states: *Frozen*, *Waiting*, *In-Progress*, *Succeeded* or *Failed*. The agent starts a new test at a fixed interval, `Ta`, which defaults to 50 ms and may never be shorter than 5 ms across all of a host's agents together. Each test can create a new NAT mapping, and RFC 8445 explains the pacing by the experience that "many NAT devices have upper limits on the rate at which they will create new bindings." It adds that deployments based on early drafts of the specification "tended to overload rate-constrained access links."

A test, called a **connectivity check**, is a STUN Binding request sent from the local candidate's base to the remote candidate's address. It is authenticated with STUN's short-term credentials. The username is the peer's username fragment, a colon and the sender's own, for example `RFRAG:LFRAG`, and the message is keyed with the peer's password. RFC 8445 requires at least 24 bits of randomness in the username fragment and 128 bits in the password, so a stranger cannot forge a check.

When agent R receives L's check, it answers and immediately queues a **triggered check** in the other direction on the same pair. The result is a four-message handshake, two requests and two responses, after which each side knows packets flow in both directions. Both agents send to each other's addresses at nearly the same time, and each outbound request opens the sender's own NAT to the peer, which makes a connectivity check [hole punching](/wiki/networking/nat-traversal/hole-punching) with a verification attached. The STUN response also reports the address the request arrived from, which is how peer-reflexive candidates are found.

Candidates sharing a foundation are likely to succeed or fail together. So ICE starts with one pair per foundation *Waiting* and the rest *Frozen*, and unfreezes the others as results come in, which avoids repeating the same doomed test many times.

## Who decides

One agent is **controlling** and the other **controlled**. When both are full implementations, the agent that initiated the session is controlling. The controlling agent chooses which successful pair to use. It **nominates** the pair by repeating the check with a `USE-CANDIDATE` attribute, and once that check succeeds, the pair is **selected** for that component. Each check carries an `ICE-CONTROLLING` or `ICE-CONTROLLED` attribute holding a random 64-bit tiebreaker. If both agents believe they hold the same role, the tiebreaker settles it.

RFC 5245 allowed *aggressive nomination*, in which the controlling agent nominated pairs as it went so that media could start early. RFC 8445 removed it: data may now flow on any pair that has passed a check, so nothing is gained by nominating early.

## After a pair is selected

The path has to stay open. An agent sends a STUN Binding indication, a one-way message that expects no reply, on the selected pair whenever it has sent nothing for 15 seconds, which keeps the NAT mappings along it alive. WebRTC adds **consent freshness** (RFC 7675), which uses full Binding requests rather than indications, because only a request's reply shows that the peer is still there. It sends one every five seconds by default, randomised between 0.8 and 1.2 times that, and stops transmitting if no response has arrived for 30 seconds. The purpose is to stop a browser sending media at a host that has stopped wanting it, not only to hold a NAT open.

When the network changes, for example a phone moving from Wi-Fi to cellular, the old candidates may be dead. An **ICE restart** runs the whole procedure again under a new username fragment and password, while media continues on the old path until the new one is ready.

## Trickle ICE

Gathering is slow compared with sending a message. A TURN allocation takes at least a round trip to the server, and a server that does not answer holds up the list until the STUN retries give up. In classic ICE, an agent waits for gathering to finish before sending its candidate list.

**Trickle ICE** (RFC 8838) sends each candidate through the signalling channel as soon as it is gathered, and the peer adds it to the checklist on arrival. Host candidates, which need no network round trip, go out first, and tests on them can start while relayed candidates are still being allocated. An explicit *end-of-candidates* indication tells the peer when no more are coming. The browser API is built around trickling: each new candidate appears as an `icecandidate` event, which the application forwards to the peer.

## ICE-lite

A server with a public address has no NAT to traverse. RFC 8445 defines a reduced **lite** implementation for agents that "will always be connected to the public Internet and have a public IP address." A lite agent offers only host candidates, never sends checks, and answers the checks it receives. A full agent paired with a lite one always takes the controlling role. A media server that browsers connect to, such as a [selective forwarding unit](/wiki/networking/webrtc#more-than-two-people) routing a group call, fits that description.

## What ICE does not do

ICE needs the two agents to exchange candidate lists, credentials and roles before any test can start, and it does not say how. That channel is the application's job. ICE was first specified for offer/answer protocols such as Session Initiation Protocol (SIP), the call-setup protocol of internet telephony, and there SIP messages carried the lists. A browser application supplies its own channel, for example a WebSocket to the application's server. WebRTC does not specify one either, and leaves it to the application.

## Sources

- [RFC 8445](https://www.rfc-editor.org/rfc/rfc8445): Interactive Connectivity Establishment (ICE) — Section 2 is a readable overview; 5.1.2 for priorities, 6.1.2 for the checklist, 7 for the checks
- [RFC 8839](https://www.rfc-editor.org/rfc/rfc8839): SDP offer/answer procedures for ICE, including the `a=candidate` grammar
- [RFC 8838](https://www.rfc-editor.org/rfc/rfc8838): Trickle ICE
- [RFC 7675](https://www.rfc-editor.org/rfc/rfc7675): STUN usage for consent freshness

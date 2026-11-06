---
title: "Network Address Linkage"
weight: 40
---

A network address links two [operational personas](/wiki/security/operational-persona), managed identity sets meant to stay separate, when records show both acting from one IP address. A service writes the account, the address and the time of each sign-in, so two accounts on one address, or taking turns on one, can be joined by whoever reads those rows.

The readers are the service and anyone who reaches its logs through [a breach or a legal demand](/wiki/security/operational-persona/isolation-failures/shared-custodian). A service that keeps few logs can be ordered to start. "The Internet is generally not anonymous," Proton's threat model warned in 2014, "and if you are breaking Swiss law, a law-abiding company such as Proton Mail can be legally compelled to log your IP address." A Swiss ruling in 2021 later narrowed what email services must retain and hand over, and Proton's account of it is under Further reading.

## What an address shows

An address is evidence about a connection, and its strength depends on how many people share it. A home router puts a household behind one address, and [carrier-grade NAT](/wiki/networking/nat-traversal/mapping-and-filtering#carrier-grade-nat) can put many households behind one. A single match on a shared address says little, and the same two accounts matching across months and across networks says a lot.

A network can narrow the field without seeing any content. In 2013 a Harvard student emailed bomb threats through Tor and a disposable mail service. The FBI affidavit reports that the university "was able to determine that, in the several hours leading up to the receipt of the e-mail messages", he "accessed TOR using Harvard's wireless network". Tor masked his address from the mail service. His use of Tor on a campus network that registers its devices stood out, and he confessed when interviewed. Slate's analysis notes that with enough Tor users on that network, the list might have been too long to narrow.

## What a virtual private network changes

A virtual private network (VPN) replaces the address a service sees with the provider's exit address. The join moves to the provider, which sees the real address and the destinations, and several gaps remain.

One VPN account used by two personas gives the provider, and anyone with its records, the link. A session opened before the tunnel is up writes the real address once, permanently. A tunnel that carries only IPv4 leaves IPv6 on the original route: Perta and colleagues found in 2015 that the majority of 14 popular commercial VPN services leaked IPv6 traffic.

A page in the browser can look past a tunnel as well. [WebRTC's public-address candidates](/wiki/networking/webrtc#local-addresses-and-privacy) reveal the address the browser appears from, and RFC 8828 warns that with a split-tunnel VPN, one that routes only some traffic through the tunnel, "WebRTC can discover not only the public address for the VPN, but also the ISP public address over which the VPN is running".

Setting up the route is part of the record too. The 2018 US indictment of twelve officers of Russian military intelligence (GRU) alleges that the VPN account used to log in to the `@Guccifer_2` Twitter account was opened "from the same server that was also used to register malicious domains" for the intrusions at issue in the case. The logins showed the VPN's address, and the allegation rests on where the account had been opened.

## One route per persona

Route selection cannot rest on memory. A persona that needs this property sends all its traffic through its own route and enforces that at a layer it cannot skip, such as a [virtual machine](/wiki/security/operational-persona/technical-context#layers-of-separation) whose only network path is the tunnel, or a firewall rule that drops everything else.

Keep the route stable. [Google challenges sign-ins from a new location](/wiki/security/operational-persona/cohesion#consistency-with-what-services-expect), so an exit that changes country every week invites a lockout.

## Check

From inside the persona's context, ask what address the world sees, over each protocol:

```bash
curl -4 -s https://ifconfig.me; echo
curl -6 -s https://ifconfig.me; echo
```

Both should show the persona's route, and an address you recognize as home is the failure. A connection error on the second line means no IPv6 route exists, which is acceptable. In the browser, `about:webrtc` in Firefox and `chrome://webrtc-internals` in Chrome list the candidates a page gathered during a call.

## Further reading

- Proton, [Important clarifications regarding arrest of climate activist](https://proton.me/blog/climate-activist-arrest) (2021)
- Josephine Wolff, [Harvard exam bomb threats: How the alleged hoaxer failed to cover his online tracks](https://www.slate.com/articles/technology/future_tense/2013/12/harvard_exam_bomb_threats_how_the_alleged_hoaxer_failed_to_cover_his_online.html), *Slate* (2013), which quotes the affidavit
- Perta, Barbera, Tyson, Haddadi & Mei, [A Glance through the VPN Looking Glass: IPv6 Leakage and DNS Hijacking in Commercial VPN clients](https://petsymposium.org/popets/2015/popets-2015-0006.pdf), PETS 2015
- [RFC 8828: WebRTC IP Address Handling Requirements](https://www.rfc-editor.org/rfc/rfc8828)
- [Indictment, *United States v. Netyksho*](https://www.justice.gov/usdoj-media/sco-durham/media/1126686/dl?inline=), No. 1:18-cr-00215 (D.D.C. 2018), paragraph 45

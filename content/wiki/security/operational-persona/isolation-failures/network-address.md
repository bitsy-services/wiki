---
title: "Network Address Linkage"
weight: 40
---

A network address links two [operational personas](/wiki/security/operational-persona), the sets of accounts and credentials one person runs as separate identities, when records show both acting from one IP address. A service writes the account, the address and the time of each sign-in, so two accounts on one address, or taking turns on one, can be joined by whoever reads those entries.

The readers are the service and anyone who reaches its logs through [a breach or a legal demand](/wiki/security/operational-persona/isolation-failures/shared-custodian). A service that keeps few logs can be ordered to start. "The Internet is generally not anonymous," warned the 2014 threat model of Proton, an encrypted mail service, "and if you are breaking Swiss law, a law-abiding company such as Proton Mail can be legally compelled to log your IP address." A Swiss ruling in 2021 later narrowed what email services must retain and hand over.

## What an address shows

An address is evidence about a connection, and its strength depends on how many people share it. A home router puts a household behind one address, and [carrier-grade NAT](/wiki/networking/nat-traversal/mapping-and-filtering#carrier-grade-nat) can put many households behind one. One match on a shared address is weak evidence. The same two accounts matching across months and across networks is strong.

A network can narrow the field without seeing any content. In 2013 a Harvard student was charged over bomb threats emailed through Tor, the anonymity network, and a disposable mail service, and confessed. The FBI affidavit reports that the university "was able to determine that, in the several hours leading up to the receipt of the e-mail messages", he "accessed TOR using Harvard's wireless network". *Slate*'s reading is that Harvard consulted its network logs, and that the logs showed only that he or someone on his computer was using Tor at the time. With enough Tor users on that network, it adds, the suspect list might have been too long to narrow.

## What a virtual private network changes

A virtual private network (VPN) replaces the address a service sees with the provider's exit address. The join moves to the provider, which sees the real address and the destinations. One VPN account used by two personas gives the provider, and anyone with its records, the link. A session opened before the tunnel is up writes the real address once, permanently. A tunnel that carries only IPv4 sends IPv6 by the original route: Perta and colleagues found in 2015 that the majority of 14 popular commercial VPN services leaked IPv6 traffic.

A page in the browser can look past a tunnel as well. [WebRTC, the browser's real-time connection system](/wiki/networking/webrtc#local-addresses-and-privacy), gathers the addresses a browser can be reached on and reveals its public address to the page. RFC 8828 warns that with a split-tunnel VPN, one that routes only some traffic through the tunnel, "WebRTC can discover not only the public address for the VPN, but also the ISP public address over which the VPN is running".

Setting up the route is part of the record too. The 2018 US indictment of twelve officers of Russian military intelligence (GRU), over the hacking and release of documents during the 2016 US election, alleges that a VPN account was used to log in to `@Guccifer_2`, the Twitter account of a fictitious persona that released some of those documents. It alleges that the account was opened "from the same server that was also used to register malicious domains" for the hacking. A login through a VPN would show the VPN's address, and this allegation concerns where the account was opened.

## One route per persona

Route selection cannot rest on memory. A persona that needs this property sends all its traffic through its own route and enforces that at a layer it cannot skip, such as a [virtual machine](/wiki/security/operational-persona/technical-context#layers-of-separation) whose only network path is the tunnel, or a firewall rule that drops everything else.

Keep the route stable, or the operator risks a lockout. Google says "if we detect a suspicious sign-in attempt (say, from a new location or device), we'll ask for additional proof that it's really you". An exit that changes country every week invites that challenge, and the proof goes to a recovery method. Without a recovery phone, Google says it "might fall back on the weaker knowledge-based challenges", and in its own experiment 38% of users did not have their phone when challenged and 34% could not recall their secondary email address.

## Check

From inside the persona's context, ask what address the world sees, over each protocol:

```bash
curl -4 -sS https://ifconfig.me; echo
curl -6 -sS https://ifconfig.me; echo
```

Both should show the persona's route, and an address you recognize as home is the failure. A connection error on the second line usually means no IPv6 route exists, and can also mean the site is down. In the browser, `about:webrtc` in Firefox and `chrome://webrtc-internals` in Chrome list the addresses a page gathered during a call.

## Further reading

- Proton, [Important clarifications regarding arrest of climate activist](https://proton.me/blog/climate-activist-arrest) (2021), including its update on the Swiss ruling
- Josephine Wolff, [Harvard exam bomb threats: How the alleged hoaxer failed to cover his online tracks](https://www.slate.com/articles/technology/future_tense/2013/12/harvard_exam_bomb_threats_how_the_alleged_hoaxer_failed_to_cover_his_online.html), *Slate* (2013), which quotes the affidavit
- Perta, Barbera, Tyson, Haddadi & Mei, [A Glance through the VPN Looking Glass: IPv6 Leakage and DNS Hijacking in Commercial VPN clients](https://petsymposium.org/popets/2015/popets-2015-0006.pdf), PETS 2015
- [RFC 8828: WebRTC IP Address Handling Requirements](https://www.rfc-editor.org/rfc/rfc8828)
- [Indictment, *United States v. Netyksho*](https://www.justice.gov/usdoj-media/sco-durham/media/1126686/dl?inline=), No. 1:18-cr-00215 (D.D.C. 2018), paragraph 45
- Google Security Blog, [How effective is basic account hygiene at preventing hijacking](https://security.googleblog.com/2019/05/new-research-how-effective-is-basic.html) (2019)

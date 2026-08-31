---
title: "Fake Job Offers"
weight: 88
---

Two unrelated frauds run through the same pipeline. One is a targeted intrusion: an engineer at a crypto company is approached by a recruiter, taken through a convincing interview process, and asked to run code as part of it. The code installs a backdoor, and the objective is the employer's signing keys. The other is a mass-market deposit trap: an advertisement for "crypto task work" or "order boosting" that pays small sums until the worker is required to deposit their own money to unlock the next tier, at which point the money is gone.

They share a lure and nothing else. The first is state-attributed and aimed at a handful of people with production access; the second is volume fraud aimed at anyone answering a job ad, shading into [money mule](/wiki/economics/finance/fraud/money-mule) recruitment and, at its worst end, into human trafficking. The defences have nothing in common, so the two are treated separately here.

## The targeted intrusion

The approach arrives on a professional network, a developer forum, or a freelance marketplace, from a recruiter profile with plausible history, and the process that follows is built to look like hiring rather than like an attack: several rounds, real-sounding compensation, a technical exercise. The exercise is the payload. Published variants include a take-home assignment in a private repository, a "debug this failing test" request, a video-call client that demands an update before the interview can start, and instructions to fix a camera or audio driver when the call fails to connect. What lands is a remote access trojan (RAT) or an information stealer that sweeps browser credential stores, wallet extension data, and key material on disk.

Attribution belongs to the analysts rather than to this page. US and allied government advisories, together with threat-intelligence reporting from Google's Mandiant, Microsoft, and Palo Alto Networks, attribute a large share of this activity to clusters linked to the Democratic People's Republic of Korea (DPRK). Two published campaign names cover most of it: **Operation Dream Job**, named by ClearSky in 2020 for fake recruitment aimed initially at defence and aerospace staff and later at crypto, and **Contagious Interview**, named by Unit 42 in 2023 for the developer-focused version that delivers its payload through the interview exercise itself.

Three mechanisms carry the payload past ordinary code review.

**Malicious packages on public registries.** A dependency published to npm or PyPI under a name close to a real one, or a package that exists solely to be pulled in by the assignment, executes on install rather than at runtime. Reading the assignment's source does not surface it.

**A payload outside the reviewed source.** Build scripts, test fixtures, editor configuration, and container definitions all execute and none of them are what a candidate reads when reviewing a take-home. A repository can look clean in every file a reviewer opens.

**The "fix your setup" step.** A video call that fails to connect, followed by a link and instructions to install a driver or a patched client, converts the interview into a supported installation session with the target's cooperation.

## Cases

**Axie Infinity / Ronin, March 2022.** Roughly $620 million was drained from the Ronin bridge after an attacker obtained enough validator signatures to authorize withdrawals — four of Sky Mavis's own validator keys plus access to the Axie [DAO](/wiki/economics/finance/defi/dao) validator, five of the nine required. Reporting after the incident traced the entry point to a senior engineer who had been recruited through a fake job offer and had opened a document delivered as part of it. The FBI publicly attributed the theft to the Lazarus Group in April 2022, and the [Office of Foreign Assets Control](/wiki/economics/finance/regulation/ofac-sanctions) added the receiving address to its sanctions list.

## The inverse: real jobs, false identities

The same actors also apply for genuine remote positions. Investigators describe applicants presenting stolen or fabricated identities, passing interviews, and being hired as ordinary remote contractors, with company laptops shipped to a facilitator inside the US who racks them at home and provides remote access so the worker appears to log in domestically. The Department of Justice (DOJ) charged an Arizona woman in 2024 with running such a laptop farm across dozens of employers; she pleaded guilty in 2025. Salary revenue flows back to the DPRK, which makes the arrangement a sanctions matter as well as a fraud.

No endpoint tooling solves this, because it is a hiring problem. The employer's exposure is paying a sanctioned party, which is strict liability, plus whatever access the hire held; identity verification at onboarding, live video that is not pre-recorded, and shipping addresses that match the claimed residence are where it gets caught.

## The mass-market fake job

The consumer version needs no malware. A message offers remote work rating apps, "optimizing" listings, or completing tasks in a web console. The first tasks pay, and small withdrawals succeed. Then the account shows a negative balance, a "frozen" commission, or a tier that requires the worker to deposit their own funds — often in stablecoins — to continue. Each deposit unlocks a further demand. The console is a display, the balance is a number in a database, and the deposits are the entire product. The structure is a [Ponzi scheme](/wiki/economics/finance/fraud/ponzi-scheme) run one victim at a time, dressed as employment so the victim files it under work rather than under investment. The Federal Trade Commission (FTC) reported in December 2024 that consumer reports of these task scams had risen several-fold since 2023.

Two adjacent recruitments use the same ads. "Payment processing agent" and "financial operations assistant" roles are money mule recruitment: the work is receiving funds and forwarding them, which is money laundering whatever the job title says, and the worker is the identity of record when it unwinds. And overseas offers of well-paid customer-service or translation work in Southeast Asia feed the compounds described on [pig butchering](/wiki/economics/finance/fraud/pig-butchering); the UN human rights office estimated in 2023 that hundreds of thousands of people across Myanmar and Cambodia were being held in conditions of forced criminality, having answered exactly such an advertisement. The recruit becomes staff, and then a victim.

## Defence

For an engineer or a company with keys:

1. **Separate signing infrastructure from development machines.** No take-home, dependency, or interview tool should ever execute on a host that holds production keys or can reach the signing path. This is the control that bounds the loss when the rest fails.
2. **Run any candidate or recruiter-supplied code in a disposable virtual machine or container**, with no credentials mounted and no persistent access, and discard it afterwards.
3. **Treat code execution or a driver install as a red flag in any interview.** Legitimate processes do not need a candidate to patch a video client, and the request is diagnostic on its own.
4. **Assume the target is the access, not the person.** A junior engineer with deployment rights is a better target than an executive without them, so the briefing has to reach everyone who holds a key rather than everyone senior.

For a jobseeker: an employer that requires a deposit is not an employer, a role whose duties are receiving and forwarding money is a laundering role, and an overseas offer arranged over a messaging app with travel paid by the recruiter is worth checking against the company's own published listings before boarding anything.

## Where the law lands

The intrusion side is charged as computer intrusion, wire fraud, and money laundering, but is handled at least as much through sanctions as through indictment, because the defendants are rarely reachable. Designations against DPRK-linked hacking groups and the addresses receiving their proceeds bind everyone downstream: an exchange handling a designated address's funds is exposed regardless of knowledge. Domestic facilitators — laptop-farm operators, identity providers — are charged with wire fraud, aggravated identity theft, and sanctions violations. The mass-market task scam is ordinary wire fraud, prosecuted rarely because the operators sit outside the jurisdiction, and its practical remedy matches a [wallet drainer](/wiki/economics/finance/fraud/wallet-drainer): the deposit addresses are traceable, and the cash-out points are the only place the loss can be interrupted.

## External links

- [US cybersecurity advisories](https://www.cisa.gov/news-events/cybersecurity-advisories) — the joint government advisories on DPRK cyber activity, including the fake-recruitment campaigns
- [Unit 42 threat research](https://unit42.paloaltonetworks.com/) — where the Contagious Interview campaign was named and its later variants tracked
- [Google Threat Intelligence blog](https://cloud.google.com/blog/topics/threat-intelligence) — Mandiant reporting on the DPRK clusters behind the recruitment lures
- [FTC data spotlights](https://www.ftc.gov/news-events/data-visualizations/data-spotlight) — the consumer-report data behind the task-scam and job-scam figures
- [OFAC sanctions list search](https://sanctionssearch.ofac.treas.gov/) — the designations, including addresses tied to the Ronin theft

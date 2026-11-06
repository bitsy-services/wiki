---
title: "Browser and Device Linkage"
weight: 30
---

A browser and the device under it identify themselves independently of any account. A site that sees two accounts arrive from one browser holds evidence connecting them, and if those accounts belong to two [operational personas](/wiki/security/operational-persona), managed identity sets meant to stay separate, that evidence is a link. The evidence takes three forms: a stored cookie, a fingerprint computed from what the browser reports about itself, and an identifier the operating system hands to apps.

## Cookies

A site sets a cookie on the first visit and reads it on every visit after. Sign in to one account, sign out and sign in to another in the same browser, and the site's logs hold two accounts under one cookie. Signing out ends the session and can leave a longer-lived cookie in place.

A [browser profile or container](/wiki/security/operational-persona/technical-context#layers-of-separation) gives each persona its own cookie store, so the site sees two unrelated visitors. Mozilla describes the mechanism for containers: site data is keyed by container as well as by site, so a cookie set in one is not readable in another.

Between sites the question is different. A tracker embedded on many sites can follow a shared third-party cookie across them. Firefox's Total Cookie Protection keeps "a separate cookie jar for each website you visit", which addresses that path and leaves the same-site case above untouched.

## Fingerprints

A fingerprint is the combination of values a browser reports: user agent, screen size, fonts, time zone, language. It needs no storage, so clearing cookies does not change it.

How identifying it is depends on the population. Peter Eckersley's 2010 study found 83.6% of browsers unique in a sample of privacy-conscious visitors, and 94.2% among those with Flash or Java. Gómez-Boix and colleagues found only 33.6% unique across 2,067,942 fingerprints from one of the top 15 French websites in 2018, and credit the removal of browser plugins for part of the drop. They add that non-unique fingerprints "tend to be fragile": a change in a few features can make one unique.

A fingerprint also works together with an address. Eckersley notes that 15 to 20 bits of fingerprint "will in almost all cases be sufficient to uniquely identify a particular browser, given its IP address, its subnet, or even just its Autonomous System Number". Two browser profiles on one machine have separate cookies and report mostly the same values, so a site can see two cookies, one fingerprint and one [address](/wiki/security/operational-persona/isolation-failures/network-address).

The Tor Browser project tries to make every user of a version "behave as uniformly as possible", and reports that uniformity has served it better than randomizing values. Tools that change a browser's reported values on their own carry the risk Eckersley named: "anti-fingerprinting privacy technologies can be self-defeating if they are not used by a sufficient number of people". For a persona that has to be unlinkable against the sites themselves, the options are a browser built for uniformity or a [separate device](/wiki/security/operational-persona/technical-context#layers-of-separation).

## Device identifiers

Native apps can read identifiers a web page cannot. On Android 8 and later, `ANDROID_ID` is "unique to each combination of app-signing key, user, and device". One vendor's apps on one phone therefore read the same value whichever account is signed in, and a second Android user on the phone gets another. Two personas in one app on one phone look to the vendor like two accounts on one device.

## A compromised device

All of this concerns what a site can observe. A compromised device is a separate failure, of containment: malware running as the user can read every session and key that user holds, [whichever profile they sit in](/wiki/security/operational-persona/technical-context#layers-of-separation).

## Check

Open [Cover Your Tracks](https://coveryourtracks.eff.org/), the Electronic Frontier Foundation's fingerprint test, in each persona's browser profile, and compare the reported values. Identical hardware, font and time-zone values mean a site that sees both profiles can connect them, and a persona that has to resist that needs a stronger layer. Then sign in to a test account in one profile and confirm that the other profile shows it signed out.

## Further reading

- Eckersley, [How Unique Is Your Web Browser?](https://coveryourtracks.eff.org/static/browser-uniqueness.pdf), PETS 2010
- Gómez-Boix, Laperdrix & Baudry, [Hiding in the Crowd: an Analysis of the Effectiveness of Browser Fingerprinting at Large Scale](https://doi.org/10.1145/3178876.3186097), WWW 2018
- Mozilla, [Containers](https://wiki.mozilla.org/Security/Contextual_Identity_Project/Containers) and [Total Cookie Protection](https://support.mozilla.org/en-US/kb/introducing-total-cookie-protection-standard-mode)
- Tor Project, [The Design and Implementation of the Tor Browser](https://2019.www.torproject.org/projects/torbrowser/design/), section 4.6 on fingerprinting
- Android Developers, [`Settings.Secure.ANDROID_ID`](https://developer.android.com/reference/android/provider/Settings.Secure#ANDROID_ID)

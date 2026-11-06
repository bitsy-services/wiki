---
title: "Behavioural Correlation"
weight: 70
---

Behavioural correlation links two [operational personas](/wiki/security/operational-persona), managed identity sets meant to stay separate, through what their operator does without choosing to: the places they post from, the hours they keep, the way they write and code. No value is shared between the two sides, so there is no setting to change, and the evidence accumulates with every post.

Goga and colleagues tested the assumption directly in 2013. Their paper describes "users' tendency to assume that, if they maintain different personas with different names, the accounts cannot be linked together", and links accounts across Yelp, Flickr and Twitter from location, timing and language model alone. Location proved the strongest of the three. Combined, the features matched Flickr users to Twitter accounts about as accurately as attacks that use usernames, and between Yelp and Twitter they found 37% more accounts than usernames did.

## Places

A person's posts cluster around where that person lives and goes, and a geotag or a photo's metadata records the place directly. Removing the [metadata](/wiki/security/identity-separation#how-identities-get-linked) from a file removes the direct record. A persona that keeps describing the same city's weather and transit still publishes the place.

## Hours

Each commit [records its author's UTC offset](/wiki/security/identity-separation#how-identities-get-linked), and a history shows the hours its author keeps. Setting [`TZ=UTC`](/wiki/security/operational-persona/technical-context#what-the-context-publishes) removes the offset and leaves the hours, so two personas that go quiet in the same eight hours of each day still share a shape.

Exact timing links more directly. Goga's group matched accounts whose posts carried almost identical timestamps, the result of an app posting to several sites at once. A persona that posts within seconds of another, every time, needs no further analysis.

## Writing

[Stylometry](/wiki/cs/stylometry) attributes text by the rates of common words, which a writer does not consciously choose. Scale limits it: Narayanan and colleagues reported in 2012 that with 100,000 candidate authors their classifiers named the right author in over 20% of cases and had the right author in the top 20 guesses in about 35%. Allowing the classifier to decline when unsure raised the precision of its top guess from 20% to over 80%, with its recall halved.

## Code

Source code has a style as well. Caliskan-Islam and colleagues attributed C and C++ solutions from Google Code Jam, a programming contest, to their authors at 94% accuracy among 1,600 programmers and 98% among 250, using features from the code's syntax tree that they describe as "difficult to obfuscate". They also found that skilled programmers were easier to attribute than less skilled ones. Contest code is a controlled sample, and these figures are from that setting.

## What an observer needs

An observer needs samples from both sides and a list of candidates. The list matters most. Searching everyone for the author of a pseudonym's text is the hard version of the problem, and confirming a suspicion is the easy one: an observer who already suspects Ines has to compare two bodies of text, the setting in which attribution works best. So the risk depends less on the method than on whether anything has already pointed at her, usually one of the [cheaper failures](/wiki/security/operational-persona/isolation-failures).

## What lowers it

Volume is the main control. RFC 6973 says "pseudonymity is strengthened when less personal data can be linked to the pseudonym; when the same pseudonym is used less often and across fewer contexts". A persona that publishes less, in fewer places, and is replaced more often gives each method a smaller sample.

Machine rewriting is the obvious countermeasure, and the evidence on it splits by adversary. [Authorship Survives Imitation](/wiki/ai/pastiche/authorship-survives) reports dedicated attacks defeating a single neural verifier much of the time, while prompting alone did not defeat forensic methods. Rewriting can be used as one layer, and should not be relied on against an observer with a forensic panel.

A code formatter normalizes layout, and layout is only part of what the code stylometry features measure.

## Check

Compare the hours two personas keep. In a repository belonging to each:

```bash
TZ=UTC git log --date=format-local:%H --format=%ad | sort | uniq -c
```

This counts commits by hour of the day in UTC. Two histograms with the same quiet hours are consistent with one operator, and on a large sample that shape can be read by anyone who clones both repositories.

## Further reading

- Goga, Lei, Parthasarathi, Friedland, Sommer & Teixeira, [Exploiting Innocuous Activity for Correlating Users Across Sites](https://doi.org/10.1145/2488388.2488428), WWW 2013
- Narayanan et al., [On the Feasibility of Internet-Scale Author Identification](https://www.ieee-security.org/TC/SP2012/papers/4681a300.pdf), IEEE Symposium on Security and Privacy 2012
- Caliskan-Islam et al., [De-anonymizing Programmers via Code Stylometry](https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-caliskan-islam.pdf), USENIX Security 2015
- [RFC 6973: Privacy Considerations for Internet Protocols](https://www.rfc-editor.org/rfc/rfc6973), section 6.1.2 on pseudonymity

---
title: "Social Graph Linkage"
weight: 20
---

A social graph links two [operational personas](/wiki/security/operational-persona), managed identity sets meant to stay separate, when both are connected to the same people. The accounts a persona follows, the people it messages and the address books that hold its number form a pattern close to unique, and other people write much of that pattern.

In October 2019 Mitt Romney told a reporter from *The Atlantic* that he kept a secret Twitter account to watch the political conversation, and that it followed 668 people. *Slate*'s reporter reasoned that he would follow his family, chose his oldest grandchild's account because it had only 481 followers, and scrolled through them. The search turned up `@qaws9876`, display name Pierre Delecto. Its first follow was his son, and its list held relatives, former aides and the reporters who covered him. Asked that evening, Romney said "C'est moi." No address, key or network record was involved.

## Structure alone identifies

The shape of a graph carries identity without any names on it. Narayanan and Shmatikov showed in 2009 that "a third of the users who can be verified to have accounts on both Twitter" and Flickr could be re-identified in an anonymized Twitter graph with a 12% error rate, using "purely" the network topology. An observer who knows one persona's contacts has a pattern to look for in the other's.

First follows carry extra weight, as the Romney case shows. A new account starts with an empty list, and the operator fills it with whoever comes to mind first.

## Other people's phones

Much of the graph sits in records the persona never touches. Hagen and colleagues note that contact discovery "potentially reveals all contacts of users to the service provider", since matching an address book against a messenger's users requires the service to see it in some form. Venkatadri and colleagues found in 2019 that Facebook let advertisers target people through phone numbers and addresses "included in friends' uploaded contact databases", with the privacy settings on their test accounts at their most private.

A number kept out of every profile can therefore reach a platform through someone else's upload. Nothing in the persona's configuration can stop that, and a person who knows both identities can also just say so.

## What lowers it

Keep the circles apart from the first follow. A persona follows its subject matter and the people it meets as that persona, and leaves out family, colleagues and old friends. Its apps get no access to an address book, and it joins no group chat with the operator's other identities.

A private follow list hides the graph from strangers and leaves it with the platform, so it helps against the [cheaper observers](/wiki/security/operational-persona/isolation-failures) only.

## Check

Compare what two personas follow on a service that publishes the lists. On GitHub:

```bash
comm -12 \
  <(curl -s 'https://api.github.com/users/brinewick/following?per_page=100' | jq -r '.[].login' | sort) \
  <(curl -s 'https://api.github.com/users/inesvarga/following?per_page=100' | jq -r '.[].login' | sort)
```

This prints the logins on both lists, from the first 100 of each. A popular project's account on both lists means little, and a colleague's or a relative's means a lot. The two requests are themselves a row in GitHub's logs, so against an observer who can read those logs, fetch each list from its own persona's context.

## Further reading

- Ashley Feinberg, [This Sure Looks Like Mitt Romney's Secret Twitter Account (Update: It Is)](https://slate.com/news-and-politics/2019/10/mitt-romney-has-a-secret-twitter-account-and-it-sure-looks-like-its-this-one.html), *Slate* (2019)
- Narayanan & Shmatikov, [De-anonymizing Social Networks](https://arxiv.org/abs/0903.3276), IEEE Symposium on Security and Privacy 2009
- Hagen, Weinert, Sendner, Dmitrienko & Schneider, [All the Numbers are US: Large-scale Abuse of Contact Discovery in Mobile Messengers](https://encrypto.de/papers/HWSDS21.pdf), NDSS 2021
- Venkatadri, Lucherini, Sapiezynski & Mislove, [Investigating sources of PII used in Facebook's targeted advertising](https://mislove.org/publications/PII-PETS.pdf), PETS 2019

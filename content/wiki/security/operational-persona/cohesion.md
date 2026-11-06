---
title: "Persona Cohesion"
weight: 40
---

An [operational persona](/wiki/security/operational-persona), a managed set of accounts, credentials, recovery methods and technical context, keeps its cohesion in three ways: its parts vouch for one another where a service or a reader can check, one inventory inside the boundary lists every part and what it depends on, and the whole set is [exercised](/wiki/security/operational-persona/lifecycle#exercise) on a schedule shorter than anything in it takes to expire. Cohesion is the property those routines maintain: any two parts checked together agree, and any lost part can be rebuilt from the others.

Cohesion and isolation are one property with opposite signs. Pfitzmann and Hansen's privacy terminology says that re-using a partial identity "supports continuity in the specific context or role by enabling linkability with, e.g., former or future messages or actions". Inside the boundary that linkability is the goal: a reader can tell that this commit and that release came from one party, and reputation accumulates. Across the boundary the same evidence is the failure. A signature proves two commits share a signer whichever names are on them.

## Parts that vouch for each other

### Commit, key and account

To verify a signed commit, GitHub "checks that the committer or tagger email address matches an email address from the GPG key's identities and is a verified email address on the user's account". The address, the key and the account have to agree. When they do not, the API's `verification.reason` field names the pair that broke:

| Reason | What disagrees |
| --- | --- |
| `no_user` | No account claims the committer address |
| `unverified_email` | An account lists the address without having verified it |
| `bad_email` | The committer address is not among the signing key's identities |
| `unknown_key` | No account has registered the signing key |

### Profile and site

Mastodon checks a link in a profile by fetching the page and looking for a link back marked `rel="me"`, and shows a verification mark if it finds one. Keyoxide extends the pattern across services: its documentation describes "online identities or 'personas'" that "can be anonymous", each listing identity claims about its accounts, with a proof at each account pointing back. A reader can check that two accounts share an owner without contacting anyone.

### Domain and mailbox

A mailbox on a domain the persona owns keeps its address when the mail provider changes, so the accounts that depend on the address need no change. The cost is another item that can lapse, and [the domain is the worst one to lose](/wiki/security/operational-persona/lifecycle#what-expires).

All of these proofs are public and machine-readable. One pointed across a boundary, such as a `rel="me"` link from the pseudonym's site to a work profile, publishes the link in a form built to be verified.

## One inventory per persona

Drift starts when a new part is created: an account opened from the wrong browser window, an autofilled address, a recovery number typed from habit. A [bound context](/wiki/security/operational-persona/technical-context) prevents most of it, and the inventory catches the rest. It lists each item with its identifiers, login factors, recovery edges, what pays for it, when it renews and when it was last exercised.

A [`pass`](/wiki/security/pass) store fits, since each entry is a secret with free-form lines after it:

```text
<password>
url: https://github.com/login
login: brinewick
factor: security key, totp
recovery: printed codes (sheet 2), brinewick@brinewick.example
paid-by: none
renews: none
exercised: 2026-10-03
```

The store is encrypted to the persona's own key, selected with `PASSWORD_STORE_DIR`, and syncs to a remote under the persona's own account. [Entry names are not encrypted](/wiki/security/pass#security-notes-ordered-by-blast-radius), so a remote under another persona's account would list this persona's services in the clear.

The inventory stays inside the boundary. A master list across personas links all of them for anyone who reads it, and a reminder reading "renew brinewick.example" in a work calendar does the same on a smaller scale.

## Consistency with what services expect

Services run a similar check on context. Google describes it this way: "if we detect a suspicious sign-in attempt (say, from a new location or device), we'll ask for additional proof that it's really you". A persona that signs in from a different country each week looks like a stolen account, and the proof requested goes to a [recovery method](/wiki/security/operational-persona/recovery-graph) that may not exist. A stable browser profile and a stable [network route](/wiki/security/operational-persona/isolation-failures/network-address) keep the persona out of these challenges.

## Check

In a repository that should belong to one persona, list each committer address with the key that signed its commits:

```bash
git log --all --format='%ce %G? %GF' | sort | uniq -c
```

```text
      1 brinewick@brinewick.example G SHA256:JxJ8AOJogEQQugGCUgkc70ELFHJYZy36hRAjGOxeKMc
      2 brinewick@brinewick.example N
      1 ines@acme.example G SHA256:JxJ8AOJogEQQugGCUgkc70ELFHJYZy36hRAjGOxeKMc
```

`G` is a good signature and `N` means none. The last line links two personas: this persona's key signed a commit under the work address. Git reports `G` for it because it verifies the key and leaves the address uncompared, so read the address column. For SSH signatures Git needs `gpg.ssh.allowedSignersFile` set, and without it `%G?` prints `N` with an error even for signed commits.

To see what GitHub concluded about a commit, run this from the persona's directory so that `gh` uses the persona's login:

```bash
gh api repos/brinewick/project/commits/HEAD --jq '.commit.verification.reason'
```

A commit that passes prints `valid`.

## Further reading

- Pfitzmann & Hansen, [A terminology for talking about privacy by data minimization](https://dud.inf.tu-dresden.de/literatur/Anon_Terminology_v0.34.pdf), section 13
- GitHub Docs, [Using a verified email address in your GPG key](https://docs.github.com/en/authentication/troubleshooting-commit-signature-verification/using-a-verified-email-address-in-your-gpg-key) and the [commits API](https://docs.github.com/en/rest/commits/commits), for the `verification` object
- Mastodon, [Link verification](https://docs.joinmastodon.org/user/profile/)
- Keyoxide, [Identity claims and proofs](https://docs.keyoxide.org/wiki/identity-claims-proofs/)
- Google Security Blog, [How effective is basic account hygiene at preventing hijacking](https://security.googleblog.com/2019/05/new-research-how-effective-is-basic.html) (2019)

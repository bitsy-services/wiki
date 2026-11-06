---
title: "Persona Cohesion"
weight: 40
---

An [operational persona](/wiki/security/operational-persona), a set of accounts, credentials, recovery methods and technical context run as one identity, keeps its cohesion in four ways: its parts vouch for one another where a service or a reader can check, new parts are created from a context bound to the persona, one inventory inside its boundary lists every part and what it depends on, and the whole set is exercised on a schedule shorter than anything in it takes to expire. Cohesion is the property those routines maintain: any two parts checked together agree, and any lost part can be rebuilt from the others.

Cohesion asks for linkability inside the boundary. Pfitzmann and Hansen's privacy terminology says that re-using a partial identity "supports continuity in the specific context or role by enabling linkability with, e.g., former or future messages or actions". A reader can tell that this commit and that release came from one party, and reputation accumulates. Where a persona also needs unlinkability, so that no observer can tell it shares an operator with another persona, the same evidence across the boundary is the failure: a signature shows two commits share a signer whichever names are on them.

The examples use `brinewick`, the pseudonym of a developer called Ines, whose work address is `ines@acme.example`.

## Parts that vouch for each other

### Commit, key and account

`brinewick` signs commits with an SSH key, and GitHub checks each signature against a public key on the account. For a GPG signature it also "checks that the committer or tagger email address matches an email address from the GPG key's identities and is a verified email address on the user's account". When the parts disagree, the API's `verification.reason` field names what broke:

| Reason | What disagrees |
| --- | --- |
| `no_user` | No account claims the committer address |
| `unverified_email` | An account lists the address without having verified it |
| `bad_email` | The committer address is not among the GPG key's identities |
| `unknown_key` | No account has registered the signing key |

### Profile and site

Mastodon checks a link in a profile by fetching the page and looking for a link back marked `rel="me"`, and shows a verification mark if it finds one. Keyoxide extends the pattern across services: its documentation describes "online identities or 'personas'" that "can be anonymous", each listing identity claims about its accounts, with a proof at each account pointing back. A reader can check that two accounts share an owner without contacting anyone.

These proofs are public and machine-readable. One pointed across a boundary, such as a `rel="me"` link from the pseudonym's site to a work profile, publishes the link in a form built to be verified.

## New parts start inside

Drift starts when a new part is created: an account opened from the wrong browser window, an autofilled address, a recovery number typed from habit. A [context bound to the persona](/wiki/security/operational-persona/technical-context), where the directory and browser profile select the identity, prevents most of it. It has to exist before the first login. A first login writes to the service's logs and a first commit is a permanent record, and [separation is cheap early and nearly impossible late](/wiki/security/identity-separation#cheap-early-nearly-impossible-late).

## One inventory per persona

The inventory catches what the context misses. It lists each item with its identifiers, login factors, recovery edges, what pays for it, when it renews and when it was last exercised. A [`pass`](/wiki/security/pass) store fits, since each entry is a secret with free-form lines after it:

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

The store is encrypted to the persona's own key and selected with `PASSWORD_STORE_DIR`, and it syncs to a remote under the persona's own account. [Entry names are not encrypted](/wiki/security/pass#security-notes-ordered-by-blast-radius), so a remote under another persona's account would list this persona's services in the clear.

The inventory stays inside the boundary. A master list across personas links all of them for anyone who reads it, and a reminder reading "renew brinewick.example" in a work calendar does the same on a smaller scale. Where two inventories have to be compared, compare them without saving the result.

## Exercise

Parts that go unused stop working: domains lapse, free mailboxes get deleted, phone numbers get reissued. [Persona upkeep](/wiki/security/operational-persona/upkeep) has the clocks and the schedule.

## Check

In a repository that should belong to one persona, list each address with the key that signed its commits:

```bash
git log --all --format='%ae %ce %G? %GK' | sort | uniq -c
```

```text
      1 brinewick@brinewick.example brinewick@brinewick.example G SHA256:0O19Q+UkZpHz1a0Z3muebjbf0Q/P0K2nUBkue6lN8IQ
      1 brinewick@brinewick.example brinewick@brinewick.example N
      1 brinewick@brinewick.example brinewick@brinewick.example U SHA256:dFDYI6gPj5AGOsVz1m2LNZvm2xaNkEQoX+NOmlLw8f8
      1 ines@acme.example brinewick@brinewick.example G SHA256:0O19Q+UkZpHz1a0Z3muebjbf0Q/P0K2nUBkue6lN8IQ
      1 ines@acme.example ines@acme.example G SHA256:0O19Q+UkZpHz1a0Z3muebjbf0Q/P0K2nUBkue6lN8IQ
```

The columns are author address, committer address, signature status and signing key. `G` is a good signature from a known key, `N` no signature, `U` a good signature from a key Git has not been told to trust, and `E` a signature Git cannot check because it lacks the key. A repository that belongs to one persona prints one address and one key.

The third line above shows another key signing under this persona's address, and the last two put the work address on its commits. Git reports `G` on those two because it verifies the key and does not compare addresses, so read the address columns. For SSH signatures Git needs `gpg.ssh.allowedSignersFile` set: without it, every signed commit shows `N` with an error.

To see what GitHub concluded about a commit, run this from the persona's directory so that `gh` uses the persona's login:

```bash
gh api repos/brinewick/project/commits/HEAD --jq '.commit.verification.reason'
```

A commit that passes prints `valid`.

## Further reading

- Pfitzmann & Hansen, [A terminology for talking about privacy by data minimization](https://dud.inf.tu-dresden.de/literatur/Anon_Terminology_v0.34.pdf), section 13
- GitHub Docs, [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification), [Using a verified email address in your GPG key](https://docs.github.com/en/authentication/troubleshooting-commit-signature-verification/using-a-verified-email-address-in-your-gpg-key) and the [commits API](https://docs.github.com/en/rest/commits/commits), for the `verification` object
- Mastodon, [Link verification](https://docs.joinmastodon.org/user/profile/)
- Keyoxide, [Identity claims and proofs](https://docs.keyoxide.org/wiki/identity-claims-proofs/)

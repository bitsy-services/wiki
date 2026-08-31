---
title: "SIM Swap"
weight: 85
---

A SIM swap moves a phone number off the subscriber's device and onto one the attacker controls, using the carrier's own provisioning tools. Nothing is broken into. The number is a routing entry in a subscriber database, a customer-service representative can rewrite that entry in a few minutes, and every account that treats the number as proof of identity follows it to the new handset.

The phone number became an identity credential without anyone designing it as one: a routing address that picked up a second job delivering one-time codes, and ended up as the recovery path of last resort for email, banking, and exchange accounts. The party holding write access to that credential is a call-centre or retail employee at a company whose relationship with the account holder is a monthly bill. No keys are stolen and no chain is touched: the swap belongs to the [social-engineering group](/wiki/economics/finance/fraud) rather than to the contract attacks.

## How a number changes hands

Two ordinary customer-service operations do it. A **port-out** moves the number to a different carrier; US number-portability rules oblige the losing carrier to release it on a valid request from the gaining one, and the process is deliberately fast because it is how carriers take each other's customers. A **SIM replacement** keeps the number where it is and binds it to a new physical SIM or eSIM profile, the operation a store performs when a customer loses a phone. Both end with the victim's device dropping to no service, frequently the only warning they get, and often at 2am. Attackers reach them by three routes.

**Social engineering of the support agent.** Verification scripts ask for billing address, date of birth, last four digits of a card, recent call detail — facts that breach dumps and data brokers have made cheap, and that the account holder cannot rotate.

**An insider.** Multiple US prosecutions have involved carrier employees paid per swap. This route defeats every customer-side control: a port freeze, an account PIN, and a note on the file are all rows in the database the insider is authorized to edit.

**Credential compromise upstream.** A carrier web account, a dealer provisioning tool, or a third-party porting portal. One set of stolen employee credentials serves many swaps, and the customer's own hygiene never enters into it.

## The chain the attacker is after

The phone is not the target. The number is the first link in a reset chain that ends at a withdrawal, and every hop is a documented recovery feature working as specified.

```text
  carrier account
    -> the phone number
       -> SMS reset of the email account password
          -> email reset of the exchange account password
             -> withdrawal to an attacker address
```

The controls that break it are the dull ones: a mandatory delay on withdrawals after a password or address change, and a withdrawal allowlist that takes a day or two to admit a new address. Both turn a five-minute theft into a window in which the victim notices the dead handset. Alerts do not, because they arrive in the mailbox the attacker now reads.

Where the victim held their own keys, a swap gets nothing — no reset path to a seed phrase, no custodian to instruct. That is a plain argument for self-custody, and the mirror of the one in [exchange collapse](/wiki/economics/finance/fraud/exchange-collapse): a balance at a custodian carries the custodian's solvency risk and its recovery flow both.

## Why SMS is a weak second factor

An SMS code authenticates a routing assignment rather than a person, and a third party can reassign it. The secret is held neither by the user nor by the relying party, and travels over infrastructure neither controls. A time-based one-time password (TOTP) app puts the shared secret on the device at enrolment, where no carrier can move it. A [hardware security key](/wiki/security/yubikey#webauthn-and-fido2) adds origin binding: the private key never leaves the device, and the browser ties each assertion to the site that requested it, so a phishing page relaying credentials in real time collects a signature that is invalid for the site it is attacking. A code — from SMS or an authenticator — read aloud to a convincing caller works exactly as well for the caller as for the user.

Signaling System No. 7 (SS7), the interconnect protocol carriers use to route calls and messages between networks, is a rarer route that never touches the subscriber account: an entity with signalling access can have messages for a number delivered elsewhere, a technique demonstrated against bank accounts in Germany and the UK. It leaves the victim's handset working normally, removing even the dead-phone warning.

## Cases

**Michael Terpin, 2018.** The crypto investor lost roughly $24 million after a January 2018 swap and sued AT&T for $224 million, alleging its employees enabled the transfer; the litigation has produced no broad rule of carrier liability and is not over — the Ninth Circuit revived his Federal Communications Act claim in September 2024 and the case has been moving toward trial since. Terpin separately won a $75.8 million default judgment in 2019 against Nicholas Truglia, who later pleaded guilty in federal court to wire fraud, was sentenced in 2022, and was ordered to pay about $20 million in restitution; he was resentenced to 12 years in July 2025 after failing to pay it.

**Joel Ortiz, 2019.** Ortiz pleaded guilty in California and was sentenced to ten years, in what was reported as the first US conviction for SIM swapping. Prosecutors accused him of taking roughly $5 million from about 40 victims.

**"The Community", 2019–2020.** The Department of Justice (DOJ) charged nine defendants in the Eastern District of Michigan — six members of a group calling itself The Community, and three former mobile-carrier employees — with wire fraud and aggravated identity theft over swaps alleged to have taken more than $2.4 million; guilty pleas and convictions followed. The swaps were bought, not talked into existence.

**The SEC's X account, January 2024.** The Securities and Exchange Commission (SEC) lost control of its own account on X, which posted a false announcement that spot bitcoin exchange-traded products had been approved. The Commission later said an unauthorized party had obtained the phone number associated with the account through a third party, and that multi-factor authentication had been disabled on the account since July 2023 after staff reported access problems. A defendant was charged in October 2024 and pleaded guilty in 2025.

## Defence, in order of effect

1. **Remove the phone number as a recovery method** on email, exchange, and banking accounts. Check the account-recovery screen, not the login screen: a number deleted from the second is often still live on the first.
2. **Use hardware security keys** where the account supports them, enrolling two so a lost key is not a lockout; an authenticator app where they are unsupported.
3. **Turn on exchange withdrawal allowlists and time locks.** These are the only controls on this list that still work after the swap has succeeded and the attacker is already reading the mailbox, which is what converts a successful swap into a failed theft.
4. **Set a carrier port freeze or number lock and an account PIN**, then confirm both are set rather than merely offered. They raise the bar against a scripted support call and against a port initiated at another carrier. They do not stop an agent who overrides the flag, they do not reach an insider or a compromised provisioning tool, and a port-out lock may not cover an in-place SIM or eSIM replacement.
5. **Give financial accounts their own email address** — never published, never reused, itself behind a hardware key.
6. **Hold long-term balances in self-custody.** An exchange account is a recovery surface; a hardware wallet is not.

## Where the law lands

Swaps are charged federally as wire fraud and aggravated identity theft, the second carrying a mandatory consecutive term; charging the bribed employee alongside the crew is the only lever that reaches the insider route. In November 2023 the Federal Communications Commission adopted rules requiring wireless providers to authenticate customers securely before moving a number to a new device or carrier and to notify them immediately of such a request. Carriers' civil liability to defrauded subscribers remains largely untested. Recovery runs through the receiving exchange, whose [know your customer](/wiki/economics/finance/regulation/know-your-customer) file is the only identity record in the chain and names the victim, because the attacker signed in as them — past that point the trail is public and the endpoints are not, as with a [wallet drainer](/wiki/economics/finance/fraud/wallet-drainer).

## External links

- [FCC: cell phone fraud](https://www.fcc.gov/cell-phone-fraud) — the regulator's account of SIM swap and port-out fraud, and the 2023 rules
- [Digital Identity Guidelines 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html) — the US standards body's authenticator guidance, which classes out-of-band SMS as restricted
- [Department of Justice press releases](https://www.justice.gov/news) — searchable source for SIM-swapping indictments, including the carrier-employee cases
- [FBI Internet Crime Complaint Center annual reports](https://www.ic3.gov/AnnualReport/Reports) — where reported US losses by crime type are published
- [Krebs on Security: SIM swapping](https://krebsonsecurity.com/tag/sim-swapping/) — case-by-case reporting on the crews and the carrier insiders

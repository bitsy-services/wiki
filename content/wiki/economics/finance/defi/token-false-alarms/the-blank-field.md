---
title: "The Blank Field"
weight: 20
---

The loudest false alarm is a red banner. The most common one is an empty response. GoPlus's booleans are tri-state — `"1"` true, `"0"` false, absent means the question was not answered — and the vendor says so in three separate places, including "No return doesn't mean it is risky" on `trust_list`. Downstream, absence gets rendered as a grey shield, a "no data" badge, or a zero, and the party that turned the blank into a verdict is the integrator rather than the API.

Twenty-one of the forty-five fields in the response schema carry the sentence "No return means unknown". Five deliberately do not, and they are exactly the reputation group: `is_open_source` and `is_in_dex` are plain true-or-false, `is_true_token` and `is_airdrop_scam` say "None means no result", and `trust_list` says `"1"` means true and "No return no result". The asymmetry is stated in the schema itself. Only `"0"` on `is_true_token` means fake; only `"1"` on `is_airdrop_scam` means scam; `is_honeypot`'s notice ends "High risk, definitely scam". The API is dispositive when accusing and silent when clearing.

## Four ways a field goes blank

**Closed source.** "When the contract is closed-source, other risk items will return null." This one is defensible — nothing can be read — and it is the reason source verification is the first item on every remediation list.

**Proxy.** "When the contract is a Proxy, we will stop detecting other risk items." Covered in detail under [capability flags](/wiki/economics/finance/defi/token-false-alarms/capability-flags#upgradeability-silences-the-scanner): USDC, stETH, AAVE and PAXG all return zero permission fields, so the upgradeable tokens report cleaner than the immutable one.

**No recognised trading pair.** `is_in_dex` is "only true if the token has a marketing pair with mainstream coins/tokens" — the typo is the vendor's — and *mainstream* is a published list, not an inference. When it reads `0`, seven things go at once: `buy_tax`, `sell_tax`, `transfer_tax`, `cannot_sell_all`, `lp_holders`, `lp_holder_count` and `lp_total_supply`. They do not go the same way, either: `dex` becomes an empty array while the tax and liquidity fields are omitted outright. A token with deep liquidity paired against an asset outside the list reads as a token with no liquidity at all. Which asset you pair against is therefore a design-time decision with a scanner consequence, and it is not documented as one.

**Nothing.** AMPL returns `is_open_source: "1"`, `is_proxy: "0"`, `is_in_dex: "1"` — neither documented suppressor applies — and still comes back with twenty keys, no permission field of any kind, and `buy_tax` as an empty string. The canonical rebasing token, whose `rebase` function is precisely the balance-modifying pattern `owner_change_balance` exists to catch, produces a report with no security signal in either direction and no explanation.

AMPL's silence and stETH's silence are indistinguishable in the response and mean different things, so a missing risk field carries no information at all — and the common integrator habit of coercing absent to false is reading a verdict the API never issued.

## The owner field has four shapes

`owner_address` is documented with two blanks and a typo — "No value will be returned if the owner address is unknown. An empty sting will be returned if the contract has no owner" — which produces four distinct live shapes:

| Shape | Example | What it means |
| --- | --- | --- |
| A real address | USDT | there is an owner |
| The zero address | PEPE, 1INCH | renounced |
| Key absent, not a proxy | COMP, CRV | unknown |
| Key absent, proxy | USDC, AAVE, stETH | suppressed |

CRV returns no `owner_address` while still returning `is_mintable: "1"`, so a reader has a live mint function and no way to learn who can call it. Nothing distinguishes the third row from the fourth without also reading `is_proxy`, and neither can be read as "renounced".

## Silence at the transport layer

The failure modes below are not about tokens at all. They are about a client library turning a delivery problem into a risk verdict.

**Throttling returns HTTP 200.** The body is `{"code":4029,"message":"too many requests"}` served with a 200 status, no `Retry-After`, and no rate-limit headers of any kind. It also has no `result` key, so client code doing `resp.result[addr]` throws rather than degrading to "no data".

**An unknown token also returns 200.** `{"code":1,"message":"OK","result":{}}` — a successful call with nothing in it. An unlisted token, a scanner outage and a chain the vendor does not cover are indistinguishable at the status line.

**The result is keyed by the lowercased address.** Send a [checksummed](/wiki/economics/finance/defi/ethereum/eip) address and the key comes back lowercase, so a lookup by the string you sent returns `undefined` — which naive code cannot tell from "no data".

**Batches are silently truncated.** Three comma-separated addresses on the free tier returned `code 1 OK` with only the first one in the result. Two more come back missing, and missing reads as clean.

So the first rule for anyone consuming these APIs is to branch on the body's `code` rather than the HTTP status, and the second is to treat an absent field as absent rather than as false.

```python
# Correct consumption of a GoPlus token-security response.
import requests

def risk_fields(chain_id: int, address: str) -> dict | None:
    r = requests.get(
        f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}",
        params={"contract_addresses": address},
        timeout=30,
    )
    body = r.json()                       # HTTP 200 even when throttled
    if body.get("code") != 1:             # 4029 = too many requests, no `result` key
        return None                       # unknown, NOT clean
    result = body.get("result") or {}
    entry = result.get(address.lower())   # keys are lowercased, never checksummed
    if not entry:
        return None                       # unknown token, NOT clean
    return entry

def is_mintable(entry: dict) -> bool | None:
    v = entry.get("is_mintable")
    return None if v is None else v == "1"   # tri-state: never coerce absent to False
```

The rate limit that governs all of this is published three times and disagrees with itself: the support page says thirty calls a minute, one product page says 150 credits a minute and 30,000 a day, another says a hundred call credits a minute. Measured behaviour matches none of them, and is not stable between runs: an unauthenticated burst throttled after nine calls on 2026-08-31 and after ten on 2026-09-01, while a third run of fourteen calls in the same span was not throttled at all. It behaves like a short-window burst bucket whose window nothing documents. The page carrying the rate limit is also the one the vendor's own documentation index omits, and it is nearly a year staler than the pages around it.

Two further constraints shape what an integrator can do about any of this. GoPlus's licence agreement requires displaying "the GoPlus logo with 'Powered by GoPlus' expression" and states "We do not suggest any modification to our API results", which is why a single vendor's flag propagates verbatim and branded across wallets and screeners that the deployer cannot contact. And the response *shape* is authentication-dependent — one documented field is returned only to callers with a console key — so every observation on this page is a claim about the anonymous free tier rather than about the product.

## Coverage is a boundary, not a verdict

The vendors are explicit about where they stop, and the stopping points are much narrower than their user interfaces suggest.

| Tool | Accepts | Scores | Simulates a trade |
| --- | --- | --- | --- |
| GoPlus | 43 chains live | same | where a recognised pair exists |
| TokenSniffer | 15 chains | 10 | 4 |
| honeypot.is | 3 chains | same | Uniswap V2 and V3-style pools only |
| MetaMask alerts | 21 networks | — | — |
| MetaMask token detection | 10 networks | — | — |

TokenSniffer's split is the one most likely to mislead: on the six scored chains where it cannot simulate, `testForUnableToSell`, `testForHighBuyFee` and `testForHighSellFee` still produce results, with no live sell behind them. A valid chain and a valid address returning no score is not an error condition, and nothing in the response says which tier you landed in.

honeypot.is supports Ethereum, BNB Smart Chain and Base, and only Uniswap V2 and V3-style pools — it names Uniswap V2, Sushiswap, Pancakeswap, Bakeryswap and BiSwap. A token whose liquidity sits in a Curve pool, a Balancer pool, or a Uniswap V4 singleton is unsimulatable, and unsimulatable returns unknown. That is not hypothetical: of the ten ordinary tokens scanned for the [overview](/wiki/economics/finance/defi/token-false-alarms#the-measurement), eight got no answer from honeypot.is — six because their liquidity is in V4 pools the API does not index, one because Arbitrum is unsupported, and one because it was asked about the wrong chain.

Lock detection has the same shape, and the same per-chain unevenness: it is an allowlist of named locker addresses rather than an inference, so the identical locking design registers on Ethereum and does not on most L2s — [liquidity and holders](/wiki/economics/finance/defi/token-false-alarms/liquidity-and-holders#a-lock-is-a-name-on-a-list) has the coverage table.

Uniswap concedes its gap in writing, and disclaims more than coverage while doing it: "Data may not be available for selected tokens, particularly newer or less popular tokens, and no tokens are reviewed for their quality, merits, or soundness as investments."

## There is a field for the missing context, and it is empty

GoPlus documents a free-text `note` field for exactly what its schema cannot hold, with the example `"note": "Contract owner is a multisign contract."` Across ten blue chips queried on 2026-08-31 — including the Ethereum Name Service (ENS) token behind a 48-hour timelock, UNI behind the Uniswap governance timelock, and LDO behind the Lido Aragon Agent — the key was absent every time, as was the sibling `other_potential_risks`. Absent, not empty: the field was never populated at all. The affordance for saying "this owner is a governance contract" exists and goes unused on the canonical governance-owned tokens.

## External links

- [GoPlus response details](https://docs.gopluslabs.io/reference/response-details) — the tri-state semantics and every suppression notice
- [GoPlus supported mainstream tokens](https://docs.gopluslabs.io/reference/supported-main-token) — the list that decides `is_in_dex`
- [GoPlus supported lockers](https://docs.gopluslabs.io/reference/supported-locker) — the per-chain locker allowlist
- [honeypot.is documentation](https://docs.honeypot.is/) — chain and pool-type coverage, stated plainly
- [TokenSniffer API reference](https://tokensniffer.readme.io/) — which chains are scored and which are simulated

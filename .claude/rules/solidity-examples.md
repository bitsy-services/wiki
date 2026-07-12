---
description: Rules for Solidity code examples in wiki pages
paths:
  - "content/wiki/defi/**/*.md"
---

# Solidity Code Examples

- Use OpenZeppelin's `SafeERC20` (`using SafeERC20 for IERC20`) instead of raw `approve` / `transfer` / `transferFrom`. Raw calls break on non-compliant tokens like USDT.
- Never set `amountOutMinimum: 0` in production-facing examples without a prominent warning. Always show how to derive it from a quote.
- Use `block.timestamp` for deadlines only in atomic contract-to-contract calls. For user-submitted transactions, accept the deadline as a function parameter.
- When showing Uniswap swap examples, note the existence of SwapRouter02 and UniversalRouter as modern alternatives.
- Include imports in every code block — don't leave readers guessing where interfaces come from.

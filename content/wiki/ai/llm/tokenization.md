---
title: "Tokenization"
weight: 100
---

A model never sees text. It sees a list of integers, and the tokenizer is the only component that ever touched a character. GPT-2's is byte-pair encoding: start from raw bytes, repeatedly merge the most frequent adjacent pair, keep the merge table. Encoding replays those merges in the order they were learned — not longest-match, which is the usual misreading. The vocabulary is what they produced: 50,000 merges plus the 256 raw bytes and an end-of-text marker, so 50,257 entries.

```text
"The cat sat"  →  ["The", " cat", " sat"]  →  [464, 3797, 3332]
```

Two consequences people trip on.

**The space lives inside the token.** Leading whitespace belongs to the token that follows it, so `" cat"` and `"cat"` are different ids with unrelated rows in the [embedding](/wiki/ai/llm/embeddings) table. Word-initial and mid-word forms of a word are, to the network, two different words that happen to correlate.

**Structure below the token is invisible.** The model gets an id, not the letters inside it. Spelling, rhyme, and character counting have to be reconstructed statistically rather than read off — hence the recurring embarrassments. Digits too: BPE chops a number into whichever chunks the merge table happened to produce, and place value isn't one of its concerns.

Tokens are the unit of everything downstream, too. The context limit, the bill, and the O(n²) attention cost are counted in them — so [context engineering](/wiki/ai/context-engineering) is downstream of a merge table built once, years ago, from a corpus.

## Check yourself

Encode `" cat"` and `"cat"` with tiktoken's `gpt2` encoding: 3797 and 9246, neither derivable from the other. Then encode `"1234567"`. It comes apart as `123|45|67` — chunks that respect nothing about place value.

## Depends on / leads to

Depends on [conventions](/wiki/ai/llm/conventions). Leads to [embeddings](/wiki/ai/llm/embeddings), where the integer becomes a row.

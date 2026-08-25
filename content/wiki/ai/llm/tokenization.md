---
title: "Tokenization"
weight: 100
---

A model never sees text. It sees a list of integers, and tokenization is the step that produces them: the incoming string is chopped into pieces drawn from a fixed inventory, and each piece is swapped for the number that identifies it. The tokenizer is the only component in the entire system that ever touches a character — everything after it does arithmetic on integers and has no way of knowing that writing was involved. Which pieces the inventory contains was settled once, before training, by an algorithm counting what happened to be common in a corpus. The model has been living with that decision ever since.

## Why not just use letters, or words?

The job sounds like it should have an obvious answer. It has two, and they fail in opposite directions.

**One token per character** gives an inventory small enough to write on a napkin, and it can spell anything at all. The cost is length. A page of English becomes thousands of positions instead of hundreds, and [attention](/wiki/ai/llm/attention) compares every position against every other, so the work grows with the *square* of that number. You would also be spending the model's first several blocks teaching it that `t`, `h`, `e` in that order is a word — something you already knew and could have handed it for free.

**One token per word** fixes the length and breaks everything else. There is no finite list of English words, let alone English plus code plus German plus every proper noun, product name, and typo. Whatever list you fix in advance will eventually meet something not on it, and then it has nothing to say. The usual patch was a single "unknown" token, which amounts to deleting the word and hoping.

What's wanted is a fixed-size inventory that can nevertheless spell anything — common things cheaply, rare things at some expense, but nothing unrepresentable.

## The compromise: merge whatever turns out to be common

[GPT-2](/wiki/ai/llm/gpt-2) uses **byte-pair encoding**, and its trick is to stop guessing what the pieces ought to be and let a corpus decide.

Start from raw bytes. There are 256 of them, every possible input is made of them, and so the inventory can already spell anything before a single decision has been made. That is the escape hatch that makes the rest safe, and it never goes away. Then count every adjacent pair of tokens across a large body of text, take the pair that occurs most often, glue it into one new token, and add it to the inventory. Count again. Repeat.

Early merges produce fragments like `th` and `in`. Later ones, built on top of the earlier, produce ` the` and ` because`. The table records not just what was merged but the order it was merged in, and that order is the rulebook.

Think of a printer setting type. You begin with individual letters, notice you keep reaching for the same combinations, and cast a single slug for `the` to save yourself the trouble. Words you set constantly earn their own slug; words you set once get spelled out letter by letter. Either way the page gets printed — the only question is how many pieces of type it took.

GPT-2 stopped after 50,000 merges. Those, plus the 256 raw bytes, plus one marker meaning *end of text*, are the [vocabulary](/wiki/ai/llm/glossary): 50,257 entries. That number is welded in — it sets the width of [the model's output layer](/wiki/ai/llm/unembedding-and-logits) and will for as long as the weights exist.

## Encoding replays the merges, in order

Tokenizing new text is *not* a search for the longest matching entry. That is the usual misreading, and it gives different answers. Encoding replays the merge table: apply merge 1 wherever it fits, then merge 2, and so on down the list. Whatever pieces survive that replay are your tokens.

```text
"The cat sat"  →  ["The", " cat", " sat"]  →  [464, 3797, 3332]
```

Common words come out whole. Rare ones come apart into whatever fragments the replay happens to leave, which is why an unusual surname can cost four tokens where a common one costs one.

## Three consequences people trip on

**The space lives inside the token.** Leading whitespace belongs to the token that follows it, so `" cat"` and `"cat"` are different ids with unrelated rows in the [embedding](/wiki/ai/llm/embeddings) table. The word-initial and mid-word forms of a word are, to the network, two different words that happen to correlate — and it has to learn that correlation from data like any other.

**Structure below the token is invisible.** The model receives an id, not the letters inside it. Spelling, rhyme, and counting characters have to be reconstructed statistically from context rather than read off directly, which is where the recurring embarrassments come from. Digits are the same story: byte-pair encoding chops a number into whichever chunks the merge table happened to produce, and place value was never one of its concerns.

**Some languages cost several times more than others.** The merges were counted over a corpus that was overwhelmingly English, so English is what got the most slugs cast for it. Text in a thinly represented language falls back toward per-byte spelling — more tokens for the same meaning, which means a smaller effective [context window](/wiki/ai/llm/context-length) and a larger bill to say the same thing. That inequity is baked in at the tokenizer, and no amount of training afterwards removes it.

## Why everything downstream is counted in tokens

The token is the unit of account for the whole system. The context limit is a token count. The bill is a token count. The O(n²) attention cost is quadratic in a token count. Even [perplexity](/wiki/ai/llm/perplexity), the standard measure of how well a model fits a body of text, is an average over tokens — which is why the same model scores differently on the same passage depending only on how it was cut up.

So the merge table isn't a preprocessing detail to be waved past. It is a set of decisions made once, years ago, from whatever text was at hand, and [context engineering](/wiki/ai/context-engineering) is the discipline of working downstream of them.

## Check yourself

Encode `" cat"` and `"cat"` with [tiktoken](/wiki/ai/llm/running-the-checks)'s `gpt2` encoding: 3797 and 9246, neither derivable from the other. Then encode `"1234567"`. It comes apart as `123|45|67` — chunks that respect nothing about place value.

Now test the cost claim, which makes a sharp prediction: for a script GPT-2 learned no merges for, the token count should track the text's **UTF-8 byte length**, not its character count — because the encoder never got past the raw bytes it started from. Take a string of Japanese or Devanagari and compare `len(enc.encode(s))` against `len(s)` and `len(s.encode("utf-8"))`. It lands near the byte count, roughly three tokens per character. English runs the other way, averaging about four characters *per* token. That order-of-magnitude gap is the tax, and it is charged on every request.

## Depends on / leads to

Depends on [conventions](/wiki/ai/llm/conventions). Leads to [embeddings](/wiki/ai/llm/embeddings), where the integer becomes a row.

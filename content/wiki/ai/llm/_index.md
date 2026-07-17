---
title: "Large Language Models"
weight: 80
bookCollapseSection: true
---

A large language model is a program that, given some text, guesses what comes next. That is the entire job. It learns to do it by being shown an enormous quantity of writing with the next piece hidden, guessing, and being corrected — over and over, until the guesses are good. Everything a model appears to do beyond that — answer a question, write a function, hold a conversation, follow an instruction — is that same guess run in a loop, with each guess added to the text and fed back in as the basis for the next one.

The interesting part is that this turns out to be enough. Nobody sat down and taught these models grammar, or geography, or how to close a bracket. Predicting text well enough, at a large enough scale, appears to require learning such things, so they get learned along the way. Competence is a side effect of the guessing game.

This section is about how that works. The rest of the [AI section](/wiki/ai) is about *using* a model; these pages are about what the thing is — what your text becomes when it goes in, what the model does to it, how a guess falls out the far end, how it was trained to guess well, and what all of it costs to run. Nearly every model in current use is built on one design, called the **transformer**, and that design is what these pages take apart. [GPT-2 small](/wiki/ai/llm/gpt-2) is the worked example throughout: old, small enough to poke at on a laptop, and structurally the same animal as the models people pay for.

Each page teaches the one thing it names, and ends with a claim you can confirm or break yourself in GPT-2 small or nanoGPT, a deliberately minimal and readable implementation of one. Reading about a transformer isn't the same as watching perplexity — roughly, how many tokens the model is choosing between at each step — climb when you delete a piece of one.

## What happens when you send a prompt

Your text is chopped into [tokens](/wiki/ai/llm/tokenization) — chunks roughly the size of a short word. Each token is looked up in a large table, which turns it into [a list of numbers standing for that token](/wiki/ai/llm/embeddings). Because a lookup can't know where in the sentence the token sat, its position has to be [added in on purpose](/wiki/ai/llm/positional-encoding).

Those numbers then pass through a stack of identically structured [blocks](/wiki/ai/llm/glossary) — the arrangement the word *transformer* refers to. Each block does two things. [Attention](/wiki/ai/llm/attention) lets every token look back at the tokens before it and pull in whatever is relevant; this is the only place in the whole model where tokens see each other at all. [The MLP](/wiki/ai/llm/the-mlp) — a multi-layer perceptron, the plainest sort of neural network there is — then works over each position on its own, and is where most of what the model knows is stored. Neither one replaces what came before: both *add* their results into a running total called [the residual stream](/wiki/ai/llm/residual-stream), which is the only thing carried forward.

At the far end, the numbers for the last token are turned back into [one score for every token in the vocabulary](/wiki/ai/llm/unembedding-and-logits), and [softmax](/wiki/ai/llm/softmax-and-temperature) turns those scores into probabilities. [Something then picks one](/wiki/ai/llm/sampling-strategies) — and the choice of *how* to pick is why the same prompt can give you different answers. The picked token is added to your text, and the whole thing runs again for the token after that.

That loop is the model. Everything else in this section is either a detail of one step in it, an account of how the model's **weights** — the numbers all that arithmetic is done with, also called its *parameters*, and the only part training changes — got their values, or a trick for making the loop cheaper.

## How it learned to guess

The weights start as noise, and training is the process of beating them into shape. [The loss function](/wiki/ai/llm/the-loss-function) scores each guess against the token that actually came next, and [backprop](/wiki/ai/llm/backprop-one-weight) works out, for every weight in the model, which direction to nudge it to have made the right answer likelier. Repeat across trillions of tokens and the result is a *base* model: an extremely good text predictor, and not yet something you'd want to talk to. That trillions of tokens is affordable at all — nobody labelling any of them, no position waiting on any other — is [the fact the whole field is built on](/wiki/ai/llm/why-scale-worked).

Turning that into an assistant is a separate step. [Fine-tuning](/wiki/ai/llm/fine-tuning) continues training on narrower data, and [RLHF](/wiki/ai/llm/rlhf) tunes the model against human judgements of which answer is better — which is what teaches it to answer a question rather than continue it, or to write a second paragraph rather than a plausible next Stack Overflow comment.

## Why it costs what it costs

Two separate things drive the bill, and it's worth keeping them apart, because each has its own countermeasures.

The first is the length of the conversation. Attention makes every token look at every earlier token, so that work grows with the *square* of the [context length](/wiki/ai/llm/context-length) — double the context and you quadruple it. [The KV cache](/wiki/ai/llm/kv-cache) is the standard answer: it keeps what each token already worked out, so the model doesn't rebuild the entire prefix every time it emits one more word. The cost is memory that grows as the conversation does.

The second has nothing to do with length: producing even a single token means working through the model's weights, so a bigger model costs more per token no matter how short the prompt. [Mixture of experts](/wiki/ai/llm/mixture-of-experts) routes each token through only a fraction of the model, buying a large parameter count without paying for all of it on every token. [Speculative decoding](/wiki/ai/llm/speculative-decoding) comes at the same cost from the other side: a small model drafts several tokens, and the large model checks them all in a single pass it would otherwise have spent on one.

[Training and inference](/wiki/ai/llm/training-vs-inference-parallelism) sit differently against both, which is why serving a model is a distinct engineering problem from training one.

## Reading order

Start with [Conventions](/wiki/ai/llm/conventions) — it's short, and every diagram after it assumes you've read it. Keep the [Glossary](/wiki/ai/llm/glossary) open. [GPT-2](/wiki/ai/llm/gpt-2) comes next: it's the model the rest of the pages measure everything against, and it explains what the numbers you're about to keep seeing — 768, 12 blocks, 50,257 — actually belong to. Then start at [tokenization](/wiki/ai/llm/tokenization) and follow each page's "leads to" links: they run in dependency order, from a string of text to a sampled token and out into training and inference tricks, ending on [why any of it worked](/wiki/ai/llm/why-scale-worked) — the argument the rest is evidence for. The sidebar lists them in that same order.

Two pages elsewhere in the wiki are this material seen from the outside: [prompt caching](/wiki/ai/prompt-caching) is the KV cache as it appears on an invoice, and [context engineering](/wiki/ai/context-engineering) is what you do for a living because attention costs O(n²).

## Wiki Pages

{{< section >}}

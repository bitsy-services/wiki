---
title: "Neural Networks"
weight: 90
---

A neural network is a function that was *fitted* rather than written. Someone chooses its shape — how many numbers go in, how many stages of arithmetic they pass through, how wide each stage is — and then leaves every number inside it blank, to be filled in by showing the thing an enormous number of examples and correcting it each time it gets one wrong. Nobody decides what any individual number ends up as, and nobody can say afterwards what any of them means. The arrangement is designed; the contents are grown.

Everything in this section is a detail of one particular arrangement. Understanding what kind of object is being arranged comes first, because it explains the two facts about language models that surprise people most: that nobody wrote the rules they follow, and that nobody can look up where any of it is stored.

## Why not just write the program?

Take the job this section is about: given some text, say what comes next. Now try to write that as instructions.

You could start on grammar, and rules for grammar do exist — enough of them to fill a career, with an exception behind every one. But grammar only narrows the field to the sentences that are *legal*. The question is which of them a person would actually have written, in a document about anything at all, given everything above it. There is no rule for that. Not a hard one, not a long one — nothing you could state, because the thing you would be trying to state is most of what a literate adult knows.

So you give up on stating the rule and specify a *shape* instead: a formula with a great many blanks in it, flexible enough that some filling-in of the blanks would reproduce almost any rule, including one nobody can articulate. Then you let the examples choose the filling.

You have done this before on a smaller scale. Fitting a straight line to a scatter plot is the same move: you don't derive the relationship between the two axes, you assume the shape `y = ax + b` and let the points pick `a` and `b`. A neural network changes two things about that. The shape can bend, so it is not restricted to relationships that happen to be straight. And instead of two blanks it has a hundred million.

## Multiply, bend, repeat

The shape itself is monotonous, which is the surprising part. One stage does two things:

```text
   numbers in  ──▶  multiply by a table of weights  ──▶  bend each result  ──▶  numbers out
```

The multiply is a matrix multiplication: every output number is a weighted sum of every input number, with the weights being the blanks that training fills in. The bend is a fixed, simple, nonlinear function applied to each number on its own — nothing is learned in it and it has no weights of its own.

Then you do it again on the result, and again. That repetition is what *deep* learning means: not a more sophisticated stage, just more stages.

The bend looks like the trivial part and is load-bearing. Two matrix multiplications back to back are equivalent to a single matrix multiplication, so a stack built without bends collapses to one stage no matter how many you paid for — [the activations page](/wiki/ai/llm/activations) does that arithmetic in full. Bends are the only reason depth buys anything.

A plain chain of stages, with nothing else going on, is a **multi-layer perceptron** — an **MLP** — the simplest network there is, and old enough that the name predates the field's current vocabulary. It is not a historical curiosity. A [transformer](/wiki/ai/llm) has one inside [every block](/wiki/ai/llm/glossary), and [those MLPs](/wiki/ai/llm/multi-layer-perceptron) hold most of the model's weights. What the architecture adds on top is [attention](/wiki/ai/llm/attention), a stage that works out *how much to mix from where* by reading the input itself — the [attention pattern](/wiki/ai/llm/glossary) — rather than having that fixed at training time like every weight in the model. It is a genuinely different kind of part, and the reason the design was worth a paper.

One vocabulary note, because it will trip you up when you leave this section. The *multi-layer* in that name is the general literature's word for one multiply-and-bend: a **layer**, counted up to give a network's *depth*. These pages [avoid the word on its own](/wiki/ai/llm/glossary#words-this-subsection-avoids), because inside a transformer it is ambiguous between a whole block and one piece of one, and that ambiguity is a reliable source of confusion. Say *block*, *attention*, or *MLP* here; expect *layer* everywhere else.

## Where "neuron" comes from, and why it misleads

The name is a 1940s analogy that outlived its usefulness. McCulloch and Pitts modelled a brain cell in 1943 as something that sums its inputs and fires if the total clears a threshold; Rosenblatt built the perceptron on that idea in 1958 — first as a simulation on an IBM 704, then two years later as a room-sized machine with the connections strung physically between its units — and the press coverage was about as measured as you would expect. Each unit in the model was a "neuron," each connection a "synapse," and the vocabulary stuck long after anyone was claiming the resemblance was more than superficial.

It is worth being clear about how superficial. A unit here is a weighted sum and a bend. It does not spike, it has no timing, its connections are entries in an array rather than anything laid out anywhere, and the procedure that sets its weights — [work out which way every weight should move, then move them all a little](/wiki/ai/llm/backprop-one-weight) — is not something a brain is believed to do. The field kept the word, not the claim.

The practical damage is that "neuron" invites you to expect one unit to *mean* something: this one detects rivers, that one fires on Python. Sometimes something close to that is true, and often it is badly false — a single unit fires on an unrelated-looking grab bag, and the thing you were looking for is spread across many units at once. That is [superposition](/wiki/ai/llm/superposition), and it is the main obstacle to reading a network rather than merely running one.

## How the weights get their values

Every weight starts as a small random number, so a fresh network's output is noise. Training is a loop with three steps, and the rest of this section fills in each of them:

1. **Guess.** Run an example through and see what comes out.
2. **Score.** Compare that against what should have come out. [The loss function](/wiki/ai/llm/the-loss-function) turns the discrepancy into a single number.
3. **Blame.** Work out, for every weight in the model, whether nudging it up would have made that number better or worse — then nudge every one of them a little in the better direction. That step is [backprop](/wiki/ai/llm/backprop-one-weight), and the reason it is affordable is that it gets all of the answers in a single backward sweep rather than one at a time.

Repeat across a large enough pile of examples and the weights stop being noise. No step in that loop involves anyone deciding what the model should learn. The examples and the score decide; the loop only follows the slope.

## What you give up

You get a function nobody could have written down. What you give up is the ability to read it.

A conventional program can be examined: the rule for a behaviour is on some line, and you can go and look at that line. A network has no line. The rule is distributed across millions of weights that each participate in countless other rules, and the only fully honest description of what the model does is the weights themselves — which is to say, no description at all. This is why *interpretability* is a research field rather than a debugging technique, and why the pages in this section keep saying things like "as far as anyone has been able to determine."

It also relocates where the value is. The arrangement is small, public, and unremarkable — [nanoGPT](/wiki/ai/llm/running-the-checks) is a complete implementation of this one in roughly three hundred readable lines, and everyone in the field has read it. What is worth anything is the numbers that went into the blanks, along with the data and the compute it took to find them.

## Check yourself

Build [GPT-2 small](/wiki/ai/llm/gpt-2)'s arrangement with nothing behind it, and put it next to the trained one:

```python
from transformers import GPT2LMHeadModel, GPT2Config

trained = GPT2LMHeadModel.from_pretrained("gpt2")
fresh   = GPT2LMHeadModel(GPT2Config())     # same arrangement, random numbers

sum(p.numel() for p in trained.parameters())   # 124,439,808
sum(p.numel() for p in fresh.parameters())     # 124,439,808 — identical
```

Same shapes, same parameter count, same code executing on the way through. Now score each on a sentence [the way the setup page does it](/wiki/ai/llm/running-the-checks), passing `labels=ids`.

`fresh` comes back just under **11**, and that is not an arbitrary number to land near. A model spreading its probability evenly over the whole [vocabulary](/wiki/ai/llm/glossary) — no opinion at all, about anything — would score exactly `ln(50257)`, which is 10.82. Random weights sit a little above that floor rather than on it, because the scores they produce are slightly uneven rather than perfectly flat. Exponentiate and the [perplexity](/wiki/ai/llm/perplexity) comes out around the size of the vocabulary itself, which is the arithmetic saying *choosing at random among fifty thousand options*. `trained` comes back in the low single digits. Generate from both and you get English out of one and noise out of the other.

Nothing about the program differed between those two runs. Only the numbers did.

## Depends on / leads to

Depends on [GPT-2](/wiki/ai/llm/gpt-2), the network the rest of these pages take apart. Leads to [tokenization](/wiki/ai/llm/tokenization), where the text becomes integers — and, further along, to [the multi-layer perceptron](/wiki/ai/llm/multi-layer-perceptron), the plain network sitting inside every block.

---
title: "Superposition"
weight: 310
---

A model keeps track of far more things than it has room for. Superposition is how it gets away with it: rather than giving every concept its own private slot, it overlaps them, cramming many more into the space than the space can strictly hold and accepting a little interference as the price. It works because on any given word almost none of those concepts are actually in play, so the collisions mostly don't happen at the same time.

## A feature is a direction

Start with what the model is storing. "This text is French." "This token is a proper noun." "We're inside a quotation." Each of these is, to a good approximation, a single **direction** in [the residual stream](/wiki/ai/llm/residual-stream) — and how far a row points along that direction is how strongly the feature is present.

Not a slot, and not one of [the MLP's hidden units](/wiki/ai/llm/the-mlp) — the individual detectors people usually have in mind when they say *neuron*. A direction, which is a thing you can have an unlimited number of in principle and a very limited number of in practice.

## The arithmetic problem

[`d_model`](/wiki/ai/llm/glossary) is 768 in [GPT-2 small](/wiki/ai/llm/gpt-2), and it never changes — the stream is exactly as wide at the right edge as at the left. Meanwhile the model plainly tracks vastly more than 768 things: every language it recognizes, every syntactic role, every topic, every register, every format.

So where do the rest live?

If each feature needed its own **orthogonal** direction — exactly perpendicular to every other, so that reading one tells you strictly nothing about any other — the answer would be brutal. You can fit exactly 768 mutually perpendicular directions into 768 dimensions and not one more. The model would be capped at 768 concepts, and it clearly isn't.

## Almost-perpendicular is good enough

The escape is to give up "exactly perpendicular" for "nearly perpendicular."

Allow each pair to sit a little off true — a couple of degrees for a typical pair, a dozen for the worst of them — and the capacity of 768 dimensions stops being 768 and becomes something on the order of ten thousand. Nineteen times more features than the space has dimensions, bought entirely by relaxing a right angle by a few degrees.

The part that matters is how that scales. Hold the tolerance fixed and the number of directions you can pack grows *exponentially in the width of the space*. At that same dozen-degree budget, 8 dimensions holds barely two directions; 768 holds ten thousand; 12,288 — the width of a frontier-scale model — holds a number with fifty-odd digits in it. Widening the model doesn't add room linearly. It detonates it.

This is the fact no amount of picturing three dimensions prepares you for. In 3D, that dozen-degree relaxation buys you precisely nothing: you get three directions, exactly as if you'd insisted on true right angles. Intuition trained on rooms and boxes says "nearly perpendicular is barely better than perpendicular," and in the space intuition was trained on, it's correct. It just doesn't survive the trip to 768 dimensions, and this is the single place it misleads people most.

(Real models are believed to carry rather more than nineteen times their width in features. They buy that by tolerating angles sloppier than a dozen degrees — which is to say, more interference. What follows is why they can afford it.)

## Why the model gets away with it

Storing features that way isn't free: near-perpendicular directions **interfere**, so reading one picks up a faint smear of every other one that happens to be active.

The model tolerates that because features are **sparse**. Of the thousands it tracks, only a handful are active on any given row — "this text is French" and "we're inside a Python docstring" are both live possibilities, and they essentially never fire on the same token. The interference is real but it's mostly potential rather than actual, because the colliding pairs are rarely present at once.

That's superposition, in one line: **more features than dimensions, paid for in noise, affordable because the noise seldom all arrives together.**

## What it costs: nothing means just one thing

This explains the single thing that most frustrates people who go poking around inside models.

Open one up, pick a hidden unit — or one coordinate of the stream — and ask what it means. You will not get an answer. It's **polysemantic**: it doesn't encode a concept, it's a coordinate that dozens of unrelated features happen to share. Look at what makes some particular unit fire and you get a list with no theme to it, because you're reading one axis of a space where nothing was ever stored axis-aligned.

The features are really there. They're just not *where you're looking*, and superposition is exactly the reason.

## Prying them back apart

Which is why interpretability largely moved to **sparse autoencoders**. The idea: train a second, small network to re-express each row in a much wider space — 32,000 directions instead of 768, an **overcomplete basis**, meaning simply more directions than the space has dimensions — while penalizing it hard for using more than a few at a time.

The extra width gives every feature room to have its own direction again. The sparsity penalty is what stops the network cheating by smearing everything across everything. What comes out the other side are directions that mean one thing each — the superposed features, pulled apart.

Which is where the Golden Gate Bridge comes in. Anthropic's widely-reported result — a version of Claude that could not stop bringing the conversation around to the bridge — worked by finding a Golden Gate *feature* with exactly this method, then clamping it on. That settles the question this page opened with rather neatly. There was no Golden Gate neuron to find, and anyone who went looking for one was always going to come back empty-handed. There was a Golden Gate *direction*, superposed with thousands of others and aligned with no axis in particular, and it took an autoencoder to see it at all.

## Check yourself

[Sample](/wiki/ai/llm/running-the-checks) 10,000 random unit vectors in 768 dimensions and take the largest pairwise cosine similarity — the standard measure of how aligned two directions are, where 1 is identical and 0 is exactly perpendicular. It lands around 0.2. Ten thousand directions, drawn *at random* with no coordination whatsoever, and the worst-aligned pair among all fifty million pairs is still nearly perpendicular. That's the room superposition is exploiting, and you get it for free.

Now repeat in 8 dimensions. Near-orthogonality collapses immediately — random vectors are all over each other, and there's nowhere to hide a feature. The gap between those two results is the whole capacity story, and it is entirely a fact about dimension.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream) and [the MLP](/wiki/ai/llm/the-mlp). Leads to [fine-tuning](/wiki/ai/llm/fine-tuning).

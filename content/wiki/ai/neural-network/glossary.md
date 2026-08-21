---
title: "Glossary"
weight: 10
---

The words this section uses — and it uses only these. Third column: what the same thing is called elsewhere, so you can translate when you leave.

| Term | Means | Elsewhere called |
|---|---|---|
| **weights** | the numbers the network's arithmetic is done with, and the only thing training changes. *Parameters* means the same thing, and this section uses both — "weights" by default, "parameters" where the surrounding term of art demands it | `n_params`, coefficients |
| **layer** | one multiply-by-a-table-of-weights followed by one [bend](/wiki/ai/neural-network/bend). The unit a network's depth is counted in | linear layer, dense layer, fully-connected layer |
| **depth** | how many layers a network stacks. The *deep* in deep learning. [What it costs against width](/wiki/ai/neural-network/depth-and-width) | number of layers |
| **width** | how many numbers a layer carries. Layers in one network need not all be the same width | hidden size, number of units |
| **activations** | the numbers flowing *between* layers, as opposed to the weights they are multiplied by. They change with every input; the weights don't | hidden states, feature maps |
| **bend** | the fixed nonlinear function applied to each number on its own between two matrix multiplications, and the reason the two don't collapse into one. Holds no weights and learns nothing. A nonlinearity that reads more than one number at a time — softmax, a norm — is not a bend | activation function, nonlinearity |
| **unit** | one number in a layer's output, together with the row of weights that produced it. The thing the field unfortunately calls a *neuron* | neuron, node |
| **loss** | the single number scoring how wrong one guess was. Training is the business of making it smaller | cost, objective, criterion |
| **gradient** | for one weight, which way the loss moves if you nudge that weight up, and how sharply. [Backprop](/wiki/ai/neural-network/backprop-one-weight) computes all of them at once | derivative, `.grad` |
| **MLP** | a plain chain of layers with nothing else going on — the simplest network there is. Short for [multi-layer perceptron](/wiki/ai/neural-network/multi-layer-perceptron) | feed-forward network, FFN, dense stack |
| **feature** | a direction in activation space that means something | concept, latent |

## Words this section uses carefully

- **"Neuron"** — avoided in favour of *unit*. The word invites you to expect one unit to mean one thing, which [is often false](/wiki/ai/neural-network/superposition), and the brain analogy behind it [does not survive contact with the arithmetic](/wiki/ai/neural-network#where-neuron-comes-from-and-why-it-misleads).
- **"Layer"** — used freely here, where it is unambiguous. Inside a specific architecture it often isn't: the [LLM section](/wiki/ai/llm) [drops the word entirely](/wiki/ai/llm/glossary#words-this-subsection-avoids) because in a transformer it could mean a whole block or one piece of one.
- **"Deep"** — a statement about how many layers there are, and nothing else. It does not mean sophisticated, and it does not mean large.

## Depends on / leads to

Depends on [the section overview](/wiki/ai/neural-network). Leads to every other page in the section, starting with [the MLP](/wiki/ai/neural-network/multi-layer-perceptron).

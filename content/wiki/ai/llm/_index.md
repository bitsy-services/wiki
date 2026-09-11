---
title: "Large Language Models"
weight: 80
bookCollapseSection: true
---

A large language model is a program that takes a piece of text and returns a probability for every token that could come next. A token is a chunk of text roughly the size of a short word, and the model has a fixed list of them, called its vocabulary. The program is a [neural network](/wiki/ai/neural-network): a fixed sequence of arithmetic, plus a very large set of numbers that the arithmetic uses. Those numbers are the model's **weights**, also called its *parameters*. Nobody writes them by hand. Training sets them, and training changes nothing else.

A reply longer than one token comes from a loop. One token is picked according to the probabilities and appended to the text, and the model runs again on the longer text. A 500-token reply is 500 runs of the model. Answering a question, writing a function and holding a conversation all come from this loop.

Most of the rest of the [AI section](/wiki/ai) is about using a model. These pages are about the model itself: what text becomes on the way in, what the arithmetic does to it, how the probabilities come out, how the weights got their values, and what running it costs. Nearly every large language model in use is built on one design, the **transformer**, published by Vaswani et al. (2017), and these pages take that design apart. The worked example throughout is [GPT-2 small](/wiki/ai/llm/gpt-2), released in 2019 with 124 million weights. It runs on a laptop. It differs from current models in size, in how it was trained, and in [a short list of swappable parts](/wiki/ai/llm/gpt-2#where-gpt-2-misleads).

The parts a transformer shares with every other neural network are covered separately, and these pages assume them: what a weight is, how training adjusts one, and why a network needs a nonlinear step between its multiplications. Start with [the neural network section](/wiki/ai/neural-network) if those are unfamiliar.

## What happens to a prompt

The text is first split into [tokens](/wiki/ai/llm/tokenization). Each token is then looked up in [a table](/wiki/ai/llm/embeddings) that holds one list of numbers per vocabulary entry. The list it retrieves is the token's **row**, 768 numbers wide in GPT-2 small, and everything after the lookup works on rows. The lookup returns the same row for a token wherever it appears, so the token's position in the text has to be [supplied separately](/wiki/ai/llm/positional-encoding). GPT-2 adds a learned vector for each position to the row. The common alternative, [rotary position embedding (RoPE)](/wiki/ai/llm/rope), never changes the row; it works inside attention, and is covered with it below.

The rows then pass through a stack of [blocks](/wiki/ai/llm/glossary): 12 in GPT-2 small, each with the same structure and its own weights. Each block has two parts. The first, [attention](/wiki/ai/llm/attention), multiplies each row by three matrices of weights, which gives each token three vectors: a [query, a key and a value](/wiki/ai/llm/qkv-projections). It then scores each token against itself and every token before it. A score is the dot product of the token's query with the other token's key: the two vectors are multiplied number by number and the results added up. Last, attention blends those tokens' values, weighted toward the tokens that scored higher, multiplies the blend by a fourth matrix, and adds the result to the token's own row. It is the only step in the model where one token's row affects another's.

RoPE supplies position at this step, and only to the query and key. In every block, just before the scores are computed, it splits each token's query and key into pairs of numbers, reads each pair as a point in a plane, and rotates the point by an angle equal to the token's position times a fixed rate for that pair. For a given query and key, the score between two tokens then depends on their positions only through the distance between them. Su et al. (2021) introduced RoPE. The values are not rotated, so position affects the row only through the scores, which set how much of each value goes into the blend.

The second part is [the MLP](/wiki/ai/llm/the-mlp), a [multi-layer perceptron](/wiki/ai/neural-network/multi-layer-perceptron), which transforms each row on its own: a matrix multiplication, a nonlinear function, and a second multiplication. The MLPs hold two thirds of the weights inside each block. Meng et al. (2022) found that, in the GPT models they studied, completing a factual prompt depends mainly on the MLPs of the middle blocks.

Neither part overwrites the row. Each adds its output to it, so the row is a running total, called the [residual stream](/wiki/ai/llm/residual-stream), and it is the only thing passed from one block to the next. Elhage et al. (2021) introduced this view of the model, in which every part reads from the residual stream and adds its output back to it.

After the final block, the row for the last token is multiplied by [the unembedding](/wiki/ai/llm/unembedding-and-logits), a matrix that turns it into one score for every token in the vocabulary. The scores are called logits. [Softmax](/wiki/ai/llm/softmax-and-temperature) turns them into probabilities that sum to 1, and [a sampling rule](/wiki/ai/llm/sampling-strategies) picks one token. When the rule picks at random in proportion to the probabilities, the same prompt can produce different replies. The picked token is appended to the text, and the whole pass runs again.

Every other page in this section covers a step in that pass, how the weights got their values, or a way to make the loop cheaper.

## Where the weights come from

Training starts with random weights. [The loss function](/wiki/ai/neural-network/the-loss-function) turns each prediction into a penalty, which is larger the less probability the model gave to the token that actually came next. [Backpropagation](/wiki/ai/neural-network/backprop-one-weight) then computes, for every weight, which direction to move it to shrink the penalty, and each training step moves every weight a small amount in that direction. Current models repeat this over trillions of tokens of text. The result is a **base model**: a program that continues whatever text it is given.

Nothing in this process teaches grammar, facts or how to close a bracket as separate subjects. A base model handles them only because handling them made its predictions of the next token more accurate.

Two facts make trillions of tokens affordable. The text needs no labelling, because each token is the correct answer for the prediction before it. And a transformer computes the prediction at every position of a training text at the same time, rather than one position after another, so a larger hardware budget buys more text processed. The first fact is as old as neural language models. [Why scale worked](/wiki/ai/llm/why-scale-worked) argues that the second, which arrived with the transformer, is the main reason current models are as capable as they are.

A base model given a question may continue it with another question, because questions often follow questions in written text. Two further stages turn it into an assistant. [Fine-tuning](/wiki/ai/llm/fine-tuning) continues training on a much smaller body of text chosen for the behaviour wanted, such as example conversations. [Reinforcement learning from human feedback (RLHF)](/wiki/ai/llm/rlhf) shows people pairs of answers, records which they prefer, and trains the model toward the preferred ones. In Ouyang et al. (2022), people preferred the answers of a 1.3-billion-weight model trained with both stages to those of GPT-3, which has 175 billion weights and went through neither.

## Why it costs what it costs

Two things set the cost of running a model, and each has its own countermeasures.

The first is the size of the model. In an ordinary model, producing one token means reading every weight from memory and doing arithmetic with it, so a larger model costs more per token however short the text. When generating a single reply, the reading takes longer than the arithmetic. A [mixture of experts](/wiki/ai/llm/mixture-of-experts) model keeps several alternative MLPs in each block, called experts, and sends each token through only a few of them, so each token reads and uses a fraction of the weights. Shazeer et al. (2017) introduced that routing. Every expert still has to be held in memory, because the next token may be sent to any of them.

[Speculative decoding](/wiki/ai/llm/speculative-decoding) reduces how many times the weights are read. A small model drafts several tokens, and the large model checks all of them in one pass, which reads the weights once for all of them. That pass costs little more than producing one token. The output has exactly the probabilities the large model would have produced alone. Leviathan et al. (2022) introduced the method.

The second cost is the [context length](/wiki/ai/llm/context-length): the number of tokens in the text so far, prompt and reply together. Attention scores every token against every earlier one, so its work grows with the square of the context length, and doubling the context quadruples it. At ordinary prompt lengths this is still smaller than the arithmetic done with the weights; the context-length page works out the length at which it overtakes. Without help, generating each new token would also rerun the model over the whole text so far, repeating work already done for the previous token. From the earlier tokens, the new token needs only their keys and values in each block. Those never change once computed, because a token's row never depends on the tokens after it. [The KV cache](/wiki/ai/llm/kv-cache) stores them, so later steps reuse them instead of recomputing them. The price is memory, which grows with the context.

[Training](/wiki/ai/llm/training-vs-inference-parallelism) is limited differently. It computes every position of a text at once, so each read of the weights serves many predictions, and the arithmetic sets the speed. That difference is why serving a model is a separate engineering problem from training one.

## Reading order

Start with [Conventions](/wiki/ai/llm/conventions). It is short, and every diagram after it uses its layout. Keep the [Glossary](/wiki/ai/llm/glossary) open. [GPT-2](/wiki/ai/llm/gpt-2) comes next: every page measures against it, and it lists the constants the other pages keep using.

Most pages include a runnable experiment and the output to expect. The experiments run against GPT-2 small or [nanoGPT](/wiki/ai/llm/running-the-checks#train-a-tiny-model-nanogpt), a readable reimplementation of GPT-2 in about 300 lines, and [Running the checks](/wiki/ai/llm/running-the-checks) sets up both. Several measure [perplexity](/wiki/ai/llm/perplexity): roughly, the number of tokens the model's probability is spread across at each step. It rises when a part the model depends on is removed.

Then read down the sidebar from [tokenization](/wiki/ai/llm/tokenization). Each page comes after the pages it depends on. The pages from tokenization to [sampling strategies](/wiki/ai/llm/sampling-strategies) follow the path from text to a sampled token. The rest cover training, serving, and design choices that vary between models, and the last is [why scale worked](/wiki/ai/llm/why-scale-worked), the argument the rest of the section supports.

Several pages these rely on sit in the neural network section, because nothing about them is specific to transformers. Read them when a page here sends you there.

- [The MLP](/wiki/ai/neural-network/multi-layer-perceptron) in its general form: multiply by a table of weights, apply a nonlinear function, multiply again.
- [The bend](/wiki/ai/neural-network/bend), that section's name for the nonlinear function. Without it, a stack of multiplications collapses into a single one.
- [Normalization](/wiki/ai/neural-network/normalization), which rescales a row's numbers to a standard size. Without it, a model with many blocks does not train.
- [Skip connections](/wiki/ai/neural-network/skip-connections), which add a part's output to its input instead of replacing it. The residual stream is built from them.
- [The loss function](/wiki/ai/neural-network/the-loss-function) and [backprop](/wiki/ai/neural-network/backprop-one-weight), which score a prediction and turn the score into an adjustment for every weight.
- [Superposition](/wiki/ai/neural-network/superposition), which is how a model represents more concepts than a row has numbers, by overlapping them.

Two pages elsewhere in the AI section apply this material. [Prompt caching](/wiki/ai/prompt-caching) is the KV cache as it appears on an API bill, and [context engineering](/wiki/ai/context-engineering) is the practice of choosing what goes into a model's limited context.

## Sources

- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), arXiv:1706.03762 (2017)
- Su et al., [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864), arXiv:2104.09864 (2021)
- Meng et al., [Locating and Editing Factual Associations in GPT](https://arxiv.org/abs/2202.05262), arXiv:2202.05262 (2022)
- Elhage et al., [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html), Transformer Circuits Thread (2021)
- Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155), arXiv:2203.02155 (2022)
- Shazeer et al., [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538), arXiv:1701.06538 (2017)
- Leviathan, Kalman & Matias, [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192), arXiv:2211.17192 (2022)

## Wiki Pages

{{< section >}}

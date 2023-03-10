# MetaInfo
- title: A neural network approach to context-sensitive generation of conversation responses
- author: Sordoni

# Contribution
**First Application of a neural network model to open-domain response generation.**

- train end-to-end on unstructured Twitter data.
- using NN to address sparsity problem when integrating context.
- dynamic-context generative model.
- data-driven.


- a multi-reference extraction technique that shows promise for 
automated evaluation. (Metrics)

# Background
- vast quantities of conversational exchanges become available on social media
such as Twitter and Reddit, giving rise to data-driven models.

# Related Works
- [Ritter 2011](../bib_db/model/ritter/Ritter2011.bib) constructs a statistical machine translation system  from Twitter Corpus to generate response from a status post.
- Drawback: responses are *not* sensitive to context. (not context-sensitive)

# What is a context
- Linguistic context, *not* physical one.
- past utterances.
- encoded in a continuous context vector.

# Benefits
- Context is important: 
    * the ability to take into account previous utterances is key to building dialog systems that can keep conversations active and engaging.
- Embedding-based model:
    * model the transition between consecutive utterances.
    * capture long-span dependency.
- Robustness to sparsity:
    * capture context info while avoiding unmanageable growth of model parameters.
   
# Challenges
- Context info is hard for the MT model to capture.
- Naive injection of context is unmanageable due to data sparsity.

# Solutions
- Using embeddings for words and phrases. (Benefits of Word Embeddings)
    * compactly encode semantic and syntactic similarity.
    * address the sparsity problem.

# Models
- simple, context-sensitive, response-generation models.
- first encode context into continuous representation and then decode it using RLM.
- completely data-driven.
- no human annotation is needed.
- As opposed to: typical complex task-oriented multi-modular dialog system.
- *Important*: Based on RLM.
   
*a line of though:* Although the training is nearly free of human annotation, the evaluation of such system relies heavily on human evaluation. The training of task-oriented system relies on human annotation but its evaluation is more supervised. One cannot gain both sides of goodness.

## Recurrent Language Model (RLM)
- benefits of using an RLM as NLG:
    * plausible
    * fluent
    * contextual relevant
- proposer:[Mikolov 2010](../bib_db/classic/mikolov/MikolovKBCK10.bib), Recurrent neural network based language model.
    
## Multi-modular Dialog System
* [Young 2002](../bib_db/model/traditional_dialog/young/Young02.bib) (Talking to machine)
* [Stent and Bangalore 2014](../bib_db/model/traditional_dialog/stent/SB2014.bib) (book: Natural Language Generation in Interactive Systems)
* requires human annotation.
* task-oriented.
* complex.

# Related Works
## Radical paradigm shift
- Accomplish both task jointly.
- latent dialog state.
- optimize directly to end-to-end performance.
- data-driven.

## Traditional Dialog System
- tease apart dialog management from response generation. (Young, Stent).
- hand-coded many components.
- labels and attributes defining dialog states.

## Previous uses of ML
- response generation, [Walker 2003](../bib_db/dialog/walker/WalkerPS03.bib)
- dialog state tracking,[Young 2010]()
- user modeling, [Georgila 2006](../bib_db/dialog/georgila/GeorgilaHL06.bib)

## Application of word embeddings
- IR:
    * [Huang 2013](../bib_db/nlp_fields/HuangHGDAH13.bib)
    * [Shen 2014](../bib_db/nlp_fields/ShenHGDM14.bib)
- Online Recommendation: [Gao 2014b](../bib_db/nlp_fields/GaoPGHD14.bib)
- MT:
    * [Auli 2013](../bib_db/nlp_fields/AuliGQZ13.bib)
    * [Cho 2014](../bib_db/nlp_fields/ChoMGBBSB14.bib)
    * [Kalchbrenner and Blunsom 2013](../bib_db/nlp_fields/KalchbrennerB13.bib)
    * [Sutskever 2014](../bib_db/model/sutskever/SutskeverVL14.bib)
- Language Modeling LM:
    * [Bengio 2003](../bib_db/classic/bengio/BengioDVJ03.bib)
    * [Collobert and Weston 2008](../bib_db/classic/CollobertW08.bib)

## Context Vector
- learnt along with the RLM that generates the responses.
- as opposed to [Mikolov 2012](../bib_db/classic/mikolov/MikolovZ12.bib), which uses a pre-trained topic model.
- do not exclude stopwords.
- stopwords carry discriminative power. Sentence `how are you?` are all stopwords.


# Overview
## RNNLM
*note:* the RNNLM described here are not using LSTM.

```latex
Given sentences $s=s_1,\cdots,s_T$, the model estimates the probability of it:
\begin{align}
    p(s) = \prod_{t=1}^{T} p(s_t|s_1,\cdots,s_{t-1})
\end{align}

The model is parametrized by 3 matrices
$\Theta_{RNN}=\left< W_{in}, W_{out}, W_{hh} \right> $.

Input $s_t$ is a one-hot vector for a word in the vocabulary.
It is projected to its embedding by the input matrix $W_{in} \in \mathcal{R}^{V \times K}$ via $s_t^T W_{in}$.

The recurrent matrix $W_{hh} \in \mathcal{R}^{K \times K}$ keeps track of the history of the seen words.

The output matrix $W_{out} \in \mathcal{R}^{K\times K}$ projects the hidden state to an output layer
$o_t$, which is used to generate a probability for each word (loggits).

The forward pass computes:
\begin{align}
    h_t = \sigma \left( s_t^T W_{in} + h_{t-1}^T W_{hh} \right), o_t = h_t^T W_{out}
\end{align}

\footnote{Apparently this does not make use of any gating like LSTM or GRU.
It is the most basic (naive) form of RNN -- only a linear layer plus a sigmod activation is used. Won't it suffer from gradient vanishing or exploring?}

$K$ is th$K$ is the vector dimension.
$V$ is the vocab size.
There is no hidden layer size.
The recurrence seed is $h_0 = 0$, the zero vector.

The probability of the next word is given by softmax:
\begin{align}
    P(s_t = w|s_1,\cdots,s_{t-1}=\frac{\exp(o_{tw})}{\sum_{v=1}^{V}\exp(o_{tv})})
\end{align}

The objective function is:
\begin{align}
    L(s) = -\sum_{t=1}^{T}\log P(s_t = w|s_1,\cdots,s_{t-1})
\end{align}
This is the \textbf{negative log likehood of the training sentence s}
```

### BPTT

The backward pass is *unrolled backwards in time* using
the _back-propagation through time_ (BPTT) algorithm.
(This may be in common use for training RNN).
Gradients are accumulated over multiple time-steps.
[Rumelhart and Hinton](../bib_db/classic/BackProp.bib)

# Proposed Models
Extending the RLM probability with context, message and response gives the general
formula for our 3 models:
```latex
\begin{align}
    p(r|c,m) = \prod_{t=1}^{T} p(r_t|r1,\cdots,r_{t-1},c,m)
\end{align}
```
Settings:
- Two users A and B.
- c: a sequence of past dialog exchanges of any length (context).
- m: a message given by B.
- r: a response reacted by A.
- Input: (c,m). Output: r.
- Three models differ in the way they compose the context-messsage pair (c,m).

## Trippled Language Model, RLMT 
concatenate c,m,r into a single *long* sentence s and train the RLM on s (predict each words in s).

*Issue*: the input is overly long and modeling such long-range dependency is difficult and an open problem. (we don't have LSTM at the time yet). The RLMT is thus considered a baseline to other proposed models.

## Dynamic-Context Generative Model, DCGM

Idea: context and message are encoded into a fixed-length vector that is used by the RLM to decode the response.

It seems the *encoder-decoder* architecture is already here and it is obviously more early than Seq2Seq.

### DCGM-I
1. c and m are considered as *a single sentence* and combined by a single bag-of-words representation
```latex
\begin{align}
    b_{cm} \in \mathcal{R}^V
\end{align}
```

2. apply a feed-forward (FF) network to the b_cm to obtain a fixed-len rep.
3. the rep is used as the bias term of the hidden state matrix W_hh.
4. both the forward encoder and the RLM decoder are trained to minimize the NLL.

Parameters of *DCGM-I*:
```latex
\begin{align}
    \Theta_{\text{DCGM-I}} = \left< W_{in}, W_{hh}, W_{out}, \{W_f^l\}_{l=1}^L \right>
\end{align}
```

The weights for L layers of feed-forward network and the context-message rep produced by it:
```latex
\begin{align}
    k_1 = b_{cm}^T W_f^1 \\
    k_l = \sigma (k_{l-1}^T W_f^l) \text{for} l=2,\cdots,L \\
    k_L \in \mathcal{R}^{K \times K} \\
\end{align}
```
- k_L is the fixed-len context vector produced by the FF.
- b_cm is the BOW combination of the context and message.
- W_f^1 is the input embedding independent from those of RLM.

The RLM decoder takes the form:
```latex
\begin{align}
    h_t = \sigma (h_{t-1}^{T} W_{hh} + k_L + s_t^T W_{in}) \\
    o_t = h_t^T W_{out} \\
    p(s) = \prod_{t=1}^{T} p(s_t|s_1,\cdots,s_{t-1},c,m) = \text{softmax}(o_t)
\end{align}
```

[Architecture illustration](../picture/DCGM/dcgm-1.svg)

The context vector don't change through time.

### DCGM-II
The DCGM-I concatenates the message and context *sentences* before applying bag-of-word on them.
In this way, the order information of context and message vanish.
But order matters. So the DCGM-II addresses this by turning the message and the context into bag-of-word
respectively and then concatenate a linear mapping of their BOW respectively, which preserves the
fact that the context comes **before** the message.
The concatenated rep is then sent to the FF.
```latex
\begin{align}
    k_1=[b_c^T W_f^1, b_m^T W_f^1], \\
    k_l=\sigma(k_{l-1}^T W_f^l) \  \text{for}\  l=2,\cdots,L
\end{align}

$[x,y]$ denotes the concatenation of $x$ and $y$ vectors.
```

[Architecture illustration](../picture/DCGM/dcgm-2.svg)

# Dataset

## Format
- context is restricted to a single sentence.
- dataset consists of triples of sentences: context, message and response or (c, m, r).
```latex
\begin{align}
    \tau \equiv (c_\tau, m_\tau, r_\tau)
\end{align}
```

## Statistics
- Twitter FireHose
- 127M triples.
- 3 months: from June 2012 through Auguest 2012
- filters:
    * Only the triples where context and response were by the same user
    * triples that contain at least one frequent bigram that appeared >= 3 times
    in the corpus.
- After the filters: 29M triples remain.
- The Tweet IDs for tuning and test sets and the model code is published at [Microsoft Research Social Media Conversation Corpus](http://research.microsoft.com/convo/)
- mean len of responses in all sets: 11.5 tokens.
- human raters involved.
- tuning set: 2118 triples.
- test set: 2114 triples.

# Automatic Evaluation
- BLEU
- METEOR

*A major challenge:* the set of reasonable responses is potentially vast and 
extremely diverse.

## Extension of References
- Extend the single reference with IR approach.
- BLEU score with these mined multi-references aligns well with human judgement.
- Extracting multiple references:
    * IR ranking using a score formula:
```latex
\begin{align}
    s(\tilde{\tau}, \tau) = d(m_\tilde{\tau}, m_\tau) (\alpha d(r_\tilde{\tau}) + (1-\alpha)\epsilon)
\end{align}
```
d is the bag-of-words BM25 similarity function.
    * human evaluators rate the the quality of the candidate.
    * 3.58 references per example on average.
    * average len of responses for tuning set is 8.75
    and is 8.13 for tet set.
    
# Training
- 4M subset of the Twitter Triples.
- vocab_size = 50K.
- Use Noise-Contrastive Estimation (NCE) loss.
[Gutmann and Hyvarinen](../bib_db/classic/GutmannH10-NCE.bib)
- Adagrad optimizer. [Duchi](../bib_db/classic/DuchiHS11-Adagrad.bib)
- mini_batch_size = 100
- alpha = 0.1
- gradient clip fixed range [-10, 10] [Mikolov 2010](../bib_db/classic/mikolov/MikolovKBCK10.bib)
- initializer
    * parameters of neural models: N(0, 0.01)
    * W_hh: random orthogonal matrix scaled by 0.01
- early stop: when objective increases.
- size of RLM hidden layer: K = 512.
- context decoder layers: 512, 256, 512.

# Decode
The decoding takes the form of using neural models to rerank the n-best list generated by NMT systems.

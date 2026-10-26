# TinyGPT — Model Weights & Local Deployment

This directory documents the TinyGPT model variants, their technical specifications, download locations, and basic local-inference setup.

> **Important:** TinyGPT is an experimental 51M-parameter language model, not a production-ready assistant. In the project's 27-prompt benchmark, it showed weaknesses in arithmetic, coding, factual grounding, instruction-following, and hallucination resistance. Lower validation loss should not be interpreted as proof of reliable answers.

## Model files

The FP16 GGUF exports are intended for local inference with compatible tools such as LM Studio or `llama.cpp`. The model files are hosted separately so the Git repository does not need to contain large binary weights.

| Variant | Intended comparison focus | Download |
|---|---|---|
| **Mix A** | Chat-heavy supervised fine-tuning mixture | [`TinyGPT-Mix-A-F16.gguf`](https://huggingface.co/FakeSiddharth/Tiny-GPT/resolve/main/TinyGPT-Mix-A-F16.gguf) |
| **Mix B** | Q&A-heavy supervised fine-tuning mixture | [`TinyGPT-Mix-B-F16.gguf`](https://huggingface.co/FakeSiddharth/Tiny-GPT/resolve/main/TinyGPT-Mix-B-F16.gguf) |

**Model repository:** [FakeSiddharth/Tiny-GPT on Hugging Face](https://huggingface.co/FakeSiddharth/Tiny-GPT)

The reported export size is approximately **99.48 MiB per model**. Check the repository for current files and availability before downloading.

## Technical specifications

| Specification | Recorded value |
|---|---|
| Project name | TinyGPT |
| Architecture | GPT-2-style decoder-only causal Transformer (`GPT2LMHeadModel`) |
| Total parameters | 51,082,752 |
| Transformer blocks | 8 |
| Attention heads per block | 8 |
| Hidden / embedding dimension | 512 |
| Feed-forward dimension | 2,048 |
| Context length | 256 tokens |
| Tokenizer | GPT-2 tokenizer |
| Vocabulary size | 50,257 |
| EOS token ID | 50,256 |
| Pretraining objective | Causal next-token prediction |
| Cumulative processed input-token positions | 3,050,037,248 |
| Processed positions per parameter | Approximately 59.71 |
| Final pretraining validation loss | 3.6472 |
| Derived final pretraining perplexity | Approximately 38.37 |
| Export format | FP16 GGUF; not integer-quantized |

The processed-token count is a count of input-token **positions**, not 3.05 billion unique tokens. Dataset sources can overlap across stages.

## Fine-tuning variants and evaluation

Both final variants were fine-tuned from the Stage 4 best pretraining checkpoint (`stage4_best.pt`) using different mixtures of chat and question-answering data.

| Metric | Mix A | Mix B |
|---|---:|---:|
| Target chat / Q&A share for the chat+Q&A portion | 70% / 30% | 30% / 70% |
| Active supervised-token budget | 1,200,046 | 589,738 |
| Chat validation loss | **2.6181** | 2.8018 |
| Q&A validation loss | 3.3462 | **3.1494** |
| Chat validation perplexity | 13.71 | 16.47 |
| Q&A validation perplexity | 28.39 | 23.32 |

Mix A had the lower recorded chat validation loss, while Mix B had the lower recorded Q&A validation loss. The active-token budgets were unequal, so this is not a perfectly budget-matched comparison and the differences cannot be attributed solely to mixture ratios. Validation loss and perplexity measure prediction on evaluation data; they do not guarantee answer correctness.

The final SFT preparation recorded 83,666 training records and 10,046 development records. Recorded data sources included SODA, EmpatheticDialogues, Dolly, OpenAssistant (OASST1), DailyDialog, Everyday Conversations, and synthetic recall examples.

## Run locally with LM Studio

1. Download one of the GGUF files above.
2. Open LM Studio and use its model-import or local-model workflow to load the downloaded `.gguf` file. The exact menu names may differ by version.
3. Start a chat with the loaded model.
4. Keep prompts short because the configured context length is **256 tokens**.
5. Treat outputs as experimental and verify factual, mathematical, and code-related answers independently.

### Suggested starting generation settings

These are practical starting points, not guaranteed optimal settings for every prompt or LM Studio version:

| Setting | Starting value |
|---|---:|
| Temperature | 0.7 |
| Top-p | 0.9 |
| Repetition penalty | 1.15 |
| Maximum new tokens | 96 |
| Context length | 256 |

The project's benchmark found that a repetition penalty reduced repeated n-gram flags in some decoding settings, but it did not make the model consistently reliable. Adjust settings if generation becomes repetitive or incoherent. Stop strings and prompt-template options vary across runtimes; if using a role-formatted prompt, follow the format supported by the loaded model and runtime rather than assuming a universal template.

## Run with `llama.cpp`

First install or build `llama.cpp` using its official instructions: [llama.cpp repository](https://github.com/ggml-org/llama.cpp).

Example command (update the model path to where you saved the file):

```bash
llama-cli \
  -m "/path/to/TinyGPT-Mix-A-F16.gguf" \
  -p $'User: Hi! How are you today?\nAssistant:' \
  -n 96 \
  -c 256 \
  --temp 0.7 \
  --top-p 0.9 \
  --repeat-penalty 1.15 \
  -r "User:"
```

To test Mix B, replace the model path with `TinyGPT-Mix-B-F16.gguf`. CLI options can change between `llama.cpp` releases; run `llama-cli --help` if an option is not recognized.

## Known limitations

The project’s 27-prompt benchmark and manual testing identified important failure modes:

- **Arithmetic and logic:** Word-problem arithmetic and some reasoning prompts were answered incorrectly.
- **Code generation:** The model sometimes described code instead of producing a working implementation.
- **Factual grounding:** It could invent details that were not available in the prompt.
- **Instruction-following and honesty:** It did not consistently follow instructions or correct false premises.
- **Repetition and relevance:** Some responses repeated phrases or were poorly matched to the prompt.
- **Short context:** The configured context length is 256 tokens, limiting long prompts and conversation history.
- **Evaluation scope:** The 27-prompt benchmark is a small project-specific probe, not a standardized leaderboard evaluation.

Use TinyGPT for experimentation, local-inference demonstrations, and studying a small-model training pipeline—not for decisions requiring dependable factual accuracy.

## Artifacts and reproducibility

The training and evaluation records are documented in the project's technical report and supplied notebooks. The reported pipeline includes four pretraining stages, two final SFT variants, evaluation, and FP16 GGUF export. Reproducing the full training process also depends on the relevant datasets and revisions, checkpoints, notebook execution order, software versions, hardware, and external storage paths.

Related project artifact names include:

- `TinyGPT-Mix-A-F16.gguf`
- `TinyGPT-Mix-B-F16.gguf`
- `TinyGPT_v2_Training_History.xlsx`

## License and dataset attribution

**Do not assume that the model weights are Apache-2.0 licensed.** The project's technical report says that dataset-license compatibility and model-redistribution permissions require a separate review before public release. Confirm the license and usage conditions in the model repository before redistributing the weights.

The recorded training sources include FineWeb and FineWeb-Edu for pretraining, and SODA, EmpatheticDialogues, DailyDialog, Dolly, OpenAssistant (OASST1), Everyday Conversations, and synthetic recall examples for fine-tuning. Each dataset may have its own license, attribution, and usage restrictions; review the applicable terms before redistribution or commercial use.

---

**Project:** TinyGPT  
**Purpose of this file:** Model artifact reference and local deployment guide.

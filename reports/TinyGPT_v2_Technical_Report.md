# TinyGPT v2 — Technical Report Summary

This Markdown file is a readable summary of the completed project. The detailed, evidence-based report is [`TinyGPT_v2_Technical_Report.pdf`](TinyGPT_v2_Technical_Report.pdf) (16 pages); consult it for full tables, methods, analysis, and caveats.

## Purpose and outcome

TinyGPT v2 set out to build and study a small conversational language model. The project did not achieve reliable general-purpose assistant behavior. It did complete and document a full small-model pipeline, from model initialization and staged pretraining through supervised fine-tuning (SFT), comparative evaluation, and FP16 GGUF export.

The project is useful as an educational and experimental record of the engineering workflow and its limitations. The final models are not suitable for consequential decisions.

## Model

The final Mix A and Mix B variants use a GPT-2-style decoder-only causal Transformer with 51,082,752 parameters, an 8-layer/8-head configuration, a hidden size of 512, the GPT-2 tokenizer (50,257-token vocabulary), and a 256-token context. The model was initialized for this project; it was not fine-tuned from pretrained GPT-2 weights. The GPT-2 tokenizer and Transformers implementation were reused.

## Training and artifacts

The numbered notebooks document four pretraining stages, SFT data preparation, two Stage 4 SFT mixtures, evaluation, and conversion. Across the four pretraining stages, the report records about 3.05 billion processed input-token positions (approximately 59.71 positions per parameter). This is a position count; dataset overlap means it is not a count of unique tokens.

Mix A uses a chat-heavy 70%/30% chat-to-Q&A target mixture; Mix B uses a Q&A-heavy 30%/70% target. Their active supervised-token budgets differed, so the comparison is not budget-matched and the outcome cannot be attributed to mixture ratio alone. The training-history workbook, five plots, benchmark summary, and infographic are included alongside the PDF report.

## Evaluation and limitations

The project-specific interactive benchmark covered 27 greedy prompts and 26 sampled prompt IDs in the supplied transcript. It was a small qualitative probe, not a standardized benchmark. It supplied no answer-key scoring or formal aggregate accuracy. The report records failures in arithmetic, coding, relevance, instruction following, factual grounding, and hallucination resistance, alongside a few isolated correct answers.

Validation loss and perplexity describe prediction on held-out data; they do not establish that generated answers are correct or safe. The models should be treated as experimental demonstrations.

## Reproduction and deployment

The workflow uses Google Colab/Drive for the initial notebook and Kaggle inputs/outputs for later stages. It depends on external datasets, checkpoints passed between notebook runs, internet access, secrets supplied by hosted runtimes, and appropriate GPU compute. Saved notebook outputs show prior runs; they do not supply every required dataset or checkpoint.

The final export notebook creates FP16 GGUF files for local inference. The GGUF weights are hosted separately and are not included in this repository. See [`../models/README.md`](../models/README.md) for the recorded model links and LM Studio/`llama.cpp` instructions.

## Licensing note

The project report says dataset-license compatibility and permission to redistribute model weights require separate review. The repository license does not replace the terms for third-party datasets or externally hosted weights. Review those terms before redistributing those materials.

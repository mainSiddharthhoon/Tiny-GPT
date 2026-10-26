<<<<<<< HEAD
# TinyGPT v2

TinyGPT v2 is an educational language-model project that documents a complete small-model workflow: initialize a GPT-2-style causal Transformer, pretrain it in stages, prepare supervised fine-tuning (SFT) data, train two data-mixture variants, compare their outputs, and export the resulting checkpoints to GGUF for local inference.

The project demonstrates how the pipeline works; it did **not** produce a dependable general-purpose assistant. The recorded 51,082,752-parameter models showed weaknesses in arithmetic, coding, factual grounding, instruction following, and hallucination resistance. Treat them as research and learning artifacts, not as systems for consequential decisions.

## What the project contains

- Eight Jupyter notebooks with the training, evaluation, and export workflow.
- A 16-page technical report, training-history workbook, qualitative benchmark summary, loss plots, and a training-pipeline infographic.
- A model deployment guide in [`models/README.md`](models/README.md). The large GGUF weights are hosted externally and are not stored in this repository.
- `requirements.txt` for the Python packages used by the notebooks.

The detailed report is [`reports/TinyGPT_v2_Technical_Report.pdf`](reports/TinyGPT_v2_Technical_Report.pdf). The report records approximately 3.05 billion processed input-token positions across four pretraining stages, and explains the methods, evidence, limitations, and reproducibility constraints. Input-token positions are not necessarily unique tokens because datasets may overlap.

## Repository map

| Path | Contents |
|---|---|
| `notebooks/01_Initial_Pretraining_Stage1_Stage2.ipynb` | Initial model setup and Stage 1/Stage 2 pretraining workflow. |
| `notebooks/02_Stage3_Continued_Pretraining.ipynb` | Kaggle workflow continuing pretraining from the Stage 2 checkpoint. |
| `notebooks/03_Stage4_Continued_Pretraining.ipynb` | Kaggle workflow continuing from the Stage 3 checkpoint. |
| `notebooks/04_Stage4_SFT_Data_Preparation.ipynb` | Cleans and combines public conversation and Q&A datasets; writes training, development, and audit files. |
| `notebooks/05_Stage4_SFT_Training_MixA_MixB.ipynb` | Fine-tunes independent Mix A and Mix B models from the Stage 4 checkpoint. |
| `notebooks/06_Final_Model_Evaluation_and_Benchmark.ipynb` | Loads saved checkpoints for an interactive playground and qualitative benchmark; it does not retrain the models. |
| `notebooks/07_GGUF_Conversion.ipynb` | Converts the two best SFT checkpoints to FP16 GGUF for tools such as LM Studio. |
| `notebooks/experiments/Stage3_Experimental_SFT_MixA_MixB.ipynb` | Separate experimental SFT comparison from a Stage 3 checkpoint; it is not part of the final Stage 4 lineage. |
| `models/README.md` | Model specifications, external weight links, limitations, and local inference instructions. |
| `reports/TinyGPT_v2_Technical_Report.pdf` | Technical report covering the training history, analysis, evaluation, and deployment. |
| `reports/TinyGPT_v2_Training_History.xlsx` | Workbook of the recorded training history. |
| `reports/benchmark_report.txt` | Human-readable summary of the interactive benchmark. |
| `reports/benchmark_summary.json` | Structured version of the benchmark summary. |
| `reports/figures/` | Five pretraining and SFT comparison figures. |
| `assets/training_pipeline.png` | Infographic of the training pipeline. |
| `LICENSE` | Apache License 2.0 declaration for this project; see the licensing note below. |

### Figure files

- `reports/figures/fig01_pretraining_progress.png`
- `reports/figures/fig02_stage1_stage2_losses.png`
- `reports/figures/fig03_stage3_pretraining_losses.png`
- `reports/figures/fig04_stage4_pretraining_losses.png`
- `reports/figures/fig05_sft_mix_comparison.png`

## Running the notebooks

The notebooks were written for hosted notebook environments: the early workflow uses Google Colab/Drive paths, while later stages use Kaggle inputs and outputs. They are not a one-command local training application. Training requires substantial compute, internet access to datasets and model/tokenizer assets, and storage for checkpoints. Later notebooks expect checkpoint and data artifacts from earlier runs to be attached or copied into the paths they search.

1. Use a Python notebook runtime with internet access. Use a CUDA-enabled PyTorch build and a GPU for the training notebooks; CPU execution is not a practical substitute for the documented multi-hour runs.
2. Install the listed dependencies in the runtime. In a local environment, create and activate a virtual environment, then run `python -m pip install -r requirements.txt`. Install the PyTorch build appropriate for your CUDA/CPU setup first if needed.
3. Start Jupyter with `jupyter lab`, or upload the notebooks to the supported Colab/Kaggle environment.
4. Run the numbered workflow in order: `01`, `02`, `03`, `04` (prepare SFT data), `05` (train Mix A and Mix B), `06` (evaluate), then `07` (GGUF export). At each hosted-runtime transition, save the outputs and attach the required checkpoint/data artifacts to the next notebook as described in its opening cells.
5. For local execution, update the notebooks' `/content/drive/...` and `/kaggle/...` paths and provide equivalent input files and credentials. Kaggle secrets and Google Drive APIs are provided by their respective hosted runtimes, not by this repository.
6. To run a model after export, follow the LM Studio or `llama.cpp` instructions in [`models/README.md`](models/README.md). You need a GGUF weight file; it is not included here.

The notebooks also contain saved outputs from prior executions. These record past runs and do not mean that the notebooks will run successfully without their external datasets, checkpoints, secrets, and hosted-runtime setup. Dataset revisions, hardware, package versions, runtime limits, and storage paths affect reproducibility.

## Model variants and evaluation

Mix A uses a chat-heavy mixture for SFT and Mix B uses a Q&A-heavy mixture. Their recorded validation losses favored different data types, and the training budgets were unequal; the comparison therefore does not isolate mixture ratio as the only cause. The project-specific interactive benchmark found serious quality failures and did not provide a formally scored accuracy percentage. See the technical report and model guide for details and caveats.

## Licensing and third-party material

The repository's `LICENSE` carries an Apache-2.0 declaration. The technical report explicitly says dataset-license compatibility and permission to redistribute model weights require separate review. The datasets and externally hosted weights are not included in this repository, and this project license does not replace the terms set by their providers. Review those terms before redistributing data or weights. The external model links in `models/README.md` are provided as project references; verify that they resolve and that the files are still available before relying on them.

## Project status

This is a notebook-based research/educational artifact set rather than an installable Python package or hosted inference service. The reports and saved notebook outputs document the completed experiments; rerunning training depends on external inputs and compute described above.
=======
# Tiny-GPT

A small GPT-style Transformer language model trained from randomly initialized weights.

Project structure and environment setup are being established first.

The project is organized into data, model, training, and utility modules under
`src/`. The tokenizer implementation lives in the top-level `tokenizer/`
package.
>>>>>>> 9aa3f7fc3b3d75997e6029e7eb3b8e510bb24701

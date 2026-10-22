# Kaggle Competitions

This repository is intended to collect experiments and solutions developed for Kaggle competitions.

> **Current status:** the repository does not contain a competition solution yet. The structure and documentation below define how future work should be organized.

## Repository goals

- Keep notebooks, reusable source code, and configuration files organized by competition.
- Record preprocessing, feature engineering, validation, and modeling decisions.
- Make experiments reproducible by documenting environments, random seeds, and evaluation results.
- Keep large datasets, generated models, and credentials outside version control.

## Recommended structure

```text
competitions/
└── <competition-name>/
    ├── README.md
    ├── notebooks/
    ├── src/
    ├── configs/
    └── submissions/
shared/
├── src/
└── tests/
```

Each competition README should include:

1. a link to the competition and its evaluation metric;
2. setup and data download instructions;
3. the validation strategy;
4. commands for training and generating a submission;
5. a summary of experiments and scores.

## Reproducibility checklist

Before adding a solution, document or provide:

- the Python version and dependency file;
- deterministic seeds where supported;
- the expected local data paths;
- the train/validation split strategy;
- the command or notebook execution order;
- the output path and schema of generated submissions.

## Validation guardrails for future solutions

For each new competition, record these decisions before comparing model scores:

- Choose the split unit to match the task: keep records from the same subject or entity together when they must not cross folds, and preserve chronological order for a forecasting evaluation.
- Fit imputers, scalers, encoders, feature selection, and other learned preprocessing on each training fold only; apply the fitted transformations to its validation fold.
- Exclude the target, post-outcome information, and features unavailable at prediction time from model inputs.
- Save fold assignments or the exact procedure that regenerates them, and compare experiments on the same folds and metric implementation.
- Keep a simple baseline alongside more complex models. Treat public leaderboard scores as a separate signal, not as a replacement for local validation.
- Before submission, compare the output with the competition's sample submission: column names, row count, identifier alignment, target shape, and allowed value ranges. Check for missing or non-finite predictions.
- Document any external data and confirm its use is permitted by that competition's rules.

These are acceptance criteria for future contributions; no validation pipeline or automated submission checks are implemented in the current repository.

## Experiment log template

Keep a compact experiment table in each competition README so results remain traceable to the exact code and validation setup:

| ID | Commit | Seed | Validation | Local score | Public LB | Private LB | Notes |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| `exp-001` | `<short-sha>` | `<seed>` | `<split-or-folds>` | — | — | — | `<model-and-feature-summary>` |

Use `—` for scores that are not available yet. Record the commit before submitting so every leaderboard result can be reproduced from a specific repository state.

## Kaggle CLI setup

Install the official CLI and place the API token downloaded from **Kaggle → Settings → API → Create New Token** in Kaggle's configuration directory:

```bash
python -m pip install kaggle
mkdir -p ~/.kaggle
mv /path/to/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
kaggle competitions list
```

After accepting a competition's rules on its Kaggle page, create its local directory and download the data using the competition slug:

```bash
COMPETITION="<competition-slug>"
mkdir -p "competitions/${COMPETITION}/data"
kaggle competitions download -c "${COMPETITION}" -p "competitions/${COMPETITION}/data"
```

On Windows, use the same standard `.kaggle` directory from PowerShell:

```powershell
python -m pip install kaggle
New-Item -ItemType Directory -Force "$HOME\.kaggle"
Move-Item "C:\path\to\kaggle.json" "$HOME\.kaggle\kaggle.json"
kaggle competitions list

$Competition = "<competition-slug>"
New-Item -ItemType Directory -Force "competitions/$Competition/data"
kaggle competitions download -c $Competition -p "competitions/$Competition/data"
```


### Inspect and extract the downloaded data

List the files published for the competition before downloading so unexpected archive contents are visible:

```bash
kaggle competitions files -c "$COMPETITION"
```

The competition download command normally creates `competitions/<slug>/data/<slug>.zip`. Extract it without adding another dependency:

```bash
ARCHIVE="competitions/${COMPETITION}/data/${COMPETITION}.zip"
python -m zipfile -e "$ARCHIVE" "competitions/${COMPETITION}/data"
```

PowerShell equivalent:

```powershell
$Archive = "competitions/$Competition/data/$Competition.zip"
Expand-Archive -LiteralPath $Archive -DestinationPath "competitions/$Competition/data" -Force
```

Confirm that the expected train, test, and sample-submission files are present before starting preprocessing. Keep or remove the ZIP locally only after verifying extraction; both the archive and extracted files remain ignored because they are under `data/`.

The `data/` directory and `kaggle.json` are already excluded by this repository's `.gitignore`. Never print or commit the token.

## Data and credentials

Do not commit Kaggle API credentials, downloaded competition datasets, trained model files, or other large generated artifacts. Store credentials using Kaggle's standard local configuration and add competition-specific data and output paths to `.gitignore` when the first solution is introduced.

## Contributing a competition

Create one directory under `competitions/`, add a focused README, and keep exploratory notebooks separate from reusable code. Verify that a fresh environment can reproduce the documented workflow before committing results.

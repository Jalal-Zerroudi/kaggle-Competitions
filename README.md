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

## Experiment log template

Keep a compact experiment table in each competition README so results remain traceable to the exact code and validation setup:

| ID | Commit | Seed | Validation | Local score | Public LB | Private LB | Notes |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| `exp-001` | `<short-sha>` | `<seed>` | `<split-or-folds>` | — | — | — | `<model-and-feature-summary>` |

Use `—` for scores that are not available yet. Record the commit before submitting so every leaderboard result can be reproduced from a specific repository state.

## Data and credentials

Do not commit Kaggle API credentials, downloaded competition datasets, trained model files, or other large generated artifacts. Store credentials using Kaggle's standard local configuration and add competition-specific data and output paths to `.gitignore` when the first solution is introduced.

## Contributing a competition

Create one directory under `competitions/`, add a focused README, and keep exploratory notebooks separate from reusable code. Verify that a fresh environment can reproduce the documented workflow before committing results.

# <Competition name>

> Replace every angle-bracket placeholder before treating this document as complete.

## Competition

- **Kaggle page:** <competition-url>
- **Slug:** `<competition-slug>`
- **Task:** <classification, regression, forecasting, ranking, ...>
- **Evaluation metric:** <metric-name-and-direction>
- **Deadline:** <deadline-and-time-zone>
- **Rules reviewed:** <yes/no and relevant restrictions>

## Environment

- **Python:** <version>
- **Dependency file:** <requirements.txt, pyproject.toml, or environment.yml>
- **Hardware assumptions:** <CPU/GPU and memory>
- **Global seed:** <seed>

Install the environment:

```bash
<installation-command>
```

## Data

Download and extract the competition data:

```bash
COMPETITION="<competition-slug>"
mkdir -p "competitions/${COMPETITION}/data"
kaggle competitions download -c "$COMPETITION" -p "competitions/${COMPETITION}/data"
python -m zipfile -e \
  "competitions/${COMPETITION}/data/${COMPETITION}.zip" \
  "competitions/${COMPETITION}/data"
```

Document the expected local files, identifiers, target column, and any permitted external data.
Never commit downloaded data or `kaggle.json`.

Record the exact local snapshot:

```bash
python scripts/write_data_manifest.py \
  "competitions/${COMPETITION}/data" \
  "competitions/${COMPETITION}/data-manifest.sha256"
```

- **Retrieved at (UTC):** <timestamp>
- **Kaggle CLI:** <version from `kaggle --version`>
- **Official file listing reviewed:** <yes/no>
- **SHA-256 manifest:** `data-manifest.sha256`
- **External data:** <none, or source, version, license, and rule allowance>

## Validation

- **Split unit:** <row, subject, group, or time>
- **Strategy:** <holdout or cross-validation details>
- **Leakage controls:** <how preprocessing and target leakage are prevented>
- **Metric implementation:** <library/function and parameters>
- **Saved fold definition:** <path or deterministic generation command>

## Train

```bash
<training-command>
```

Record where checkpoints, logs, and out-of-fold predictions are written.

## Generate a submission

```bash
<submission-command>
```

Expected output:

- **Path:** `submissions/<experiment-id>.csv`
- **Columns:** <identifier-and-prediction-columns>
- **Row count:** <expected-row-count>
- **Value constraints:** <allowed-range-or-labels>

Before uploading, compare the file with the sample submission and check identifiers, missing
values, non-finite values, duplicate rows, and prediction ranges.

## Experiments

| ID | Commit | Seed | Validation | Local score | Public LB | Private LB | Notes |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| `exp-001` | `<short-sha>` | <seed> | <split-or-folds> | — | — | — | <baseline> |

## Reproduce the selected result

- **Selected experiment:** `<experiment-id>`
- **Commit:** `<full-commit-sha>`
- **Configuration:** `<config-path>`

```bash
<commands-from-clean-environment-to-submission>
```

## Known limitations

- <limitation-or-open-risk>

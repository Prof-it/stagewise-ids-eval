# Beyond E2E Metrics: Stage-wise Evaluation of a Cascaded Hybrid IDS

Code for evaluating what the second stage of a hybrid intrusion detection system adds: an Isolation Forest scored only on the traffic that Snort missed, reported as conditional recovery (CDR), ΔRecall and ΔFPR.

## 📚 Publication

This repository accompanies the following research contribution:

* **Bilinski, G. and Lu, T. (2026).** *Beyond E2E Metrics: Evaluating Incremental Contributions in Cascaded Hybrid IDS.* IEEE 2026 International Conference on Emerging Trends in Engineering and Computing (ETECOM), Paris, France, 26–27 October 2026. **In Press**
* **Talk recording (ETECOM 2026):** https://youtu.be/qzrZKH5UOO4

It is an **extension of the original bachelor's thesis (*"Evaluation des Zusatznutzens unüberwachter Anomalieerkennung in hybriden Intrusion-Detection-Systemen"*)**, with additional development, analysis, and documentation for open, reproducible research. If using this code or methodology for research, please cite the above paper when available, and/or this repository.


```bibtex
@inproceedings{bilinski_lu_2026_ids,
  author    = {Bilinski, Gina and Lu, Tianxiang},
  title     = {Beyond E2E Metrics: Evaluating Incremental Contributions in Cascaded Hybrid IDS},
  booktitle = {IEEE 2026 International Conference on Emerging Trends in Engineering and Computing (ETECOM)},
  year      = {2026},
  address   = {Paris, France},
  month     = oct,
  note      = {In press, 26--27 October 2026}
}
```

# Repository Purpose & Reproducibility

All experiment steps, evaluation logic, and all result figures/tables referenced in the paper can be exactly reproduced using the scripts and notebooks in this repository. See [Reproducibility & Navigation for the Paper](#reproducibility--navigation-for-the-paper) for a guide mapping between each main methodology/result (metric, table, or figure) in the paper and the corresponding scripts/outputs.
## Reproducibility & Navigation for the Paper


This repository provides the code, notebooks and documentation needed to reproduce the results. The CICIDS2017 dataset is not included (see [Data acquisition](#data-acquisition)), and large intermediate files are provided separately via OneDrive. The paper manuscript is not part of this repository. For each main stage, metric, or result table/figure, use the mapping below:

- **Data Preparation & Preprocessing** (see Sec. 3 "Experimental Setup"):
   - `data/timestampAddSekAndEnd.py`: Generates time-precise flows.
   - `data/flow_csv/prepared/`: Time-aligned CSVs for all experiment days.
   - `snort/matchingSnort.ipynb`: Bidirectional 5-tuple flow matching and alert assignment. Produces the residual set and provides sensitivity analysis results (see Table 2, matching tolerance Table 5 in paper).

- **Snort Detection & Residual Construction** (Sec. 4.1–4.2, Figure 2, Table 3):
   - Snort configuration as described under [Installation](#installation), alerts in `snort/logs/alert_csvTotal.txt`, and the residual calculation outputs (see confusion matrix, per-class recall, and precision breakdown; used for paper's Figure 2 and Table 3).

- **Anomaly Detection, Feature Selection & Evaluation** (Sec. 4.2–4.3, Table 4, Table of selected features, feature comparison Table 5/6):
   - `iForest/isolationForest.ipynb`: Implements full anomaly detection protocol including feature selection, model training, threshold calibration (at 1% FPR and others), and repeated random-state evaluation.
   - Tables reproduced: Feature selection output (see paper's Table 1/"selected features"), feature set comparison (Table 5/6), and all plots (confusion matrices, tradeoff/threshold curves for CDR, ΔRecall, ΔFPR, and per-class results). 
   - Outputs and figures for every main result are in `iForest/figures/`.
   - All metrics—**Conditional Detection Rate (CDR), ΔRecall, ΔFPR**—and per-class breakdowns (Table 7: attack-class CDRs) are computed in this notebook and saved in outputs/figures.
   - **Parameter Settings/Variants:** All important experiment settings (feature sets, thresholds, tolerance, etc.) are visible in the notebook and referenced by table/section in the paper.

For methodology details, all metric definitions, and guidance on pipeline replication, see the accompanying paper, especially Sec. 3–4 and the corresponding result table/figure captions.

# Hybrid IDS – Snort + Isolation Forest

The implemented pipeline combines Snort as a signature-based first detection stage with an Isolation Forest as an unsupervised second detection stage on the CICIDS2017 dataset. All pipeline logic, metrics, and intermediate results directly support the incremental and conditional stage-wise evaluation paradigm of the accompanying paper.

## Repository contents

`data/timestampAddSekAndEnd.py` Adds second-precise timestamps and calculated end timestamps to the official CICIDS2017 CSV files
`snort/matchingSnort.ipynb` Loads flows and Snort alerts, performs bidirectional 5-tuple matching, and creates the residual CSV
`iForest/isolationForest.ipynb` Feature selection, training, threshold calibration, application of the Isolation Forest, and complete evaluation

## Requirements

### System environment

The pipeline was developed and tested in the following environment:

- **Host system:** macOS (Apple Silicon)
- **Virtualization:** UTM
- **Virtual machine:** Ubuntu 26.04 LTS, 8 CPU cores, 12 GB RAM, 80 GB storage, architecture: aarch64
- **Development environment:** Visual Studio Code with SSH access to the Ubuntu VM

### Required software

- Snort - 3.12.2.0 - First detection stage
- Python - 3.14.4 - Data processing, ML
- pandas - 3.0.3 - Tabular data
- NumPy - 2.4.6 - Numerical operations
- scikit-learn - 1.8.0 - Isolation Forest, metrics
- ipykernel - 7.2.0 - Jupyter notebooks
- CICFlowMeter - 4.0 - PCAP → CSV (Windows/WSL2)

## Project structure

The following directory layout is assumed by the scripts and notebooks.

```
stagewise-ids-eval/
├── data/
│   ├── timestampAddSekAndEnd.py
│   ├── flow_csv/
│   │   ├── original/          # official CICIDS2017 CSV files (Tue–Fri)
│   │   ├── with_seconds/      # CICFlowMeter-generated CSV files with seconds
│   │   └── prepared/          # prepared files with timestamps (output of timestampAddSekAndEnd.py)
│   ├── pcap/                  # CICIDS2017 PCAP files (Tue–Fri)
│   └── ml_csv/                # Monday-WorkingHours.pcap_ISCX.csv (for IF training)
├── snort/
│   ├── logs/                  # alert_csvTotal.txt (Snort output)
│   ├── residuals/             # snort_residuals.csv, snort_metrics.json
│   ├── figures/               # figures from matchingSnort.ipynb
│   ├── rules/                 # Snort/Talos LightSPD rule files
│   └── matchingSnort.ipynb
├── iForest/
│   ├── figures/               # figures from isolationForest.ipynb
│   └── isolationForest.ipynb
└── README.md
```

## Data acquisition

### CICIDS2017 dataset

The dataset is provided by the Canadian Institute for Cybersecurity:

**https://www.unb.ca/cic/datasets/ids-2017.html**

If you use the dataset, cite: Iman Sharafaldin, Arash Habibi Lashkari and Ali A. Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization", 4th International Conference on Information Systems Security and Privacy (ICISSP), Portugal, January 2018.

Required:

- **PCAP files** for Tuesday through Friday → place in `data/pcap/`
- **Official flow CSV files** for Tuesday through Friday → place in `data/flow_csv/original/`
- **Official flow CSV file** for Monday → place in `data/ml_csv/` (filename: `Monday-WorkingHours.pcap_ISCX.csv`)

### Precomputed intermediate results (OneDrive)

All data preparation for this work (CICFlowMeter flow generation, timestamp alignment, Snort runs and residual construction) was carried out entirely by Gina Bilinski. The following prepared files are provided via OneDrive to reduce preprocessing effort:

**https://1drv.ms/f/c/69e7c6ee2f5c825b/IgD1bOr2AUfCTLETywey-4yMAYDsCO4eXvFiE0Pcto1TNIA?e=0voYX1**

Included:

- CICFlowMeter-generated CSV files (`data/flow_csv/with_seconds/`)
- Prepared flow files with timestamps (`data/flow_csv/prepared/`)
- Snort alert file (`snort/logs/alert_csvTotal.txt`)
- Residual file (`snort/residuals/snort_residuals.csv`)

If these files are used from OneDrive, **steps 1, 2, and 3** of the pipeline can be skipped.

## Installation

### 1. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy scikit-learn matplotlib ipykernel jupyter
```

### 2. Install Snort 3

The installation follows the official Snort 3 documentation:

**https://docs.snort.org/welcome**

### 3. Download Talos LightSPD rules

After free registration at **https://www.snort.org/downloads**, download the LightSPD rules for Snort 3 and extract them into the Snort rules directory.

### 4. Configure Snort

In the configuration file `snort.lua`, make the following settings:

**Adjust network ranges:**

```lua
HOME_NET = '192.168.10.0/24'
EXTERNAL_NET = '!$HOME_NET'
```

**Enable PortScan inspector:**

```lua
port_scan = {
    protos      = 'all',
    scan_types  = 'all',
    alert_all   = true,
    ignore_scanners = '192.168.10.0/24',
}
```

**Set alert format:**

```lua
alert_csv =
{
    file = true,
    fields = 'timestamp proto src_addr src_port dst_addr dst_port rule msg'
}
```

All LightSPD rule files must be included in `snort.lua`. Then verify the configuration:

```bash
snort -c /usr/local/snort3/etc/snort/snort.lua -T
```

## Running the pipeline

The pipeline consists of five steps that must be executed in the specified order.

### Step 1: Generate CSV files with seconds (Windows/WSL2)

Since the official CICIDS2017 CSV files only contain minute-precise timestamps, new CSV files with second-precise timestamps are generated from the PCAP files using CICFlowMeter 4.0. CICFlowMeter is run under Windows with WSL2, once per PCAP file for Tuesday through Friday. Save each output as `data/flow_csv/with_seconds/<Day>-WorkingHours.pcap_withSek.csv`.

### Step 2: Merge timestamps

`data/timestampAddSekAndEnd.py` combines the official CSV files (with labels) with the CICFlowMeter files (with seconds) and calculates end timestamps from the flow duration. The file paths at the beginning of the script must be adjusted for each day. Where the official dataset provides several CSV files for one day (e.g. Thursday, Friday), concatenate them into one file per day first (e.g. `Friday-WorkingHours_Gesamt.csv`):

```bash
python data/timestampAddSekAndEnd.py
```

Then merge all four daily files into the combined file expected by `snort/matchingSnort.ipynb`:

```python
import pandas as pd
from pathlib import Path

prepared = Path("data/flow_csv/prepared")
days = ["Tuesday", "Wednesday", "Thursday", "Friday"]
merged = pd.concat(
    [pd.read_csv(prepared / f"{day}-WorkingHours_matchingNEU.csv", low_memory=False) for day in days],
    ignore_index=True,
)
merged.to_csv(prepared / "TueWedThuFri-WorkingHours_matching.csv", index=False)
```

### Step 3: Run Snort on the PCAP files

The following bash script runs Snort sequentially on all PCAP files and collects all alerts in a common file:

```bash
for pcap in data/pcap/*.pcap; do
    echo "Processing: $pcap"
    rm -f snort/logs/alert_csv.txt
    snort -q \
      -c /usr/local/snort3/etc/snort/snort.lua \
      -r "$pcap" \
      -A alert_csv \
      -l snort/logs
    cat snort/logs/alert_csv.txt >> snort/logs/alert_csvTotal.txt
done
```

### Step 4: Alert-flow matching and residual creation

Open `snort/matchingSnort.ipynb` in Jupyter or VSCode and run all cells in order. The notebook loads flows and Snort alerts, performs bidirectional 5-tuple matching with time-window checking, and saves the results.

**Output:**

- `snort/residuals/snort_residuals.csv` – all flows without a unique Snort alert
- `snort/residuals/snort_metrics.json` – TP, FP, FN, TN of the first detection stage
- `snort/figures/` – confusion matrix and detection overview

### Step 5: Train and evaluate Isolation Forest

Open `iForest/isolationForest.ipynb` in Jupyter or VSCode and run all cells in order. The notebook performs stability-based feature selection, trains the Isolation Forest on Monday traffic, calibrates the threshold at the 99th percentile, and applies the model to the Snort residuals.

**Output:**

- Confusion matrix, precision, recall, F1 score, PR-AUC
- Pipeline metrics: CDR, ΔRecall, ΔFPR, hybrid recall, hybrid FPR
- `iForest/figures/` – all figures

## Related Work

The same principle, designing and evaluating a security pipeline stage by stage rather than only end to end, is applied to entity resolution for cyber threat intelligence in:

* **Haßlinger, T., Lu, T. and Zöller, T. (2026).** *The Signal in the Noise: Semantic Entity Resolution for Cyber Threat Intelligence with Relational Context.* AINOW 2026, Lisbon. Code: [Prof-it/cti-entity-resolution](https://github.com/Prof-it/cti-entity-resolution)

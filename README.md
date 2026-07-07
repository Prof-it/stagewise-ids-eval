# Hybrid IDS – Snort + Isolation Forest

This repository contains the complete code for the bachelor's thesis _"Evaluation des Zusatznutzens unüberwachter Anomalieerkennung in hybriden Intrusion-Detection-Systemen"_.

The implemented pipeline combines Snort as a signature-based first detection stage with an Isolation Forest as an unsupervised second detection stage on the CICIDS2017 dataset.

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
AnomalyDetection-StageWiseEvaluation-IsoForest-RuleBased/
├── data/
│   ├── timestampAddSekAndEnd.py
│   ├── flow_csv/
│   │   ├── original/          # official CICIDS2017 CSV files (Tue–Fri)
│   │   ├── with_seconds/      # CICFlowMeter-generated CSV files with seconds
│   │   └── prepared/          # prepared files with timestamps (output of timestampAddSekAndEnd.py)
│   ├── pcap/                  # CICIDS2017 PCAP files (Tue–Fri)
│   └── ml_csv/                # Monday-WorkingHours.pcap_ISCX.csv (for IF training)
├── snort/
│   ├── logs/                  # alert_csvGesamt.txt (Snort output)
│   ├── residuals/             # snort_residuen.csv, snort_metriken.json
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

Required:

- **PCAP files** for Tuesday through Friday → place in `data/pcap/`
- **Official flow CSV files** for Tuesday through Friday → place in `data/flow_csv/original/`
- **Official flow CSV file** for Monday → place in `data/ml_csv/` (filename: `Monday-WorkingHours.pcap_ISCX.csv`)

### Precomputed intermediate results (OneDrive)

The following prepared files are provided via OneDrive to reduce preprocessing effort:

**https://1drv.ms/f/c/69e7c6ee2f5c825b/IgD1bOr2AUfCTLETywey-4yMAYDsCO4eXvFiE0Pcto1TNIA?e=0voYX1**

Included:

- CICFlowMeter-generated CSV files (`data/flow_csv/with_seconds/`)
- Prepared flow files with timestamps (`data/flow_csv/prepared/`)
- Snort alert file (`snort/logs/alert_csvGesamt.txt`)
- Residual file (`snort/residuals/snort_residuen.csv`)

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

Since the official CICIDS2017 CSV files only contain minute-precise timestamps, new CSV files with second-precise timestamps are generated from the PCAP files using CICFlowMeter 4.0. CICFlowMeter is run under Windows with WSL2 – one per PCAP file for Tuesday through Friday:

### Step 2: Merge timestamps

`data/timestampAddSekAndEnd.py` combines the official CSV files (with labels) with the CICFlowMeter files (with seconds) and calculates end timestamps from the flow duration. The file paths at the beginning of the script must be adjusted for each day:

```bash
python data/timestampAddSekAndEnd.py
```

Then merge all four daily files into one combined file:

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
    cat snort/logs/alert_csv.txt >> snort/logs/alert_csvGesamt.txt
done
```

### Step 4: Alert-flow matching and residual creation

Open `snort/matchingSnort.ipynb` in Jupyter or VSCode and run all cells in order. The notebook loads flows and Snort alerts, performs bidirectional 5-tuple matching with time-window checking, and saves the results.

**Output:**

- `snort/residuals/snort_residuen.csv` – all flows without a unique Snort alert
- `snort/residuals/snort_metriken.json` – TP, FP, FN, TN of the first detection stage
- `snort/figures/` – confusion matrix and detection overview

### Step 5: Train and evaluate Isolation Forest

Open `iForest/isolationForest.ipynb` in Jupyter or VSCode and run all cells in order. The notebook performs stability-based feature selection, trains the Isolation Forest on Monday traffic, calibrates the threshold at the 99th percentile, and applies the model to the Snort residuals.

**Output:**

- Confusion matrix, precision, recall, F1 score, PR-AUC
- Pipeline metrics: CDR, ΔRecall, ΔFPR, hybrid recall, hybrid FPR
- `iForest/figures/` – all figures

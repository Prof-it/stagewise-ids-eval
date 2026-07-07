import pandas as pd
from pathlib import Path

# File paths (adjust daily)
folder = Path("data/flow_csv")
file_original = folder / "original" / "Friday-WorkingHours_Gesamt.csv"
file_seconds = folder / "with_seconds" / "Friday-WorkingHours.pcap_withSek.csv"
file_new = folder / "prepared" / "Friday-WorkingHours_matchingNEU.csv"

# Load CSVs
original = pd.read_csv(file_original, low_memory=False, encoding="cp1252")
seconds = pd.read_csv(file_seconds, low_memory=False)
original.columns = original.columns.str.strip()
seconds.columns = seconds.columns.str.strip()
official = original.copy()

# Adjust column names of the seconds CSV
seconds = seconds.rename(columns={
    "Src IP": "Source IP",
    "Src Port": "Source Port",
    "Dst IP": "Destination IP",
    "Dst Port": "Destination Port",
    "Tot Fwd Pkts": "Total Fwd Packets",
    "Tot Bwd Pkts": "Total Backward Packets",
    "TotLen Fwd Pkts": "Total Length of Fwd Packets",
    "TotLen Bwd Pkts": "Total Length of Bwd Packets"
})

official["_id"] = official.index
seconds["_sec_id"] = seconds.index
official["Label"] = official["Label"].astype(str).str.strip()

# Correct timestamps -> official CSV is minute-precision without AM/PM
official["Timestamp"] = pd.to_datetime(official["Timestamp"], format="%d/%m/%Y %H:%M", errors="raise")
afternoon = official["Timestamp"].dt.hour.isin([1, 2, 3, 4, 5])
# 01:xx-05:xx correspond to 13:xx-17:xx
official.loc[afternoon, "Timestamp"] = official.loc[afternoon, "Timestamp"] + pd.Timedelta(hours=12)

# Timestamps of the seconds CSV -> with AM/PM, verified offset of -5h
seconds["Timestamp"] = pd.to_datetime(seconds["Timestamp"], format="%d/%m/%Y %I:%M:%S %p", errors="raise")
seconds["Timestamp"] = seconds["Timestamp"] - pd.Timedelta(hours=5)

# Matching on a minute basis -> official CSV has no seconds
official["Matching Minute"] = official["Timestamp"].dt.floor("min")
seconds["Matching Minute"] = seconds["Timestamp"].dt.floor("min")

# Unify matching columns numerically
numeric_columns = [
    "Source Port", "Destination Port", "Protocol", "Flow Duration",
    "Total Fwd Packets", "Total Backward Packets",
    "Total Length of Fwd Packets", "Total Length of Bwd Packets"
]
official[numeric_columns] = official[numeric_columns].apply(pd.to_numeric, errors="raise")
seconds[numeric_columns] = seconds[numeric_columns].apply(pd.to_numeric, errors="raise")

# Join only unique keys of both files
def find_matches(orig, sec, columns, method):
    orig_unique = orig[~orig.duplicated(subset=columns, keep=False)]
    sec_unique = sec[~sec.duplicated(subset=columns, keep=False)]
    return (
        orig_unique[["_id", "Label"] + columns]
        .merge(sec_unique[["_sec_id", "Timestamp"] + columns], on=columns, how="inner", validate="one_to_one")
        .rename(columns={"Timestamp": "Timestamp new"})
        .assign(Method=method)
    )

base_columns = ["Matching Minute", "Source IP", "Source Port", "Destination IP", "Destination Port", "Protocol", "Flow Duration"]
packet_columns = base_columns + ["Total Fwd Packets", "Total Backward Packets"]
byte_columns = packet_columns + ["Total Length of Fwd Packets", "Total Length of Bwd Packets"]

matching_stages = [
    ("Base", base_columns),
    ("Additionally packet counts", packet_columns),
    ("Additionally byte counts", byte_columns)
]

open_original_rows = official.copy()
open_second_rows = seconds.copy()
all_matches = []

print("\nChecking staged matching")
for method, columns in matching_stages:
    matches = find_matches(open_original_rows, open_second_rows, columns, method)
    all_matches.append(matches)
    open_original_rows = open_original_rows[~open_original_rows["_id"].isin(matches["_id"])].copy()
    open_second_rows = open_second_rows[~open_second_rows["_sec_id"].isin(matches["_sec_id"])].copy()
    print(f"{method}: {len(matches)} new unique matches")

matches = pd.concat(all_matches, ignore_index=True)

# Build result from the official CSV with second-precise timestamps
timestamp_mapping = matches.set_index("_id")["Timestamp new"]
unique_ids = sorted(timestamp_mapping.index)
result = original.loc[unique_ids].copy()
result.columns = result.columns.str.strip()
result["Timestamp"] = pd.to_datetime(timestamp_mapping.reindex(unique_ids).to_numpy(), errors="raise")

# Timestamp End from start + Flow Duration (microseconds)
result["Flow Duration"] = pd.to_numeric(result["Flow Duration"], errors="raise")
timestamp_end = result["Timestamp"] + pd.to_timedelta(result["Flow Duration"], unit="us")
result.insert(result.columns.get_loc("Flow Duration") + 1, "Timestamp End", timestamp_end)

# Save in unambiguous 24h format with microseconds
for col in ["Timestamp", "Timestamp End"]:
    result[col] = result[col].dt.strftime("%Y-%m-%d %H:%M:%S.%f")
result.to_csv(file_new, index=False)

# Result summary
print("\nResult")
print(f"Official rows:    {len(original)}")
print(f"Seconds rows:      {len(seconds)}")
print(f"Adopted:           {len(result)}")
print(f"Not adopted:       {len(open_original_rows)}")

if len(open_original_rows) > 0:
    print("\nFlows not adopted:")
    print(open_original_rows["Label"].value_counts().to_string())

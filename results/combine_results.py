import pandas as pd

results_files = ["pilot_11_Feb_21/all_results.jsonl", "second_launch-15_Feb_21/all_results.jsonl"]
df = pd.concat([pd.read_json(f, orient="records", lines=True) for f in results_files])
df.to_json("all_results_combined.jsonl", orient="records", lines=True)
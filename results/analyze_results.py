import pandas as pd

results = pd.read_json("pilot_11_Feb_21/all_results.jsonl", orient="records", lines=True)
print(results.to_string())
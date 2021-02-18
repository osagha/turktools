import pandas as pd

df = pd.read_json("all_results.jsonl", orient="records", lines=True)
df["repeat"] = False
df["include"] = df["passed"]
df.to_json("all_results.jsonl", orient="records", lines=True)
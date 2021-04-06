import pandas as pd
import os

results_dirs = ["pilot_11_Feb_21/round1",
                "pilot_11_Feb_21/redo",
                "pilot_11_Feb_21/redo2",
                "pilot_11_Feb_21/redo3",
                "pilot_11_Feb_21/redo4",
                 "second_launch-15_Feb_21/round1",
                 "second_launch-15_Feb_21/redo",
                 "second_launch-15_Feb_21/redo2",
                 "second_launch-15_Feb_21/redo3",
                ]

# Combine results
# df = pd.concat([pd.read_json(os.path.join(d, "all_results.jsonl"), orient="records", lines=True) for d in results_dirs])
# df.to_json("all_results_combined.jsonl", orient="records", lines=True)


# Combine workers
# df = pd.concat([pd.read_json(os.path.join(d, "secret", "workers.jsonl"), orient="records", lines=True) for d in results_dirs])
# df.to_json("secret/all_workers_combined.jsonl", orient="records", lines=True)


# Combine bonuses
df = pd.concat([pd.read_csv(os.path.join(d, "secret", "bonus.csv"), ) for d in results_dirs if d != "pilot_11_Feb_21/round1"])
df = df.sort_values(by="WorkerId")
# df = df[""]
df.to_csv("secret/bonuses_combined.csv")

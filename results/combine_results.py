import pandas as pd
import os

results_dirs = ["pilot_11_Feb_21/round1",
                "pilot_11_Feb_21/redo",
                "pilot_11_Feb_21/redo2",
                 "second_launch-15_Feb_21/round1",
                 "second_launch-15_Feb_21/redo",
                 "second_launch-15_Feb_21/redo2",
                ]


df = pd.concat([pd.read_json(os.path.join(d, "all_results.jsonl"), orient="records", lines=True) for d in results_dirs])
df.to_json("all_results_combined.jsonl", orient="records", lines=True)
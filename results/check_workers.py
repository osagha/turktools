import pandas as pd
from results.results_to_df import df_helpfulness, df_posterior, df_prior, df
import collections
from hashlib import sha256

# print(df.to_string())

# Check that workers did not do more than one HIT
workers = df.drop_duplicates(subset=["WorkerId", "Input.list"])[["WorkerId", "Input.list", "experiment", "AssignmentId"]]
repeat_worker_ids = [item for item, count in collections.Counter(workers["WorkerId"]).items() if count > 1]
previous_workers = list(set(pd.read_json("pilot_11_Feb_21/secret/workers.jsonl", orient="records", lines=True)["WorkerId"]))
barred_workers = repeat_worker_ids + previous_workers
workers["repeat"] = workers["WorkerId"].apply(lambda x: x in repeat_worker_ids)
# print(workers.to_string())
# print(workers[workers["WorkerId"].apply(lambda x: x in repeat_worker_ids)].to_string())




# Check worker attention
fillers_answer_key = pd.read_csv("../stimuli/fillers_answer_key.csv")
def check(r):
    if r["response"] <= r["max"] and r["response"] >= r["min"]:
        multiplier = 1
    # elif r["response"] <= r["max"]+.05 and r["response"] >= r["min"]-0.05:
    #     multiplier = 1
    else:
        multiplier = 0
    score = 3 if r["filler_type"] == "attention" else 2
    return score * multiplier

def check2(r):
    if r["response"] <= r["max"] and r["response"] >= r["min"]:
        multiplier = 1
    elif r["response"] <= r["max"]+.05 and r["response"] >= r["min"]-0.05:
        multiplier = 1
    else:
        multiplier = 0
    score = 3 if r["filler_type"] == "attention" else 2
    return score * multiplier

worker_statuses = []
for worker in workers["WorkerId"]:
    if worker == "A34DYM8J0X5VK":
        x=1
        pass
    worker_responses = df[(df["WorkerId"] == worker) & (df["condition"] == "filler")]
    worker_responses = worker_responses.merge(fillers_answer_key, on=["experiment", "item_number"])
    score = sum(worker_responses.apply(check, axis=1))
    score2 = sum(worker_responses.apply(check2, axis=1))
    experiment = worker_responses["experiment"][0]
    passed = score >= 10 #(experiment=="helpfulness" and score>=10) or (experiment=="prior" and score>=10) or (experiment=="posterior" and score>=8)
    worker_statuses.append({"WorkerId": worker, "passed": passed})
    # if score2 < 10:
    #     print(worker_responses.to_string())
    #     print(score, experiment)
    #     print("-" * 1000)

worker_statuses = pd.DataFrame(worker_statuses)
df = df.merge(worker_statuses, on="WorkerId")
workers = workers.merge(worker_statuses, on="WorkerId")

# Figure whose repsonses to include and who to bonus
workers["include"] = workers.apply(lambda x: x["passed"] and not x["repeat"], axis=1)
df = df.merge(workers[["include", "WorkerId"]], on="WorkerId")
bonus = workers[workers["include"]][["WorkerId", "AssignmentId"]].sort_values(by="WorkerId")
bonus.to_csv("second_launch-15_Feb_21/secret/bonus.csv")
# bonus = list(workers[workers["include"]][["WorkerId", "AssignmentId"]])
# bonus.sort()
# with open("second_launch-15_Feb_21/secret/bonus.txt", "w") as f:
#     f.write("\n".join(bonus))






# Anonymize workers
workers["anon_id"] = workers["WorkerId"].apply(lambda x: sha256(x.encode("utf-8")).hexdigest())
workers.to_json("second_launch-15_Feb_21/secret/workers.jsonl", orient="records", lines=True)

df = df.merge(workers[["WorkerId", "anon_id"]], on="WorkerId")
df = df.drop("WorkerId", axis="columns")
df.to_json("second_launch-15_Feb_21/all_results.jsonl", orient="records", lines=True)

pass


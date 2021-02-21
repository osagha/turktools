import pandas as pd
# from results.results_to_df import df_helpfulness, df_posterior, df_prior, df
import collections
import csv
from hashlib import sha256
import os
# print(df.to_string())

# Check that workers did not do more than one HIT
# results_dir = "pilot_11_Feb_21/redo2"
results_dir = "second_launch-15_Feb_21/redo2"
results_files = [x for x in os.listdir(os.path.join(results_dir, "secret")) if "bonus" not in x and "workers" not in x]
num_items = 15


# prior = os.path.join(results_dir, "secret", "prior.csv")
# posterior = os.path.join(results_dir, "secret", "posterior.csv")
# helpfulness = os.path.join(results_dir, "secret", "helpfulness.csv")


def LLO(p):
    if p == 0:
        return 0
    else:
        return 1 / (1 + ((-1 + 1 / p) ** 1.5))

def create_df(file, experiment):
    with open(file) as f:
        data = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]

    data_columns = ["WorkerId", "Input.list", "AssignmentId"]
    responses = []
    for worker in data:
        for i in range(1, num_items+1):
            item_dic = {
                "item_number": int(worker["Input.item_%d_number" % i]),
                "condition": worker["Input.item_%d_condition" % i],
                "response": float(worker["Answer.response%d" % i]) if experiment=="helpfulness" else LLO(float(worker["Answer.response%d" % i])),
                "slider_position": float(worker["Answer.response%d" % i]),
                "context": worker["Input.field_%d_1" % i],
                "answer": None if experiment=="prior" else worker["Input.field_%d_3" % i] if experiment=="posterior" else worker["Input.field_%d_5" % i],
            }
            for k in worker:
                if k in data_columns:
                    item_dic[k] = worker[k]
            responses.append(item_dic)
    df = pd.DataFrame(responses)
    return df


dfs = []
for f in results_files:
    experiment = "prior" if "prior" in f \
        else "posterior" if "posterior" in f \
        else "helpfulness"

    df = create_df(os.path.join(results_dir, "secret", f), experiment)
    if experiment == "prior":
        df["condition_context"] = df["condition"].apply(lambda x: x if x == "filler" else x[8:])
        df["condition_answer"] = float("nan")
    else:
        df["condition_context"] = df["condition"].apply(lambda x: x if x == "filler" else x.split()[0][8:])
        df["condition_answer"] = df["condition"].apply(lambda x: x if x == "filler" else x.split(" ")[1][7:])
    df["experiment"] = experiment
    dfs.append(df)

# df_posterior = create_df(posterior, "posterior")
# df_posterior["condition_context"] = df_posterior["condition"].apply(lambda x: x if x == "filler" else x.split()[0][8:])
# df_posterior["condition_answer"] = df_posterior["condition"].apply(lambda x: x if x == "filler" else x.split(" ")[1][7:])
# df_posterior["experiment"] = "posterior"
#
# df_helpfulness = create_df(helpfulness, "helpfulness")
# df_helpfulness["condition_context"] = df_helpfulness["condition"].apply(lambda x: x if x == "filler" else x.split()[0][8:])
# df_helpfulness["condition_answer"] = df_helpfulness["condition"].apply(lambda x: x if x == "filler" else x.split()[1][7:])
# df_helpfulness["experiment"] = "helpfulness"

df = pd.concat(dfs)

# print(df.to_string())


workers = df.drop_duplicates(subset=["WorkerId", "Input.list"])[["WorkerId", "Input.list", "experiment", "AssignmentId"]]
repeat_worker_ids = [item for item, count in collections.Counter(workers["WorkerId"]).items() if count > 1]
results_dirs = ["pilot_11_Feb_21/redo",
                "pilot_11_Feb_21/redo2",
                "pilot_11_Feb_21/round1",
                "second_launch-15_Feb_21/redo",
                "second_launch-15_Feb_21/redo2",
                "second_launch-15_Feb_21/round1",
                ]
previous_workers = [x for d in results_dirs if d != results_dirs for x in list(set(pd.read_json(os.path.join(d, "secret/workers.jsonl"), orient="records", lines=True)["WorkerId"]))]
print(previous_workers)
barred_workers = repeat_worker_ids + previous_workers
workers["repeat"] = workers["WorkerId"].apply(lambda x: x in repeat_worker_ids)
print(workers.to_string())




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
    # score2 = sum(worker_responses.apply(check2, axis=1))
    experiment = worker_responses["experiment"][0]
    passed = score >= 10 #(experiment=="helpfulness" and score>=10) or (experiment=="prior" and score>=10) or (experiment=="posterior" and score>=8)
    worker_statuses.append({"WorkerId": worker, "passed": passed})
    if score < 100:
        print(worker_responses.to_string())
        print(score, experiment)
        print("-" * 1000)

worker_statuses = pd.DataFrame(worker_statuses)
df = df.merge(worker_statuses, on="WorkerId")
workers = workers.merge(worker_statuses, on="WorkerId")

# Figure whose repsonses to include and who to bonus
workers["include"] = workers.apply(lambda x: x["passed"] and not x["repeat"], axis=1)
df = df.merge(workers[["include", "WorkerId"]], on="WorkerId")
bonus = workers[workers["include"]][["WorkerId", "AssignmentId"]].sort_values(by="WorkerId")
bonus.to_csv(os.path.join(results_dir, "secret", "bonus.csv"))
# bonus = list(workers[workers["include"]][["WorkerId", "AssignmentId"]])
# bonus.sort()
# with open("second_launch-15_Feb_21/secret/bonus.txt", "w") as f:
#     f.write("\n".join(bonus))






# Anonymize workers
workers["anon_id"] = workers["WorkerId"].apply(lambda x: sha256(x.encode("utf-8")).hexdigest())
workers.to_json(os.path.join(results_dir, "secret", "workers.jsonl"), orient="records", lines=True)

df = df.merge(workers[["WorkerId", "anon_id"]], on="WorkerId")
df = df.drop("WorkerId", axis="columns")
df.to_json(os.path.join(results_dir, "all_results.jsonl"), orient="records", lines=True)

pass


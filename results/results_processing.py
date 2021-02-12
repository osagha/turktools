import csv
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt



results_dir = "pilot_11_Feb_21"
prior = os.path.join(results_dir, "prior.csv")
posterior = os.path.join(results_dir, "posterior.csv")
helpfulness = os.path.join(results_dir, "helpfulness.csv")

def LLO(p):
    if p == 0:
        return 0
    else:
        return 1 / (1 + ((-1 + 1 / p) ** 1.5))

def create_df(file, experiment):
    with open(file) as f:
        data = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]

    data_columns = ["WorkerId", "Input.list"]
    responses = []
    for worker in data:
        for i in range(1,15):
            item_dic = {
                "item_number": worker["Input.item_%d_number" % i],
                "condition": worker["Input.item_%d_condition" % i],
                "response": LLO(float(worker["Answer.response%d" % i])),
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

df_prior = create_df(prior, "prior")
df_prior["condition_context"] = df_prior["condition"].apply(lambda x: x if x == "filler" else x[8:])
df_prior["condition_answer"] = float("nan")
df_prior["experiment"] = "prior"

df_posterior = create_df(posterior, "posterior")
df_posterior["condition_context"] = df_posterior["condition"].apply(lambda x: x if x == "filler" else x.split()[0][8:])
df_posterior["condition_answer"] = df_posterior["condition"].apply(lambda x: x if x == "filler" else x.split(" ")[1][7:])
df_posterior["experiment"] = "posterior"

df_helpfulness = create_df(helpfulness, "helpfulness")
df_helpfulness["condition_context"] = df_helpfulness["condition"].apply(lambda x: x if x == "filler" else x.split()[0][8:])
df_helpfulness["condition_answer"] = df_helpfulness["condition"].apply(lambda x: x if x == "filler" else x.split()[1][7:])
df_helpfulness["experiment"] = "helpfulness"

df = pd.concat([df_helpfulness, df_prior, df_posterior])
# print(df_helpfulness.to_string())


def passed_fillers(items):
    attention_score = 10
    for item in items:
        if item["condition"] != "filler":
            continue
        if item["item_number"] == "1":
            if item["response"] < 0.1 or item["response"] > 0.15:
                attention_score -= 3
        if item["item_number"] == "2":
            if item["response"] < 0.8 or item["response"] > 0.85:
                attention_score -= 3
        if item["item_number"] == "3":
            if item["response"] < 0.3 or item["response"] > 0.4:
                attention_score -= 2
        if item["item_number"] == "4":
            if item["response"] < 0.1 or item["response"] > 0.15:
                attention_score -= 2
    return attention_score == 10, attention_score


# filtered_responses = []
# for w in responses:
#     test1 = w["positive_bias_average"] > w["negative_bias_average"]
#     test2, attention_score = passed_fillers(w["items"])
#     test1_text = "passed" if test1 else "failed"
#     test2_text = "passed" if test2 else "failed"
#     print("%s\t %s test1\t%s test2\tattention score=%s\t%s" % (w["WorkerId"], test1_text, test2_text, attention_score, w["Input.list"]))
#     if test1 and test2:
#         filtered_responses.append(w)
#
# items = {}
# for w in responses:
#     _, attention_score = passed_fillers(w["items"])
#     if attention_score < 6:
#         continue
#     for i in w["items"]:
#         if i["condition"] == "filler":
#             continue
#         if (i["item_number"], i["condition"]) not in items:
#             items[(i["item_number"], i["condition"])] = {
#                 "responses": [],
#                 "context": i["context"],
#                 "prompt": i["prompt"]
#             }
#         items[(i["item_number"], i["condition"])]["responses"].append(i["response"])
#
# print("\t".join(["item number", "condition", "average", "length", "range", "standard deviation", "context", "prompt"]))
# for i in items:
#     length = len(items[i]["responses"])
#     average = np.mean(items[i]["responses"])
#     i_min = min(items[i]["responses"])
#     i_max = max(items[i]["responses"])
#     std = np.std(items[i]["responses"])
#     print("\t".join([i[0], i[1], str(average), str(length), str(i_max - i_min), str(std), items[i]["context"], items[i]["prompt"]]))



pass
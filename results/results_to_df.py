import csv
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt



results_dir = "pilot_11_Feb_21/secret/"
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
                "item_number": int(worker["Input.item_%d_number" % i]),
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

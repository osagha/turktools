import csv
import pandas as pd
import numpy as np

with open('prior_10_8.csv') as f:
    data = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

# df = pd.read_csv("prior_10_8.csv", header=0)

def LLO(p):
    return 1 / (1 + ((-1 + 1 / p) ** 1.5))

# for column in df:
#     if column.startswith("Answer.response"):
#         df[column] = df[column].apply(LLO)
#
data_columns = ["WorkerId", "Input.list",
                'Answer.response1', 'Answer.response10', 'Answer.response2',
                'Answer.response3', 'Answer.response4', 'Answer.response5',
                'Answer.response6', 'Answer.response7', 'Answer.response8', 'Answer.response9',
                'Input.item_1_condition', 'Input.item_2_condition','Input.item_3_condition',
                'Input.item_4_condition','Input.item_5_condition','Input.item_6_condition',
                'Input.item_7_condition','Input.item_8_condition','Input.item_9_condition','Input.item_10_condition',
                ]
#
# responses = df[data_columns]

responses = []
for worker in data:
    new = {}
    for k in worker:
        if k in data_columns:
            new[k] = worker[k]
    responses.append(new)

for worker in responses:
    for k in worker:
        if k.startswith("Answer.response"):
            worker[k] = LLO(float(worker[k]))

new_responses = []
for worker in responses:
    items = []
    for i in range(1, 11):
        condition = worker["Input.item_%d_condition" % i]
        response = worker["Answer.response%d" % i]
        items.append({"condition": condition, "response": response})
    new_responses.append({"WorkerId": worker["WorkerId"],
                          "Input.list": worker["Input.list"],
                          "Responses": items
                          })


responses = new_responses
print("\t".join(["WorkerId", "Input.list", "negative_bias_average", "low_bias_average", "positive_bias_average"]))
for worker in responses:
    low_bias_average = np.mean([r["response"] for r in worker["Responses"] if r["condition"] == "low-bias"])
    positive_bias_average = np.mean([r["response"] for r in worker["Responses"] if r["condition"] == "positive-bias"])
    negative_bias_average = np.mean([r["response"] for r in worker["Responses"] if r["condition"] == "negative-bias"])
    worker["low_bias_average"] = low_bias_average
    worker["positive_bias_average"] = positive_bias_average
    worker["negative_bias_average"] = negative_bias_average
    print("\t".join([worker["WorkerId"], worker["Input.list"], str(negative_bias_average), str(low_bias_average), str(positive_bias_average)]))

filtered_responses = []
for w in responses:
    if w["negative_bias_average"] < w["low_bias_average"] and w["low_bias_average"] < w["positive_bias_average"]:
        if w["positive_bias_average"] - w["negative_bias_average"] > 0.3:
            filtered_responses.append(w)
        else:
            print(w["WorkerId"] + " failed " + w["Input.list"])
    else:
        print(w["WorkerId"] + " failed " + w["Input.list"])


pass
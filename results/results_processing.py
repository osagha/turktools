import csv
import pandas as pd
import numpy as np

with open('prior_10_15.csv') as f:
    data = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

# df = pd.read_csv("prior_10_8.csv", header=0)

def LLO(p):
    if p == 0:
        return 0
    else:
        return 1 / (1 + ((-1 + 1 / p) ** 1.5))

# for column in df:
#     if column.startswith("Answer.response"):
#         df[column] = df[column].apply(LLO)
#
data_columns = ["WorkerId", "Input.list"]
item_columns = ["Answer.response%d", "Input.item_%d_condition"]
# data_columns.extend(["Answer.response%d" % i for i in range(1, 15)])
# data_columns.extend(["Input.item_%d_condition" % i for i in range(1, 15)])
#
# responses = df[data_columns]

responses = []
for worker in data:
    new = {}
    for k in worker:
        if k in data_columns:
            new[k] = worker[k]
        new["items"] = []
        for i in range(1,15):
            item_dic = {
                "item_number": worker["Input.item_%d_number" % i],
                "condition": worker["Input.item_%d_condition" % i],
                "response": LLO(float(worker["Answer.response%d" % i])),
                "context": worker["Input.field_%d_1" % i],
                "prompt": worker["Input.field_%d_2" % i],
            }
            new["items"].append(item_dic)
    responses.append(new)

# for worker in responses:
#     for k in worker:
#         if k.startswith("Answer.response"):
#             worker[k] = LLO(float(worker[k]))

# new_responses = []
# for worker in responses:
#     items = []
#     for i in range(1, 15):
#         condition = worker["Input.item_%d_condition" % i]
#         response = worker["Answer.response%d" % i]
#         items.append({"condition": condition, "response": response})
#     new_responses.append({"WorkerId": worker["WorkerId"],
#                           "Input.list": worker["Input.list"],
#                           "Responses": items
#                           })


# responses = new_responses
print("\t".join(["WorkerId", "Input.list", "negative_bias_average", "low_bias_average", "positive_bias_average"]))
for worker in responses:
    low_bias_average = np.mean([r["response"] for r in worker["items"] if r["condition"] == "low-bias"])
    positive_bias_average = np.mean([r["response"] for r in worker["items"] if r["condition"] == "positive-bias"])
    negative_bias_average = np.mean([r["response"] for r in worker["items"] if r["condition"] == "negative-bias"])
    worker["low_bias_average"] = low_bias_average
    worker["positive_bias_average"] = positive_bias_average
    worker["negative_bias_average"] = negative_bias_average
    print("\t".join([worker["WorkerId"], worker["Input.list"], str(negative_bias_average), str(low_bias_average), str(positive_bias_average)]))

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


filtered_responses = []
for w in responses:
    test1 = w["positive_bias_average"] > w["negative_bias_average"]
    test2, attention_score = passed_fillers(w["items"])
    test1_text = "passed" if test1 else "failed"
    test2_text = "passed" if test2 else "failed"
    print("%s\t %s test1\t%s test2\tattention score=%s\t%s" % (w["WorkerId"], test1_text, test2_text, attention_score, w["Input.list"]))
    if test1 and test2:
        filtered_responses.append(w)

items = {}
for w in responses:
    _, attention_score = passed_fillers(w["items"])
    if attention_score < 6:
        continue
    for i in w["items"]:
        if i["condition"] == "filler":
            continue
        if (i["item_number"], i["condition"]) not in items:
            items[(i["item_number"], i["condition"])] = {
                "responses": [],
                "context": i["context"],
                "prompt": i["prompt"]
            }
        items[(i["item_number"], i["condition"])]["responses"].append(i["response"])

print("\t".join(["item number", "condition", "average", "length", "range", "standard deviation", "context", "prompt"]))
for i in items:
    length = len(items[i]["responses"])
    average = np.mean(items[i]["responses"])
    i_min = min(items[i]["responses"])
    i_max = max(items[i]["responses"])
    std = np.std(items[i]["responses"])
    print("\t".join([i[0], i[1], str(average), str(length), str(i_max - i_min), str(std), items[i]["context"], items[i]["prompt"]]))



pass
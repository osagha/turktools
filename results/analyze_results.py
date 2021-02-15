import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import entropy
import numpy as np

results = pd.read_json("pilot_11_Feb_21/all_results.jsonl", orient="records", lines=True)
results = results[results["condition"] != "filler"]
results = results[results["passed"]]
items = results[results["experiment"] != "prior"].set_index(["item_number", "condition_answer", "condition", "condition_context", "experiment"])["response"].unstack()
prior = results[results["experiment"] == "prior"][["response", "item_number", "condition_context"]].set_index(["item_number", "condition_context"])
items = items.reset_index().merge(prior, on=["item_number", "condition_context"]).rename({"response":"prior"}, axis=1)
posterior_prior = items.set_index(['item_number', 'condition_answer', 'condition', 'condition_context', 'helpfulness'])
posterior_prior = posterior_prior.stack().reset_index().rename({"level_5":"judgment", 0:"response"}, axis=1)

# create df with metrics & write to csv
items = items[(~ np.isnan(items["helpfulness"])) &
              (~ np.isnan(items["prior"])) &
              (~ np.isnan(items["posterior"]))]

def kl(p, q):
    return entropy([p, 1-p], [q, 1-q])

def exp(x):
    return 1 - np.exp(-1 * x)

def entropy_reduction(p, q):
    return(entropy([p, 1-p]) - entropy([q, 1-q]))

items["kl"] = items.apply(lambda x: kl(x["prior"], x["posterior"]), axis=1)
items["kl_exp"] = items.apply(lambda x: exp(kl(x["prior"], x["posterior"])), axis=1)
items["entropy_reduction"] = items.apply(lambda x: entropy_reduction(x["prior"], x["posterior"]), axis=1)
items = items.merge(results[results["experiment"]=="helpfulness"], on=["condition", "item_number"])
items.to_csv("pilot_11_Feb_21/analyzed_results.csv")



# Trellis of lineplots by item number
# sns.relplot(data=posterior_prior[["judgment", "response", "condition", "item_number", "helpfulness"]],
#             x="judgment", y="response",
#             hue="helpfulness",
#             kind="line", col="item_number", col_wrap=5, ci=None)


# Aggregate lineplot
# sns.lineplot(data=posterior_prior[["judgment", "response", "condition", "item_number", "helpfulness"]],
#             x="judgment", y="response",
#             hue="helpfulness", ci=None)


# Plot KL vs helpfulness
# ax = plt.gca()
# ax.set_xlim(-0.05, 1.05)
# sns.regplot(data=items, x="kl_exp", y="helpfulness")


# Plot entropy reduction vs helpfulness
# sns.regplot(data=items, x="entropy_reduction", y="helpfulness")


plt.show()



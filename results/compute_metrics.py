import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import entropy
from scipy.stats import spearmanr
import numpy as np

results = pd.read_json("all_results_combined.jsonl", orient="records", lines=True)
results = results[results["condition"] != "filler"]
results = results[results["include"]]
items = pd.pivot_table(results, values="response", index=["item_number", "condition_answer", "condition", "condition_context", "experiment"], aggfunc=list).unstack()
items.columns = items.columns.droplevel()
prior = pd.pivot_table(results[results["experiment"] == "prior"], index=["item_number", "condition_context"], values="response", aggfunc=list)
items = items.reset_index().merge(prior, on=["item_number", "condition_context"]).rename({"response":"prior"}, axis=1)
# posterior_prior = items.set_index(['item_number', 'condition_answer', 'condition', 'condition_context', 'helpfulness'])
# posterior_prior = posterior_prior.stack().reset_index().rename({"level_5":"judgment", 0:"response"}, axis=1)

# create df with metrics & write to csv

def range(l):
    return max(l) - min(l)

items = items[items.apply(lambda x: len(x["helpfulness"]) > 0 and
                                    len(x["prior"]) > 0 and
                                    len(x["posterior"]) > 0, axis=1)]

for exp in ["helpfulness", "posterior", "prior"]:
    items[exp + "_mean"] = items[exp].apply(np.mean)
    items[exp + "_stdev"] = items[exp].apply(np.std)
    items[exp + "_range"] = items[exp].apply(lambda l: max(l) - min(l))



# # Filter aggressively
# items = items[items.apply(lambda x: x["helpfulness_stdev"] < 0.3 and
#                                     x["prior_stdev"] < 0.3 and
#                                     x["posterior_stdev"] < 0.3, axis=1)]
#
# items = items[(items["condition_context"] == "negative-bias") | (items["condition_context"] == "low-bias")]









def kl(p, q):
    return entropy([p, 1-p], [q, 1-q])

def exp(x):
    return 1 - (10 ** (-1 * x))

def entropy_reduction(p, q):
    return(entropy([p, 1-p]) - entropy([q, 1-q]))

items["kl"] = items.apply(lambda x: kl(x["prior_mean"], x["posterior_mean"]), axis=1)
items["kl_exp"] = items.apply(lambda x: exp(kl(x["prior_mean"], x["posterior_mean"])), axis=1)
items["entropy_reduction"] = items.apply(lambda x: entropy_reduction(x["prior_mean"], x["posterior_mean"]), axis=1)
items = items.merge(results[results["experiment"]=="helpfulness"][["condition", "item_number", "answer", "context"]], on=["condition", "item_number"])
items = items.drop_duplicates(subset=["condition", "item_number"])
items.to_csv("analyzed_results_combined.csv")
items.to_json("analyzed_results_combined.jsonl", orient="records", lines=True)
# print(items.to_string())
#
# print(spearmanr(items["kl"], items["helpfulness_mean"]))
# print(spearmanr(items["kl_exp"], items["helpfulness_mean"]))
# print(spearmanr(items["entropy_reduction"], items["helpfulness_mean"]))


# # Trellis of lineplots by item number
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
# # ax.set_xlim(-0.05, 4)
# # sns.regplot(data=items, x="kl_exp", y="helpfulness", scatter_kws={'alpha':0.2})
# sns.scatterplot(data=items, x="kl_exp", y="helpfulness_mean", alpha=0.2)
#
#
# # Plot entropy reduction vs helpfulness
# # sns.regplot(data=items, x="entropy_reduction", y="helpfulness")
#
#
# plt.show()



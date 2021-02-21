import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import entropy
from scipy.stats import spearmanr
import numpy as np

results = pd.read_json("all_results_combined.jsonl", orient="records", lines=True)
results = results[results["condition"] != "filler"]
results = results[results["include"]]
items = pd.pivot_table(results, values="response", index=["item_number", "condition_answer", "condition", "condition_context", "experiment"]).unstack()
items.columns = items.columns.droplevel()
prior = pd.pivot_table(results[results["experiment"] == "prior"], index=["item_number", "condition_context"], values="response", aggfunc=np.mean)
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
    return 1 - (10 ** (-1 * x))

def entropy_reduction(p, q):
    return(entropy([p, 1-p]) - entropy([q, 1-q]))

items["kl"] = items.apply(lambda x: kl(x["prior"], x["posterior"]), axis=1)
items["kl_exp"] = items.apply(lambda x: exp(kl(x["prior"], x["posterior"])), axis=1)
items["entropy_reduction"] = items.apply(lambda x: entropy_reduction(x["prior"], x["posterior"]), axis=1)
items = items.merge(results[results["experiment"]=="helpfulness"], on=["condition", "item_number"])
items.to_csv("analyzed_results_combined.csv")


print(spearmanr(items["kl"], items["helpfulness"]))
print(spearmanr(items["kl_exp"], items["helpfulness"]))
print(spearmanr(items["entropy_reduction"], items["helpfulness"]))


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
ax = plt.gca()
# ax.set_xlim(-0.05, 4)
# sns.regplot(data=items, x="kl_exp", y="helpfulness", scatter_kws={'alpha':0.2})
sns.scatterplot(data=items, x="entropy_reduction", y="helpfulness", alpha=0.2)


# Plot entropy reduction vs helpfulness
# sns.regplot(data=items, x="entropy_reduction", y="helpfulness")


plt.show()



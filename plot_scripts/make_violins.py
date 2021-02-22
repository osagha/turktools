import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

results = pd.read_json("../results/analyzed_results_combined.jsonl", orient="records", lines=True)





# Make trellises of violin plots by condition for every measurement / metric
# for name in ["helpfulness", "prior", "posterior", "kl_exp", "entropy_reduction"]:
#     y_name = name if name == "kl_exp" or name == "entropy_reduction" else f"{name}_mean"
#     g = sns.catplot(data=results,
#                     x="condition_answer", y=y_name,
#                     col="condition_context",
#                     kind="violin",
#                     cut=0, scale="width", col_order=["negative-bias", "low-bias", "positive-bias"])
#     g.set_xticklabels(rotation=30, ha="right")
#     g.set_ylabels(name)
#     g.set_xlabels("Answer")
#     g.fig.suptitle(f"{name} by Answer/Context Condition")
#     g.fig.tight_layout()
#     plt.savefig(f"../figures/violins/{name}_by_condition.png")
#     plt.savefig(f"../figures/violins/{name}_by_condition.pdf")





# All relevance metrics
r = results[["condition_answer", "condition_context", "item_number",
             "entropy_reduction", "kl_exp",
             "posterior_mean", "prior_mean", "helpfulness_mean",
             "posterior_stdev", "prior_stdev", "helpfulness_stdev"]]
r = r.melt(id_vars=["condition_answer", "condition_context", "item_number"], value_vars=["helpfulness_mean", "kl_exp", "entropy_reduction"])


name = "All Relevance Metrics"
g = sns.catplot(data=r,
                x="variable", y="value",
                row="condition_context", col="condition_answer",
                kind="violin",
                cut=0, scale="width", row_order=["negative-bias", "low-bias", "positive-bias"])
g.set_xticklabels(rotation=30, ha="right")
g.set_ylabels(name)
g.set_xlabels("Answer")
g.fig.suptitle(f"{name} by Answer/Context Condition")
g.fig.tight_layout()
g.add_legend()
name = "_".join(name.split())
plt.savefig(f"../figures/violins/{name}_by_condition.png")
plt.savefig(f"../figures/violins/{name}_by_condition.pdf")


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

results = pd.read_json("../results/analyzed_results_combined.jsonl", orient="records", lines=True)





# Make trellises of violin plots by condition for every measurement / metric
# for name in ["helpfulness", "prior", "posterior", "kl_exp", "entropy_reduction"]:
#     y_name = name if name == "kl_exp" or name == "entropy_reduction" else f"{name}_mean"
#     x_name, col_name = ("condition_context", None) if name == "prior" else ("condition_answer", "condition_context")
#     if name == "kl_exp" or name == "entropy_reduction":
#         plot_data = results[results.apply(lambda x: x["helpfulness_range"] < 0.75 and
#                                                     x["prior_range"] < 0.75 and
#                                                     x["posterior_range"] < 0.75, axis=1)]
#     else:
#         plot_data = results
#     g = sns.catplot(data=plot_data,
#                     x=x_name, y=y_name, col=col_name,
#                     kind="violin",
#                     cut=0, scale="width", col_order=["negative-bias", "low-bias", "positive-bias"])
#     g.set_xticklabels(rotation=30, ha="right")
#     g.set_ylabels(name)
#     g.set_xlabels("Answer")
#     g.fig.suptitle(f"{name} by Answer/Context Condition")
#     g.fig.tight_layout()
#     filtered = "_filtered_by_range" if name == "kl_exp" or name == "entropy_reduction" else ""
#     plt.savefig(f"../figures/violins/{name}_by_condition{filtered}.png")
#     plt.savefig(f"../figures/violins/{name}_by_condition{filtered}.pdf")







r = results[["condition_answer", "condition_context", "item_number",
             "entropy_reduction", "kl_exp",
             "posterior_mean", "prior_mean", "helpfulness_mean",
             "posterior_range", "prior_range", "helpfulness_range",
             "posterior_stdev", "prior_stdev", "helpfulness_stdev"]]

# All relevance metrics
# r = r.melt(id_vars=["condition_answer", "condition_context", "item_number"], value_vars=["helpfulness_mean", "kl_exp", "entropy_reduction"])
#
#
# name = "All Relevance Metrics"
# g = sns.catplot(data=r,
#                 x="variable", y="value",
#                 row="condition_context", col="condition_answer",
#                 kind="violin",
#                 cut=0, scale="width", row_order=["negative-bias", "low-bias", "positive-bias"])
# g.set_xticklabels(rotation=30, ha="right")
# g.set_ylabels(name)
# g.set_xlabels("Answer")
# g.fig.suptitle(f"{name} by Answer/Context Condition")
# g.fig.tight_layout()
# g.add_legend()
# name = "_".join(name.split())
# plt.savefig(f"../figures/violins/{name}_by_condition.png")
# plt.savefig(f"../figures/violins/{name}_by_condition.pdf")




# # Agreement metrics: Range
# r = r.melt(id_vars=["condition_answer", "condition_context", "item_number"], value_vars=["helpfulness_range", "prior_range", "posterior_range"])
# name = "Response Range"
# g = sns.catplot(data=r,
#                 x="variable", y="value",
#                 row="condition_context", col="condition_answer",
#                 kind="violin",
#                 cut=0, scale="width", row_order=["negative-bias", "low-bias", "positive-bias"])
# g.set_xticklabels(rotation=30, ha="right")
# g.set_ylabels(name)
# g.set_xlabels("Answer")
# g.fig.suptitle(f"{name} by Answer/Context Condition")
# g.fig.tight_layout()
# g.add_legend()
# name = "_".join(name.split())
# plt.savefig(f"../figures/violins/{name}_by_condition.png")
# plt.savefig(f"../figures/violins/{name}_by_condition.pdf")



# # Agreement metrics: stdev
# r = r.melt(id_vars=["condition_answer", "condition_context", "item_number"], value_vars=["helpfulness_stdev", "prior_stdev", "posterior_stdev"])
# name = "Response stdev"
# g = sns.catplot(data=r,
#                 x="variable", y="value",
#                 row="condition_context", col="condition_answer",
#                 kind="violin",
#                 cut=0, scale="width", row_order=["negative-bias", "low-bias", "positive-bias"])
# g.set_xticklabels(rotation=30, ha="right")
# g.set_ylabels(name)
# g.set_xlabels("Answer")
# g.fig.suptitle(f"{name} by Answer/Context Condition")
# g.fig.tight_layout()
# g.add_legend()
# name = "_".join(name.split())
# plt.savefig(f"../figures/violins/{name}_by_condition.png")
# plt.savefig(f"../figures/violins/{name}_by_condition.pdf")


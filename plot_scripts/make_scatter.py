import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
import numpy as np

results = pd.read_json("../results/analyzed_results_combined.jsonl", orient="records", lines=True)
#
# # Plot KL vs helpfulness
# sns.scatterplot(data=results, x="kl_exp", y="helpfulness_mean", alpha=0.7, hue="prior_mean", s=80)
# plt.savefig("../figures/scatter/klexp_vs_helpfulness_color.png")
# plt.savefig("../figures/scatter/klexp_vs_helpfulness_color.pdf")
#
# # Plot ER vs helpfulness
# sns.scatterplot(data=results, x="entropy_reduction", y="helpfulness_mean", alpha=0.7, hue="prior_mean", s=80)
# plt.savefig("../figures/scatter/ER_vs_helpfulness_color.png")
# plt.savefig("../figures/scatter/ER_vs_helpfulness_color.pdf")

def annotate(data, **kws):
    r = spearmanr(data["x"], data["y"])
    ax = plt.gca()
    ax.text(.8, .1, f"ρ={r[0]}"[:6], transform=ax.transAxes, fontsize=20)
#
# name = "KL_exp"
# g = sns.relplot(data=results, col="condition_context", x="kl_exp", y="helpfulness_mean", alpha=0.7, s=80, col_order=["negative-bias", "low-bias", "positive-bias"])
# g.fig.suptitle(f"{name} by Answer/Context Condition")
# g.fig.tight_layout()
# g.map_dataframe(annotate)
# plt.savefig(f"../figures/scatter/{name}_vs_helpfulness_by_context.png")
# plt.savefig(f"../figures/scatter/{name}_vs_helpfulness_by_context.pdf")
#
# name = "ER"
# g = sns.relplot(data=results, col="condition_context", x="entropy_reduction", y="helpfulness_mean", alpha=0.7, s=80, col_order=["negative-bias", "low-bias", "positive-bias"])
# g.fig.suptitle(f"{name} by Answer/Context Condition")
# g.fig.tight_layout()
# g.map_dataframe(annotate)
# plt.savefig(f"../figures/scatter/{name}_vs_helpfulness_by_context.png")
# plt.savefig(f"../figures/scatter/{name}_vs_helpfulness_by_context.pdf")





# Filtered Results

# # Filter by stdev
# results = results[results.apply(lambda x: x["helpfulness_stdev"] < 0.3 and
#                                     x["prior_stdev"] < 0.3 and
#

results = results[results.apply(lambda x: x["helpfulness_range"] < 0.75 and
                                    x["prior_range"] < 0.75 and
                                    x["posterior_range"] < 0.75, axis=1)]



name = "KL_exp"
g = sns.relplot(data=results, col="condition_context", x="kl_exp", y="helpfulness_mean",
                alpha=0.7, s=80, col_order=["negative-bias", "low-bias", "positive-bias"])
g.fig.suptitle(f"{name} by Answer/Context Condition")
g.fig.tight_layout()
g.map_dataframe(annotate)
plt.savefig(f"../figures/scatter/{name}_vs_helpfulness_by_context_filtered_by_range.png")
plt.savefig(f"../figures/scatter/{name}_vs_helpfulness_by_context_filtered_by_range.pdf")

name = "ER"
g = sns.relplot(data=results, col="condition_context", x="entropy_reduction", y="helpfulness_mean",
                alpha=0.7, s=80, col_order=["negative-bias", "low-bias", "positive-bias"])
g.fig.suptitle(f"{name} by Answer/Context Condition")
g.fig.tight_layout()
g.map_dataframe(annotate)
plt.savefig(f"../figures/scatter/{name}_vs_helpfulness_by_context_filtered_by_range.png")
plt.savefig(f"../figures/scatter/{name}_vs_helpfulness_by_context_filtered_by_range.pdf")
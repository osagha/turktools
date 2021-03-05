import pandas as pd
from scipy.stats import entropy
import seaborn as sns
import numpy as np
# from results.compute_metrics import kl, exp, entropy_reduction
import matplotlib.pyplot as plt



def kl(p, q):
    return entropy([p, 1-p], [q, 1-q])

def kl_exp(p, q):
    return 1 - (10 ** (-1 * kl(p, q)))

def entropy_reduction(p, q):
    return(entropy([p, 1-p]) - entropy([q, 1-q]))

def cross_entropy(p, q):
    return kl(p, q) + entropy([p, 1-p])


n = 100
priors = np.arange(0, 1+1/n, 1/n)
posteriors = np.arange(0, 1+1/n, 1/n)
array = np.zeros((n+1, n+1))

for metric in ["KL", "KL_exp", "Entropy Reduction", "Cross Entropy"]:
    f = kl if metric == "KL" else kl_exp if metric == "KL_exp" else entropy_reduction if metric == "Entropy Reduction" else cross_entropy
    for i, q in enumerate(priors):
        for j, p in enumerate(posteriors):
            array[i][j] = f(p, q)

    df = pd.DataFrame(array, index=priors, columns=posteriors)
    min = -0.5 if metric=="Entropy Reduction" else 0
    # max = 0.5 if metric=="Entropy Reduction" else 1 if metric=="KL_exp" else 1.2
    max = {"Entropy Reduction": 0.5, "KL_exp": 1, "KL": 1.2, "Cross Entropy": 2}[metric]
    cmap = "icefire" if metric == "Entropy Reduction" else "rocket"
    g = sns.heatmap(df, vmin=min, vmax=max, xticklabels=20, yticklabels=20, cmap=cmap, square=True, cbar_kws={'label': metric})
    g.invert_yaxis()
    g.set_xlabel("Prior P(yes|context)")
    g.set_ylabel("Posterior P(yes|response, context)")
    plt.savefig(f"../figures/heatmaps/{metric}.pdf")
    plt.savefig(f"../figures/heatmaps/{metric}.png")
    plt.close()

import pandas as pd
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit




results = pd.read_json("../results/analyzed_results_combined.jsonl", orient="records", lines=True)


results = results[results.apply(lambda x: x["helpfulness_range"] < 0.75 and
                                    x["prior_range"] < 0.75 and
                                    x["posterior_range"] < 0.75, axis=1)]

# def quadratic(x, x0, y0, a, b, c):
#     return a*(x[0]-x0)**2 + b*(x[1]-y0)**2 + c*x[0]*x[1]
#
# xs = np.array(results[["prior_mean", "posterior_mean"]]).transpose()
# ys = np.array(results["helpfulness_mean"])
#
# p0 = [0.5, 0.5, 1, 1, 0]
# bounds = ([0.3, 0.3, -np.inf, -np.inf, -np.inf], [0.7, 0.7, np.inf, np.inf, np.inf])
# popt, pcov = curve_fit(quadratic, xs, ys, p0, bounds=bounds, method='trf', maxfev=2000)
# print(popt)
#
# n = 100
# priors = np.arange(0, 1+1/n, 1/n)
# posteriors = np.arange(0, 1+1/n, 1/n)
# array = np.zeros((n+1, n+1))
#
# for i, q in enumerate(priors):
#     for j, p in enumerate(posteriors):
#         array[i][j] = quadratic((p, q), popt[0], popt[1], popt[2], popt[3], popt[4])
#
# # print(array)
#
# df = pd.DataFrame(array, index=priors, columns=posteriors)
# min = 0
# max = 1
#
# # max = {"Entropy Reduction": 0.5, "KL_exp": 1, "KL": 1.2, "Cross Entropy": 2}[metric]
# cmap = "rocket"
# print(df.to_string)
# g = sns.heatmap(df, vmin=min, vmax=max, xticklabels=20, yticklabels=20, cmap=cmap, square=True, cbar_kws={'label': "helpfulness"})
# g.invert_yaxis()
# g.set_xlabel("Prior P(yes|context)")
# g.set_ylabel("Posterior P(yes|response, context)")
# plt.savefig(f"../figures/heatmaps/helpfulness_quadratic.pdf")
# plt.savefig(f"../figures/heatmaps/helpfulness_quadratic.png")
# plt.close()



# def quadratic2(x, a, b, c, d, e, f, g, h):
#     return a*x[0]**2 + b*x[1]**2 + c*x[0]**2*x[1] + d*x[0]*x[1]**2 + e*x[0]*x[1] + f*x[0] + g*x[1] + h
#
# xs = np.array(results[["prior_mean", "posterior_mean"]]).transpose()
# ys = np.array(results["helpfulness_mean"])
#
# p0 = [1, 1, 1, 1, 1, 1, 1, 1]
# # bounds = ([0.3, 0.3, -np.inf, -np.inf, -np.inf], [0.7, 0.7, np.inf, np.inf, np.inf])
# popt, pcov = curve_fit(quadratic2, xs, ys, p0, method='trf', maxfev=2000)
# print(popt)
#
# n = 100
# priors = np.arange(0, 1+1/n, 1/n)
# posteriors = np.arange(0, 1+1/n, 1/n)
# array = np.zeros((n+1, n+1))
#
# for i, q in enumerate(priors):
#     for j, p in enumerate(posteriors):
#         array[i][j] = quadratic2((p, q), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7])
#
# # print(array)
#
# df = pd.DataFrame(array, index=priors, columns=posteriors)
# min = 0
# max = 1
#
# # max = {"Entropy Reduction": 0.5, "KL_exp": 1, "KL": 1.2, "Cross Entropy": 2}[metric]
# cmap = "rocket"
# print(df.to_string)
# g = sns.heatmap(df, vmin=min, vmax=max, xticklabels=20, yticklabels=20, cmap=cmap, square=True, cbar_kws={'label': "helpfulness"})
# g.invert_yaxis()
# g.set_xlabel("Prior P(yes|context)")
# g.set_ylabel("Posterior P(yes|response, context)")
# plt.savefig(f"../figures/heatmaps/helpfulness_quadratic2.pdf")
# plt.savefig(f"../figures/heatmaps/helpfulness_quadratic2.png")
# plt.close()
#




def cubic(x, a, b, c, d, e, f, g, h, i, j, k, l):
    return a*x[0]**2 + b*x[1]**2 + \
           c*x[0]**2*x[1] + d*x[0]*x[1]**2 + \
           e*x[0]*x[1] + f*x[0] + g*x[1] + h + \
           i*x[0]**3 + j*x[1]**3+ k*x[0]**3*x[1] + l*x[0]*x[1]**3



xs = np.array(results[["prior_mean", "posterior_mean"]]).transpose()
ys = np.array(results["helpfulness_mean"])

p0 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# bounds = ([0.3, 0.3, -np.inf, -np.inf, -np.inf], [0.7, 0.7, np.inf, np.inf, np.inf])
popt, pcov = curve_fit(cubic, xs, ys, p0, method='trf', maxfev=2000)
print(popt)

n = 100
priors = np.arange(0, 1+1/n, 1/n)
posteriors = np.arange(0, 1+1/n, 1/n)
array = np.zeros((n+1, n+1))

for i, q in enumerate(priors):
    for j, p in enumerate(posteriors):
        array[i][j] = cubic((p, q), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11])

# print(array)

df = pd.DataFrame(array, index=priors, columns=posteriors)
min = 0
max = 1

# max = {"Entropy Reduction": 0.5, "KL_exp": 1, "KL": 1.2, "Cross Entropy": 2}[metric]
cmap = "rocket"
print(df.to_string)
g = sns.heatmap(df, vmin=min, vmax=max, xticklabels=20, yticklabels=20, cmap=cmap, square=True, cbar_kws={'label': "helpfulness"})
g.invert_yaxis()
g.set_xlabel("Prior P(yes|context)")
g.set_ylabel("Posterior P(yes|response, context)")
plt.savefig(f"../figures/heatmaps/helpfulness_cubic.pdf")
plt.savefig(f"../figures/heatmaps/helpfulness_cubic.png")
plt.close()


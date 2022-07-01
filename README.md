# dp-rmse
Differentially private estimation of the root-mean-square deviation of a sample of differences (errors). Instead of calculating $(x, y) \mapsto \sqrt{\sum_i (x_i - y_i)^2}$, we calculate $e \mapsto \sqrt{\sum_i e_i^2}$ and expect $e$ to be $x - y$. The vector $e$ is what we call errors.
Reducing the number of arguments down to 1 made the sensitivity analysis easier.

# Benchmark results (unimodal synthetic data)
We analyzed the quality of the differentially private root mean squared error (rMSE)
approximations of our implementation, based on synthetic samples drawn from Gaussian
and Laplaceian distributions. For various 
locations $\mu \in \Set{10^{-3}, 10^{-1}, 0, 1, 10, 10^3, 10^6}$,
scales $\sigma \in \Set{0.1 \mu, \mu, 10 \mu}$,
sample sizes $n \in \Set{10, 100, 1000, 10000}$,
privacy budgets $\epsilon \in \Set{0.01, 0.1, 1.0, 10.0}$ and 
upper bounds $U$ ranging from 0.5 to 1.0 percentiles (in steps of 0.1),
we estimated the DP rMSE 10 times and show the statistics in [Table 1](table_1.md).

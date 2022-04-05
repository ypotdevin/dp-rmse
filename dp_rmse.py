import numpy as np

#/**
# * @param errors The errors (differences) to apply the root mean squared error
# * function on.
# * @param epsilon The privacy budget.
# * @param U The upper bound on the error terms in errors.
# * @param rng The (pseudo) random number generator to use when drawing from the
# * Cauchy distribution.
# * @return double The epsilon-differentially private rMSE estimate of errors.
# */
def dp_rms_cauchy(errors: np.ndarray, epsilon: float, U: float, rng = None) -> float:
    if rng is None:
        rng = np.random.default_rng()
    sorted_errors = np.sort(errors)
    gamma = 2.0
    beta = epsilon / (2 * (gamma + 1.0))
    (sens, rmse) = rMS_smooth_sensitivity(sorted_errors, beta, U)
    noise = rng.standard_cauchy()
    dp_rmse = rmse + 2 * (gamma + 1) * sens * noise / epsilon
    return dp_rmse

#/**
# * @param errors The precomputed errors (to avoid having two arguments which
# * then have to be subtracted), sorted ascendingly.
# * @param beta The beta defining the beta-smooth sensitivity.
# * @param U The upper bound on the errors (not squared errors).
# * @return std::tuple<double, double> The beta-smooth sensitivity and the result
# * of the root mean squared error function, i.e. the function
# *
# *     e_1, ..., e_n |-> sqrt((e_1 ** 2 + ... + e_n ** 2) / n).
# */
def rMS_smooth_sensitivity(errors: np.ndarray, beta: float, U: float) -> tuple[float, float]:
    # If U is chosen well, i.e. a true upper bound on the errors, the clipping
    # will have no effect.
    np.clip(errors, -U, U, out=errors)
    U = U ** 2
    sqe_sum = errors.sum()
    n = len(errors)
    rmse = np.sqrt(sqe_sum / n)

    smooth_sens = -np.inf
    (prefix_sum, suffix_sum) = (sqe_sum, sqe_sum)
    for k in range(1, n + 1):
        largest = errors[n - k]
        smallest = errors[k - 1]
        prefix_sum -= largest # implicitly replace largest by 0)
        suffix_sum -= smallest
        prefix_local_sens = _local_sensitivity(largest, 0, prefix_sum, n, U)
        suffix_local_sens = _local_sensitivity(smallest, U, suffix_sum, n, U)
        local_sens = max(prefix_local_sens, suffix_local_sens)
        smooth_sens = max(smooth_sens, local_sens * np.exp(-beta * k))
        suffix_sum += U # replace smallest by U, but only after calculation
    return (smooth_sens, rmse)

#/**
# * @brief The local sensitivity of the rMSE function, already operating on the
# * vector of differences (not on two vectors which then will be subtracted).
# *
# * @param x the current squared error to replace.
# * @param substitute the replacement for x.
# * @param s the sum of the squared errors, but *without* x.
# * @param n the number of squared error (terms) in s, plus 1 for x.
# * @param U the upper bound of the squared errors terms in s, and x.
# * @return double The local sensitivity of the root mean squared error function.
# */
def _local_sensitivity(x: float, substitute: float, s: float, n: int, U: float) -> float:
    s = max(s, 1e-12) # to avoid division by zero
    sens = np.sqrt(s / n) * np.abs(np.sqrt(1 + x / s) - np.sqrt(1 + substitute / s))
    return sens

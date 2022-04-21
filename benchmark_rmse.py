from typing import Iterable, Sequence

import numpy as np
import pandas as pd

import dp_rmse


def params_generator():
    sample_sizes = [1, 10, 100, 1000, 10000]
    locations = [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6]

    for loc in locations:
        scales = [1e-3 * loc, 1e-2 * loc, 1e-1 * loc, 1e0 * loc, 1e1 * loc]
        for scale in scales:
            for n in sample_sizes:
                yield dict(
                    size=n, loc=loc, scale=scale,
                )
    for n in sample_sizes:
        yield dict(
            size=n, loc=0.0, scale=1.0,
        )


def compare_on(
    sample: np.ndarray, epsilons: Iterable[float], U: float, rng: np.random.Generator,
) -> Sequence[dict[str, float]]:
    leaky_rmse = np.sqrt(sample.mean())
    sorted_sample = np.sort(sample)
    results = [
        dict(
            leaky_rmse=leaky_rmse,
            dp_rmse=dp_rmse.dp_rms_cauchy(sorted_sample, eps, U, rng),
            execution=i,
            epsilon=eps,
        )
        for i in range(10)
        for eps in epsilons
    ]
    return results


def _loc_scale(loc_scale_dist_fun, name):
    epsilons = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
    rng = np.random.default_rng()
    lines = []
    for params in params_generator():
        sample = loc_scale_dist_fun(rng, params["loc"], params["scale"], params["size"])
        sample = np.abs(sample)
        for U in [
            np.percentile(sample, 80),
            np.percentile(sample, 90),
            np.percentile(sample, 95),
            sample.max(),
        ]:
            comparisons = compare_on(sample, epsilons, U, rng)
            for comparison in comparisons:
                line = dict(**params, **comparison, U=U, distribution=name)
                print(line)
                lines.append(line)
    df = pd.DataFrame(lines)
    df.to_csv("comparison_{}.csv".format(name))


def laplace():
    f = lambda rng, loc, scale, size: rng.laplace(loc, scale, size)
    _loc_scale(f, "laplace")


def normal():
    f = lambda rng, loc, scale, size: rng.normal(loc, scale, size)
    _loc_scale(f, "normal")


def poisson():
    f = lambda rng, loc, _, size: rng.poisson(loc, size)
    _loc_scale(f, "poisson")


def main():
    laplace()
    normal()
    poisson()


if __name__ == "__main__":
    main()

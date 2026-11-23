"""Smoke test: the package is importable and the scientific stack is installed."""

import numpy as np

import optlab


def test_package_importable() -> None:
    assert optlab.__version__ == "0.1.0"


def test_numpy_seeded_rng_is_reproducible() -> None:
    a = np.random.default_rng(42).standard_normal(5)
    b = np.random.default_rng(42).standard_normal(5)
    np.testing.assert_array_equal(a, b)

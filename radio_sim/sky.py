import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1
from astropy import units as un
from astropy import constants as const
from scipy.interpolate import interp1d
from tqdm import tqdm
from multiprocessing import Pool


def point_source_foregrounds(
    nu,
    n_sources=1000,
    Smin=0.3,
    Smax=300.0,
    alpha=-1.25,
    chromatic=False,
    return_beta=True,
    beta=None,
    seed=42,
):
    """
    Generate a catalogue of point source foregrounds
    """
    np.random.seed(seed)
    theta = np.random.uniform(0, np.pi / 2.0, n_sources)
    phi = np.random.uniform(0, 2 * np.pi, n_sources)

    if chromatic:
        alpha = np.random.uniform(-1.5, -1.25, size=n_sources)
        beta = (nu.value / 150) ** alpha[:, None]
        sources = (np.random.uniform(Smin, Smax, size=n_sources)[:, None] * beta).T

    else:
        if beta is None:
            beta = (nu.value / 150) ** alpha

        sources = np.random.uniform(Smin, Smax, size=n_sources) * beta[:, None]

    if return_beta:
        return sources, theta, phi, beta

    else:
        return sources, theta, phi

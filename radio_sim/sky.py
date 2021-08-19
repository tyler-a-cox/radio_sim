import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1
from astropy import units as un
from astropy import constants as const
from scipy.interpolate import interp1d
from tqdm import tqdm
from multiprocessing import Pool


def diffuse_sky(
    nu,
    chromatic=False,
    return_beta=True,
    beta=None,
    seed=42,
    alpha_low=-1.5,
    alpha_high=-1.25,
    mfreq=150,
):
    pass


def point_source_foregrounds(
    nu,
    n_sources=1000,
    Smin=0.3,
    Smax=300.0,
    chromatic=False,
    return_beta=True,
    beta=None,
    seed=42,
    alpha_low=-1.5,
    alpha_high=-1.25,
    mfreq=150,
    return_sources=False,
):
    """
    Generate a catalogue of point source foregrounds
    """
    np.random.seed(seed)
    theta = np.random.uniform(0, np.pi / 2.0, n_sources)
    phi = np.random.uniform(0, 2 * np.pi, n_sources)

    if chromatic:
        alpha = np.random.uniform(alpha_low, alpha_high, size=n_sources)
        beta = (nu.value / mfreq) ** alpha[:, None]
        sources = (np.random.uniform(Smin, Smax, size=n_sources)[:, None] * beta).T

    else:
        alpha = alpha_low
        if beta is None:
            beta = (nu.value / mfreq) ** alpha

        flux = np.random.uniform(Smin, Smax, size=n_sources)
        sources = flux * beta[:, None]

    if return_beta:
        if return_sources:
            return sources, theta, phi, beta, flux, mfreq, alpha

        return sources, theta, phi, beta

    else:
        return sources, theta, phi


def resimulate_sky(nu, flux, mfreq, alpha):
    """
    """
    beta = (nu.value / mfreq) ** alpha
    sources = flux * beta[:, None]
    return sources

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1
from astropy import units as un
from astropy import constants as const
from scipy.interpolate import interp1d
import aipy

from tqdm import tqdm
from hera_cal.redcal import get_pos_reds

from multiprocessing import Pool


def tau(b, theta, phi):
    """
    Solves for the delay

    b : np.ndarray, (3,)
        baseline vector

    theta : np.
    """
    bx, by, bz = b * un.m
    l, m, n = (np.cos(theta) * np.sin(phi), np.cos(theta) * np.cos(phi), np.sin(theta))
    return (bx * l + by * m + bz * n) / const.c


def beam_gaussian(xs, fqs, width=0.07, mfreq=150, chromatic=True):
    """
    Gaussian Beam

    """
    if chromatic:
        width = width * mfreq / fqs

    else:
        width = width * np.ones_like(fqs)

    resp = np.exp(-(xs ** 2) / (2 * np.sin(width[:, None]) ** 2)).astype(np.float32)
    return resp


def simulate_vis(sources, theta, delay, nu, chromatic=True):
    """
    Simulate visibilities using the Radio Interferometry Measurement Equation (RIME)

    Parameters
    ----------
    sources : np.ndarray
        Array containing the flux density of sources

    theta : np.ndarray
        Beam position of sources

    delay : np.ndarray

    """
    beam = beam_gaussian(np.pi / 2.0 - theta, nu.value, chromatic=chromatic)
    sky = sources * beam
    return np.sum(sky * np.exp(-2 * np.pi * 1j * nu[:, None] * delay).value, axis=1)


def point_source_foregrounds(
    nu,
    n_sources=1000,
    Smin=0.3,
    Smax=300.0,
    alpha=-1.25,
    chromatic=False,
    return_beta=True,
    beta=None,
):
    """
    Generate a catalogue of point source foregrounds
    """
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


def add_noise(v, scale=0.01):
    """ """
    return np.random.normal(0, np.abs(v.real) * scale) + 1j * np.random.normal(
        0, np.abs(v.imag) * scale
    )


def fft(data):
    """ """
    window = aipy.dsp.gen_window(data.shape[0], window="blackman-harris")
    dat = np.abs(np.fft.fft(data * window, axis=0)) ** 2
    return np.fft.fftshift(dat)

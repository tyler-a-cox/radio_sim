import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1
from astropy import units as un
from astropy import constants as const
from scipy.interpolate import interp1d
from tqdm import tqdm
from hera_cal.redcal import get_pos_reds

from multiprocessing import Pool


def beam_gaussian(xs, fqs, width=0.0001, mfreq=150, chromatic=True, n=0.5):
    """
    Gaussian shaped beam

    A bit longer description.

    Args:
        xs (np.ndarray, or float):
        fqs:
        width:
        mfreq:
        chromatic:

    Returns:
        type: description

    Raises:
        Exception: description

    """

    if chromatic:
        width = width * mfreq / fqs

    else:
        width = width * np.ones_like(fqs)

    resp = np.exp(-(xs ** 2) / (2 * np.sin(width[:, None] ** n))).astype(np.float32)
    return resp


def beam_sinc(xs, fqs, width=0.045, mfreq=150, n=0.5, chromatic=True):
    """
    Gaussian shaped beam

    A bit longer description.

    Args:
        xs (np.ndarray, or float):
        fqs:
        width:
        mfreq:
        chromatic:

    Returns:
        type: description

    Raises:
        Exception: description

    """
    xs = np.array(xs)
    xs.shape = (xs.size, 1)
    fqs = np.array(fqs)
    fqs.shape = (1, fqs.size)

    if chromatic:
        width = width * mfreq / fqs

    else:
        width = width * np.ones_like(fqs)

    width.shape = (1, -1)
    resp = np.sinc(xs / np.sin(width ** n)).astype(np.float32) ** 2
    resp.shape = (xs.size, fqs.size)
    return resp.T

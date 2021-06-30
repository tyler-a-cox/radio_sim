import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1
from astropy import units as un
from astropy import constants as const
from scipy.interpolate import interp1d
from tqdm import tqdm
from hera_cal.redcal import get_pos_reds

from multiprocessing import Pool


def beam_gaussian(xs, fqs, width=0.07, mfreq=150, chromatic=True):
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

    resp = np.exp(-(xs ** 2) / (2 * np.sin(width[:, None]) ** 2)).astype(np.float32)
    return resp


def beam_sinc(xs, fqs, width=0.07, mfreq=150, chromatic=True):
    """
    A short description.

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

    # TODo: replace this with an implementation of a sinc beam
    resp = ...
    return resp


def beam_airy(xs, fqs):
    """
    A short description.

    A bit longer description.

    AArgs:
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

    # TODo: replace this with an implementation of a sinc beam
    resp = ...
    return resp

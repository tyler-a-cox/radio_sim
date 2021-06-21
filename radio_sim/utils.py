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

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
from .beams import beam_gaussian
from .sky import point_source_foregrounds

c = const.c  # speed of light in meters per second


class RadioSim:
    """
    Class for simulating radio visibilities
    """

    def __init__(self, antpos, beam, sky, theta, phi, nu):
        """ """
        self.antpos = antpos
        self.beam = beam
        self.sky = sky
        self.theta = theta
        self.phi = phi
        self.nu = nu

        self.uv = {}

        for i, vi in self.antpos.items():
            for j, vj in self.antpos.items():
                if i != j and self.uv.get((j, i)) is None:
                    self.uv[(i, j)] = np.abs(vi - vj)

        self.delays = {k: self.tau(v, theta, phi) for k, v in self.uv.items()}

    def tau(self, b, theta, phi):
        """
        Solves for the delay

        b : np.ndarray, (3,)
            baseline vector

        theta : np.
        """
        bx, by, bz = b * un.m
        l, m, n = (
            np.cos(theta) * np.sin(phi),
            np.cos(theta) * np.cos(phi),
            np.sin(theta),
        )
        return (bx * l + by * m + bz * n) / const.c

    def simulate(self):
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
        sky = self.sky * self.beam
        visibilities = {}

        for k, delay in tqdm(self.delays.items()):
            visibilities[k] = np.sum(
                sky * np.exp(-2 * np.pi * 1j * self.nu[:, None] * delay).value, axis=1
            )

        return visibilities

    def simulate_u(self, us):
        """ """
        sky = self.sky * self.beam
        data = {u: None for u in us}
        length = (us.min() * c / self.nu[0]).to(un.meter)
        visibilities = {}

        for u in us:
            fqs = (u * c / length).to(un.MHz)
            if fqs > self.nu.max():
                length = (u * c / self.nu[0]).to(un.meter)
                fqs = (u * c / length).to(un.MHz)

            bm = beam_gaussian(
                np.pi / 2.0 - self.theta, np.array([fqs.value]), chromatic=False
            )

            sk, theta, phi, beta = point_source_foregrounds(
                np.array([fqs.value]) * fqs.unit
            )

            sky = sk * bm
            delay = self.tau(np.array([length.value, 0, 0]), self.theta, self.phi)

            visibilities[u] = (
                np.sum(
                    sky
                    * np.exp(
                        -2
                        * np.pi
                        * 1j
                        * (np.array([fqs.value])[:, None] * fqs.unit * delay).to(
                            un.dimensionless_unscaled
                        )
                    ).value,
                    axis=1,
                )
                / beta
            )

        return visibilities

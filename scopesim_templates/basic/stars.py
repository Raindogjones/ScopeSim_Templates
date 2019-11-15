import numpy as np
from astropy.io import ascii as ioascii
from astropy.io import fits
from astropy.table import Table
from astropy import units
from synphot import Empirical1D, SpectralElement, SourceSpectrum

from .. import rc
from . import utils


def star_field(n, mmin, mmax, width, height=None, photometric_system="vega"):
    """
    Creates a super basic field of stars with random positions and brightnesses

    Parameters
    ----------
    n : int
        number of stars

    mmin, mmax : float
        [mag] minimum and maximum magnitudes of the population

    width : float
        [arcsec] width of region to put stars in

    height : float, optional
        [arcsec] if None, then height=width

    photometric_system : str, optional
        [vega, AB]


    Returns
    -------
    stars : scopesim.Source object
        A Source object with a field of stars that can be fed into the method:
        ``<OpticalTrain>.observe()``

    See Also
    --------
    ``<OpticalTrain>.observe``
    ``<OpticalTrain>.readout``

    """
    if height is None:
        height = width

    if photometric_system.lower() == "ab":
        spec = utils.ab_spectrum()
    else:
        spec = utils.vega_spectrum()

    if rc.__config__["!SIM.random.seed"] is not None:
        np.random.seed(rc.__config__["!SIM.random.seed"])

    rands = np.random.random(size=(2, n)) - 0.5
    x = width * rands[0]
    y = height * rands[1]
    mags = np.random.random(size=n) * (mmax - mmin) + mmin
    w = 10**(-0.4 * mags)
    ref = np.zeros(n, dtype=int)

    tbl = Table(data=[x, y, w, ref, mags],
                names=["x", "y", "weight", "ref", "mag"])
    tbl.meta["photometric_system"] = photometric_system
    stars = rc.Source(spectra=spec, table=tbl)

    return stars

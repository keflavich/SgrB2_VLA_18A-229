import os
import numpy as np
from astropy.io import fits
from astropy import units as u
from astropy.stats import mad_std
import radio_beam
import glob
from spectral_cube import SpectralCube
import regions

import matplotlib
matplotlib.use('agg')
import pylab as pl

import re
nh3_re = re.compile("NH3_?([0-9][0-9])")

nh3_regs = regions.read_ds9('SgrB2M_NH3_22_masers.reg')


freq_dict = {
    '11': 23.6944955e9,
    '21': 23.098815e9,
    '22': 23.722633335e9,
    '32': 22.8341851e9,
    '33': 23.8701296e9,
    '44': 24.1394169e9,
    '55': 24.53299e9,
    '54': 22.653022e9,
    '53': 21.285275e9,
    '66': 25.05603e9,
    '65': 22.732429e9,
    '77': 25.71518e9,
    '88': 26.51898e9,
    '99': 27.477943e9,
}

for ii,reg in enumerate(nh3_regs):

    print(ii, reg)
    pl.figure(1).clf()

    for jj,fn in enumerate(glob.glob("*combined_Sgr_B2_MN_K*NH3*.image.pbcor.fits")):

        linename = nh3_re.search(fn).groups()[0]

        if linename == '22':
            fn = 'NH322_zoom_on_SgrB2M_40to80kms_selfcal_iter3.image.pbcor.fits'

        restfreq = freq_dict[linename]*u.Hz

        cube = SpectralCube.read(fn).with_spectral_unit(u.km/u.s,
                                                        velocity_convention='radio',
                                                        rest_value=restfreq)
        cube.beam_threshold = 1
        print(linename, cube.wcs.wcs.restfrq)

        rpix = reg.to_pixel(cube.wcs.celestial)

        if rpix.center.y > 0 and rpix.center.y < cube.shape[1] and rpix.center.x > 0 and rpix.center.x < cube.shape[2]:

            spec = cube[:, int(rpix.center.y), int(rpix.center.x)]

            spec.write("nh3spectra/{0}_{1}".format(ii, fn), overwrite=True)

            if ii == 0 and linename == '22':
                pl.plot(spec.spectral_axis, jj*0.01 + spec.value/10, label=linename+"/10")
            else:
                pl.plot(spec.spectral_axis, jj*0.01 + spec.value, label=linename)

    pl.legend(loc='best')
    pl.xlabel("$V_{LSR}$ [km s$^{-1}$]")
    pl.ylabel("Flux Density (Jy)")
    pl.savefig("nh3spectra/{0}_nh3_lines.png".format(ii), dpi=150)
    pl.savefig("nh3spectra/{0}_nh3_lines.pdf".format(ii))

"""
imaging tests: what gridders do what to the data?
"""
import os
#import runpy
#runpy.run_path('continuum_imaging_general.py')
import pyregion
import numpy as np
import sys
assert os.getenv('SCRIPT_DIR') is not None
sys.path.append(os.getenv('SCRIPT_DIR'))
from continuum_imaging_general import myclean, makefits
from continuum_windows import Qmses

from astropy.io import fits
from astropy import wcs

from taskinit import msmdtool, iatool, casalog, tbtool

from tclean_cli import tclean_cli as tclean
from flagdata_cli import flagdata_cli as flagdata
from ft_cli import ft_cli as ft
from gaincal_cli import gaincal_cli as gaincal
from applycal_cli import applycal_cli as applycal
from concat_cli import concat_cli as concat
from importfits_cli import importfits_cli as importfits
from imhead_cli import imhead_cli as imhead
from makemask_cli import makemask_cli as makemask
from exportfits_cli import exportfits_cli as exportfits
from importfits_cli import importfits_cli as importfits
from clearcal_cli import clearcal_cli as clearcal
from split_cli import split_cli as split
ia = iatool()
msmd = msmdtool()
tb = tbtool()


def myprint(x):
    print(x)
    casalog.post(str(x), origin='singlefield')


mses = list(Qmses.keys())


fullpath_mses = ['../' + ms[:-3] + "_continuum_split_for_selfcal.ms"
                 for ms in mses if ms in Qmses]

cont_vis = []
for ms in fullpath_mses:
    splitagain = ms[:-3] + "_SgrB2_NM_Q.ms"
    myprint("{0} -> {1}".format(ms, splitagain))
    if not os.path.exists(splitagain):
        assert split(vis=ms, outputvis=splitagain,
                     field='Sgr B2 NM Q',
                     datacolumn='corrected')
    cont_vis.append(splitagain)



cleanbox_mask_image = 'cleanbox_mask_SgrB2.image'
cleanbox_mask = 'cleanbox_mask.mask'
mask = cleanbox_mask_image


selfcal_fields = "Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q".split(",")
selfcal_fields = ['Sgr B2 NM Q']


extrapars = {'wproject': {'wprojplanes': 64,
                          'rotatepastep': 5.0,
                          'cfcache':'test_wtermmerge.cfcache',
                         },
             'mosaic': {},
             'standard': {},
             'widefield': {},
             'awproject': {'wprojplanes': 64,
                           'rotatepastep': 5.0,
                           'cfcache':'test_awtermmerge.cfcache',
                         },
            }

for gridder in ('standard', 'wproject', 'widefield', 'mosaic', 'awproject'):

    try:
        imagename = '18A-229_Q_singlefield_imaging_smallfield_test_{0}'.format(gridder)
        myclean(vis=cont_vis,
                fields=selfcal_fields,
                spws='',
                imsize=1000,
                phasecenters={"Sgr B2 N Q":'J2000 17h47m19.897 -28d22m17.340',
                              "Sgr B2 NM Q":'J2000 17h47m20.166 -28d23m04.968',
                              "Sgr B2 MS Q":'J2000 17h47m20.166 -28d23m04.968',
                              "Sgr B2 S Q":'J2000 17h47m20.461 -28d23m45.059',
                             },
                cell='0.01arcsec',
                name=imagename,
                gridder=gridder,
                niter=10000,
                threshold='3mJy',
                scales=[0,3,9],
                robust=0.5,
                savemodel='none',
                mask=mask,
                noneg=False,
                **extrapars[gridder]
               )
    except Exception as ex:
        myprint(ex)

for gridder in ('standard', 'wproject', 'widefield', 'mosaic', 'awproject'):

    imagename = '18A-229_Q_singlefield_imaging_largefield_test_{0}'.format(gridder)
    try:
        myclean(vis=cont_vis,
                fields=selfcal_fields,
                spws='',
                imsize=4000,
                cell='0.01arcsec',
                name=imagename,
                gridder=gridder,
                niter=10000,
                threshold='3mJy',
                scales=[0,3,9],
                robust=0.5,
                savemodel='none',
                mask=mask,
                noneg=False,
                **extrapars[gridder]
               )
    except Exception as ex:
        myprint(ex)

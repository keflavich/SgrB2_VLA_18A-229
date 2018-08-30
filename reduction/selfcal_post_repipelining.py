"""
Self-calibrate the Q-band data on maps made from the 'good' dates.
"""
import os
#import runpy
#runpy.run_path('continuum_imaging_general.py')
import sys
sys.path.append('.')
from continuum_imaging_general import myclean, tclean, makefits
from continuum_windows import Qmses

from tclean_cli import tclean_cli as tclean
from flagdata_cli import flagdata_cli as flagdata
from ft_cli import ft_cli as ft
from gaincal_cli import gaincal_cli as gaincal
from applycal_cli import applycal_cli as applycal
from importfits_cli import importfits_cli as importfits
from imhead_cli import imhead_cli as imhead

from astropy.io import fits

mses = list(Qmses.keys())

if not os.path.exists('18A-229_mosaic_for_selfcal.model.tt0.noneg'):
    """
    This is to generate the first iteration model.  This won't always be needed...
    """
    fh0 = fits.open('../continuum/18A-229_mosaic_for_selfcal.model.tt0.fits')
    fh1 = fits.open('../continuum/18A-229_mosaic_for_selfcal.model.tt1.fits')
    bad = fh0[0].data < 0
    fh0[0].data[bad] = 0
    fh1[0].data[bad] = 0
    fh0.writeto('../continuum/18A-229_mosaic_for_selfcal.model.tt0.noneg.fits', overwrite=True)
    fh1.writeto('../continuum/18A-229_mosaic_for_selfcal.model.tt1.noneg.fits', overwrite=True)

    importfits(fitsimage='../continuum/18A-229_mosaic_for_selfcal.model.tt0.noneg.fits',
               imagename='../continuum/18A-229_mosaic_for_selfcal.model.tt0.noneg',
               defaultaxes=True,
               defaultaxesvalues=[fh0[0].header['CRVAL1'],
                                  fh0[0].header['CRVAL2'],
                                  '4.59132771e+10Hz', 'I'],
               overwrite=True
              )
    importfits(fitsimage='../continuum/18A-229_mosaic_for_selfcal.model.tt1.noneg.fits',
               imagename='../continuum/18A-229_mosaic_for_selfcal.model.tt1.noneg',
               defaultaxes=True,
               defaultaxesvalues=[fh0[0].header['CRVAL1'],
                                  fh0[0].header['CRVAL2'],
                                  '4.59132771e+10Hz', 'I'],
               overwrite=True
              )
    imhead('../continuum/18A-229_mosaic_for_selfcal.model.tt0.noneg', mode='put',
           hdkey='cdelt4', hdvalue='10GHz',)
    imhead('../continuum/18A-229_mosaic_for_selfcal.model.tt1.noneg', mode='put',
           hdkey='cdelt4', hdvalue='10GHz',)

for ms in mses:

    assert ms in Qmses

    name = ms[:22]

    fullpathms = '../'+ms
    cont_ms = fullpathms[:-3]+"_continuum.ms"

    if not os.path.exists(cont_ms):
        # ensure that both phase-calibrator and data are not flagged.
        flagdata(vis=fullpathms, mode='unflag',
                 field=('J1744-3116,Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,'
                        'Sgr B2 S Q,Sgr B2 DS1 Q,Sgr B2 DS2 Q,Sgr B2 DS3 Q'))
        flagdata(vis=fullpathms, mode='manual', autocorr=True)

        # flag edge channels
        flagchans = ",".join(["{0}:0~5;123~128".format(xx) for xx in
                              Qmses[ms].split(",")])
        flagdata(vis=fullpathms, mode='manual', spw=flagchans)

        # flag CH3OH maser
        flagdata(vis=fullpathms, mode='manual',
                 spw='44054800170~44084179830Hz:44054800170~44084179830Hz')

        split(vis=fullpathms,
              outputvis=fullpathms[:-3]+"_continuum.ms",
              field=('Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,'
                     'Sgr B2 S Q,Sgr B2 DS1 Q,Sgr B2 DS2 Q,Sgr B2 DS3 Q'),
              width=16,
              spw=Qmses[ms],
             )

        # Unflag CH3OH maser
        flagdata(vis=fullpathms, mode='unflag',
                 spw='44054800170~44084179830Hz:44054800170~44084179830Hz')

        clearcal(cont_ms, addmodel=True)
        #ft(vis=cont_ms,
        #   field='Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q',
        #   spw='',
        #   model=['../continuum/18A-229_mosaic_for_selfcal.model.tt0.noneg',
        #          '../continuum/18A-229_mosaic_for_selfcal.model.tt1.noneg'],
        #   nterms=2)


    caltable = '{0}_sgrb2_selfcal_phase_30ssolint.cal'.format(name)

    if not os.path.exists(caltable):

        ft(vis=cont_ms,
           field='Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q',
           spw='',
           model='../continuum/18A-229_mosaic_for_selfcal.model.tt0.noneg')

        gaincal(vis=cont_ms,
                caltable=caltable,
                field='Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q',
                calmode='p',
                refant='',
                solint='30s',
                #uvrange='0~2000klambda',
                minblperant=3,
               )

    applycal(flagbackup=False,
             gainfield=[],
             interp=[],
             gaintable=[caltable],
             calwt=[False],
             vis=cont_ms,
             applymode='calonly',
             antenna='*&*',
             spwmap=[],
             parang=True)

    myclean(vis=cont_ms,
            name=name,
            imsize=8000,
            cell='0.01arcsec',
            fields=['Sgr B2 N Q', 'Sgr B2 NM Q', 'Sgr B2 MS Q', 'Sgr B2 S Q'],
            threshold='2mJy',
            savemodel='modelcolumn',
            spws='', # all windows are continuum now
           )

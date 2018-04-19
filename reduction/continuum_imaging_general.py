"""
Tools (functions) for continuum imaging.
Not a standalone script; meant to be imported.
"""

import datetime
import os
import glob

from tclean_cli import tclean_cli as tclean
from impbcor_cli import impbcor_cli as impbcor
from exportfits_cli import exportfits_cli as exportfits

def makefits(myimagebase, cleanup=True):
    impbcor(imagename=myimagebase+'.image.tt0', pbimage=myimagebase+'.pb.tt0', outfile=myimagebase+'.image.tt0.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.tt0.pbcor', fitsimage=myimagebase+'.image.tt0.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.image.tt1', fitsimage=myimagebase+'.image.tt1.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb.tt0', fitsimage=myimagebase+'.pb.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt0', fitsimage=myimagebase+'.model.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt1', fitsimage=myimagebase+'.model.tt1.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual.tt0', fitsimage=myimagebase+'.residual.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.alpha', fitsimage=myimagebase+'.alpha.fits', dropdeg=True, overwrite=True)
    exportfits(imagename=myimagebase+'.alpha.error', fitsimage=myimagebase+'.alpha.error.fits', dropdeg=True, overwrite=True)

    if cleanup:
        for ttsuffix in ('.tt0', '.tt1', '.tt2'):
            for suffix in ('pb{tt}', 'weight', 'sumwt{tt}', 'psf{tt}',
                           'model{tt}', 'mask', 'image{tt}', 'residual{tt}',
                           'alpha', 'alpha.error'):
                os.system('rm -rf {0}.{1}'.format(myimagebase, suffix).format(tt=ttsuffix))


def myclean(
    vis,
    name,
    spws="2,4,5,6,7,8,9,11,12,13,14,15,16,17,18,21,22,23,24,25,27,28,29,30,31,33,34,35,36,38,41,43,44,46,47,48,49,51,52,53,54,55,56,57,58,59,60,62,63,64",
    imsize=8000,
    cell='0.01arcsec',
    fields=["Sgr B2 N Q", "Sgr B2 NM Q", "Sgr B2 MS Q", "Sgr B2 S Q", "Sgr B2 DS1 Q", "Sgr B2 DS2 Q", "Sgr B2 DS3 Q",],
    niter=10000,
    threshold='0.75mJy',
    robust=0.5,
    savemodel='none',
    **kwargs
):
    for field in fields:
        imagename = ("{name}_{field}_r{robust}_allcont_clean1e4_{threshold}"
                     .format(name=name, field=field.replace(" ","_"),
                             robust=robust, threshold=threshold)
                    )
        if not os.path.exists(imagename+".image.tt0.pbcor.fits"):
            tclean(vis=vis,
                   field=field,
                   spw=spws,
                   imsize=[imsize, imsize],
                   cell=cell,
                   imagename=imagename,
                   niter=niter,
                   threshold=threshold,
                   robust=robust,
                   gridder='standard',
                   deconvolver='mtmfs',
                   specmode='mfs',
                   nterms=2,
                   weighting='briggs',
                   pblimit=0.2,
                   interactive=False,
                   outframe='LSRK',
                   datacolumn='corrected',
                   savemodel=savemodel,
                   **kwargs
                  )
            makefits(imagename)

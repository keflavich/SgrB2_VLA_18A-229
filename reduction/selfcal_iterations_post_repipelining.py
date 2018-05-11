"""
Self-calibrate the Q-band data on maps made from the 'good' dates.
"""
import os
#import runpy
#runpy.run_path('continuum_imaging_general.py')
import pyregion
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

fullpath_mses = ['../'+ms for ms in mses if ms in Qmses]

cont_vis = 'continuum_concatenated.ms'
if not os.path.exists(cont_vis):
    assert concat(vis=fullpath_mses, concatvis=cont_vis)

imagename = '18A-229_Q_mosaic_for_selfcal_iter1'
tclean(vis=cont_vis,
       field="Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q",
       spw='',
       imsize=[20000,20000],
       phasecenter='J2000 17h47m19.523 -28d23m08.497',
       cell='0.01arcsec',
       imagename=imagename,
       niter=10000,
       threshold='1mJy',
       robust=0.5,
       gridder='mosaic',
       deconvolver='mtmfs',
       specmode='mfs',
       nterms=2,
       weighting='briggs',
       pblimit=0.2,
       interactive=False,
       outframe='LSRK',
       savemodel='modelcolumn',
      )
makefits(imagename, cleanup=False)

caltable = '18A-229_Q_concatenated_cal_iter1'
gaincal(vis=cont_vis,
        caltable=caltable,
        field='Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q',
        calmode='p',
        refant='',
        solint='10s',
        #uvrange='0~2000klambda',
        minblperant=3,
       )

applycal(vis=cont_ms, flagbackup=False, gainfield=[], interp=[],
         gaintable=[caltable], calwt=[False], applymode='calonly',
         antenna='*&*', spwmap=[], parang=True)



# create a mask
cleanimagename = imagename+".image.tt0.pbcor"
exportfits(cleanimagename, cleanimagename+".fits", overwrite=True)
reg = pyregion.open('cleanbox_regions_SgrB2.reg')
imghdu = fits.open(cleanimagename+".fits")[0]
mask = reg.get_mask(imghdu)[None, None, :, :]
imghdu.data = mask.astype('int16')
imghdu.header['BITPIX'] = 16
imghdu.writeto('cleanbox_mask_SgrB2.fits', clobber=True)
cleanbox_mask_image = 'cleanbox_mask_SgrB2.image'
importfits(fitsimage='cleanbox_mask_SgrB2.fits',
           imagename=cleanbox_mask_image,
           overwrite=True)
ia.open(cleanbox_mask_image)
ia.calcmask(mask=cleanbox_mask_image+" > 0.5",
            name='cleanbox_mask_{0}'.format(field_nospace))

ia.close()
cleanbox_mask = 'cleanbox_mask_{0}.mask'.format(field_nospace)
makemask(mode='copy', inpimage=cleanbox_mask_image,
         inpmask=cleanbox_mask_image+":cleanbox_mask_{0}".format(field_nospace),
         output=cleanbox_mask,
         overwrite=True)

mask = cleanbox_mask_image

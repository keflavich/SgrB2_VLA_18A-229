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

from taskinit import msmdtool, iatool, casalog

from tclean_cli import tclean_cli as tclean
from flagdata_cli import flagdata_cli as flagdata
from ft_cli import ft_cli as ft
from gaincal_cli import gaincal_cli as gaincal
from applycal_cli import applycal_cli as applycal
from importfits_cli import importfits_cli as importfits
from imhead_cli import imhead_cli as imhead
from makemask_cli import makemask_cli as makemask
from exportfits_cli import exportfits_cli as exportfits
from importfits_cli import importfits_cli as importfits
ia = iatool()
msmd = msmdtool()


from astropy.io import fits
from astropy import wcs

mses = list(Qmses.keys())

fullpath_mses = ['../' + ms[:-3] + "_continuum.ms"
                 for ms in mses if ms in Qmses]

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

applycal(vis=cont_vis, flagbackup=False, gainfield=[], interp=['linearperobs'],
         gaintable=[caltable], calwt=[False], applymode='calonly',
         antenna='*&*', spwmap=[], parang=True,)



# create a mask
cleanimagename = imagename+".image.tt0.pbcor"
exportfits(cleanimagename, cleanimagename+".fits", overwrite=True)
reg = pyregion.open('cleanbox_regions_SgrB2.reg')
imghdu = fits.open(cleanimagename+".fits")[0]
#mask = reg.get_mask(imghdu)[None, None, :, :]
mask = reg.get_mask(header=wcs.WCS(imghdu.header).celestial.to_header(), shape=imghdu.data.shape[2:])
imghdu.data = mask.astype('int16')
imghdu.header['BITPIX'] = 16
imghdu.writeto('cleanbox_mask_SgrB2.fits', clobber=True)
cleanbox_mask_image = 'cleanbox_mask_SgrB2.image'
importfits(fitsimage='cleanbox_mask_SgrB2.fits',
           imagename=cleanbox_mask_image,
           overwrite=True)
ia.open(cleanbox_mask_image)
ia.calcmask(mask=cleanbox_mask_image+" > 0.5",
            name='cleanbox_mask')

ia.close()
cleanbox_mask = 'cleanbox_mask.mask'
makemask(mode='copy', inpimage=cleanbox_mask_image,
         inpmask=cleanbox_mask_image+":cleanbox_mask",
         output=cleanbox_mask,
         overwrite=True)

mask = cleanbox_mask_image

imagename = '18A-229_Q_mosaic_for_selfcal_iter2'
tclean(vis=cont_vis,
       mask=mask,
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

caltable = '18A-229_Q_concatenated_cal_iter2'
gaincal(vis=cont_vis,
        caltable=caltable,
        field='Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q',
        calmode='p',
        refant='',
        solint='10s',
        #uvrange='0~2000klambda',
        minblperant=3,
       )

caltable = '18A-229_Q_concatenated_cal_iter2_combinespw'
gaincal(vis=cont_vis,
        caltable=caltable,
        field='Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q',
        calmode='p',
        refant='',
        solint='10s',
        #uvrange='0~2000klambda',
        minblperant=3,
        combine='spw',
       )

caltable = '18A-229_Q_concatenated_cal_iter2_combinespw_30s'
gaincal(vis=cont_vis,
        caltable=caltable,
        field='Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q',
        calmode='p',
        refant='',
        solint='30s',
        #uvrange='0~2000klambda',
        minblperant=3,
        combine='spw',
       )

caltable = '18A-229_Q_concatenated_cal_iter2_30s'
gaincal(vis=cont_vis,
        caltable=caltable,
        field='Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q',
        calmode='p',
        refant='',
        solint='30s',
        #uvrange='0~2000klambda',
        minblperant=3,
       )


tb.open(cont_vis+"/SPECTRAL_WINDOW")
nspw = len(tb.getcol('NAME'))
tb.close()

applycal(vis=cont_vis, flagbackup=False, gainfield=[], interp=['linearperobs'],
         gaintable=[caltable], calwt=[False], applymode='calonly',
         antenna='*&*', 
         #spwmap=[0]*nspw,
         parang=True,)


imagename = '18A-229_Q_mosaic_for_selfcal_iter3'
outlierfile = """# Outlier File
imagename={imname}_M
phasecenter=J2000 17h47m20.167 -28d23m04.337
imsize=[1000,1000]


imagename={imname}_N
phasecenter=J2000 17h47m19.837 -28d22m18.867
imsize=[1000,1000]

imagename={imname}_Z
phasecenter=J2000 17h47m20.040 -28d22m41.397
imsize=[500,500]

imagename={imname}_S
phasecenter=J2000 17h47m20.455 -28d23m45.067
imsize=[1000,1000]""".format(imname=imagename)
with open("outlierfile.txt","w") as fh:
    fh.write(outlierfile)

tclean(vis=cont_vis,
       imagename=imagename,
       field="Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q",
       spw='',
       mask=mask,
       #outlierfile="outlierfile.txt",
       imsize=[20000,20000],
       phasecenter='J2000 17h47m19.523 -28d23m08.497',
       cell='0.01arcsec',
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
       scales=[0,3,9],
      )
for nm in [imagename+'_M', imagename+'_N', imagename+"_Z", imagename+"_S"]:
    makefits(nm, cleanup=False)

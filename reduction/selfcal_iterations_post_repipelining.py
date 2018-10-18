"""
Self-calibrate the Q-band data on maps made from the 'good' dates.
"""
import os
#import runpy
#runpy.run_path('continuum_imaging_general.py')
import pyregion
import numpy as np
import sys
assert os.getenv('SCRIPT_DIR') is not None
sys.path.append(os.getenv('SCRIPT_DIR'))
from continuum_imaging_general import myclean, makefits, mygaincal, myapplycal
from continuum_windows import Qmses

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


from astropy.io import fits
from astropy import wcs

mses = list(Qmses.keys())

fullpath_mses = ['../' + ms[:-3] + "_continuum.ms"
                 for ms in mses if ms in Qmses]

# raw_and_corr_vis = 'continuum_concatenated_raw_and_corr.ms'
# if not os.path.exists(raw_and_corr_vis):
#     assert concat(vis=fullpath_mses, concatvis=raw_and_corr_vis,
#                   # should be used but isn't freqtol='5MHz',
#                  )
# cont_vis = 'continuum_concatenated_selfcal.ms'
# if not os.path.exists(cont_vis):
#     assert split(vis=raw_and_corr_vis, outputvis=cont_vis,
#                  datacolumn='corrected')
# 
# this is OK because there should be no corrected column
#clearcal(vis=cont_vis, addmodel=True)

def myprint(x):
    print(x)
    casalog.post(str(x), origin='singlefield')


selfcal_mses = {}
for ms in fullpath_mses:
    outms = ms[:-3]+"_split_for_selfcal.ms"
    if not os.path.exists(outms):
        # TODO: come back later & keep in DS...
        split(vis=ms, outputvis=outms,
              datacolumn='corrected',
              field="Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q")
    msname = ms[16:21]
    if msname == '03_06':
        if 'T12' in ms:
            msname = '03_06_T12'
        else:
            msname = '03_06_T01'

    myprint(msname)
    selfcal_mses[msname] = outms

myprint(selfcal_mses)
cont_vis = list(selfcal_mses.values())


imagename = '18A-229_Q_mosaic_selfcal_iter0_dirty'
if not os.path.exists(imagename+".image.tt0.pbcor"):
    # do a full-mosaic clean to enable mask creation
    tclean(
           vis=cont_vis,
           spw='',
           field="Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q",
           phasecenter='J2000 17h47m19.693 -28d23m11.527',
           imsize=[9000,9000],
           cell='0.02arcsec',
           imagename=imagename,
           niter=0,
           threshold='1000mJy',
           robust=0.5,
           gridder='mosaic',
           scales=[0,3,9],
           deconvolver='mtmfs',
           specmode='mfs',
           nterms=2,
           weighting='briggs',
           pblimit=0.2,
           interactive=False,
           outframe='LSRK',
           savemodel='none',
          )
    makefits(imagename)


cleanbox_mask = 'cleanbox_mask.mask'
cleanbox_mask_image = 'cleanbox_mask_SgrB2.image'
if not os.path.exists(cleanbox_mask) or not os.path.exists(cleanbox_mask_image):
    # create a mask based on region selection (no thresholding here)
    dirtyimagename = imagename+".image.tt0.pbcor"
    exportfits(dirtyimagename, dirtyimagename+".fits", overwrite=True)
    reg = pyregion.open('cleanbox_regions_SgrB2.reg')
    imghdu = fits.open(dirtyimagename+".fits")[0]
    #mask = reg.get_mask(imghdu)[None, None, :, :]
    mask = reg.get_mask(header=wcs.WCS(imghdu.header).celestial.to_header(),
                        shape=imghdu.data.shape[2:])
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
    makemask(mode='copy', inpimage=cleanbox_mask_image,
             inpmask=cleanbox_mask_image+":cleanbox_mask",
             output=cleanbox_mask,
             overwrite=True)

mask = cleanbox_mask_image









imagename = '18A-229_Q_singlefield_selfcal_iter1'
myclean(vis=cont_vis,
        fields="Sgr B2 NM Q,Sgr B2 MS Q".split(","),
        spws='',
        imsize=1000,
        phasecenters={"Sgr B2 N Q":'J2000 17h47m19.897 -28d22m17.340',
                      "Sgr B2 NM Q":'J2000 17h47m20.166 -28d23m04.968',
                      "Sgr B2 MS Q":'J2000 17h47m20.166 -28d23m04.968',
                      "Sgr B2 S Q":'J2000 17h47m20.461 -28d23m45.059',
                     },
        cell='0.01arcsec',
        name=imagename,
        niter=10000,
        threshold='3mJy',
        scales=[0,3,9],
        robust=0.5,
        savemodel='modelcolumn',
        mask=mask,
       )

caltable = '18A-229_Q_concatenated_cal_iter1.cal'
if not os.path.exists(caltable):
    mygaincal(vis=cont_vis,
              caltable=caltable,
              field='Sgr B2 NM Q,Sgr B2 MS Q',
              calmode='p',
              refant='',
              solint='60s',
              minsnr=5,
              #uvrange='0~2000klambda',
              #minblperant=3,
             )

# do a purely diagnostic ampcal
diagnostic_ampcal_table = '18A-229_Q_concatenated_cal_iter1_ampcal_diagnostic.cal'
if not os.path.exists(diagnostic_ampcal_table):
    mygaincal(vis=cont_vis,
              caltable=diagnostic_ampcal_table,
              gaintype='G',
              combine='spw,scan,field',
              solint='inf',
              calmode='a',
              solnorm=True)


#moved to an earlier step
# # create a mask
# cleanimagename = imagename+".image.tt0.pbcor"
# exportfits(cleanimagename, cleanimagename+".fits", overwrite=True)
# reg = pyregion.open('cleanbox_regions_SgrB2.reg')
# imghdu = fits.open(cleanimagename+".fits")[0]
# #mask = reg.get_mask(imghdu)[None, None, :, :]
# mask = reg.get_mask(header=wcs.WCS(imghdu.header).celestial.to_header(), shape=imghdu.data.shape[2:])
# imghdu.data = mask.astype('int16')
# imghdu.header['BITPIX'] = 16
# imghdu.writeto('cleanbox_mask_SgrB2.fits', clobber=True)
# cleanbox_mask_image = 'cleanbox_mask_SgrB2.image'
# importfits(fitsimage='cleanbox_mask_SgrB2.fits',
#            imagename=cleanbox_mask_image,
#            overwrite=True)
# ia.open(cleanbox_mask_image)
# ia.calcmask(mask=cleanbox_mask_image+" > 0.5",
#             name='cleanbox_mask')
# 
# ia.close()
# cleanbox_mask = 'cleanbox_mask.mask'
# makemask(mode='copy', inpimage=cleanbox_mask_image,
#          inpmask=cleanbox_mask_image+":cleanbox_mask",
#          output=cleanbox_mask,
#          overwrite=True)
# 
# mask = cleanbox_mask_image

imagename = '18A-229_Q_singlefield_selfcal_iter2'
if not os.path.exists(imagename+'_Sgr_B2_NM_Q_r0.5_allcont_clean1e4_2mJy.image.tt0.pbcor.fits'):
    myapplycal(vis=cont_vis, flagbackup=False, gainfield=[], interp=['linearperobs'],
             gaintable=[caltable], calwt=[False], applymode='calonly',
             antenna='*&*', spwmap=[], parang=True,)

myclean(vis=cont_vis,
        fields="Sgr B2 NM Q,Sgr B2 MS Q".split(","),
        spws='',
        imsize=1000,
        phasecenters={"Sgr B2 N Q":'J2000 17h47m19.897 -28d22m17.340',
                      "Sgr B2 NM Q":'J2000 17h47m20.166 -28d23m04.968',
                      "Sgr B2 MS Q":'J2000 17h47m20.166 -28d23m04.968',
                      "Sgr B2 S Q":'J2000 17h47m20.461 -28d23m45.059',
                     },
        cell='0.01arcsec',
        name=imagename,
        scales=[0,3,9],
        niter=10000,
        threshold='2mJy',
        robust=0.5,
        savemodel='modelcolumn',
        mask=mask,
       )

caltable = '18A-229_Q_concatenated_cal_iter2.cal'
if not os.path.exists(caltable):
    mygaincal(vis=cont_vis,
            caltable=caltable,
            field='Sgr B2 NM Q,Sgr B2 MS Q',
            calmode='p',
            refant='',
            solint='30s',
            #uvrange='0~2000klambda',
            #minblperant=3,
           )

caltable = '18A-229_Q_concatenated_cal_iter2_combinespw.cal'
if not os.path.exists(caltable):
    mygaincal(vis=cont_vis,
            caltable=caltable,
            field='Sgr B2 NM Q,Sgr B2 MS Q',
            calmode='p',
            refant='',
            solint='30s',
            #uvrange='0~2000klambda',
            #minblperant=3,
            combine='spw',
           )

caltable = '18A-229_Q_concatenated_cal_iter2_combinespw_30s.cal'
if not os.path.exists(caltable):
    mygaincal(vis=cont_vis,
            caltable=caltable,
            field='Sgr B2 NM Q,Sgr B2 MS Q',
            calmode='p',
            refant='',
            solint='30s',
            #uvrange='0~2000klambda',
            #minblperant=3,
            combine='spw',
           )

caltable = '18A-229_Q_concatenated_cal_iter2_30s.cal'
if not os.path.exists(caltable):
    mygaincal(vis=cont_vis,
            caltable=caltable,
            field='Sgr B2 NM Q,Sgr B2 MS Q',
            calmode='p',
            refant='',
            solint='30s',
            #uvrange='0~2000klambda',
            #minblperant=3,
           )

# do a purely diagnostic ampcal
diagnostic_ampcal_table = '18A-229_Q_concatenated_cal_iter2_ampcal_diagnostic.cal'
if not os.path.exists(diagnostic_ampcal_table):
    mygaincal(vis=cont_vis,
              caltable=diagnostic_ampcal_table,
              gaintype='G',
              combine='spw,scan,field',
              solint='inf',
              calmode='a',
              solnorm=True)



tb.open(cont_vis[0]+"/SPECTRAL_WINDOW")
nspw = len(tb.getcol('NAME'))
tb.close()

imagename = '18A-229_Q_singlefield_selfcal_iter3'
if not os.path.exists(imagename+'_Sgr_B2_NM_Q_r0.5_allcont_clean1e4_1mJy.image.tt0.pbcor.fits'):
    myapplycal(vis=cont_vis, flagbackup=False, gainfield=[], interp=['linearperobs'],
             gaintable=[caltable], calwt=[False], applymode='calonly',
             antenna='*&*',
             #spwmap=[0]*nspw,
             parang=True,)

myclean(vis=cont_vis,
        fields="Sgr B2 NM Q,Sgr B2 MS Q".split(","),
        spws='',
        imsize=1000,
        phasecenters={"Sgr B2 N Q":'J2000 17h47m19.897 -28d22m17.340',
                      "Sgr B2 NM Q":'J2000 17h47m20.166 -28d23m04.968',
                      "Sgr B2 MS Q":'J2000 17h47m20.166 -28d23m04.968',
                      "Sgr B2 S Q":'J2000 17h47m20.461 -28d23m45.059',
                     },
        cell='0.01arcsec',
        name=imagename,
        niter=10000,
        scales=[0,3,9],
        threshold='1mJy',
        robust=0.5,
        savemodel='modelcolumn',
        mask=mask,
       )


caltable = '18A-229_Q_concatenated_cal_iter3_20s.cal'
if not os.path.exists(caltable):
    mygaincal(vis=cont_vis,
            caltable=caltable,
            field='Sgr B2 NM Q,Sgr B2 MS Q',
            calmode='p',
            refant='',
            solint='20s',
            #uvrange='0~2000klambda',
            #minblperant=3,
           )

# do a purely diagnostic ampcal
diagnostic_ampcal_table = '18A-229_Q_concatenated_cal_iter3_ampcal_diagnostic.cal'
if not os.path.exists(diagnostic_ampcal_table):
    mygaincal(vis=cont_vis,
              caltable=diagnostic_ampcal_table,
              gaintype='G',
              combine='spw,scan,field',
              solint='inf',
              calmode='a',
              solnorm=True)



imagename = '18A-229_Q_singlefield_selfcal_iter4'
if not os.path.exists(imagename+'_Sgr_B2_NM_Q_r0.5_allcont_clean1e4_1mJy.image.tt0.pbcor.fits'):
    myapplycal(vis=cont_vis, flagbackup=False, gainfield=[], interp=['linearperobs'],
             gaintable=[caltable], calwt=[False], applymode='calonly',
             antenna='*&*',
             #spwmap=[0]*nspw,
             parang=True,)

#selfcal_split_vis = 'continuum_concatenated_selfcal.ms'
#split(vis=cont_vis, outputvis=selfcal_split_vis,
#      datacolumn='corrected',)
selfcal_split_vis = cont_vis

myclean(vis=selfcal_split_vis,
        fields="Sgr B2 NM Q,Sgr B2 MS Q".split(","),
        spws='',
        imsize=1000,
        phasecenters={"Sgr B2 N Q":'J2000 17h47m19.897 -28d22m17.340',
                      "Sgr B2 NM Q":'J2000 17h47m20.166 -28d23m04.968',
                      "Sgr B2 MS Q":'J2000 17h47m20.166 -28d23m04.968',
                      "Sgr B2 S Q":'J2000 17h47m20.461 -28d23m45.059',
                     },
        cell='0.01arcsec',
        name=imagename,
        niter=10000,
        scales=[0,3,9],
        threshold='1mJy',
        robust=0.5,
        savemodel='modelcolumn',
        mask=mask,
       )


caltable = '18A-229_Q_concatenated_cal_iter4_20s.cal'
if not os.path.exists(caltable):
    mygaincal(vis=selfcal_split_vis,
            caltable=caltable,
            field='Sgr B2 NM Q,Sgr B2 MS Q',
            calmode='p',
            refant='',
            solint='20s',
            #uvrange='0~2000klambda',
            #minblperant=3,
           )

# do a purely diagnostic ampcal
diagnostic_ampcal_table = '18A-229_Q_concatenated_cal_iter4_ampcal_diagnostic.cal'
if not os.path.exists(diagnostic_ampcal_table):
    mygaincal(vis=cont_vis,
              caltable=diagnostic_ampcal_table,
              gaintype='G',
              combine='spw,scan,field',
              solint='inf',
              calmode='a',
              solnorm=True)




imagename = '18A-229_Q_singlefield_selfcal_iter5'
if not os.path.exists(imagename+'_Sgr_B2_NM_Q_r0.5_allcont_clean1e4_1mJy.image.tt0.pbcor.fits'):
    # apply calibration from 4 self-cal'd fields to *all* fields
    gainfield = 'Sgr B2 NM Q,Sgr B2 MS Q'
    #for field in 'Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q,Sgr B2 DS1 Q,Sgr B2 DS2 Q,Sgr B2 DS3 Q'.split(","):
    for field in 'Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q'.split(","):
        # apply the self-calibrations to the rest of the data
        myapplycal(vis=selfcal_split_vis, field=field, flagbackup=False, gainfield=[gainfield], interp=['linearperobs'],
                 gaintable=[caltable], calwt=[False], applymode='calonly',
                 antenna='*&*',
                 #spwmap=[0]*nspw,
                 parang=True,)

myclean(vis=selfcal_split_vis,
        fields="Sgr B2 NM Q,Sgr B2 MS Q".split(","),
        name=imagename,
        spws='', # even for indiv, we're dealing with cont splitted data...
        niter=10000,
        threshold='1mJy',
        scales=[0,3,9],
        robust=0.5,
        mask=mask,
        savemodel='modelcolumn',
       )

caltable = '18A-229_Q_concatenated_cal_iter5_20s.cal'
if not os.path.exists(caltable):
    mygaincal(vis=selfcal_split_vis,
            caltable=caltable,
            field='Sgr B2 NM Q,Sgr B2 MS Q',
            calmode='p',
            refant='',
            solint='20s',
            #uvrange='0~2000klambda',
            #minblperant=3,
           )

# do a purely diagnostic ampcal
diagnostic_ampcal_table = '18A-229_Q_concatenated_cal_iter5_ampcal_diagnostic.cal'
if not os.path.exists(diagnostic_ampcal_table):
    mygaincal(vis=cont_vis,
              caltable=diagnostic_ampcal_table,
              gaintype='G',
              combine='spw,scan,field',
              solint='inf',
              calmode='a',
              solnorm=True)


imagename = '18A-229_Q_singlefield_selfcal_iter6'
if not os.path.exists(imagename+'_Sgr_B2_NM_Q_r0.5_allcont_clean1e4_1mJy.image.tt0.pbcor.fits'):
    gainfield = 'Sgr B2 NM Q,Sgr B2 MS Q'
    #for field in 'Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q,Sgr B2 DS1 Q,Sgr B2 DS2 Q,Sgr B2 DS3 Q'.split(","):
    for field in 'Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q'.split(","):
        # apply the self-calibrations to the rest of the data
        myapplycal(vis=selfcal_split_vis, field=field, flagbackup=False, gainfield=[gainfield], interp=['linearperobs'],
                 gaintable=[caltable], calwt=[False], applymode='calonly',
                 antenna='*&*',
                 #spwmap=[0]*nspw,
                 parang=True,)


# fullfield cleans: can't use mask w/ DS
myclean(vis=selfcal_split_vis,
        fields="Sgr B2 NM Q,Sgr B2 MS Q".split(","),
        name=imagename,
        spws='', # even for indiv, we're dealing with cont splitted data...
        niter=10000,
        mask=mask,
        threshold='1mJy',
        robust=0.5,
        scales=[0,3,9],
        savemodel='modelcolumn',
       )

imagename = '18A-229_Q_mosaic_selfcal_iter6'
tclean(
       vis=selfcal_split_vis,
       spw='',
       field="Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q",
       phasecenter='J2000 17h47m19.693 -28d23m11.527',
       imsize=[9000,9000],
       cell='0.02arcsec',
       imagename=imagename,
       niter=10000,
       threshold='1mJy',
       robust=0.5,
       gridder='mosaic',
       scales=[0,3,9],
       deconvolver='mtmfs',
       specmode='mfs',
       nterms=2,
       weighting='briggs',
       pblimit=0.2,
       interactive=False,
       outframe='LSRK',
       savemodel='none',
       mask=mask,
      )
makefits(imagename)

# make some smaller diagnostic images
msmd.open(selfcal_split_vis)
summary = msmd.summary()
msmd.close()
for spw in np.unique(summary['spectral windows']['names']):
    imagename = '18A-229_Q_M_selfcal_iter6_diagnostics_spw{0}'.format(spw)
    tclean(vis=cont_vis,
           imagename=imagename,
           field="Sgr B2 NM Q,Sgr B2 MS Q",
           spw=spw,
           imsize=[500,500],
           phasecenter='J2000 17h47m20.163 -28d23m04.680',
           cell='0.01arcsec',
           niter=1000,
           threshold='1mJy',
           robust=0.5,
           gridder='awproject',
           conjbeams=True,
           deconvolver='multiscale',
           specmode='mfs',
           nterms=1,
           weighting='briggs',
           pblimit=0.2,
           interactive=False,
           outframe='LSRK',
           savemodel='none',
           scales=[0,3,9],
           mask=mask,
          )
    makefits(imagename, cleanup=False)

# do a purely diagnostic ampcal
diagnostic_ampcal_table = '18A-229_Q_concatenated_cal_iter6_ampcal_diagnostic.cal'
if not os.path.exists(diagnostic_ampcal_table):
    mygaincal(vis=cont_vis,
              caltable=diagnostic_ampcal_table,
              gaintype='G',
              combine='spw,scan,field',
              solint='inf',
              calmode='a',
              solnorm=True)


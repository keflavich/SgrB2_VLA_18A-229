import os
import sys
sys.path.append('.')
assert os.getenv('SCRIPT_DIR') is not None
sys.path.append(os.getenv('SCRIPT_DIR'))

from ms_lists import Kmses
from maserline_imaging import makefits

from tclean_cli import tclean_cli as tclean
from split_cli import split_cli as split
from concat_cli import concat_cli as concat
from gaincal_cli import gaincal_cli as gaincal
from applycal_cli import applycal_cli as applycal

from taskinit import mstool, msmdtool

mst = mstool()
msmd = msmdtool()

spws={'../18A-229_2018_03_29_T13_19_55.276/18A-229.sb35069722.eb35251855.58206.45698415509.ms':
      '7',
      '../18A-229_2018_03_28_T17_09_22.432/18A-229.sb35069722.eb35251150.58205.383514664354.ms':
      '5', }

field = 'Sgr B2 MN K,Sgr B2 MS K,Sgr B2 SDS K'
restfreq = '23.722633335GHz'
selfcal_spw = '0~5:23.7178~23.7185GHz'

merged_ms = 'NH322_merged.ms'
if not os.path.exists(merged_ms):
    splitvises = []

    for ms, spw in spws.items():
        basems = os.path.split(ms)[-1]
        outputvis = 'NH322_{0}'.format(basems)
        if not os.path.exists(outputvis):
            split(vis=ms,
                  outputvis=outputvis,
                  field=field,
                  # have to pick these carefully, they're topo.
                  spw='{0}:23.714~23.723GHz'.format(spw),)

        msmd.open(outputvis)
        ref0 = msmd.reffreq(0)
        msmd.close()

        if ref0['refer'] == 'TOPO':
            mst.open(outputvis, nomodify=False)
            mst.regridspw(outframe='LSRK', mode='vrad', restfreq=23.722633335e9)
            mst.close()

        splitvises.append(outputvis)

    concat(vis=splitvises,
           concatvis=merged_ms,
           )

imagename = 'NH322_zoom_on_SgrB2M_40to80kms'
if not os.path.exists(imagename+".image.pbcor.fits"):
    tclean(vis=merged_ms,
           imagename=imagename,
           imsize=500,
           cell='0.02arcsec',
           field=field,
           savemodel='modelcolumn',
           restfreq=restfreq,
           nchan=50, # 0.8 km/s channels
           start='40km/s',
           phasecenter='J2000 17h47m20.178 -28d23m04.109',
           niter=10000,
           threshold='50mJy',
           gridder='standard',
           deconvolver='hogbom',
           specmode='cube',
           weighting='briggs',
           pblimit=0.2,
           interactive=False,
           outframe='LSRK',
           datacolumn='data',
           robust=0.5,
          )
    makefits(imagename)

caltable1='NH322_selfcal_iter1_phase30s.cal'
gaincal(vis=merged_ms,
        caltable=caltable1,
        field=field,
        calmode='p',
        refant='',
        solint='30s',
        minblperant=3,
        spw=selfcal_spw,
       )
assert os.path.exists(caltable1)


applycal(flagbackup=False,
         gainfield=[],
         interp=[],
         gaintable=[caltable1],
         calwt=[False],
         vis=merged_ms,
         applymode='calonly',
         antenna='*&*',
         spwmap=[],
         parang=True)

imagename = 'NH322_zoom_on_SgrB2M_40to80kms_selfcal_iter1'
if not os.path.exists(imagename+".image.pbcor.fits"):
    tclean(vis=merged_ms,
           imagename=imagename,
           imsize=500,
           cell='0.02arcsec',
           field=field,
           savemodel='modelcolumn',
           restfreq=restfreq,
           nchan=50, # 0.8 km/s channels
           start='40km/s',
           phasecenter='J2000 17h47m20.178 -28d23m04.109',
           niter=10000,
           threshold='7mJy',
           gridder='standard',
           deconvolver='hogbom',
           specmode='cube',
           weighting='briggs',
           pblimit=0.2,
           interactive=False,
           outframe='LSRK',
           datacolumn='corrected',
           robust=0.5,
          )
    makefits(imagename)


caltable2='NH322_selfcal_iter2_phase20s.cal'
gaincal(vis=merged_ms,
        caltable=caltable2,
        field=field,
        calmode='p',
        refant='',
        solint='20s',
        minblperant=3,
        spw=selfcal_spw,
       )
assert os.path.exists(caltable2)


applycal(flagbackup=False,
         gainfield=[],
         interp=[],
         gaintable=[caltable2],
         calwt=[False],
         vis=merged_ms,
         applymode='calonly',
         antenna='*&*',
         spwmap=[],
         parang=True)

imagename = 'NH322_zoom_on_SgrB2M_40to80kms_selfcal_iter2'
if not os.path.exists(imagename+".image.pbcor.fits"):
    tclean(vis=merged_ms,
           imagename=imagename,
           imsize=500,
           cell='0.02arcsec',
           field=field,
           savemodel='modelcolumn',
           restfreq=restfreq,
           nchan=50, # 0.8 km/s channels
           start='40km/s',
           phasecenter='J2000 17h47m20.178 -28d23m04.109',
           niter=10000,
           threshold='5mJy',
           gridder='standard',
           deconvolver='hogbom',
           specmode='cube',
           weighting='briggs',
           pblimit=0.2,
           interactive=False,
           outframe='LSRK',
           datacolumn='corrected',
           robust=0.5,
          )
    makefits(imagename)


caltable3='NH322_selfcal_iter3_phase20s.cal'
gaincal(vis=merged_ms,
        caltable=caltable3,
        field=field,
        calmode='p',
        refant='',
        solint='20s',
        minblperant=3,
        spw=selfcal_spw,
       )
assert os.path.exists(caltable3)


applycal(flagbackup=False,
         gainfield=[],
         interp=[],
         gaintable=[caltable3],
         calwt=[False],
         vis=merged_ms,
         applymode='calonly',
         antenna='*&*',
         spwmap=[],
         parang=True)

imagename = 'NH322_zoom_on_SgrB2M_40to80kms_selfcal_iter3'
if not os.path.exists(imagename+".image.pbcor.fits"):
    tclean(vis=merged_ms,
           imagename=imagename,
           imsize=500,
           cell='0.02arcsec',
           field=field,
           savemodel='modelcolumn',
           restfreq=restfreq,
           nchan=50, # 0.8 km/s channels
           start='40km/s',
           phasecenter='J2000 17h47m20.178 -28d23m04.109',
           niter=10000,
           threshold='3mJy',
           gridder='standard',
           deconvolver='hogbom',
           specmode='cube',
           weighting='briggs',
           pblimit=0.2,
           interactive=False,
           outframe='LSRK',
           datacolumn='corrected',
           robust=0.5,
          )
    makefits(imagename)

for field in ('MN', 'MS', 'SDS'):
    imagename = 'NH322_SgrB2{0}_40to80kms_selfcal_iter3'.format(field)
    if not os.path.exists(imagename+".image.pbcor.fits"):
        tclean(vis=merged_ms,
               imagename=imagename,
               imsize=4000,
               cell='0.03arcsec',
               field='Sgr B2 {0} K'.format(field),
               savemodel='none',
               restfreq=restfreq,
               nchan=50, # 0.8 km/s channels
               start='40km/s',
               niter=10000,
               threshold='5mJy',
               gridder='standard',
               deconvolver='hogbom',
               specmode='cube',
               weighting='briggs',
               pblimit=0.2,
               interactive=False,
               outframe='LSRK',
               datacolumn='corrected',
               robust=0.5,
              )
        makefits(imagename)

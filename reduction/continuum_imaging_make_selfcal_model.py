"""
Overall imaging script to make combined continuum images for Ka, Q, and K bands
"""
import os
import sys
sys.path.append('.')

print(sys.path)

from continuum_imaging_general import myclean, tclean, makefits

from continuum_windows import Qmses, Kamses, Kmses

good_Q_mses = [
 '18A-229_2018_03_06_T01_29_24.948/18A-229.sb35058339.eb35201848.58183.55541637732.ms',
 '18A-229_2018_04_05_T10_59_52.640/18A-229.sb35258391.eb35265194.58213.344589120374.ms',
 '18A-229_2018_04_06_T14_19_50.811/18A-229.sb35258391.eb35276197.58214.498005057874.ms',
 '18A-229_2018_04_18_T13_19_53.878/18A-229.sb35258391.eb35349729.58226.46470898148.ms',
]

imagename = '18A-229_mosaic_for_selfcal'
if not os.path.exists(imagename+'.image.tt0.pbcor.fits'):
    # mosaic for Q-band
    tclean(
           #vis=['../'+x for x in good_Q_mses],
           #spw=[Qmses[x] for x in good_Q_mses],
           vis=['../'+x.replace(".ms","_continuum.ms") for x in good_Q_mses],
           spw='',
           field="Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q",
           phasecenter='J2000 17h47m19.693 -28d23m11.527',
           imsize=[18000,18000],
           cell='0.01arcsec',
           imagename=imagename,
           niter=10000,
           threshold='1mJy',
           robust=0.5,
           gridder='mosaic',
           scales=[0,3,9,27],
           deconvolver='mtmfs',
           specmode='mfs',
           nterms=2,
           weighting='briggs',
           pblimit=0.2,
           interactive=False,
           outframe='LSRK',
           savemodel='none',
          )
    makefits('18A-229_mosaic_for_selfcal', cleanup=False)


    
#myclean(['../'+x for x in good_Q_mses],
#        name='18A-229_combined_for_selfcal',
#        threshold='2mJy', # no signal at 5...
#        spws=[Qmses[x] for x in good_Q_mses],
#       )
#
# myclean(['../'+x for x in Kamses],
#         name='18A-229_combined_for_selfcal',
#         threshold='2mJy',
#         cell='0.015arcsec',
#         fields=['Sgr B2 MN Ka', 'Sgr B2 MS Ka', 'Sgr B2 S Ka', 'Sgr B2 DS1 Ka', 'Sgr B2 DS2 Ka'],
#         spws=[x for x in Kamses.values()],
#        )
# 
# myclean(['../'+x for x in Kmses],
#         name='18A-229_combined_for_selfcal',
#         threshold='2mJy',
#         cell='0.02arcsec',
#         fields=['Sgr B2 MN K', 'Sgr B2 MS K', 'Sgr B2 SDS K',],
#         spws=[x for x in Kmses.values()],
#        )

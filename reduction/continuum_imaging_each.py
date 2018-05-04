"""
Overall imaging script to make combined continuum images for Ka, Q, and K bands
"""
from continuum_imaging_general import myclean, tclean, makefits

from continuum_windows import Qmses, Kamses, Kmses

for ms in Qmses:
    myclean('../'+ms,
            name=ms[:22],
            threshold='5mJy',
            spws=Qmses[ms],
            niter=1000,
            imsize=2000,
            cell='0.04arcsec',
           )

for ms in Kamses:
    myclean('../'+ms,
            name=ms[:22],
            threshold='5mJy',
            cell='0.05arcsec',
            niter=1000,
            imsize=2000,
            fields=['Sgr B2 MN Ka', 'Sgr B2 MS Ka', 'Sgr B2 S Ka', 'Sgr B2 DS1 Ka', 'Sgr B2 DS2 Ka'],
            spws=Kamses[ms],
           )

for ms in Kmses:
    myclean('../'+ms,
            name=ms[:22],
            threshold='5mJy',
            cell='0.08arcsec',
            imsize=2000,
            fields=['Sgr B2 MN K', 'Sgr B2 MS K', 'Sgr B2 SDS K',],
            spws=Kmses[ms],
           )




#myclean(['../'+x for x in Qmses],
#        name='18A-229_combined',
#        threshold='5mJy'
#       )


#for ms in Qmses:
#
#    name = ms[:22]
#
#    myclean('../'+ms,
#            name=name,
#            threshold='5mJy',)
#


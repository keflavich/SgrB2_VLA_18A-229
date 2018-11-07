"""
Image the calibrators to make sure fluxes are sane
"""
import sys
import os
assert os.getenv('SCRIPT_DIR') is not None
sys.path.append(os.getenv('SCRIPT_DIR'))

from continuum_imaging_general import myclean, tclean, makefits

from continuum_windows import all_Qmses, Kamses, Kmses
Qmses = all_Qmses

calibrators = ['J1744-3116', 'J1733-1304', "1331+305=3C286",]

for ms in Qmses:
    myclean('../'+ms,
            name=ms[:22],
            threshold='5mJy',
            spws=Qmses[ms],
            niter=1000,
            imsize=200,
            cell='0.01arcsec',
            fields=calibrators,
            noneg=False,
           )

for ms in Kamses:
    myclean('../'+ms,
            name=ms[:22],
            threshold='5mJy',
            cell='0.01arcsec',
            niter=1000,
            imsize=200,
            spws=Kamses[ms],
            fields=calibrators,
            noneg=False,
           )

for ms in Kmses:
    myclean('../'+ms,
            name=ms[:22],
            threshold='5mJy',
            cell='0.01arcsec',
            imsize=200,
            spws=Kmses[ms],
            fields=calibrators,
            noneg=False,
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


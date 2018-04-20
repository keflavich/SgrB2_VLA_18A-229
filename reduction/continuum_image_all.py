"""
Overall imaging script to make combined continuum images for Ka, Q, and K bands
"""
from continuum_imaging_general import myclean, tclean, makefits

from continuum_windows import Qmses, Kamses, Kmses

myclean(['../'+x for x in Kamses],
        name='18A-229_combined',
        threshold='5mJy',
        cell='0.015arcsec',
        fields=['Sgr B2 MN Ka', 'Sgr B2 MS Ka', 'Sgr B2 S Ka', 'Sgr B2 DS1 Ka', 'Sgr B2 DS2 Ka'],
        spws=[x for x in Kamses.values()],
       )

myclean(['../'+x for x in Kmses],
        name='18A-229_combined',
        threshold='5mJy',
        cell='0.02arcsec',
        fields=['Sgr B2 MN K', 'Sgr B2 MS K', 'Sgr B2 SDS K',],
        spws=[x for x in Kmses.values()],
       )

#myclean(['../'+x for x in Qmses],
#        name='18A-229_combined',
#        threshold='5mJy',
#        spws=[x for x in Qmses.values()],
#       )



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


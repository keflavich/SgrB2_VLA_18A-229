import os
import sys
sys.path.append('.')
from utilities import get_spw_mapping

from ms_lists import Qmses

caltable = '../continuum/18A-229_Q_concatenated_cal_iter2_30s'


for ms in Qmses:
    vis = "../"+ms

    spwmap = get_spw_mapping(vis, caltable)

    print(spwmap, vis, caltable)

    assert os.path.exists(vis)
    assert os.path.exists(caltable)

    applycal(vis=vis, flagbackup=False, gainfield=[],
             interp=['linearperobs,linear'], gaintable=[caltable],
             calwt=[False], applymode='calonly', spwmap=spwmap, parang=True,)

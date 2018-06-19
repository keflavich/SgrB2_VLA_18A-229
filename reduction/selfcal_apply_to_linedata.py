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

    pipeline_tables = [vis+'.hifv_priorcals.s5_5.rq.tbl',
                       vis+'.hifv_priorcals.s5_7.ants.tbl',
                       vis+'.hifv_priorcals.s5_3.gc.tbl',
                       vis+'.hifv_priorcals.s5_4.opac.tbl',
                       vis+'.finaldelay.k',
                       vis+'.finalBPcal.b',
                       vis+'.averagephasegain.g',
                       vis+'.finalphasegaincal.g',
                       vis+'.finalampgaincal.g',
                      ]
    interp = ['', '', '', '', '', 'linear', '', '', '']
    calwt = [False] * len(pipeline_tables)
    spwmap_pipeline = [[]]*len(pipeline_tables)
    gainfield = [''] * len(pipeline_tables)

    # 'linearperobs' doesn't work because we're not applying to the same MS
    # spwmap should just take care of that, though.
    
    # this is without the pipeline tables
    #applycal(vis=vis, flagbackup=False, gainfield=[],
    #         interp=['linear,linear'], gaintable=[caltable],
    #         calwt=[False], applymode='calonly', spwmap=spwmap, parang=True,)

    # with the pipeline tables
    applycal(vis=vis,
             flagbackup=False,
             gainfield=['']+gainfield,
             interp=['linear,linear']+interp,
             gaintable=[caltable]+pipeline_tables,
             calwt=[False]+calwt,
             applymode='calonly',
             spwmap=[spwmap]+spwmap_pipeline,
             parang=True,)

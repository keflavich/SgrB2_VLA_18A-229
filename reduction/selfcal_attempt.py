"""
Self-calibrate the Q-band data on the DePree maps.  This approach completely
discards astrometric information.
"""
import os
#import runpy
#runpy.run_path('continuum_imaging_general.py')
import sys
sys.path.append('.')
from continuum_imaging_general import myclean, tclean, makefits
from continuum_windows import Qmses

from tclean_cli import tclean_cli as tclean
from flagdata_cli import flagdata_cli as flagdata
from ft_cli import ft_cli as ft
from gaincal_cli import gaincal_cli as gaincal
from applycal_cli import applycal_cli as applycal

mses = [
    # commented out = done
# # (already done) '18A-229_2018_03_02_T23_06_49.534/18A-229.sb35058339.eb35183211.58179.45517583333.ms',
# '18A-229_2018_03_03_T15_27_35.951/18A-229.sb35058339.eb35189568.58180.4553891088.ms',
# '18A-229_2018_03_05_T15_05_28.584/18A-229.sb35065347.eb35195562.58182.447515127315.ms',
# ##Ka '18A-229_2018_03_05_T15_05_30.260/18A-229.sb35040205.eb35195564.58182.530614965275.ms',
# '18A-229_2018_03_06_T01_29_24.948/18A-229.sb35058339.eb35201848.58183.55541637732.ms',
# '18A-229_2018_03_06_T12_39_58.178/18A-229.sb35065347.eb35201827.58183.43683233796.ms',
# '18A-229_2018_03_07_T13_19_55.375/18A-229.sb35058339.eb35204985.58184.437571539354.ms',
# '18A-229_2018_03_08_T12_39_54.188/18A-229.sb35065347.eb35212154.58185.43138087963.ms',
# '18A-229_2018_03_10_T12_59_53.135/18A-229.sb35065347.eb35215346.58187.443269247684.ms',
# NOT Q '18A-229_2018_03_23_T15_19_54.203/18A-229.sb35040205.eb35243608.58200.54285351852.ms',
# NOT Q '18A-229_2018_03_25_T12_19_54.375/18A-229.sb35040205.eb35249737.58202.41833868055.ms',
# NOT Q '18A-229_2018_03_28_T17_09_22.432/18A-229.sb35069722.eb35251150.58205.383514664354.ms',
'18A-229_2018_04_05_T10_59_52.640/18A-229.sb35258391.eb35265194.58213.344589120374.ms',
'18A-229_2018_04_06_T14_19_50.811/18A-229.sb35258391.eb35276197.58214.498005057874.ms',
'18A-229_2018_04_18_T13_19_53.878/18A-229.sb35258391.eb35349729.58226.46470898148.ms',
]


# NOT USED now
spw_bb = [('2,4,5,6,7,8,9,11,12,13,14,15,16', 'A1C1'),
          ("17,18,21,22,23,24,25,27,28,29,30,31", 'A2C2'),
          ("33,34,35,36,38,41,43,44,46,47,48", 'B1D1'),
          ("49,51,52,53,54,55,56,57,58,59,60,62,63,64", 'B2D2'),
         ]

for ms in mses:

    assert ms in Qmses

    name = ms[:22]

    ms = '../'+ms

    flagdata(vis=ms, mode='unflag',
             field=('J1744-3116,Sgr B2 N Q,Sgr B2 NM Q,SgrB2 MS Q,'
                    'Sgr B2 S Q,Sgr B2 DS1 Q,Sgr B2 DS2 Q,Sgr B2 DS3 Q'))
    flagdata(vis=ms, mode='manual', autocorr=True)

    ft(vis=ms,
       field='Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q',
       spw='',
       model='../reduction_scripts/DePree_NM_regridNM.image',
       nterms=1)

    #splitvis = '{0}.1744-3116.split.ms'.format(name)

    ## *do not* split out spw to avoid re-mapping later
    #split(vis="../"+ms, outputvis=splitvis,
    #      datacolumn='corrected',
    #      width=512, # averaged each spw to 1 channel
    #      field='J1744-3116',
    #      timebin='5s',)

    pipeline_tables = [ms+'.hifv_priorcals.s5_5.rq.tbl',
                       ms+'.hifv_priorcals.s5_7.ants.tbl',
                       ms+'.hifv_priorcals.s5_3.gc.tbl',
                       ms+'.hifv_priorcals.s5_4.opac.tbl',
                       ms+'.finaldelay.k',
                       ms+'.finalBPcal.b',
                       #ms+'.averagephasegain.g',
                       #ms+'.finalphasegaincal.g',
                       ms+'.finalampgaincal.g',
                      ]

    caltable_nocombine = 'sgrb2m_selfcal_phase_refFLEX_withpipe_{0}_{1}_30ssolint_shortbaselines.cal'.format('nocombine', name)

    if not os.path.exists(caltable_nocombine):

        gaintables = [x for x in pipeline_tables if os.path.exists(x)]
        gainfield = ['' for x in pipeline_tables if os.path.exists(x)]
        interp = ['linear,nearestflag' if 'BPcal' in x else '' for x in pipeline_tables if os.path.exists(x)]


        gaincal(vis=ms,
                caltable=caltable_nocombine,
                field='Sgr B2 NM Q,Sgr B2 MS Q',
                calmode='p',
                refant='',
                solint='30s',
                uvrange='0~2000klambda',
                minblperant=3,
                gaintable=gaintables,
                gainfield=gainfield,
                interp=interp,
               )


    if False:
        for spw, bb in spw_bb:

            caltable = 'sgrb2m_selfcal_phase_refFLEX_withpipe_{0}_{1}_30ssolint_shortbaselines.cal'.format(bb, name)

            if not os.path.exists(caltable):
                gaintables = [x for x in pipeline_tables if os.path.exists(x)]
                gainfield = ['' for x in pipeline_tables if os.path.exists(x)]
                interp = ['linear,nearestflag' if 'BPcal' in x else '' for x in pipeline_tables if os.path.exists(x)]


                gaincal(vis=ms,
                        spw=spw,
                        combine='spw',
                        caltable=caltable,
                        field='Sgr B2 NM Q,Sgr B2 MS Q',
                        calmode='p',
                        refant='',
                        solint='30s',
                        uvrange='0~2000klambda',
                        minblperant=3,
                        gaintable=gaintables,
                        gainfield=gainfield,
                        interp=interp,
                       )



    gaintables = [x for x in pipeline_tables if os.path.exists(x)] + [caltable_nocombine]
    gainfield = ['' for x in pipeline_tables if os.path.exists(x)] + []
    calwt = [False for x in pipeline_tables if os.path.exists(x)] + [False]
    spwmap = [[] for x in pipeline_tables if os.path.exists(x)] + []
    interp = ['linear,nearestflag' if 'BPcal' in x else '' for x in pipeline_tables if os.path.exists(x)] + ['']

    applycal(flagbackup=False,
             gainfield=gainfield,
             interp=interp,
             gaintable=gaintables,
             calwt=calwt,
             vis=ms,
             applymode='calonly',
             antenna='*&*',
             spwmap=spwmap,
             parang=True)

    myclean(vis=ms,
            name=name+'_taper',
            imsize=2000,
            cell='0.04arcsec',
            fields=['Sgr B2 N Q', 'Sgr B2 NM Q', 'Sgr B2 MS Q'],
            uvrange='0~2000klambda',
            threshold='5mJy',)

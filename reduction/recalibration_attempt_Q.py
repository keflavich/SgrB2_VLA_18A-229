import os

mses = [
'18A-229_2018_03_02_T23_06_49.534/18A-229.sb35058339.eb35183211.58179.45517583333.ms',
#'18A-229_2018_03_03_T15_27_35.951/18A-229.sb35058339.eb35189568.58180.4553891088.ms',
#'18A-229_2018_03_05_T15_05_28.584/18A-229.sb35065347.eb35195562.58182.447515127315.ms',
##Ka '18A-229_2018_03_05_T15_05_30.260/18A-229.sb35040205.eb35195564.58182.530614965275.ms',
#'18A-229_2018_03_06_T01_29_24.948/18A-229.sb35058339.eb35201848.58183.55541637732.ms',
'18A-229_2018_03_06_T12_39_58.178/18A-229.sb35065347.eb35201827.58183.43683233796.ms',
#'18A-229_2018_03_07_T13_19_55.375/18A-229.sb35058339.eb35204985.58184.437571539354.ms',
#'18A-229_2018_03_08_T12_39_54.188/18A-229.sb35065347.eb35212154.58185.43138087963.ms',
#'18A-229_2018_03_10_T12_59_53.135/18A-229.sb35065347.eb35215346.58187.443269247684.ms',
]


spw_bb = [('2,4,5,6,7,8,9,11,12,13,14,15,16', 'A1C1'),
          ("17,18,21,22,23,24,25,27,28,29,30,31", 'A2C2'),
          ("33,34,35,36,38,41,43,44,46,47,48", 'B1D1'),
          ("49,51,52,53,54,55,56,57,58,59,60,62,63,64", 'B2D2'),
         ]

for ms in mses:

    name = ms[:22]

    ms = '../'+ms

    #splitvis = '{0}.1744-3116.split.ms'.format(name)

    ## *do not* split out spw to avoid re-mapping later
    #split(vis="../"+ms, outputvis=splitvis,
    #      datacolumn='corrected',
    #      width=512, # averaged each spw to 1 channel
    #      field='J1744-3116',
    #      timebin='5s',)

    #flagdata(vis=ms, mode='unflag', field='J1744-3116')
    #flagdata(vis=splitvis, mode='manual', autocorr=True)

    for spw, bb in spw_bb:

        caltable = 'phase_refFLEX_withpipe_{0}_{1}_60ssolint_shortbaselines.cal'.format(bb, name)

        if not os.path.exists(caltable):
            pipeline_tables = [ms+'.hifv_priorcals.s5_5.rq.tbl',
                               ms+'.hifv_priorcals.s5_7.ants.tbl',
                               ms+'.hifv_priorcals.s5_3.gc.tbl',
                               ms+'.hifv_priorcals.s5_4.opac.tbl',
                               ms+'.finaldelay.k',
                               ms+'.finalBPcal.b',
                               #'18A-229.sb35058339.eb35183211.58179.45517583333.ms.averagephasegain.g',
                               #'18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalphasegaincal.g',
                               ms+'.finalampgaincal.g',
                              ]

            gaintables = [x for x in pipeline_tables if os.path.exists(x)]
            gainfield = ['' for x in pipeline_tables if os.path.exists(x)]
            interp = ['linear,nearestflag' if 'BPcal' in x else '' for x in pipeline_tables if os.path.exists(x)]

            #gaincal(vis=splitvis,
            #        spw=spw, combine='spw',
            #        caltable=caltable,
            #        field='J1744-3116', calmode='p',
            #        refant='ea21', solint='5s')
            gaincal(vis=ms,
                    spw=spw,
                    combine='spw',
                    caltable=caltable,
                    field='J1744-3116',
                    calmode='p',
                    refant='',
                    solint='60s',
                    uvrange='0~800klambda',
                    minblperant=3,
                    gaintable=gaintables,
                    gainfield=gainfield,
                    interp=interp,
                   )

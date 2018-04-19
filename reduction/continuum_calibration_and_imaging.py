"""
These are one-off, copy-and-paste commands from when I was attempting to
improve the calibration using the phase calibrator.
This isn't a script that should be run
"""

# '/lustre/aginsbur/sgrb2/18A-229/18A-229_2018_03_02_T23_06_49.534'

gaincal(vis='18A-229.sb35058339.eb35183211.58179.45517583333.ms',
        spw='2,4,5,6,7,8,9,11,12,13,14,15,16', combine='spw',
        caltable='phase_refea21_withpipe_A1C1_60ssolint.cal', field='J1744-3116', calmode='p',
        refant='ea21', solint='60s',
        gaintable=['18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_5.rq.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_7.ants.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_3.gc.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_4.opac.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finaldelay.k',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalBPcal.b',
                   #'18A-229.sb35058339.eb35183211.58179.45517583333.ms.averagephasegain.g',
                   #'18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalphasegaincal.g',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalampgaincal.g',
                  ],
        gainfield=['', '', '', '', '', '', '', ],
        interp=['', '', '', '', '', 'linear,nearestflag', '', ],
       )

# TEST
# gaincal(vis='18A-229.sb35058339.eb35183211.58179.45517583333.ms',
#         spw='2,4,5,6,7,8,9,11,12,13,14,15,16', combine='spw',
#         caltable='TEST_a1c1.cal', field='J1744-3116', calmode='p',
#         refant='ea21', solint='5s',)

gaincal(vis='18A-229.sb35058339.eb35183211.58179.45517583333.ms',
        spw="17,18,21,22,23,24,25,27,28,29,30,31",
        combine='spw',
        caltable='phase_refea21_withpipe_A2C2.cal', field='J1744-3116', calmode='p',
        refant='ea21', solint='5s',
        gaintable=['18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_5.rq.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_7.ants.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_3.gc.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_4.opac.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finaldelay.k',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalBPcal.b',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.averagephasegain.g',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalphasegaincal.g',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalampgaincal.g'])

gaincal(vis='18A-229.sb35058339.eb35183211.58179.45517583333.ms',
        spw="33,34,35,36,38,41,43,44,46,47,48",
        combine='spw',
        caltable='phase_refea21_withpipe_B1D1.cal', field='J1744-3116', calmode='p',
        refant='ea21', solint='5s',
        gaintable=['18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_5.rq.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_7.ants.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_3.gc.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_4.opac.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finaldelay.k',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalBPcal.b',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.averagephasegain.g',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalphasegaincal.g',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalampgaincal.g'])

gaincal(vis='18A-229.sb35058339.eb35183211.58179.45517583333.ms',
        spw="49,51,52,53,54,55,56,57,58,59,60,62,63,64",
        combine='spw',
        caltable='phase_refea21_withpipe_B2D2.cal', field='J1744-3116', calmode='p',
        refant='ea21', solint='5s',
        gaintable=['18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_5.rq.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_7.ants.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_3.gc.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_4.opac.tbl',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finaldelay.k',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalBPcal.b',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.averagephasegain.g',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalphasegaincal.g',
                   '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalampgaincal.g'])




applycal(flagbackup=False,
         gainfield=['', '', '', '', '', '', '', '', '', '', '', '', ''],
         interp=['', '', '', '', '', 'linear,nearestflag', '', '', '', '', '', '', ''],
         gaintable=['18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_3.gc.tbl',
                    '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_4.opac.tbl',
                    '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_5.rq.tbl',
                    '18A-229.sb35058339.eb35183211.58179.45517583333.ms.hifv_priorcals.s5_7.ants.tbl',
                    '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finaldelay.k',
                    '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalBPcal.b',
                    '18A-229.sb35058339.eb35183211.58179.45517583333.ms.averagephasegain.g',
                    '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalampgaincal.g',
                    '18A-229.sb35058339.eb35183211.58179.45517583333.ms.finalphasegaincal.g',
                    'phase_refea21_withpipe_A1C1.cal',
                    'phase_refea21_withpipe_A2C2.cal',
                    'phase_refea21_withpipe_B1D1.cal',
                    'phase_refea21_withpipe_B2D2.cal',
                   ],
         calwt=[False]*13,
         vis='18A-229.sb35058339.eb35183211.58179.45517583333.ms',
         applymode='calonly', antenna='*&*',
         spwmap=[[], [], [], [], [],
                 [], [], [], [],
                 # mine below:
                 [0, 1,]+[2]*15+[17]*16+[33]*16+[49]*16,
                 [0, 1,]+[2]*15+[17]*16+[33]*16+[49]*16,
                 [0, 1,]+[2]*15+[17]*16+[33]*16+[49]*16,
                 [0, 1,]+[2]*15+[17]*16+[33]*16+[49]*16,
                ],
         parang=True)


applycal(gaintable=['../recal/phase_refea21_withpipe_A1C1_18A-229_2018_03_03_T15.cal',
                    #'phase_refea21_withpipe_A2C2_18A-229_2018_03_03_T15.cal',
                    #'../recal/phase_refea21_withpipe_B1D1_18A-229_2018_03_03_T15.cal',
                    '../recal/phase_refea21_withpipe_B2D2_18A-229_2018_03_03_T15.cal',
                   ],
         vis='18A-229.sb35058339.eb35183211.58179.45517583333.corrected.ms',
         applymode='calonly', antenna='*&*',
         spwmap=[[0, 1,]+[2]*15+[17]*16+[33]*16+[49]*16,
                 #[0, 1,]+[2]*15+[17]*16+[33]*16+[49]*16,
                 #[0, 1,]+[2]*15+[17]*16+[33]*16+[49]*16,
                 [0, 1,]+[2]*15+[17]*16+[33]*16+[49]*16,
                ],
         parang=True)



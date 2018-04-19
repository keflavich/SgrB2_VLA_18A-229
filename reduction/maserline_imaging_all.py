"""
Script to create merged images of the masers and other lines
"""

from maserline_imaging import (myclean, tclean, makefits, siov1clean,
                               siov2clean, ch3ohmaserclean, ch3ohthermalclean,
                               csclean, so10clean, ch3ohKamaserclean,
                               h2oclean,
                              )

Qmses = [
'18A-229_2018_03_02_T23_06_49.534/18A-229.sb35058339.eb35183211.58179.45517583333.ms',
'18A-229_2018_03_03_T15_27_35.951/18A-229.sb35058339.eb35189568.58180.4553891088.ms',
'18A-229_2018_03_05_T15_05_28.584/18A-229.sb35065347.eb35195562.58182.447515127315.ms',
#Ka '18A-229_2018_03_05_T15_05_30.260/18A-229.sb35040205.eb35195564.58182.530614965275.ms',
'18A-229_2018_03_06_T01_29_24.948/18A-229.sb35058339.eb35201848.58183.55541637732.ms',
'18A-229_2018_03_06_T12_39_58.178/18A-229.sb35065347.eb35201827.58183.43683233796.ms',
'18A-229_2018_03_07_T13_19_55.375/18A-229.sb35058339.eb35204985.58184.437571539354.ms',
'18A-229_2018_03_08_T12_39_54.188/18A-229.sb35065347.eb35212154.58185.43138087963.ms',
'18A-229_2018_03_10_T12_59_53.135/18A-229.sb35065347.eb35215346.58187.443269247684.ms',
#'18A-229_2018_03_23_T15_19_54.203/18A-229.sb35040205.eb35243608.58200.54285351852.ms',
#'18A-229_2018_03_25_T12_19_54.375/18A-229.sb35040205.eb35249737.58202.41833868055.ms',
#'18A-229_2018_03_28_T17_09_22.432/18A-229.sb35069722.eb35251150.58205.383514664354.ms',
#'18A-229_2018_04_05_T10_59_52.640/18A-229.sb35258391.eb35265194.58213.344589120374.ms',
#'18A-229_2018_04_06_T14_19_50.811/18A-229.sb35258391.eb35276197.58214.498005057874.ms',
#'18A-229_2018_04_18_T13_19_53.878/18A-229.sb35258391.eb35349729.58226.46470898148.ms',
]

#siov1clean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
#siov2clean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
#ch3ohmaserclean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
#ch3ohthermalclean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
#csclean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')

#ch3ohmaserclean(['../'+x for x in mses], name='18A-229_combined', threshold='25mJy',
#                fields=["Sgr B2 S Q", "Sgr B2 DS1 Q", "Sgr B2 DS2 Q", "Sgr B2 DS3 Q",])

#for ms in mses:
#
#    name = ms[:22]
#
#    siov1clean('../'+ms, name=name, threshold='50mJy',)


Kamses = [
    '18A-229_2018_03_05_T15_05_30.260/18A-229.sb35040205.eb35195564.58182.530614965275.ms',
    '18A-229_2018_03_23_T15_19_54.203/18A-229.sb35040205.eb35243608.58200.54285351852.ms',
    '18A-229_2018_03_25_T12_19_54.375/18A-229.sb35040205.eb35249737.58202.41833868055.ms',
    '18A-229_2018_03_29_T15_19_51.154/18A-229.sb35040205.eb35251857.58206.540094131946.ms',
]

#ch3ohKamaserclean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#so10clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')

Kmses = [
    '18A-229_2018_03_29_T13_19_55.276/18A-229.sb35069722.eb35251855.58206.45698415509.ms',
    '18A-229_2018_03_28_T17_09_22.432/18A-229.sb35069722.eb35251150.58205.383514664354.ms',
]

h2oclean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')


for fn in glob.glob("18A-229_2018_0*/*_continuum.ms"):
    msmd.open(fn)
    restfreqs = msmd.restfreqs()
    msmd.close()

    if restfreqs['0']['m0']['value'] < 40e9:
        # not Q-band
        continue

    ms.open(fn)
    print("{fn}: min={min:0.4g} max={max:0.4g} median={median:0.4g} mean={mean:0.4g}"
          .format(fn=fn, **ms.statistics(column='DATA', complex_value='amp', spw='0', field='Sgr B2 MS Q')['']))
    ms.close()
"""
18A-229_2018_03_06_T01_29_24.948/18A-229.sb35058339.eb35201848.58183.55541637732_continuum.ms: min=0.0001102 max=5.176 median=0.1771 mean=0.2241
18A-229_2018_03_10_T12_59_53.135/18A-229.sb35065347.eb35215346.58187.443269247684_continuum.ms: min=0.001623 max=173 median=4.263 mean=5.612
18A-229_2018_04_05_T10_59_52.640/18A-229.sb35258391.eb35265194.58213.344589120374_continuum.ms: min=0.0003424 max=8.593 median=1.04 mean=1.169
18A-229_2018_03_05_T15_05_28.584/18A-229.sb35065347.eb35195562.58182.447515127315_continuum.ms: min=0.0001478 max=8.243 median=0.8084 mean=0.9138
18A-229_2018_03_03_T15_27_35.951/18A-229.sb35058339.eb35189568.58180.4553891088_continuum.ms: min=0.00105 max=8.42 median=0.7338 mean=0.8465
18A-229_2018_04_18_T13_19_53.878/18A-229.sb35258391.eb35349729.58226.46470898148_continuum.ms: min=0.001338 max=5.832 median=0.6901 mean=0.7676
18A-229_2018_04_06_T14_19_50.811/18A-229.sb35258391.eb35276197.58214.498005057874_continuum.ms: min=0.0006005 max=13.74 median=0.7119 mean=0.8367
18A-229_2018_03_02_T23_06_49.534/18A-229.sb35058339.eb35183211.58179.45517583333_continuum.ms: min=0.0007638 max=13.72 median=0.7438 mean=0.8717
18A-229_2018_03_07_T13_19_55.375/18A-229.sb35058339.eb35204985.58184.437571539354_continuum.ms: min=0.0008296 max=11.26 median=0.7887 mean=0.9418
18A-229_2018_03_08_T12_39_54.188/18A-229.sb35065347.eb35212154.58185.43138087963_continuum.ms: min=0.000282 max=4.31 median=0.2546 mean=0.2992
18A-229_2018_03_06_T12_39_58.178/18A-229.sb35065347.eb35201827.58183.43683233796_continuum.ms: min=0.0002581 max=12.42 median=0.8085 mean=0.9537
"""


for fn in glob.glob("18A-229_2018_0*/18A*[0-9].ms"):
    msmd.open(fn)
    restfreqs = msmd.reffreq(2)
    msmd.close()

    if restfreqs['m0']['value'] < 40e9:
        # not Q-band
        continue

    ms.open(fn)
    print("DATA {fn}: min={min:0.4g} max={max:0.4g} median={median:0.4g} mean={mean:0.4g}"
          .format(fn=fn, **ms.statistics(column='DATA', complex_value='amp', spw='2', field='Sgr B2 MS Q')['']))
    print("CORRECTED {fn}: min={min:0.4g} max={max:0.4g} median={median:0.4g} mean={mean:0.4g}"
          .format(fn=fn, **ms.statistics(column='CORRECTED', complex_value='amp', spw='2', field='Sgr B2 MS Q')['']))
    ms.close()

"""
DATA 18A-229_2018_03_06_T01_29_24.948/18A-229.sb35058339.eb35201848.58183.55541637732.ms: min=8.046e-07 max=0.02032 median=0.003223 mean=0.003457
CORRECTED 18A-229_2018_03_06_T01_29_24.948/18A-229.sb35058339.eb35201848.58183.55541637732.ms: min=7.616e-05 max=13.91 median=0.4149 mean=0.5211
DATA 18A-229_2018_03_10_T12_59_53.135/18A-229.sb35065347.eb35215346.58187.443269247684.ms: min=9.5e-07 max=0.01632 median=0.003115 mean=0.003335
CORRECTED 18A-229_2018_03_10_T12_59_53.135/18A-229.sb35065347.eb35215346.58187.443269247684.ms: min=0.002958 max=427.5 median=10.06 mean=13.14
DATA 18A-229_2018_04_05_T10_59_52.640/18A-229.sb35258391.eb35265194.58213.344589120374.ms: min=8.872e-07 max=0.01743 median=0.003032 mean=0.003247
CORRECTED 18A-229_2018_04_05_T10_59_52.640/18A-229.sb35258391.eb35265194.58213.344589120374.ms: min=0.0008108 max=23.21 median=2.465 mean=2.755
DATA 18A-229_2018_03_05_T15_05_28.584/18A-229.sb35065347.eb35195562.58182.447515127315.ms: min=1.12e-07 max=0.01644 median=0.003086 mean=0.003305
CORRECTED 18A-229_2018_03_05_T15_05_28.584/18A-229.sb35065347.eb35195562.58182.447515127315.ms: min=9.171e-05 max=22.49 median=1.885 mean=2.119
DATA 18A-229_2018_03_03_T15_27_35.951/18A-229.sb35058339.eb35189568.58180.4553891088.ms: min=2.494e-07 max=0.01407 median=0.002655 mean=0.002841
CORRECTED 18A-229_2018_03_03_T15_27_35.951/18A-229.sb35058339.eb35189568.58180.4553891088.ms: min=0.0001102 max=17.3 median=1.47 mean=1.679
DATA 18A-229_2018_04_18_T13_19_53.878/18A-229.sb35258391.eb35349729.58226.46470898148.ms: min=1.658e-06 max=0.01798 median=0.003282 mean=0.003514
CORRECTED 18A-229_2018_04_18_T13_19_53.878/18A-229.sb35258391.eb35349729.58226.46470898148.ms: min=0.0006633 max=14.93 median=1.606 mean=1.77
DATA 18A-229_2018_04_06_T14_19_50.811/18A-229.sb35258391.eb35276197.58214.498005057874.ms: min=1.776e-06 max=0.01801 median=0.00328 mean=0.003511
CORRECTED 18A-229_2018_04_06_T14_19_50.811/18A-229.sb35258391.eb35276197.58214.498005057874.ms: min=0.0007699 max=34.39 median=1.656 mean=1.938
DATA 18A-229_2018_03_02_T23_06_49.534/18A-229.sb35058339.eb35183211.58179.45517583333.ms: min=5.061e-07 max=0.01895 median=0.003102 mean=0.003324
CORRECTED 18A-229_2018_03_02_T23_06_49.534/18A-229.sb35058339.eb35183211.58179.45517583333.ms: min=0.0002519 max=31.95 median=1.735 mean=2.018
DATA 18A-229_2018_03_07_T13_19_55.375/18A-229.sb35058339.eb35204985.58184.437571539354.ms: min=2.615e-07 max=0.01675 median=0.003079 mean=0.003299
CORRECTED 18A-229_2018_03_07_T13_19_55.375/18A-229.sb35058339.eb35204985.58184.437571539354.ms: min=0.0001026 max=28.57 median=1.844 mean=2.187
DATA 18A-229_2018_03_08_T12_39_54.188/18A-229.sb35065347.eb35212154.58185.43138087963.ms: min=2.534e-07 max=0.01742 median=0.003047 mean=0.003268
CORRECTED 18A-229_2018_03_08_T12_39_54.188/18A-229.sb35065347.eb35212154.58185.43138087963.ms: min=4.678e-05 max=9.192 median=0.5974 mean=0.6976
DATA 18A-229_2018_03_06_T12_39_58.178/18A-229.sb35065347.eb35201827.58183.43683233796.ms: min=7.501e-07 max=0.01878 median=0.003085 mean=0.003305
CORRECTED 18A-229_2018_03_06_T12_39_58.178/18A-229.sb35065347.eb35201827.58183.43683233796.ms: min=0.0003601 max=26.36 median=1.891 mean=2.219
"""


for fn in glob.glob("*amp*cal"):
    tb.open(fn)
    cp = tb.getcol('CPARAM').ravel().real
    tb.close()
    ok = cp.real != 1
    print("{fn}: mean={mean:0.4g} median={median:0.4g}"
          .format(fn=fn, mean=cp[ok].mean(), median=np.median(cp[ok])))

"""
18A-229_2018_03_02_T23_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.5354 median=0.4705
18A-229_2018_03_03_T15_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.3954 median=0.3603
18A-229_2018_03_05_T15_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.5781 median=0.5078
18A-229_2018_03_06_T01_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.2717 median=0.2411
18A-229_2018_03_06_T12_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.6094 median=0.5185
18A-229_2018_03_07_T13_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.5606 median=0.5044
18A-229_2018_03_08_T12_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.3053 median=0.2568
18A-229_2018_03_10_T12_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=1.953 median=1.148
18A-229_2018_04_05_T10_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.625 median=0.4924
18A-229_2018_04_06_T14_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.5092 median=0.4341
18A-229_2018_04_18_T13_sgrb2_selfcal_amp_INFsolint_dontuse.cal: mean=0.5724 median=0.4894
"""




for fn in glob.glob("18A-229_2018_0*/18A*[0-9].ms"):
    msmd.open(fn)
    restfreqs = msmd.reffreq(2)
    msmd.close()

    if restfreqs['m0']['value'] > 30e9:
        # Ka or Q-band
        continue

    ms.open(fn)
    print("DATA {fn}: min={min:0.4g} max={max:0.4g} median={median:0.4g} mean={mean:0.4g}"
          .format(fn=fn, **ms.statistics(column='DATA', complex_value='amp', spw='2', field='Sgr B2 MS K')['']))
    print("CORRECTED {fn}: min={min:0.4g} max={max:0.4g} median={median:0.4g} mean={mean:0.4g}"
          .format(fn=fn, **ms.statistics(column='CORRECTED', complex_value='amp', spw='2', field='Sgr B2 MS K')['']))
    ms.close()


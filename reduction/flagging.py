import os
from flagdata_cli import flagdata_cli as flagdata
from taskinit import casalog

def get_flagonline_base(fn):
    comps = fn.split("/")
    basedir = comps[1]
    ms = comps[2]
    msbase = ms.split("_")[0]

    return os.path.join('..', 'reduction_scripts', basedir, msbase+".flagonline.txt")

for suffix in ("_split_for_selfcal", "", ):


    vis='../18A-229_2018_04_05_T10_59_52.640/18A-229.sb35258391.eb35265194.58213.344589120374_continuum{0}.ms'.format(suffix)

    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    # high and discrepant amplitudes
    # conservative: flagdata(vis=vis, mode='manual', antenna='ea24&ea25', spw='23,24', correlation='LL')
    # aggressive:
    flagdata(vis=vis, mode='manual', antenna='ea24&ea25', spw='', correlation='LL')
    # no solutions =(
    flagdata(vis=vis, mode='manual', antenna='ea18', spw='', correlation='')
    # EA19 is OK on NM, but not MS or N.  ??bad pointing??
    flagdata(vis=vis, mode='manual', antenna='ea19', spw='', correlation='')
    flagdata(vis=vis, mode='manual', antenna='ea14', timerange='09:55:00~10:40:00')
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7

    vis='../18A-229_2018_03_10_T12_59_53.135/18A-229.sb35065347.eb35215346.58187.443269247684_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    # conservative: flagdata(vis=vis, mode='manual', antenna='ea24&ea25', spw='4,5,6,7,13', correlation='LL')
    # aggressive:
    flagdata(vis=vis, mode='manual', antenna='ea24&ea25', spw='', correlation='LL')
    flagdata(vis=vis, mode='manual', antenna='ea24', spw='', correlation='LL')
    flagdata(vis=vis, mode='manual', antenna='ea25&ea10,ea21', spw='', correlation='RR')
    flagdata(vis=vis, mode='manual', antenna='ea19')
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7

    vis='../18A-229_2018_03_03_T15_27_35.951/18A-229.sb35058339.eb35189568.58180.4553891088_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    # ea19 subreflector, as usual
    # ea25 had some subreflector flags
    flagdata(vis=vis, mode='manual', antenna='ea18,ea19')
    # ea14, 28, 2, 3, 23, 22, 25, 11, 12 are all at least somewhat quesitonable.
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7


    vis='../18A-229_2018_03_05_T15_05_28.584/18A-229.sb35065347.eb35195562.58182.447515127315_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    # ea19 flubbed several test gains, as did 03.  but 01 and 18 were fine?
    flagdata(vis=vis, mode='manual', antenna='ea03,ea01,ea18', )
    # ea9 still had a bad subreflector
    flagdata(vis=vis, mode='manual', antenna='ea19', )
    flagdata(vis=vis, mode='manual', antenna='ea25', spw='17~32') # just one poln, but not sure which
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7


    vis='../18A-229_2018_03_06_T01_29_24.948/18A-229.sb35058339.eb35201848.58183.55541637732_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    flagdata(vis=vis, mode='manual', antenna='ea19')
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7


    vis='../18A-229_2018_03_06_T12_39_58.178/18A-229.sb35065347.eb35201827.58183.43683233796_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    # ea19 subreflector
    flagdata(vis=vis, mode='manual', antenna='ea18,ea19', spw='', correlation='')
    # ea28 high-freq issues
    flagdata(vis=vis, mode='manual', antenna='ea28', spw='17~32')
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7


    vis='../18A-229_2018_03_07_T13_19_55.375/18A-229.sb35058339.eb35204985.58184.437571539354_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    flagdata(vis=vis, mode='manual', antenna='ea19')
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7


    # this whole data set appears to just be awful
    vis='../18A-229_2018_03_08_T12_39_54.188/18A-229.sb35065347.eb35212154.58185.43138087963_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    flagdata(vis=vis, mode='manual', antenna='ea19')
    flagdata(vis=vis, mode='manual', antenna='ea03', spw='', correlation='',
             timerange='12:05:00~12:12:00')
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7


    vis='../18A-229_2018_04_06_T14_19_50.811/18A-229.sb35258391.eb35276197.58214.498005057874_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    flagdata(vis=vis, mode='manual', antenna='ea19')
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7


    vis='../18A-229_2018_04_18_T13_19_53.878/18A-229.sb35258391.eb35349729.58226.46470898148_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    flagdata(vis=vis, mode='manual', antenna='ea19')
    flagdata(vis=vis, mode='manual', antenna='ea07,ea17,ea22', spw='36~49') #  EVLA_Q#B2D2
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7

    # was there a reason I just excluded this one?
    vis='../18A-229_2018_03_02_T23_06_49.534/18A-229.sb35058339.eb35183211.58179.45517583333_continuum{0}.ms'.format(suffix)
    flagdata(vis=vis, mode='unflag')
    flagdata(vis=vis, mode='quack', quackmode='beg', quackinterval=10.0)
    # these get no solns, maybe don't detect src?
    # ea19 had a subreflector error; it was missing phase solutions for many phasecal obs
    flagdata(vis=vis, mode='manual', antenna='ea18')
    flagdata(vis=vis, mode='manual', antenna='ea19')
    # maybe ea14.  Part of ea28?  ea28 looks like it had problems in one baseband
    flagdata(vis=vis, mode='manual', antenna='ea28', spw='17~32')
    # ea10, ea23 have some questionable features...
    flagfile = get_flagonline_base(vis)
    if os.path.exists(flagfile):
        flagdata(vis=vis, inpfile=flagfile, mode='list')
    else:
        raise ValueError("Flagfile {0} does not exist".format(flagfile))
    summary = flagdata(vis=vis, mode='summary')
    casalog.post("Flag fraction = {0}".format(summary['flagged'] / summary['total']))
    assert summary['flagged'] / summary['total'] < 0.7


    # FOR ALL: flag out CH3OH line.  This is done in the selfcal_post_repipelining script

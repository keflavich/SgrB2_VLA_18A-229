"""
In September 2018, I discovered that almost all of the measurement sets are
fully populated with uncalibrated data in the 'corrected' column, despite the
pipeline having been run.  This script copies the data from rng9000,
reapplies the calibration tables, then re-splits the continuum
Run this from /lustre/aginsbur/sgrb2/18A-229 on rng9000
"""

import os
import sys
import glob
import shutil
import socket
import datetime
assert os.getenv('SCRIPT_DIR') is not None
sys.path.append(os.getenv('SCRIPT_DIR'))
from continuum_imaging_general import myclean, tclean, makefits
from continuum_windows import Qmses

from flagdata_cli import flagdata_cli as flagdata
from applycal_cli import applycal_cli as applycal
from split_cli import split_cli as split

cwd = os.getcwd()
assert cwd == "/lustre/aginsbur/sgrb2/18A-229"

for dir in glob.glob("18A-229*"):
    os.chdir(dir)

    avgphasegain = glob.glob("*.ms.averagephasegain.g")
    assert len(avgphasegain) == 1

    ms = avgphasegain[0][:-19]
    fullpathms = os.path.join(dir, ms)

    if os.path.exists('done_recalibrating_{0}'.format(ms)):
        print("Skipping {0}".format(ms))
        os.chdir(cwd)
        continue

    if fullpathms not in Qmses:
        print("Skipping non-Q-band MS {0}".format(ms))
        os.chdir(cwd)
        continue

    if os.path.exists('WORKING'):
        print("Skipping {0} because it's actively being worked on.".format(ms))
        os.chdir(cwd)
        continue

    with open('WORKING', 'w') as fh:
        fh.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if not os.path.exists(ms):
        rngms = "/home/rng90002/sgrb2/18A-229/{0}".format(ms)
        if not os.path.exists(rngms):
            print("Skipping {0} because /home/rng90002 doesn't exist".format(rngms))
            os.remove('WORKING')
            os.chdir(cwd)
            continue
        print("Copying {0} to {1}/{2}".format(rngms, dir, ms))
        shutil.copytree(rngms, ms)

        if socket.gethostname() == "rng9000":
            print("Done copying; moving on...")
            os.remove('WORKING')
            os.chdir(cwd)
            continue

    def find_file(globstr):
        result = glob.glob(globstr)
        if len(result) != 1:
            raise ValueError("Found wrong # of tbls: {0} from {1} in {2}"
                             .format(result, globstr, dir))
        return result[0]

    gc_tbl = find_file("*_3.gc.tbl")
    opac_tbl = find_file("*_4.opac.tbl")
    rq_tbl = find_file('*_5.rq.tbl')
    ants_tbl = find_file('*_7.ants.tbl')

    applycal(vis=ms,
             field='"Sgr B2 N Q",J1733-1304,"Sgr B2 DS3 Q","Sgr B2 MS Q","Sgr B2 DS2 Q","Sgr B2 DS1 Q","Sgr B2 S Q","Sgr B2 NM Q",J1744-3116,"1331+305=3C286"',
             spw='',
             antenna='',
             gaintable=[gc_tbl,
                        opac_tbl,
                        rq_tbl,
                        ants_tbl,
                        ms+'.finaldelay.k',
                        ms+'.finalBPcal.b',
                        ms+'.averagephasegain.g',
                        ms+'.finalampgaincal.g',
                        ms+'.finalphasegaincal.g'],
             gainfield=['', '', '', '', '', '', '', '', ''],
             spwmap=[[], [], [], [], [], [], [], [], []],
             interp=['', '', '', '', '', 'linear,nearestflag', '', '', ''],
             calwt=[False, False, False, False, False, False, False, False, False])

    cont_ms = ms[:-3]+"_continuum.ms"

    if os.path.exists(cont_ms):
        os.rename(cont_ms, "_"+cont_ms)

    # flag edge channels
    flagchans = ",".join(["{0}:0~5;123~128".format(xx) for xx in
                          Qmses[fullpathms].split(",")])
    flagdata(vis=ms, mode='manual', spw=flagchans)

    # flag CH3OH maser
    flagdata(vis=ms, mode='manual',
             spw='44054800170~44084179830Hz:44054800170~44084179830Hz')

    split(vis=ms,
          outputvis=cont_ms,
          field=('Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,'
                 'Sgr B2 S Q,Sgr B2 DS1 Q,Sgr B2 DS2 Q,Sgr B2 DS3 Q'),
          width=16,
          spw=Qmses[fullpathms],
         )

    # Unflag CH3OH maser
    flagdata(vis=ms, mode='unflag',
             spw='44054800170~44084179830Hz:44054800170~44084179830Hz')

    with open('done_recalibrating_{0}'.format(ms), 'w') as fh:
        fh.write("cont_ms={0}, ms={1}".format(cont_ms, ms))

    os.remove('WORKING')

    os.chdir(cwd)

import os
from plotms_cli import plotms_cli as plotms
assert os.getenv('SCRIPT_DIR') is not None
sys.path.append(os.getenv('SCRIPT_DIR'))
from continuum_imaging_general import myclean, makefits
from continuum_windows import Qmses
from taskinit import msmdtool
msmd = msmdtool()


def dpath(x):
    return os.path.join("diagnostic_figures/", x)

for ms,contspw in Qmses.items():
    basename = os.path.split(ms)[-1][:-3]

    msmd.open('../'+ms)
    antennae = msmd.antennanames()
    msmd.close()

    for ant in antennae:
        plotms(vis='../'+ms,
               xaxis='time',
               yaxis='phase',
               field='J1744-3116',
               showgui=False,
               antenna=ant,
               plotfile=dpath(basename+"_J1744-3116_phasevstime_{0}.png".format(ant)),
               avgtime='60',
               avgchannel='128',
               spw=contspw,
               coloraxis='corr',
               ydatacolumn='corrected',
              )

        plotms(vis='../'+ms,
               xaxis='time',
               yaxis='amp',
               field='J1744-3116',
               showgui=False,
               antenna=ant,
               plotfile=dpath(basename+"_J1744-3116_ampvstime_{0}.png".format(ant)),
               avgtime='60',
               avgchannel='128',
               spw=contspw,
               coloraxis='corr',
               ydatacolumn='corrected',
              )

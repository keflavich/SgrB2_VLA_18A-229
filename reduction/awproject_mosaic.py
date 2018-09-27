import os
assert os.getenv('SCRIPT_DIR') is not None
sys.path.append(os.getenv('SCRIPT_DIR'))
from tclean_cli import tclean_cli as tclean
from continuum_imaging_general import makefits
from continuum_windows import Qmses

# ms = 'continuum_concatenated_selfcal_wterms.ms'

mses = list(Qmses.keys())

fullpath_mses = ['../' + ms[:-3] + "_continuum_split_for_selfcal.ms"
                 for ms in mses if ms in Qmses]
ms = fullpath_mses

imagename='18A-229_SgrB2_M_NM_M_S_mosaic_awproject'
tclean(vis=ms,
       spw='',
       field="Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q",
       phasecenter='J2000 17h47m19.693 -28d23m11.527',
       imsize=[9000,9000],
       cell='0.02arcsec',
       imagename=imagename,
       niter=0,   # first iteration to create the cache
       threshold='1mJy',
       robust=0.5,
       gridder='awproject',
       rotatepastep=5.0,
       wprojplanes=64,
       scales=[0,3,9],
       deconvolver='mtmfs',
       specmode='mfs',
       nterms=2,
       weighting='briggs',
       pblimit=0.05,
       interactive=False,
       outframe='LSRK',
       savemodel='none',
       parallel=True,
       cfcache=imagename+".cfcache",
      )
tclean(vis=ms,
       spw='',
       field="Sgr B2 N Q,Sgr B2 NM Q,Sgr B2 MS Q,Sgr B2 S Q",
       phasecenter='J2000 17h47m19.693 -28d23m11.527',
       imsize=[9000,9000],
       cell='0.02arcsec',
       imagename=imagename,
       niter=10000,
       threshold='1mJy',
       robust=0.5,
       gridder='awproject',
       rotatepastep=5.0,
       wprojplanes=64,
       scales=[0,3,9],
       deconvolver='mtmfs',
       specmode='mfs',
       nterms=2,
       weighting='briggs',
       pblimit=0.05,
       interactive=False,
       outframe='LSRK',
       savemodel='none',
       parallel=True,
       cfcache=imagename+".cfcache",
      )
makefits(imagename)


do_south = False
if do_south:
    ms = 'continuum_concatenated_selfcal_wterms.ms'
    imagename='18A-229_SgrB2_SDS_mosaic_awproject'
    tclean(vis=ms,
           spw='',
           field="Sgr B2 S Q,Sgr B2 DS1 Q, Sgr B2 DS2 Q, Sgr B2 DS3 Q",
           phasecenter='J2000 17h47m21.371 -28d24m41.085',
           imsize=[9000,9000],
           cell='0.02arcsec',
           imagename=imagename,
           niter=10000,
           threshold='1mJy',
           robust=0.5,
           gridder='awproject',
           rotatepastep=5.0,
           wprojplanes=64,
           scales=[0,3,9],
           deconvolver='mtmfs',
           specmode='mfs',
           nterms=2,
           weighting='briggs',
           pblimit=0.05,
           interactive=False,
           outframe='LSRK',
           savemodel='none',
           parallel=True,
           cfcache=imagename+".cfcache",
          )
    makefits(imagename)

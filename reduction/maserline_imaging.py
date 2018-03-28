
import datetime
import os
import glob

def makefits(myimagebase, cleanup=True):
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.image', fitsimage=myimagebase+'.image.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model', fitsimage=myimagebase+'.model.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', dropdeg=True, overwrite=True) # export the PB image

    if cleanup:
        for suffix in ('pb', 'weight', 'sumwt', 'psf',
                       'model', 'mask', 'image', 'residual',
                       'alpha', 'alpha.error'):
            os.system('rm -rf {0}.{1}'.format(myimagebase, suffix))


def myclean(
    vis,
    name,
    linename,
    spws,
    imsize=2000,
    cell='0.04arcsec',
    fields=["Sgr B2 N Q", "Sgr B2 NM Q", "Sgr B2 MS Q"],
    niter=1000,
    threshold='25mJy',
    robust=0.5,
    savemodel='none',
    **kwargs
):
    for field in fields:
        imagename = ("{name}_{field}_r{robust}_{linename}_clean1e4_{threshold}"
                     .format(name=name, field=field.replace(" ","_"),
                             robust=robust, threshold=threshold,
                             linename=linename,
                            )
                    )
        tclean(vis=vis,
               field=field,
               spw=spws,
               imsize=[imsize, imsize],
               cell=cell,
               imagename=imagename,
               niter=niter,
               threshold=threshold,
               robust=robust,
               gridder='standard',
               deconvolver='hogbom',
               specmode='cube',
               weighting='briggs',
               pblimit=0.2,
               interactive=False,
               outframe='LSRK',
               datacolumn='corrected',
               savemodel=savemodel,
               **kwargs
              )
        makefits(imagename)

def siov1clean(vis, name, **kwargs):
    return myclean(vis=vis, name=name, linename='SiOv=1', spws="42", **kwargs)

def siov2clean(vis, name, **kwargs):
    return myclean(vis=vis, name=name, linename='SiOv=2', spws="39", **kwargs)

def ch3ohmaserclean(vis, name, **kwargs):
    return myclean(vis=vis, name=name, linename='CH3OH44.1', spws="50", **kwargs)

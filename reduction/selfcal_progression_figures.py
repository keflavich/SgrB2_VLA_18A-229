import os
import numpy as np
from astropy.io import fits
import pylab as pl
from astropy import wcs
import astropy.visualization
import radio_beam
from visualization import hide_labels
from astropy.nddata import Cutout2D
from astropy import coordinates
from astropy import units as u
import warnings

warnings.filterwarnings('ignore', category=wcs.FITSFixedWarning, append=True)

ra1m,dec1m = (266.8343197, -28.3848343)
ra2m,dec2m = (266.8336595, -28.38431563)
ra1mw,dec1mw = (266.83525, -28.385893)
ra2mw,dec2mw = (266.83284, -28.383568)

def fpath(x, base='/lustre/aginsbur/sgrb2/18A-229/continuum'):
    return os.path.join(base, x)

sc1 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter1_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_2mJy.image.tt0.pbcor.fits'))
sc2 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter2_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.image.tt0.pbcor.fits'))
sc3 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter3_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.image.tt0.pbcor.fits'))
sc4 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter4_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.image.tt0.pbcor.fits'))
sc5 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter5_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.image.tt0.pbcor.fits'))

rsc1 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter1_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_2mJy.residual.tt0.fits'))
rsc2 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter2_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.residual.tt0.fits'))
rsc3 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter3_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.residual.tt0.fits'))
rsc4 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter4_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.residual.tt0.fits'))
rsc5 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter5_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.residual.tt0.fits'))


msc1 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter1_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_2mJy.model.tt0.fits'))
msc2 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter2_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.model.tt0.fits'))
msc3 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter3_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.model.tt0.fits'))
msc4 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter4_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.model.tt0.fits'))
msc5 = fits.open(fpath('18A-229_Q_singlefield_selfcal_iter5_Sgr_B2_MS_Q_r0.5_allcont_clean1e4_1mJy.model.tt0.fits'))

imlist = [sc1,sc2,sc3,sc4,sc5]
residlist = [rsc1,rsc2,rsc3,rsc4,rsc5]
modellist = [msc1,msc2,msc3,msc4,msc5]

pl.close(1)

for name, ((ra1,dec1),(ra2,dec2)),(vmin,vmax) in [
         ('SgrB2M', ((ra1m,dec1m),(ra2m,dec2m)), [-0.001, 0.1]),
         ('SgrB2Mwide', ((ra1mw,dec1mw),(ra2mw,dec2mw)), [-0.001, 0.05]),
    ]:

    fig = pl.figure(1, figsize=(20,10), dpi=75)
    fig.clf()

    all_axes = {}

    for ii, (fh,rfh,mfh) in enumerate(zip(imlist,
                                          residlist,
                                          modellist
                                         )
                                 ):


        print(ii,fh,rfh,mfh)
        mywcs = wcs.WCS(fh[0].header).celestial
        center = coordinates.SkyCoord((ra1+ra2)/2, (dec1+dec2)/2, frame='icrs',
                                      unit=(u.deg, u.deg))
        size = max([np.abs(ra2-center.ra.deg), np.abs(dec2-center.dec.deg)]) * 2.1 * u.deg
        cutout_im = Cutout2D(fh[0].data.squeeze(), position=center, size=size, wcs=mywcs)
        cutout_res = Cutout2D(rfh[0].data.squeeze(), position=center, size=size,
                              wcs=mywcs)
        cutout_mod = Cutout2D(mfh[0].data.squeeze(), position=center, size=size,
                              wcs=mywcs)

        beam = radio_beam.Beam.from_fits_header(fh[0].header)
        ppbeam = (beam.sr / (wcs.utils.proj_plane_pixel_area(cutout_im.wcs)*u.deg**2)).decompose()
        assert ppbeam.unit == u.dimensionless_unscaled
        ppbeam = ppbeam.value

        ax1 = fig.add_subplot(3,len(imlist),ii+1, projection=cutout_im.wcs)
        im = ax1.imshow(cutout_im.data*1e3, cmap='gray',
                        norm=astropy.visualization.simple_norm(fh[0].data.squeeze(),
                                                               stretch='asinh',
                                                               min_cut=vmin*1e3,
                                                               max_cut=vmax*1e3,
                                                               asinh_a=0.001),
                        transform=ax1.get_transform(cutout_im.wcs),
                        origin='lower',)

        ax2 = fig.add_subplot(3,len(imlist),ii+len(imlist)+1, projection=cutout_res.wcs)
        im2 = ax2.imshow(cutout_res.data*1e3, cmap='gray',
                         norm=astropy.visualization.simple_norm(rfh[0].data.squeeze(),
                                                                stretch='asinh',
                                                                min_cut=vmin*1e3,
                                                                max_cut=vmax*1e3,
                                                                asinh_a=0.001),
                         transform=ax2.get_transform(cutout_res.wcs),
                         origin='lower',)

        ax3 = fig.add_subplot(3,len(imlist),ii+len(imlist)*2+1, projection=cutout_mod.wcs)
        im3 = ax3.imshow(cutout_mod.data*1e3, cmap='gray',
                         norm=astropy.visualization.simple_norm(mfh[0].data.squeeze(),
                                                                stretch='asinh',
                                                                min_cut=vmin*1e3/ppbeam,
                                                                max_cut=vmax*1e3/ppbeam,
                                                                asinh_a=0.001),
                         transform=ax3.get_transform(cutout_mod.wcs),
                         origin='lower',)

        all_axes[(ii, 1)] = ax1
        all_axes[(ii, 2)] = ax2
        all_axes[(ii, 3)] = ax3

        #(x1,y1),(x2,y2) = mywcs.wcs_world2pix([[ra1,dec1]],0)[0], mywcs.wcs_world2pix([[ra2,dec2]],0)[0]
        (x1,y1),(x2,y2) = cutout_im.wcs.wcs_world2pix([[ra1,dec1]],0)[0], cutout_im.wcs.wcs_world2pix([[ra2,dec2]],0)[0]
        ax1.axis([x1,x2,y1,y2])
        (x1,y1),(x2,y2) = cutout_res.wcs.wcs_world2pix([[ra1,dec1]],0)[0], cutout_res.wcs.wcs_world2pix([[ra2,dec2]],0)[0]
        ax2.axis([x1,x2,y1,y2])
        ax3.axis([x1,x2,y1,y2])
        #tr_fk5 = ax.get_transform("fk5")
        hide_labels(ax1)
        hide_labels(ax2)
        hide_labels(ax3)
        #ax.plot([ra1,ra2], [dec1,dec2], transform=tr_fk5, marker='o', color='r', zorder=50)

    fig.subplots_adjust(wspace=0, hspace=0)
    fig.canvas.draw()

    x1 = ax1.bbox.x1 / (fig.bbox.x1-fig.bbox.x0)
    # y0 = ax.bbox.y0 / (fig.bbox.y1-fig.bbox.y0)
    y0 = ax3.bbox.y0 / (fig.bbox.y1-fig.bbox.y0)
    # single-ax version height = (ax.bbox.y1-ax.bbox.y0) / (fig.bbox.y1-fig.bbox.y0)
    height = (ax1.bbox.y1-ax3.bbox.y0) / (fig.bbox.y1-fig.bbox.y0)
    cax_bbox = [x1 + 0.02, y0, 0.02, height]
    cb = pl.colorbar(mappable=im, cax=fig.add_axes(cax_bbox))
    cb.set_label('mJy/beam')


    fig.savefig("selfcal_progression_18A229_Q_{0}.pdf".format(name),
                bbox_inches='tight', dpi=300)

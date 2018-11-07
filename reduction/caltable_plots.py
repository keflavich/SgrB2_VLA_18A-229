import numpy as np
import pylab as pl
from astropy import table
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

tbl = table.Table.read('calibrator_data.txt', format='ascii.ipac')

colors = {'"1331+305=3C286"': 'b',
          'J1733-1304': 'orange',
          'J1744-3116': 'g',
         }

for jd in np.unique(tbl['JD']):
    fig = pl.figure(1)
    fig.clf()
    ax = fig.gca()

    mask = tbl['JD'] == jd

    subtbl = tbl[mask]
    subtbl.sort('freq')

    bands = set(subtbl['BandName'])
    assert len(bands) == 1
    band, = bands

    sources = np.unique(subtbl['FieldID'])

    for source in sources:
        sourcemask = subtbl['FieldID'] == source
        contmask = subtbl['bw'] == 128e3
        mask = sourcemask & contmask

        freqs = subtbl[mask]['freq']
        peak = subtbl[mask]['peak']
        rms = subtbl[mask]['rms']

        ax.errorbar(freqs, peak, yerr=rms, label=source, marker='s',
                    color=colors[source]
                   )

    #print(freqs)

    pl.legend(loc='best')
    pl.savefig('calplots/{0}_{1}.png'.format(jd, band))

fluxes = {}

sources = np.unique(tbl['FieldID'])
for bpname,frqrange in (('B1D1', (42,43.8)),
                        ('B2D2', (43.8, 45.8)),
                        ('A1C1', (46,47.75)),
                        ('A2C2', (47.75, 50))):
    frqmask = (tbl['freq']/1e3 > frqrange[0]) & (tbl['freq']/1e3 < frqrange[1])


    for jd in np.unique(tbl['JD']):

        datemask = tbl['JD'] == jd

        for source in sources:
            sourcemask = tbl['FieldID'] == source
            contmask = tbl['bw'] == 128e3
            mask = sourcemask & contmask & frqmask & datemask


            subtbl = tbl[mask]
            if any(mask):
                flux = np.mean(subtbl['peak'])
                rms = np.std(subtbl['peak'])

                fluxes[(source, jd, bpname)] = (flux,rms)


    for source in sources:
        fig = pl.figure(1)
        fig.clf()
        ax = fig.gca()
        for bb in ('A1C1','A2C2','B1D1','B2D2'):
            ax.errorbar([k[1] for k in fluxes
                         if k[0] == source and k[2] == bb],
                        [v[0] for k,v in fluxes.items()
                         if k[0] == source and k[2] == bb],
                        yerr=[v[1] for k,v in fluxes.items()
                              if k[0] == source and k[2] == bb],
                        linestyle='none',
                        marker='o',
                        label=bb)

        pl.xlim(58177, 58229)
        pl.legend(loc='best')
        pl.savefig('calplots/{0}_vs_time.png'.format(source))



# make a grid showing which SB was observed when
qmask = tbl['BandName'] == 'Q'
qtbl = tbl[qmask]

jds = np.unique(qtbl['JD'])
spws = np.unique(qtbl['spw'])

rectangles = []

for ii,jd in enumerate(jds):
    jdmask = qtbl['JD'] == jd

    dtbl = qtbl[jdmask]

    for frq,bw in zip(dtbl['freq'], dtbl['bw']/1e3):
        rectangles.append(Rectangle([frq-bw/2, jd], width=bw,
                                    height=0.75,
                                    #height=2/24.,
                                    linewidth=1,
                                    linestyle='solid',
                                    facecolor=(0,0.1,1,0.5), edgecolor='k', ec='k'))

fig = pl.figure(2)
fig.clf()
ax = fig.gca()
ax.add_collection(PatchCollection(rectangles, edgecolors=(0,0,0,0.5),
                                  linewidths=0.5, facecolor=(0,0.3,1.0,0.25),
                                  alpha=0.5))

ax.axis([42000, 50000, jds.min()-1, jds.max()+3])
ax.set_xlabel("Frequency")
ax.set_ylabel("Julian date")

pl.savefig("frequency_coverage_Q.png")

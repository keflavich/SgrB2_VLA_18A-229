import numpy as np
import pylab as pl
from astropy import table

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

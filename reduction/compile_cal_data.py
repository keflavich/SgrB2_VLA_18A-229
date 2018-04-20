import os
from listobs_parser import get_spws
from astropy.table import Table

def get_cal_data(fn):
    data = {}
    stats_begun = False
    with open(fn, 'r') as fh:
        for row in fh:
            if 'Clean image iter' in row:
                stats_begun = True
            if 'Clean image annulus area rms' in row:
                rms = float(row.split()[-1])
            if 'Clean image max' in row:
                mx = float(row.split()[-1])
            if 'Cleaning for intent' in row and stats_begun:
                spw = int(row.split()[-1])
                field = row.split("field")[-1].split(",")[0].strip()
                data[(field,spw)] = (mx, rms)
                stats_begun = False
    return data


all_data = {}

for directory, dirnames, filenames in os.walk('.'):
    for fn in filenames:
        if 'listobs.txt' == fn:
            listfn = os.path.join(directory, fn)
            msname, spws, bws, band, bbs, fields_table = get_spws(listfn)
            if '/' in msname:
                msname = os.path.split(msname)[-1]
                #print('--',directory, msname, band)
    if 'stage20' in directory and 'casapy.log' in filenames:
        stage20path = os.path.join(directory, 'casapy.log')
        data = get_cal_data(stage20path)

        all_data[msname] = data, spws, bws, band, bbs, fields_table
        #print(directory, msname, band)

titles = ['JD', 'BandName', 'FieldID', 'spw', 'freq', 'bw', 'peak', 'rms', 'msname']
rows = []

for msname in all_data:
    jd = float('.'.join(msname.split('.')[3:5]))

    for (field,spw),(mx,rms) in all_data[msname][0].items():
        band = all_data[msname][3]
        spws = all_data[msname][1]
        bws = all_data[msname][2]
        row = [jd, band, field, spw, spws[spw], bws[spw], mx, rms, msname]
        rows.append(row)

tbl = Table(rows=rows, names=titles)
tbl.write('reduction_scripts/calibrator_data.txt', format='ascii.ipac', overwrite=True)

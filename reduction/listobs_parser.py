
def get_spws(fn):
    spws = {}
    bws = {}
    bbs = {}

    fields_table = []

    in_fields = False
    with open(fn, 'r') as fh:
        for row in fh.readlines():
            
            if 'MeasurementSet Name' in row:
                msname = ("/".join(row.split("/")[-2:])).split(" ")[0]
            if 'EVLA_' in row:
                spw = int(row.split()[0])
                frq = float(row.split()[7])
                bw = float(row.split()[6])
                bb = row.split()[1].split("#")[1]
                band = row.split()[1].split("#")[0].split("_")[-1]
                if band not in ("X","C"):
                    spws[spw] = frq
                    bws[spw] = bw
                    bbs[spw] = bb
            if 'Spectral Windows:' in row:
                in_fields = False
            if in_fields:
                fields_table.append(row)
            if 'Fields:' in row:
                in_fields = True


    return msname, spws, bws, band, bbs, fields_table

def parse_fields_table(fields_table):
    title_row = fields_table[0]

    name_start = title_row.find("Name")
    name_end = title_row.find("RA")

    sources = [row[name_start:name_end].strip() for row in fields_table[1:]]

    return sources

if __name__ == "__main__":
    import glob
    listobsfiles = glob.glob("listobs/*.listobs")

    results = {x[0]: (x[3], x[1], x[2], x[4], x[5]) for x in [get_spws(fn) for fn in listobsfiles]}

    for key in sorted(results):
        print("{0:3s} {1:95s} {2}".format(results[key][0], key,  len(results[key][1])))


    for key in sorted(results):
        rslt = results[key]
        if rslt[0] == 'Q':
            cont_bands = [k for k in rslt[2] if rslt[2][k]==128e3]
            print("\"{0}\": \"{1}\",".format(key, ",".join(map(str, sorted([k for k in cont_bands])))))


    for key in sorted(results):
        rslt = results[key]
        print(key, parse_fields_table(rslt[4]))

#    for key in sorted(results):
#        rslt = results[key]
#
#        if rslt[0] == 'Q':
#
#            bbs = rslt[3]
#            for bb in sorted(set(bb.values())):
#                

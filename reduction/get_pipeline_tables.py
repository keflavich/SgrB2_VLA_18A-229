"""
Extract the calibration tables from the pipeline runs.

These tables are used for re-calibrating the data with selfcal.  Everything, or
everything except the phase calibration, will be applied, then self-cal will be
used (phase-only) to get the best phase solutions.
"""
import glob
import tarfile
import os

dirs = glob.glob('18A*')
cwd = os.getcwd()

for dir in dirs:
    tf = tarfile.open('{0}/products/unknown.session_1.caltables.tgz'.format(dir))

    members = []
    for member in tf.getmembers():
        if os.path.splitext(member.name)[-1] in ('.k', '.b', '.cal', '.g', '.tbl'):
            print("Extracting {0} into {1}".format(member.name, dir))
            members.append(member)
        elif member.name.split(".")[0] == '18A-229':
            members.append(member)
            #print("Skipped {0}".format(member.name))

    tf.extractall(path=dir, members=members)

"""
Extract the weblogs
"""
import glob
import tarfile
import os

dirs = glob.glob('18A*')
cwd = os.getcwd()

for dir in dirs:
    tf = tarfile.open('{0}/products/weblog.tgz'.format(dir))

    extractdir = "{0}/products".format(dir)

    tf.extractall(path=extractdir)

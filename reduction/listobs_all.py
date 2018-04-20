import glob
import os

dirs = glob.glob('18A*/*ms')

for ms in dirs:
    listobs(vis=ms, listfile=ms+".listobs", overwrite=True)


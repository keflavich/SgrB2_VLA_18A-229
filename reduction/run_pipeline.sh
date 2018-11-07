#!/bin/sh

#This script is ment to be set in the COMMAND variable
#in the configure file to submit.  That submit script will create the
#clusterspec file for us in the WORK_DIR we specified in the configure file.
#PBS -l mem=30gb
#PBS -l nodes=1:ppn=8
#PBS -d /lustre/aginsbur/sgrb2/18A-229/continuum/
#PBS -N SHORTDATE
#PBS -m abe
# # Send mail on begin, end, abort, and fail

WORK_DIR='/lustre/aginsbur/sgrb2/18A-229/LONGDATE'

cd ${WORK_DIR}

# casa's python requires a DISPLAY for matplot so create a virtual X server
xvfb-run -d casa-pipe --nogui --nologger -c "execfile('$WORK_DIR/casa_pipescript.py')"

#!/bin/sh

#This script is ment to be set in the COMMAND variable
#in the configure file to submit.  That submit script will create the
#clusterspec file for us in the WORK_DIR we specified in the configure file.
#PBS -l mem=30gb
#PBS -l nodes=1:ppn=8
#PBS -d /lustre/aginsbur/sgrb2/18A-229/continuum/
#PBS -N sb2_18A229_cont
#PBS -m abe
# # Send mail on begin, end, abort, and fail

WORK_DIR='/lustre/aginsbur/sgrb2/18A-229/continuum/'

cd ${WORK_DIR}
echo ${WORK_DIR}

export SCRIPT_DIR="/lustre/aginsbur/sgrb2/18A-229/reduction_scripts/"

# casa's python requires a DISPLAY for matplot so create a virtual X server
xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$SCRIPT_DIR/selfcal_post_repipelining.py')"
#xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$SCRIPT_DIR/continuum_imaging_make_selfcal_model.py')"
xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$SCRIPT_DIR/selfcal_iterations_post_repipelining.py')"

#export CASAPATH=/home/casa/packages/RHEL6/release/casa-release-5.1.0-74
#export PATH=${CASAPATH}/bin:$PATH
#
#export CASACMD="execfile('$REDUCTION_DIR/scriptForImaging_lines.py')"
#echo $CASACMD
#
#mpicasa -machinefile $PBS_NODEFILE casa -quiet --nogui --nologger --log2term -c "${CASACMD}"

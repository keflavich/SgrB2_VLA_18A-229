#!/bin/sh

#This script is ment to be set in the COMMAND variable
#in the configure file to submit.  That submit script will create the
#clusterspec file for us in the WORK_DIR we specified in the configure file.
#PBS -l mem=30gb
#PBS -l nodes=1:ppn=8
#PBS -d /lustre/aginsbur/sgrb2/18A-229/continuum/
#PBS -N sb2_singltest
#PBS -m abe
# # Send mail on begin, end, abort, and fail

WORK_DIR='/lustre/aginsbur/sgrb2/18A-229/continuum/'

cd ${WORK_DIR}
echo ${WORK_DIR}

export SCRIPT_DIR="/lustre/aginsbur/sgrb2/18A-229/reduction_scripts/"
export CASAPATH=/lustre/aoc/projects/18A-199/Imaging/casa-test-ARD-master-sb-1.el6
export PATH=${CASAPATH}/bin:$PATH

echo "PBS_NODEFILE = ",$PBS_NODEFILE
cat $PBS_NODEFILE

casa --nogui --nologger --log2term -c "${SCRIPT_DIR}/singlefield_imaging_tests.py"
casa --nogui --nologger --log2term -c "${SCRIPT_DIR}/deeper_singlefield_clean.py"

# mpicasa -machinefile $PBS_NODEFILE casa --nogui --nologger --log2term -c "${SCRIPT_DIR}/singlefield_imaging_tests.py"

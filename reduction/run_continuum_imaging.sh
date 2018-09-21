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

# sanity check: script was failing without reason.
#xvfb-run -d casa-prerelease --nogui --nologger -c "from impbcor_cli import impbcor_cli as impbcor; assert(hasattr(impbcor, 'defaults'))"

# casa's python requires a DISPLAY for matplot so create a virtual X server
#xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$SCRIPT_DIR/flagging.py')"
#xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$SCRIPT_DIR/selfcal_post_repipelining.py')"
#xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$SCRIPT_DIR/continuum_imaging_make_selfcal_model.py')"
#xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$SCRIPT_DIR/selfcal_iterations_post_repipelining.py')"
xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$SCRIPT_DIR/selfcal_iterations_post_repipelining_wterms.py')"
# the single-field selfcal script ported from W51
#xvfb-run -d casa-prerelease --nogui --nologger -c "execfile('$SCRIPT_DIR/imaging_continuum_selfcal_incremental.py')"


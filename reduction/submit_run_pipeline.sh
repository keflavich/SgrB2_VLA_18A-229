#!/bin/bash

OBSDATE=$1
OBSDATE_SHORT=${OBSDATE:13:9}
BASECOMMAND='/lustre/aginsbur/sgrb2/18A-229/reduction_scripts/run_pipeline.sh'
COMMAND=${BASECOMMAND%.*}_$OBSDATE.sh
sed "s/LONGDATE/${OBSDATE}/g; s/SHORTDATE/${OBSDATE_SHORT}/g" $BASECOMMAND > $COMMAND
qsub $COMMAND

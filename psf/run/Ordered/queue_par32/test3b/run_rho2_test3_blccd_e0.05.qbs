#!/bin/bash
#PBS -M alsina@ifi.unicamp.br
#PBS -m abe
#PBS -N par32a
#PBS -e par32a.err
#PBS -o par32a.out
#PBS -q par32
#PBS -l nodes=4:ppn=8


source /home/sw/masternode/intel/2015/install/composerxe/bin/compilervars.sh intel64
source /home/sw/masternode/intel/2015/install/mpi/impi/5.1.2.150/bin64/mpivars.sh

export I_MPI_HYDRA_BOOTSTRAP=rsh
export I_MPI_HYDRA_BOOTSTRAP_EXEC=/opt/pbs/bin/pbs_tmrsh
export I_MPI_DEVICE=rdssm

export PATH=/home/dfa/sobreira/alsina/sw/pyhton/2714/install/bin:$PATH
export PYTHONPATH=$PYTHONPATH:/home/dfa/sobreira/alsina/sw/galsim/install/lib/python2.7/site-packages
export PATH=/home/dfa/sobreira/alsina/sw/cfitsio/install/bin:$PATH
export LD_LIBRARY_PATH=/home/dfa/sobreira/alsina/sw/cfitsio/install/lib:/home/dfa/sobreira/alsina/sw/ccfits/25/install/lib:/home/dfa/sobreira/alsina/sw/tmv/install/lib:/home/dfa/sobreira/alsina/sw/boost/166/install/lib:$LD_LIBRARY_PATH

cd /home/dfa/sobreira/alsina/DESWL/psf/run

INSTALL=/home/dfa/sobreira/alsina/sw
START_PATH=/home/dfa/sobreira/alsina/DESWL/psf
INPUT_PATH=/home2/dfa/sobreira/alsina/catalogs
OUTPUT_PATH=/home2/dfa/sobreira/alsina/catalogs/output
TAG=y3a1-v29

$INSTALL/pyhton/2714/install/bin/python $START_PATH/run_rho2_outand_ellipfilter_piff_ccd.py --file=$START_PATH/ally3.riz --tag=$TAG --work=$INPUT_PATH/$TAG --outpath=$OUTPUT_PATH/$TAG/test3b_beccd_epiff/allzones_e0.05 --bands=riz --threshold=0.05 --use_reserved #--bandcombo


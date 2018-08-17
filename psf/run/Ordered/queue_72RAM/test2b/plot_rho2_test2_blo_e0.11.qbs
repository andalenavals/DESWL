#!/bin/bash
#PBS -M alsina@ifi.unicamp.br
#PBS -m abe
#PBS -N par72RAM
#PBS -e par72RAM.err
#PBS -o par72RAM.out
#PBS -q par72RAM
#PBS -l nodes=1:ppn=16

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
INPUT_PATH=/home2/dfa/sobreira/alsina/catalogs/output
OUTPUT_PATH=/home2/dfa/sobreira/alsina/catalogs/output
TAG=y3a1-v29

$INSTALL/pyhton/2714/install/bin/python $START_PATH/plot_rho_outand.py --work=$INPUT_PATH/$TAG/test2_beo_epiff/allzones_e0.11/	 --outpath=$OUTPUT_PATH/$TAG/test2_beo_epiff/allzones_e0.11/rho

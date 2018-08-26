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

/home/sw/masternode/pbs/pbsdshV /home/dfa/sobreira/alsina/DESWL/psf/run/gopiff_zone29_magcut0_maxmag22_sf2

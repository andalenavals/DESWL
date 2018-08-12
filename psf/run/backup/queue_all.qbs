#!/bin/bash
#PBS -M alsina@ifi.unicamp.br
#PBS -m abe
#PBS -N par64a
#PBS -e par64a.err
#PBS -o par64a.out
#PBS -q par64
#PBS -l nodes=4:ppn=16

source /home/sw/masternode/intel/2015/install/composerxe/bin/compilervars.sh intel64
source /home/sw/masternode/intel/2015/install/mpi/impi/5.1.2.150/bin64/mpivars.sh

/home/sw/masternode/pbs/pbsdshV /home/dfa/sobreira/alsina/DESWL/psf/run/goall

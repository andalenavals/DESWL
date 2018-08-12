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

mpirun -n 32 ./home/dfa/sobreira/alsina/DESWL/psf/run/gorho
##/home/sw/masternode/pbs/pbsdshV /home/dfa/sobreira/alsina/DESWL/psf/run/gopiff64par

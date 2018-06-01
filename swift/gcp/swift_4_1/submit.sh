#!/bin/bash
#SBATCH --nodes 4
#SBATCH --ntasks 4
#SBATCH -J imb_4_1
#SBATCH --output=/home/mdavezac/swift/swift_4_1/out
#SBATCH --error=/home/mdavezac/swift/swift_4_1/err
#SBATCH --exclusive
#SBATCH --time=12:00:00

set -e

module purge
module load $(spack module find mpich +pmi)
module load $(spack module find hdf5 -fortran -mpi)
module load $(spack module find gsl)
module load $(spack module find metis)
# module load $(spack module find swiftsim +mpi ^mpich +pmi)

cd /home/mdavezac/swift/swift_4_1
cp /home/mdavezac/swift/eagle_25.yml  .
[ ! -e /home/mdavezac/swift/swift_4_1/EAGLE_ICs_25.hdf5 ] && ln -s /home/mdavezac/swift/EAGLE_ICs_25.hdf5 .

time mpirun /home/mdavezac/swift/usr/bin/swift_mpi -s -a -t 16 -n 4096 eagle_25.yml

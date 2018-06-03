#!/bin/bash

#SBATCH --nodes=4
#SBATCH --ntasks-per-node=16
#SBATCH --time=10:00:00
#SBATCH --job-name=GridITT

mpirun -n 4  --mca btl vader,self Benchmark_ITT --mpi 2.1.1.1 --shm 1024


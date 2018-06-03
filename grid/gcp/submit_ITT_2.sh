#!/bin/bash

#SBATCH --nodes=2
#SBATCH --ntasks-per-node=16
#SBATCH --time=10:00:00
#SBATCH --job-name=GridITT

mpirun -n 2  --mca btl vader,self Benchmark_ITT --mpi 2.1.1.1 --shm 1024


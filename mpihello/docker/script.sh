#!/bin/bash -l
set -x
set -e
set -o

source /etc/profile.d/modules.sh
module load mpi

function mpirun() {
    IFS=',' read -ra HOSTS <<< "$AZ_BATCH_HOST_LIST"
    nodes=${#HOSTS[@]}
    /usr/lib64/openmpi/bin/mpirun \
        -np $nodes\
        --allow-run-as-root \
        --host $AZ_BATCH_HOST_LIST \
        "$@"
}

mpirun python36 /root/job.py

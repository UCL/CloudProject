""" Helps submitting nektar jobs """
import jinja2

TEMPLATE = jinja2.Template("""#!/bin/bash
#SBATCH -N {{nnodes}}
#SBATCH --ntasks-per-node {{nprocs_per_node}}
#SBATCH -J imb_{{nnodes}}_{{nprocs_per_node}}
#SBATCH --output=nektar_{{nnodes}}_{{nprocs_per_node}}
#SBATCH --exclusive
#SBATCH --time=2:00:00

set -e

module purge
module load $(spack module find nektar +scotch +mpi)
module load $(spack module find mpich +pmi)

directory=~/nektar/test-cases/cardiac/$SLURM_JOB_NAME/
mkdir -p $directory
cd $directory
cp ../conditions.xml ../patient_tn_refined_p6_iso.xml .
time srun --mpi=pmi2 CardiacEPSolver-rg \
    patient_tn_refined_p6_iso.xml conditions.xml 1> out 2> err
""")


def sendme(nnodes=2, nprocs_per_node=1):
    """ Sends a single nektar process """
    from subprocess import Popen, PIPE
    proc = Popen(["sbatch"], stdin=PIPE)
    proc.stdin.write(TEMPLATE.render(nnodes=nnodes,
                                     nprocs_per_node=nprocs_per_node))
    proc.stdin.close()
    proc.wait()


# for nnodes in range(1, 3):
#     for nprocs_per_node in range(1, 17):
#         sendme(nnodes, nprocs_per_node)

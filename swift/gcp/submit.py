""" Helps submitting nektar jobs """
import jinja2

TEMPLATE = jinja2.Template("""#!/bin/bash
#SBATCH --nodes {{nnodes}}
#SBATCH --ntasks {{nnodes * nprocs_per_node}}
#SBATCH -J imb_{{nnodes}}_{{nprocs_per_node}}
#SBATCH --output={{outdir}}/out
#SBATCH --error={{outdir}}/err
#SBATCH --exclusive
#SBATCH --time=12:00:00

set -e

module purge
module load $(spack module find mpich +pmi)
module load $(spack module find hdf5 -fortran -mpi)
module load $(spack module find gsl)
module load $(spack module find metis)
# module load $(spack module find swiftsim +mpi ^mpich +pmi)

cd {{outdir}}
cp {{indir}}/eagle_25.yml  .
[ ! -e {{outdir}}/EAGLE_ICs_25.hdf5 ] && ln -s {{indir}}/EAGLE_ICs_25.hdf5 .

time mpirun {{indir}}/usr/bin/swift_mpi -s -a -t 16 -n 4096 eagle_25.yml

""")


def sendme(nnodes=2, nprocs_per_node=1):
    """ Sends a single nektar process """
    from os.path import exists, join
    from os import makedirs, getcwd
    from subprocess import Popen, PIPE
    outdir = join(getcwd(), f"swift_{nnodes}_{nprocs_per_node}")
    if not exists(outdir):
        makedirs(outdir)

    script = TEMPLATE.render(
        nnodes=nnodes,
        nprocs_per_node=nprocs_per_node,
        outdir=outdir,
        indir=getcwd())
    with open(join(outdir, "submit.sh"), "w") as file:
        file.write(script)

    proc = Popen(["sbatch"], stdin=PIPE)
    proc.stdin.write(script.encode())
    proc.stdin.close()
    proc.wait()

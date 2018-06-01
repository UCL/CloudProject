""" Helps submitting nektar jobs """
import jinja2

TEMPLATE = jinja2.Template("""#!/bin/bash -l
#BSUB -L /bin/bash
#BSUB -n {{nnodes * nprocs_per_node}}
#BSUB -J swift_{{nnodes}}_{{nprocs_per_node}}
#BSUB -o swift_{{nnodes}}_{{nprocs_per_node}}/out
#BSUB -e swift_{{nnodes}}_{{nprocs_per_node}}/err
#BSUB -R "span[ptile={{nprocs_per_node}}]"
#BSUB -q cosma5
#BSUB -P ds006
#BSUB -W 24:00

module purge
module load intel_comp/c5/2017
module load intel_mpi/2017
module load hdf5
module load fftw/3.3.4
module load metis
module load gsl
export LD_LIBRARY_PATH=$LIBRARY_PATH:$LD_LIBRARY_PATH

directory=$(pwd)/swift_{{nnodes}}_{{nprocs_per_node}}
cd $directory
binpath=/cosma5/data/ds006/dc-dave3/software/bin
time mpirun $binpath/swift_mpi -s -a -t 16 -n 4096 eagle_25.yml
""")


def sendme(nnodes=8, nprocs_per_node=1):
    """ Sends a single nektar process """
    from subprocess import Popen, PIPE
    from os.path import exists, join
    from os import makedirs
    from shutil import copy

    directory = f"swift_{nnodes}_{nprocs_per_node}"
    if not exists(directory):
        makedirs(directory)
    if not exists(join(directory, "eagle_25.yml")):
        copy("eagle_25.yml", directory)
    if not exists(join(directory, "EAGLE_ICs_25.hdf5")):
        copy("EAGLE_ICs_25.hdf5", directory)

    proc = Popen(["bsub"], stdin=PIPE)
    proc.stdin.write(TEMPLATE.render(nnodes=nnodes,
                                     nprocs_per_node=nprocs_per_node).encode())
    proc.stdin.close()
    proc.wait()

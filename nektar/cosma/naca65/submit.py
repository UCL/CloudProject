""" Helps submitting nektar jobs """
import jinja2

TEMPLATE = jinja2.Template("""#!/bin/bash -l
#BSUB -L /bin/bash
#BSUB -n {{nnodes * nprocs_per_node}}
#BSUB -J naca64_{{nnodes}}_{{nprocs_per_node}}
#BSUB -o nektar_{{nnodes}}_{{nprocs_per_node}}.o
#BSUB -e nektar_{{nnodes}}_{{nprocs_per_node}}.e
#BSUB -R "span[ptile={{nprocs_per_node}}]"
#BSUB -q cosma5
#BSUB -P ds006
#BSUB -W 0:30

module purge
module load gnu_comp/c5/4.8.1 intel_mpi/2017
module load fftw/3.3.4
module load cmake/3.7.0
module load boost/1_57_0
export LD_LIBRARY_PATH=$LIBRARY_PATH:$LD_LIBRARY_PATH

directory=$(pwd)/naca64_{{nnodes}}_{{nprocs_per_node}}
mkdir -p $directory
cd $directory
ln -s ../NACA65_2-5D.xml ../NACA65-geometry.xml .
mkdir initial_condition.rst
cd initial_condition.rst
ln -s ../../initial_condition.rst/* .
cd ..
binpath=/cosma5/data/ds006/dc-dave3/software/bin
time mpirun $binpath/IncNavierStokesSolver \
    NACA65_2-5D.xml  NACA65-geometry.xml 1> out 2> err
""")


def sendme(nnodes=2, nprocs_per_node=1):
    """ Sends a single nektar process """
    from subprocess import Popen, PIPE
    proc = Popen(["bsub"], stdin=PIPE)
    proc.stdin.write(TEMPLATE.render(nnodes=nnodes,
                                     nprocs_per_node=nprocs_per_node).encode())
    proc.stdin.close()
    proc.wait()

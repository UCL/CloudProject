#!/bin/bash
source ~/.bashrc
module load mpi

git clone https://gitlab.cosma.dur.ac.uk/swift/swiftsim.git /build/src
cd /build/src
autoreconf --install --symlink
./configure --prefix=/build  --libdir=/usr/lib64 --bindir=/usr/bin
make -j 2
make install
rm /usr/lib64/libswiftsim_mpi.la /usr/lib64/libswiftsim_mpi.a
rm /usr/lib64/libswiftsim.la /usr/lib64/libswiftsim.a

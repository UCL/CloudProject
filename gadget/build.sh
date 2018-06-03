#!/bin/bash
cd /gadget/src
source ~/.bashrc
module load mpi

curl -L http://www.fftw.org/fftw-2.1.5.tar.gz | tar xzv 
cd fftw-2.1.5
./configure --prefix=/gadget/ --enable-mpi --enable-type-prefix \
    --libdir=/usr/lib64 --disable-shared
make -j 2
make install
make clean
./configure --prefix=/gadget/ --enable-mpi --enable-type-prefix \
    --libdir=/usr/lib64 --enable-float --disable-shared
make -j 2
make install
make clean


cd /gadget/src/gadget
sed -i "s/^SYSTYPE=.*$//" Makefile
make CC=mpicc OPTIMIZE="-O3 -Wall" \
    GSL_INCL=-I/usr/include GSL_LIBS=-lgsl \
    FFTW_INCL=-I/gadget/include \
    FFTW_LIBS="-ldfftw_mpi -lsfftw_mpi" \
    HDF5INCL=-DH5_USE_16_API HDF5LIB=-lhdf5 \
    MPICHLIB="" -j 2

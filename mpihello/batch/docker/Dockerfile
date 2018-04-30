# Builds mpi4py
FROM centos:7.1.1503 as builder
RUN yum swap -y fakesystemd systemd \
    && yum install -y epel-release \
    && yum groupinstall -y 'Development Tools' \
    && yum install -y openssh-clients gnuplot openmpi-devel python36-devel \
    && yum clean all \
    && rm -rf /var/cache/yum \
    && python36 -m ensurepip \
    && source /etc/profile.d/modules.sh \
    && module load mpi \
    && python36 -m pip install mpi4py

# mpi4py + azure ssh stuff
FROM centos:7.1.1503

COPY --from=builder /usr/local/lib64/python3.6/site-packages/mpi4py \
     /usr/local/lib64/python3.6/site-packages/mpi4py/
WORKDIR /root
COPY script.sh /root/ascript.sh
COPY job.py /root/job.py
RUN chmod a+Xr /root/job.py /root/ascript.sh /root

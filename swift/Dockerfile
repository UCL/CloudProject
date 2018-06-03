FROM centos:7

# set up base
COPY ssh_config /root/.ssh/config
RUN yum swap -y fakesystemd systemd \
    && yum install -y openssh-clients openssh-server net-tools libmlx4 \
       librdmacm libibverbs dapl rdma \
    && yum clean all \
    && rm -rf /var/cache/yum \
    && mkdir -p /var/run/sshd \
    && ssh-keygen -A \
    && sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config \
    && sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config \
    && sed -i 's/#RSAAuthentication yes/RSAAuthentication yes/g' /etc/ssh/sshd_config \
    && sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' /etc/ssh/sshd_config \
    && ssh-keygen -f /root/.ssh/id_rsa -t rsa -N '' \
    && chmod 600 /root/.ssh/config \
    && chmod 700 /root/.ssh \
    && cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

VOLUME /build
COPY build.sh /build/
RUN yum install -y epel-release \
    && yum-config-manager --enable epel \
	&& yum install -y openmpi-devel build-essentials gsl-devel \
		 hdf5-openmpi-devel make metis-devel git libtool fftw3-devel \
    && /build/build.sh \
    && yum erase -y openmpi-devel gsl-devel hdf5-openmpi-devel make \
        autoconf automake libtool cpp zlib-devel glibc-devel \
        glibc-headers gcc gcc-gfortran kernel-headers libaec-devel \
        libmpc libquadmath-devel mpfr zlib-devel git build-essentials \
        metis-devel fftw3-devel \
	&& yum install -y openmpi gsl hdf5-openmpi metis fftw3 \
    && yum clean all \
    && rm -rf /var/cache/yum

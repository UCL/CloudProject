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
# set up base and ssh keys
COPY ssh_config /root/.ssh/config
RUN yum swap -y fakesystemd systemd \
    && yum install -y epel-release \
    && yum install -y  openssh-clients openssh-server net-tools numactl \
        libmlx4 librdmacm libibverbs dapl rdma \
        openmpi python36 \
    && yum clean all \
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

COPY --from=builder /usr/local/lib64/python3.6/site-packages/mpi4py \
     /usr/local/lib64/python3.6/site-packages/mpi4py/
WORKDIR /root
COPY script.sh /root/script.sh
EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]

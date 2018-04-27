from socket import gethostname
from mpi4py import MPI
rank = MPI.COMM_WORLD.rank
size = MPI.COMM_WORLD.size
hostname = gethostname()
print('Hello from ', rank, ' of ', size, ' on ', hostname)
for i in range(size):
    if rank == i:
        print('1. {} will write'.format(rank))
        with open('ThisOutput', 'a') as file:
            print('2. {} will write'.format(rank))
            file.write("I am {} on {}\n".format(rank, hostname))
            print('3. {} will write'.format(rank))
        print('4. {} will write'.format(rank))

    print('1. {} barrier'.format(rank))
    MPI.COMM_WORLD.Barrier()
    print('2. {} barrier'.format(rank))
print('All done')

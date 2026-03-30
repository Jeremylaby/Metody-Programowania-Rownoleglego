#!/usr/bin/env python
from mpi4py import MPI
import sys

def pinpong(n, rank, comm):
    if rank == 0:
        data = f"0b{"0"*n}".encode()
        print(f"sended: {sys.getsizeof(data)} bytes")
        start = MPI.MPI_Wtime
        comm.send(data, dest=1)
        data = comm.recv(source=1)
        end =MPI.MPI_Wtime
        print(f"returned: {sys.getsizeof(data)} bytes")
        return start-end
    elif rank == 1:
        data = comm.recv(source=0)
        comm.send(data, dest=0)
    else:
        print("Expected only two nodes")
    return 0
timeMs =0



comm = MPI.COMM_WORLD
rank = comm.Get_rank()


for i in range(1000):
 time+= pinpong(8, rank, comm)
if rank ==1:
   print(timeMs)

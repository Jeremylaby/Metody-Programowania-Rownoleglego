#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>

#define REPEATS 1000

int main(int argc, char *argv[])
{
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size != 2) {
        if (rank == 0)
            fprintf(stderr, "Uruchom z dokladnie 2 procesami: mpirun -np 2\n");
        MPI_Finalize();
        return 1;
    }

    /* rozmiary komunikatow w bajtach */
    int sizes[] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512,
                   1024, 4096, 16384, 65536, 262144, 1048576,
                   4194304, 16777216};
    int n_sizes = sizeof(sizes) / sizeof(sizes[0]);

    if (rank == 0)
        printf("size_bytes,bandwidth_mbit_s,latency_ms\n");

    for (int i = 0; i < n_sizes; i++) {
        int msg_size = sizes[i];
        char *buf = malloc(msg_size);
        memset(buf, 0, msg_size);

        MPI_Barrier(MPI_COMM_WORLD);
        double t_start = MPI_Wtime();

        for (int r = 0; r < REPEATS; r++) {
            if (rank == 0) {
                MPI_Send(buf, msg_size, MPI_BYTE, 1, 0, MPI_COMM_WORLD);
                MPI_Recv(buf, msg_size, MPI_BYTE, 1, 0, MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);
            } else {
                MPI_Recv(buf, msg_size, MPI_BYTE, 0, 0, MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);
                MPI_Send(buf, msg_size, MPI_BYTE, 0, 0, MPI_COMM_WORLD);
            }
        }

        double t_end = MPI_Wtime();

        if (rank == 0) {
            /* czas jednego pelnego round-trip */
            double t_roundtrip = (t_end - t_start) / REPEATS;
            /* opoznienie = polowa round-trip */
            double latency_ms  = t_roundtrip / 2.0 * 1000.0;
            /* przepustowosc: 2 * msg_size bo tam i z powrotem */
            double bandwidth   = (2.0 * msg_size * 8.0) /
                                 (t_roundtrip * 1e6);
            printf("%d,%.4f,%.6f\n", msg_size, bandwidth, latency_ms);
        }

        free(buf);
    }

    MPI_Finalize();
    return 0;
}

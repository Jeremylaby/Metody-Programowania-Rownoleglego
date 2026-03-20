#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <mpi.h>

int main(int argc, char *argv[])
{
    int rank, size;
    long long total_points;
    long long local_points;
    long long local_inside = 0;
    long long global_inside = 0;
    double pi_approx;
    double t_start, t_end;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    unsigned int seed = (unsigned int)(time(NULL)) ^ (unsigned int)(rank * 1234567);



    if (argc < 2) {
        if (rank == 0)
            fprintf(stderr, "Użycie: %s <liczba_punktow>\n", argv[0]);
        MPI_Finalize();
        return EXIT_FAILURE;
    }

    total_points = atoll(argv[1]);

    if (total_points <= 0) {
        if (rank == 0)
            fprintf(stderr, "Błąd: liczba punktów musi być dodatnia.\n");
        MPI_Finalize();
        return EXIT_FAILURE;
    }


    local_points = total_points / size;
    if (rank == size - 1)
        local_points += total_points % size;

    MPI_Barrier(MPI_COMM_WORLD);
    t_start = MPI_Wtime();
    MPI_Barrier(MPI_COMM_WORLD);


    srand(seed);

    for (long long i = 0; i < local_points; i++) {
        double x = (double)rand() / RAND_MAX;
        double y = (double)rand() / RAND_MAX;
        if (x * x + y * y <= 1.0)
            local_inside++;
    }
    MPI_Reduce(&local_inside, &global_inside, 1,
               MPI_LONG_LONG_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    t_end = MPI_Wtime();

    if (rank == 0) {
        pi_approx = 4.0 * (double)global_inside / (double)total_points;

        printf("Przybliżenie PI  : %.10f\n", pi_approx);
        printf("Czas [s]         : %.6f\n",  t_end - t_start);
    }

    MPI_Finalize();
    return EXIT_SUCCESS;
}


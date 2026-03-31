#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define SIZE 100

int main(int argc, char* argv[]) {

    int *arr = (int *)malloc((size_t)SIZE * sizeof(int));
    if (!arr) {
        fprintf(stderr, "Błąd alokacji pamięci\n");
        return 1;
    }

    #pragma omp parallel for schedule(static)
    for (int i = 0; i < SIZE; i++) {
        unsigned int seed = 42 + omp_get_thread_num() * 1000 + i;
        arr[i] = rand_r(&seed);
        printf("thread: %d  index: %d  number: %d\n",
               omp_get_thread_num(), i, arr[i]);
    }

    free(arr);
    return 0;
}
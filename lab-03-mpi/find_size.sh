#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=00:30:00
#SBATCH --partition=plgrid-testing
#SBATCH --account=plgmpr26-cpu

module add .plgrid plgrid/tools/openmpi
mpicc -O2 -o program_c concurency_montecarlo_2.c -lm

echo "=== looking for small N (T at p=1 << 1s) ==="
for N in 1000000 5000000 10000000 50000000 100000000; do
    T=$(mpirun -np 1 ./program_c $N 2>/dev/null | grep "Czas" | awk '{print $NF}')
    echo "p=1  N=$N  T=${T}s"
done

echo ""
echo "=== looking for large N (T at p=12 >= 60s) ==="
for N in 500000000 1000000000 5000000000 10000000000; do
    T=$(mpirun -np 12 ./program_c $N 2>/dev/null | grep "Czas" | awk '{print $NF}')
    echo "p=12 N=$N  T=${T}s"
done
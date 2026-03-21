#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=00:30:00
#SBATCH --partition=plgrid-testing
#SBATCH --account=plgmpr26-cpu

module add .plgrid plgrid/tools/openmpi
mpicc -O2 -o program_c concurency_montecarlo_2.c -lm

echo "=== looking for small N (T at p=1 << 1s) ==="
for N in 1200 2400 12000 24000 120000; do
    T=$(mpirun -np 1 ./program_c $N 2>/dev/null | grep "Czas" | awk '{print $NF}')
    echo "p=1  N=$N  T=${T}s"
done

echo ""
echo "=== looking for large N (T at p=12 >= 60s) ==="
for N in 2772000000 5544000000 27720000000 55440000000 277200000000; do
    T=$(mpirun -np 12 ./program_c $N 2>/dev/null | grep "Czas" | awk '{print $NF}')
    echo "p=12 N=$N  T=${T}s"
done

echo "================ Done ================"

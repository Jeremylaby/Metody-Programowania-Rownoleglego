#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=08:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr26-cpu

module add .plgrid plgrid/tools/openmpi
mpicc -O2 -o program_c concurency_montecarlo_2.c -lm

REP=${1:-1}
OUT="results/ares/raw_rep${REP}.csv"
mkdir -p results/ares

PROCS=(1 2 3 4 5 6 7 8 9 10 11 12)
N_SMALL=12000
N_MID=18238420
N_BIG=27720000000

for N in $N_SMALL $N_MID $N_BIG; do

    for P in "${PROCS[@]}"; do
        T=$(mpirun -np $P ./program_c $N 2>/dev/null | grep "Czas" | awk '{print $NF}')
        echo "strong,$N,$P,$REP,$T" >> "$OUT"
        echo "[strong] N=$N P=$P rep=$REP T=${T}s"
    done

    for P in "${PROCS[@]}"; do
        N_PER_PROC=$(( N / 10 ))
        N_TOTAL=$(( N_PER_PROC * P ))
        T=$(mpirun -np $P ./program_c $N_TOTAL 2>/dev/null | grep "Czas" | awk '{print $NF}')
        echo "weak,$N_TOTAL,$P,$REP,$T" >> "$OUT"
        echo "[weak] N/proc=$N_PER_PROC N_total=$N_TOTAL P=$P rep=$REP T=${T}s"
    done

done
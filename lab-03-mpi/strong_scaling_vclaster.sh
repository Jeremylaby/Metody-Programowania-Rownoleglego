#!/bin/bash -l
REP=${1:-1}

PROCS=(1 2 3 4 5 6 7 8 9 10 11 12)
N=27720000
N_PER_PROC=2310000

OUT="results/vcluster/raw_rep${REP}.csv"

mkdir -p results/vcluster/
mpicc -o program_c concurency_montecarlo_2.c

if [ ! -f "$OUT" ]; then
    echo "scaling,n_points,procs,rep,time" > "$OUT"
fi

for P in "${PROCS[@]}"; do
    OUTPUT=$(mpiexec -machinefile ./mynodes -np $P ./program_c $N 2>/dev/null)
    T=$(echo "$OUTPUT" | grep "Czas" | awk '{print $NF}')
    echo "strong,$N,$P,$REP,$T" >> "$OUT"
    echo "[strong] N=$N P=$P rep=$REP T=${T}s"
done



for P in "${PROCS[@]}"; do
    N_TOTAL=$(( N_PER_PROC * P ))
    OUTPUT=$(mpiexec -machinefile ./mynodes -np $P ./program_c $N_N_TOTAL 2>/dev/null)
    T=$(echo "$OUTPUT" | grep "Czas" | awk '{print $NF}')
    echo "weak,$N_TOTAL,$P,$REP,$T" >> "$OUT"
    echo "[weak] N=$N_TOTAL P=$P rep=$REP T=${T}s"
done
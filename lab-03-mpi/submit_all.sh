mkdir -p results/ares

module add .plgrid plgrid/tools/openmpi
mpicc -O2 -o program_c concurency_montecarlo_2.c -lm

echo "Kompilacja zakończona"

for i in $(seq 1 12); do
    JOB_ID=$(sbatch --parsable run_ares.sh $i)
    echo "Submitted rep $i → job $JOB_ID"
done


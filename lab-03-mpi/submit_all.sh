mkdir -p results/ares

for i in $(seq 1 12); do
    JOB_ID=$(sbatch --parsable run_ares.sh $i)
    echo "Submitted rep $i → job $JOB_ID"
done

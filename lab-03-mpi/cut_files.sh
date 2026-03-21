for f in results/ares/raw_rep*.csv; do
    tail -72 "$f" > tmp && mv tmp "$f"
done

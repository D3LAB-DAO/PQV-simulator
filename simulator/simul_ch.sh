for r in `seq 1 1 2`; do
    python3 simulator-ch.py --pqvMethod='power' "$@"
done

for r in `seq 1 1 2`; do
        python3 simulator-CH.py --pqvMethod='power' "$@"
    done
done

for r in `seq 1 1 100`; do
    for p in `seq 2 1 16`; do
        for a in `seq 30 30 300`; do
            # python simulator-2.py --pqvMethod='power' --power=2.0 --nPolicies=$p --nAgents=$a "$@"
            python simulator-2.py --pqvMethod='power' --power=2.5 --nPolicies=$p --nAgents=$a --path='./log/'$r "$@"
        done
    done
done

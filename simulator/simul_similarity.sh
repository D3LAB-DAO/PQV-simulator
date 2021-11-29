for r in `seq 1 1 100`; do
    for i in `seq 1.0 0.1 3.05`; do  # 3.0
        # python simulator_similarity.py --pqvMethod='power' --power=$i "$@"
        python simulator_similarity.py --pqvMethod='power' --power=$i --path='./log/'$r "$@"
    done
done

# for i in `seq 10 10 100`; do
#     python simulator_similarity.py --pqvMethod='window' --window=$i "$@"
# done

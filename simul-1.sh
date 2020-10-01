for i in `seq 1.0 0.1 3.1`; do  # 3.0
    python simulator-1.py --pqvMethod='power' --power=$i ${@:1}
done

# for i in `seq 10 10 100`; do
#     python simulator-1.py --pqvMethod='window' --window=$i ${@:1}
# done

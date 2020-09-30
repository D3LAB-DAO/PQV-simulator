for i in `seq 1.0 0.5 3.0`; do
    # echo "$i"
    # python simulator-1.py --nRounds=1000 --nPolicies=16 --nAgents=300 --totalBallots=100000 --nProcess=4 --pqvMethod='power' --power=$i
    python simulator-1.py --pqvMethod='power' --power=$i
done

for i in `seq 10 10 100`; do
    # echo "$i"
    # python simulator-1.py --nRounds=1000 --nPolicies=16 --nAgents=300 --totalBallots=100000 --nProcess=4 --pqvMethod='window' --window=$i
    python simulator-1.py --pqvMethod='window' --window=$i
done

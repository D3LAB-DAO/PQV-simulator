from multiprocessing import Process, Queue
import os
import argparse
import random
# import matplotlib.pyplot as plt
from math import floor
from copy import deepcopy
from tqdm import tqdm
import numpy as np
from numpy.random import permutation, choice

from dist import pareto
from agent import Agent
from box import Box


def simulation(index, s, agents, ps, rounds, args, result):
    random.seed(s)

    unmatchingCount_PQV_vs_equal = 0
    unmatchingCount_PQV_vs_plain = 0
    unmatchingCount_PQV_vs_QV = 0

    for r in tqdm(range(rounds), position=index):
        # print(">>> Process: ", index, "\tRound ", r+1, "\t/", rounds, end='\r')

        """Set Ballot Box"""
        box = Box(args.nPolicies)
        box_equal = deepcopy(box)
        box_plain = deepcopy(box)
        box_QV = deepcopy(box)
        box_PQV = deepcopy(box)
        # box.reset(nPolicies)

        if args.pqvMethod == 'window':
            # idx = list(range())
            total_wheres, total_amounts = [], []

        for a, agent in enumerate(agents):
            # print("\tAgent ", a, end='\r')

            wheres, amounts = agent.voting("equal")
            for where, amount in zip(wheres, amounts):
                box_plain.addBallotOnce(where, amount, args.totalBallots, "equal")

            wheres, amounts = agent.voting("plain")
            for where, amount in zip(wheres, amounts):
                box_plain.addBallotOnce(where, amount, args.totalBallots, "plain")

            wheres, amounts = agent.voting("QV")
            for where, amount in zip(wheres, amounts):
                box_QV.addBallotOnce(where, amount, args.totalBallots, "QV")

            wheres, amounts = agent.voting("PQV")
            if args.pqvMethod == 'window':
                total_wheres += list(wheres)
                total_amounts += list(amounts)
            elif args.pqvMethod == 'power':
                for where, amount in zip(wheres, amounts):
                    box_PQV.addBallotOnce(where, amount, args.totalBallots, "PQV", **{'pqvMethod': 'power', 'power': args.power})

        if args.pqvMethod == 'window':
            idx = list(range(len(total_amounts)))
            p = np.array(total_amounts) / sum(total_amounts)
            res_idx = choice(idx, floor(args.window / 100. * len(total_amounts)), p=p, replace=False)
            total_wheres, total_amounts = np.array(total_wheres)[res_idx], np.array(total_amounts)[res_idx]
            for where, amount in zip(total_wheres, total_amounts):
                box_PQV.addBallotOnce(where, amount, args.totalBallots, "QV")

        """Set Agents"""
        # # Pareto dist
        # ps = pareto(nAgents)
        # ps = [floor(p * (totalBallots / sum(ps))) for p in ps]
        # ps[-1] = totalBallots - sum(ps[:-1])
        for agent, p in zip(agents, ps):
            agent.reset(args.nPolicies, p)

        if box_PQV.getWinner() != box_equal.getWinner():
            unmatchingCount_PQV_vs_equal += 1
        if box_PQV.getWinner() != box_plain.getWinner():
            unmatchingCount_PQV_vs_plain += 1
        if box_PQV.getWinner() != box_QV.getWinner():
            unmatchingCount_PQV_vs_QV += 1

    # print(unmatchingCount)
    result.put((unmatchingCount_PQV_vs_equal,
                unmatchingCount_PQV_vs_plain,
                unmatchingCount_PQV_vs_QV))


if __name__ == "__main__":

    """argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--nRounds', type=int, default=330000)
    parser.add_argument('--nPolicies', type=int, default=16)
    parser.add_argument('--nAgents', type=int, default=300)
    parser.add_argument('--totalBallots', type=int, default=100000)
    parser.add_argument('--nProcesses', type=int, default=33)
    parser.add_argument('--seed', type=int, default=950327)

    parser.add_argument('--pqvMethod', type=str, default='power',
                        choices=('power', 'window'))
    parser.add_argument('--power', type=float, default=1.0)
    parser.add_argument('--window', type=int, default=0)

    parser.add_argument('--path')  # location of log files
    parser.add_argument('--no-save', action='store_true')
    args = parser.parse_args()
    print(args)

    random.seed(args.seed)
    if args.pqvMethod == 'power':
        args.window = None
    elif args.pqvMethod == 'window':
        args.power = None

    # Pareto dist
    ps = pareto(args.nAgents)
    ps = [floor(p * (args.totalBallots / sum(ps))) for p in ps]
    ps[-1] = args.totalBallots - sum(ps[:-1])

    # Agents
    agents = []
    for i in range(args.nAgents):
        agents.append(Agent(args.nPolicies, ps[i]))

    """
    Multiprocessing
    """
    result = Queue()
    seeds = permutation([i for i in range(args.nProcesses)])  # diff. seeds
    procs = []
    for index, s in enumerate(seeds):
        # Process Objects Creation
        procs.append(Process(target=simulation, args=(index, s, agents, ps, floor(args.nRounds / args.nProcesses), args, result)))

    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()

    result.put('STOP')

    _PQV_vs_equal, _PQV_vs_plain, _PQV_vs_QV = 0, 0, 0
    while True:
        tmp = result.get()
        if tmp == 'STOP':
            break
        else:
            _PQV_vs_equal += tmp[0]
            _PQV_vs_plain += tmp[1]
            _PQV_vs_QV += tmp[2]

    sim_PQV_vs_equal = 100. - (_PQV_vs_equal / args.nRounds * 100.)
    sim_PQV_vs_plain = 100. - (_PQV_vs_plain / args.nRounds * 100.)
    sim_PQV_vs_QV = 100. - (_PQV_vs_QV / args.nRounds * 100.)
    # print("\nsimilarity: ", sim, "%")

    path = (args.path or './log')
    os.makedirs(path, exist_ok=True)
    with open(path + "/simul-heatmap.txt", "a") as f:
        f.write(
            str(args.nPolicies) + "\t" + str(args.nAgents) + "\t" +
            str(sim_PQV_vs_equal) + "\t" +
            str(sim_PQV_vs_plain) + "\t" +
            str(sim_PQV_vs_QV) + "\t" +
            "\n")

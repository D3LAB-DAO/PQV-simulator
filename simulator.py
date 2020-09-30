from multiprocessing import Process, Queue
import os
import argparse
import random
# import matplotlib.pyplot as plt
from math import floor
from copy import deepcopy
from tqdm import tqdm
from numpy.random import permutation

from dist import pareto
from agent import Agent
from box import Box


def simulation(index, s, agents, ps, rounds, args, result):
    random.seed(s)

    unmatchingCount = 0

    for r in tqdm(range(rounds), position=index):
        # print(">>> Process: ", index, "\tRound ", r+1, "\t/", rounds, end='\r')

        """Set Ballot Box"""
        box = Box(args.nPolicies)
        box_equal = deepcopy(box)
        box_QV = deepcopy(box)
        box_PQV = deepcopy(box)
        # box.reset(nPolicies)

        for a, agent in enumerate(agents):
            # print("\tAgent ", a, end='\r')

            wheres, amounts = agent.voting("equal")
            for where, amount in zip(wheres, amounts):
                box_equal.addBallotOnce(where, amount, args.totalBallots, "equal")

            wheres, amounts = agent.voting("QV")
            for where, amount in zip(wheres, amounts):
                box_QV.addBallotOnce(where, amount, args.totalBallots, "QV")

            wheres, amounts = agent.voting("PQV")
            for where, amount in zip(wheres, amounts):
                box_PQV.addBallotOnce(where, amount, args.totalBallots, "PQV")

        """Set Agents"""
        # # Pareto dist
        # ps = pareto(nAgents)
        # ps = [floor(p * (totalBallots / sum(ps))) for p in ps]
        # ps[-1] = totalBallots - sum(ps[:-1])
        for agent, p in zip(agents, ps):
            agent.reset(args.nPolicies, p)

        if box_PQV.getWinner() != box_QV.getWinner():
            # print(">>> winner : ", box_equal.getWinner(), "\t", box_QV.getWinner(), "\t", box_PQV.getWinner())
            unmatchingCount += 1
        # print(">>> current: ", box_equal.policies, "\t", box_QV.policies, "\t", box_PQV.policies,)
        # print("\n")

    # print(unmatchingCount)
    result.put(unmatchingCount)


if __name__ == "__main__":

    """argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--nRounds', type=int, default=10000)
    parser.add_argument('--nPolicies', type=int, default=15)
    parser.add_argument('--nAgents', type=int, default=10000)
    parser.add_argument('--totalBallots', type=int, default=1000000)
    # parser.add_argument('--txWindowMin', type=int, default=51)
    # parser.add_argument('--votingMethod', type=str, default='QV',
    #                     choices=('equal', 'QV', 'PQV'))
    parser.add_argument('--nProcesses', type=int, default=20)
    parser.add_argument('--seed', type=int, default=950327)
    # parser.add_argument('--path')  # location of log files
    # parser.add_argument('--no-save', action='store_true')
    args = parser.parse_args()
    print(args)

    random.seed(args.seed)

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

    _sum = 0
    while True:
        tmp = result.get()
        if tmp == 'STOP':
            break
        else:
            _sum += tmp

    # print("\nunmatchingCount: ", _sum)
    print("\nsimilarity: ", 100. - (_sum / args.nRounds * 100.), "%")

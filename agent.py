from numpy.random import permutation
from random import randint
from math import floor


class Agent():
    def __init__(self, nPolicies, ballot):
        self.nPolicies = nPolicies
        self.ballot = ballot
        self.setPolicies()

    def setPolicies(self):
        self.policies = permutation([i for i in range(self.nPolicies)])
        self.ineqs = [randint(0, 1) for _ in range(self.nPolicies - 1)]  # 0 for > | 1 for >=

    def voting(self, method):
        if method == "equal":
            return [self.policies[0]], [self.ballot]
        elif (method == "QV") or (method == "PQV"):
            try:
                selectedNum = self.ineqs.index(0)
            except(ValueError):
                selectedNum = len(self.ineqs)
            if selectedNum == 0:
                return [self.policies[0]], [self.ballot]
            else:
                perAmount = floor(self.ballot / selectedNum)
                return self.policies[:selectedNum], [perAmount] * (selectedNum - 1) + [self.ballot - perAmount * (selectedNum - 1)]
        else:
            raise Exception("Wrong Method")

    def reset(self, nPolicies, ballot):
        self.nPolicies = nPolicies
        self.ballot = ballot
        self.setPolicies()

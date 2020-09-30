from math import sqrt, floor
from random import randint


class Box():
    def __init__(self, nPolicies):
        self.nPolicies = nPolicies
        self.initPolicies()

    def initPolicies(self):
        self.policies = [0 for _ in range(self.nPolicies)]

    def getWinner(self):
        return self.policies.index(max(self.policies))

    def _linear(self, amount, totalBallots):
        if amount >= randint(1, totalBallots):
            return True
        else:
            return False

    def addBallotOnce(self, policy, amount, totalBallots, method):
        if method == "equal":
            self.policies[policy] += amount
        elif method == "QV":
            self.policies[policy] += floor(sqrt(amount))
        elif method == "PQV":
            picked = self._linear(amount, totalBallots)
            if picked:
                self.policies[policy] += floor(sqrt(amount))
            else:
                pass
        else:
            raise Exception("Wrong Method")

    def reset(self, nPolicies):
        self.nPolicies = nPolicies
        self.initPolicies()

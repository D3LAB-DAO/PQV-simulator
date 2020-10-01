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

    def _power(self, amount, totalBallots, power):
        if amount ** power >= randint(1, totalBallots):
            return True
        else:
            return False

    def _window(self):
        return True

    def addBallotOnce(self, policy, amount, totalBallots, votingMethod, **kwargs):
        if votingMethod == "equal":
            self.policies[policy] += 1
        elif votingMethod == "plain":
            self.policies[policy] += amount
        elif votingMethod == "QV":
            self.policies[policy] += floor(sqrt(amount))
        elif votingMethod == "PQV":
            if kwargs['pqvMethod'] == "linear":
                picked = self._linear(amount, totalBallots)
            elif kwargs['pqvMethod'] == "power":
                picked = self._power(amount, totalBallots, kwargs['power'])
            # elif kwargs['pqvMethod'] == "window":
            #     return
            else:
                raise Exception("Wrong Method")

            if picked:
                self.policies[policy] += floor(sqrt(amount))
            else:
                pass
        else:
            raise Exception("Wrong Method")

    def reset(self, nPolicies):
        self.nPolicies = nPolicies
        self.initPolicies()

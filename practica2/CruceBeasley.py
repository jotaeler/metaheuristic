# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.
#

import random


class CruceBeasley(object):
    """Perform single point crossover between genomes at some defined rates.

    This performs a single crossover between two genomes at some
    defined frequency. The location of the crossover is chosen randomly
    if the crossover meets the probability to occur.
    """
    def __init__(self, crossover_prob=.1, uniform_prob=0.7):
        """Initialize to do uniform crossover at the specified probability and frequency.
        """
        self._crossover_prob = crossover_prob
        self._uniform_prob = uniform_prob
        return

    def do_crossover(self, org_1, org_2):
        """Potentially do a crossover between the two organisms.
        """
        new_org_1 = org_1.copy()
        new_org_2 = org_2.copy()
        new_hijo = org_1.copy()

        suma = new_org_1.fitness+new_org_2.fitness
        if suma == 0: suma = random.random()
        p = new_org_1.fitness / suma

        minlen = min(len(new_org_1.genome), len(new_org_2.genome))
        for i in range(minlen):
            if new_org_1.genome[i] == new_org_2.genome[i]:
                new_hijo.genome[i] = new_org_1.genome[i]
            else:
                rand = random.random()
                if rand >= p:
                    new_hijo.genome[i] = new_org_1.genome[i]
                else:
                    new_hijo.genome[i] = new_org_2.genome[i]
        return new_hijo, new_hijo

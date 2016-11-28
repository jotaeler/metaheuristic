# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.
#

"""Evolution Strategies for a Population.

Evolver classes manage a population of individuals, and are responsible
for taking care of the transition from one generation to the next.
"""
# standard modules
from __future__ import print_function
from LocalSearch import LocalSearch

import sys

class GenerationEvolver(object):
    """Evolve a population from generation to generation.

    This implements a Generational GA, in which the population moves from
    generation to generation.
    """
    def __init__(self, starting_population, selector):
        """Initialize the evolver.

        Arguments:

        o starting_population -- An initial set of individuals to begin
        the evolution process from. This should be a list of Organism
        objects.

        o selector -- A Selection object that implements selection, along
        with mutation and crossover to select a new population from a
        given population.
        """
        self._population = starting_population
        self._selector = selector

    def evolve(self, stopping_criteria, generations, mode, costs, matrix, sectors, subsectors):
        """Evolve the population through multiple generations.

        Arguments:

        o stoppping_criteria -- A function which, when passed the current
        individuals in the population, will determine when to stop
        the evolution process.

        Returns:

        o The final evolved population.
        """
        generation = 0
        while not(stopping_criteria(self._population)):
            try:
                if generation == 10:
                    if mode == 1:
                        for organism in self._population:
                            organism.recalculate_fitness()
                    elif mode == 2:
                        pass
                    elif mode == 3:
                        pass
                # perform selection, mutation, crossover on the population
                self._population = self._selector.select(self._population)

                # update the fitness of the new popultation
                for organism in self._population:
                    organism.recalculate_fitness()

            # dump out all of the organisms for debugging if the
            # evolution process is broken with a Control-C
            except KeyboardInterrupt:
                # sort the population so we can look at duplicates
                self._population.sort()
                for org in self._population:
                    print(org)
                sys.exit()

        return self._population

import numpy as np
from typing import List, Tuple, Callable
from Problem import Problem, Placement
from functools import partial

"""
We implement a genetic algorithm to solve the 3D bin packing problem.
- Instead of determining the exact coordinate of each item, we look for the order in which items are placed in the bin.
- The placement of items in the bin can follow several heuristic methods.
- This approach significantly reduces the search space and computational complexity.
"""

# Use singleton technique as a Configuration class to store global parameters
class Configuration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance
    
    def __init__(self,
                 objective_function: Callable[[List[float]], float] = None,
                 n_items: int = None,
                 n_individuals: int = None,
                 n_elites: int = None,
                 n_generations: int = None,
                 p_crossover: float = None,
                 p_mutation: float = None,
                 problem: Problem = None,
                 verbose: bool = False):
        if not hasattr(self, 'initialized'):
            self.objective_function = objective_function
            self.n_items = n_items
            self.n_individuals = n_individuals
            self.n_elites = n_elites
            self.n_generations = n_generations
            self.p_crossover = p_crossover
            self.p_mutation = p_mutation
            self.problem = problem
            self.verbose = verbose
            self.initialized = True

class Individual:
    """
    We use Random-Key Representation to encode the chromosome of an individual.
    * First n genes are used to encode the order of n items.
    - Each gene is a random number between 0 and 1.
    - The order of genes in the chromosome determines the order of items placed in the bin.

    Example:
    - Chromosome: [0.2, 0.7, 0.1, 0.5, 0.3]
    - Order of items: [3, 1, 5, 2, 4]

    * Last n genes are used to encode the orientation of n items.
    - Each gene is a random number between 0 and 1.
    - There are 6 possible orientations for each item: O = [1, 2, 3, 4, 5, 6]
    - The orientation of item is calculated by: O[ceil(6 * gene)]

    Example:
    - Chromosome: [0.8, 0.3, 0.6, 0.9, 0.4]
    - Orientation of items: [5, 2, 4, 6, 3]
    """
    def __init__(self, chromosome: List[float]):
        # Access the unique instance of Configuration class to get global parameters
        self.cofig = Configuration()

        self.chromosome = chromosome
        self.fitness = self.cofig.objective_function(chromosome)

class Population:
    def __init__(self):
        # Access the unique instance of Configuration class to get global parameters
        self.cofig = Configuration()

        self.n_items = self.cofig.n_items
        self.n_individuals = self.cofig.n_individuals
        self.n_elites = self.cofig.n_elites
        self.n_generations = self.cofig.n_generations
        self.p_crossover = self.cofig.p_crossover
        self.p_mutation = self.cofig.p_mutation

        self.n_genes = 2 * self.n_items
        self.n_mutants = int(self.p_mutation * self.n_individuals)
        self.n_offsprings = self.n_individuals - self.n_elites - self.n_mutants

        self.individuals: List[Individual] = []
        self.elites: List[Individual] = []
        self.non_elites: List[Individual] = []
        
    def initialize(self):
        """
        - Initialize the population by uniformly sampling the chromosome space.
        """
        for _ in range(self.n_individuals):
            chromosome = np.random.rand(2 * self.n_items)
            individual = Individual(chromosome)
            self.individuals.append(individual)

    def partition(self):
        """
        - The population is partitioned into two groups: elite and non-elite based on their fitness.
        """
        self.fitnesses = [individual.fitness for individual in self.individuals]
        indices = np.argsort(self.fitnesses)
        self.elites = [self.individuals[i] for i in indices[:self.n_elites]]
        self.non_elites = [self.individuals[i] for i in indices[self.n_elites:]]

    def crossover(self, elite: Individual, non_elite: Individual) -> Individual:
        """
        - Crossover is performed between one elite and one non-elite individual.
        - Each gene is randomly chosen from either parent with a probability of p_crossover. 
        """

        offspring = [0] * (self.n_genes)

        for i in range(self.n_genes):
            if np.random.rand() < self.p_crossover:
                offspring[i] = elite.chromosome[i]
            else:
                offspring[i] = non_elite.chromosome[i]

        return Individual(offspring)
    
    def mating(self):
        """
        - Mating is performed between elite and non-elite individuals to generate offsprings.
        """
        offsprings: List[Individual] = []
        for _ in range(self.n_offsprings):
            elite = np.random.choice(self.elites)
            non_elite = np.random.choice(self.non_elites)
            offspring = self.crossover(elite, non_elite)
            offsprings.append(offspring)

        return offsprings
    
    def mutation(self):
        """
        - Create entirely new individuals by uniformly sampling to increase diversity.
        """
        mutants: List[Individual] = []
        for _ in range(self.n_mutants):
            chromosome = np.random.rand(2 * self.n_items)
            mutant = Individual(chromosome)
            mutants.append(mutant)

        return mutants

class Optimizer:
    def __init__(self):
        self.config = Configuration()
        self.population = Population()

        self.n_generations = self.config.n_generations

    def optimize(self):
        self.population.initialize()
        for generation in range(self.n_generations):
            self.population.partition()
            if self.config.verbose and generation % 10 == 0:
                print(f'Best fitness: {self.population.elites[0].fitness} | Number of bins used: {self.config.problem.used_bins} | Loads: {self.config.problem.loads}')
            offsprings = self.population.mating()
            mutants = self.population.mutation()
            self.population.individuals = self.population.elites + offsprings + mutants

# TEST THE GENETIC ALGORITHM
if 11 < 3:
    def objective_function(chromosome: List[float]) -> float:
        return sum(chromosome)

    Configuration(objective_function, 5, 10, 2, 10, 0.8, 0.1)
    np.random.seed(0)
    Optimizer().optimize()

# Define the objective function to evaluate the fitness of an individual

"""
In this part, we decode the chromosome of an individual as an placement strategy to calculate its fitness.
- Each bin maintains a list of Empty Maximal Spaces (EMSs) to store the remaining space in the bin.
- We choose the EMS for an item based on Distance to the Front-Top-Right Corner (FTR) rule.
"""

def evaluate(solution: List[float], problem: Problem) -> float:
    placement = Placement(problem)
    return placement.evaluate(solution)
        
if 1 < 3:
    def solve(path, seed=10):
        np.random.seed(seed)
        problem = Problem(path)
        objective_function = partial(evaluate, problem)
        Configuration(objective_function, problem.total_items, 100, 10, 1000, 0.8, 0.3, problem, True)
        Optimizer().optimize()

    solve('Data/Dataset/test.dat', 1)
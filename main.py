import random
import numpy as np

# Simple Genetic Algorithm with 20 Chromosomes(solutions) with length of 5 genes


def Generate_Probabilities(array):
    shape = array.shape# The dimensions of the array
    solutions = np.zeros(shape[0] , dtype=float)
    for i in range(shape[0]):
        for j in range(shape[1]):
            solutions[i] += array[i][j]

    probabilities = solutions/solutions.sum()
    return probabilities


def Selection(array):
    # Generate cumulative probabilities
    cumulative_probabilities = np.cumsum(array)
    num1 = random.random()
    i = 0
    while num1 > cumulative_probabilities[i]:
        i += 1
    j=0
    while i == j:
        num2 = random.random()
        while num2 > cumulative_probabilities[j]:
            j+=1

    return i , j


# Crossover function takes two lists as parents and returns two lists as children using one-point cross over
def crossover(parent1, parent2):

    pCross = random.random()
    if pCross < 0.6:
        # Take the index of separation randomly
        split_point = random.randint(0 , len(parent1)-1)
        child1 = parent1[:split_point] + parent2[split_point:]
        child2 = parent2[:split_point] + parent1[split_point:]
        return child1 , child2
    else:
        return parent1 , parent2


# Mutation Function takes a 2d array that contains the solutions and perform mutation on them with parameter = 0.01
def Mutation(array):
    for i in range(len(array)):
        if random.random() < 0.05:# Then there is a mutation
            flib_index = int(random.uniform(0 , 5))
            if array[i][flib_index] == 1:
                array[i][flib_index] = 0
            else:
                array[i][flib_index] = 1
    # No need for returning it its values will be changed




# Initialize an arbitrary solution at the first
nums_of_solutions = 5
nums_of_genes = 5
generations = 100
population = np.random.randint(0,2 , size=(nums_of_solutions , nums_of_genes))# Create 2D array with random values zeros or ones with dimensions of 20*5
new_generation = np.zeros((nums_of_solutions , nums_of_genes) , dtype=int)# New Generation initializes with zero values

print(f"Before\n{population}")

for i in range(generations):

    probabilities = Generate_Probabilities(population)
    sorted_prob_indices = np.argsort(probabilities)
    sorted_population = population[sorted_prob_indices][::-1]# Sort the population 2D array with the order of the probabilities descending
    new_generation[0] = sorted_population[0]
    new_generation[1] = sorted_population[1]
    j=2
    while j < nums_of_solutions-1:
        parent1_index, parent2_index = Selection(probabilities)# This line returns the index of two parents which are married
        # Get the two parents from the population by their index
        parent1 = population[parent1_index , :]
        parent2 = population[parent2_index , :]

        child1 , child2 = crossover(parent1.tolist(), parent2.tolist())# Get the new children by crossover function which takes two lists and returns two lists
        new_generation[j] = child1
        new_generation[j+1] = child2
        j += 2

    Mutation(new_generation)
    population = new_generation


print("#"*60)
print(f"After\n{population}")

probabilities = Generate_Probabilities(population)
sorted_prob_indices = np.argsort(probabilities)
print(f"The Best solution of the final population is: {population[sorted_prob_indices[nums_of_solutions-1]]}")






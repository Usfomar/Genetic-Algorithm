import random
import numpy as np

# Simple Genetic Algorithm with 20 Chromosomes(solutions) with length of 5 genes


def Generate_Probabilities(array):
    shape = array.shape  # The dimensions of the array
    fitness = np.zeros(shape[0], dtype=int)
    for i in range(shape[0]):
        for j in range(shape[1]):
            fitness[i] += array[i][j]

    probabilities = fitness / fitness.sum()
    return fitness , probabilities


def Selection(array):
    # Generate cumulative probabilities
    cumulative_probabilities = np.cumsum(array)
    num1 = random.random()
    i = 0
    while num1 > cumulative_probabilities[i]:
        i += 1
    j = 0
    while i == j:
        num2 = random.random()
        while num2 > cumulative_probabilities[j]:
            j += 1

    return i, j


# Crossover function takes two lists as parents and returns two lists as children using one-point cross over
def crossover(parent1, parent2, PCross):

    pCross = random.random()
    if pCross < PCross:
        # Take the index of separation randomly
        split_point = random.randint(0, len(parent1) - 1)
        child1 = parent1[:split_point] + parent2[split_point:]
        child2 = parent2[:split_point] + parent1[split_point:]
        return child1, child2
    else:
        return parent1, parent2


# Mutation Function takes a 2d array that contains the solutions
# and perform mutation on them with parameter = 0.01
def Mutation(array, PMuation):
    for i in range(len(array)):
        if random.random() < PMuation:  # Then there is a mutation
            flib_index = int(random.uniform(0, 5))
            if array[i][flib_index] == 1:
                array[i][flib_index] = 0
            else:
                array[i][flib_index] = 1
    # No need for returning it its values will be changed



def Do_GA(Pop_Size, Num_Generations, Chromosome_Length, Prop_Crossover, Prop_Mutation):
    #Create 2D array with random values zeros or ones with dimensions of 20*5
    Intial_Population = np.random.randint(0, 2, size=(Pop_Size, Chromosome_Length))
    Population = Intial_Population
    
    new_generation = np.zeros((Pop_Size, Chromosome_Length), dtype=int)

    Best_Hist_Fitness = []#Best fitness in each generation
    
    for i in range(Num_Generations):
        #Generates a probability of each solution based on its fitness
        fitness , probabilities = Generate_Probabilities(Population)
        
        #Sort the indices of the probability list acsending
        sorted_prob_indices = np.argsort(probabilities)
        
        #Rearrange the population in a new list by the indices above
        sorted_population = Population[sorted_prob_indices][::-1]

        Best_Hist_Fitness.append(fitness.max())
        
        # Add best two solutions in the new generation
        new_generation[0] = sorted_population[0]
        new_generation[1] = sorted_population[1]
        
        # And start adding children from index 2 and jumps step = 2
        j = 2
        while j < Pop_Size - 1:
            # Returns the index of two parents which are married
            parent1_index, parent2_index = Selection(probabilities)
            # Get the two parents from the population by their index
            parent1 = Population[parent1_index, :]
            parent2 = Population[parent2_index, :]
            #Get the new children by crossover function which takes two lists and returns two lists
            child1, child2 = crossover(parent1.tolist(), parent2.tolist(), Prop_Crossover)
            # Add child in this index and one in the next index
            new_generation[j] = child1
            new_generation[j + 1] = child2
            
            j += 2  # jumps two steps

        Mutation(new_generation, Prob_Muation)
        Population = new_generation
    
    #The result of the algorithm as a list
    return Intial_Population , Population , Best_Hist_Fitness


Pop_Size = 6
Chromosome_Length = 5
generations = 10
Prob_Crossover = 0.6
Prob_Muation = 0.05

Initial_Solution , Result , Best_Hist_Fitness = Do_GA(Pop_Size , generations , Chromosome_Length , Prob_Crossover , Prob_Muation)
AVG_Best_Fitness = sum(Best_Hist_Fitness)/len(Best_Hist_Fitness)

print(f"Initial Population:\n{Initial_Solution}")
print(f"Final Solutions:\n{Result}")
print(f"The best solutions over {generations} generations:\n{Best_Hist_Fitness}")
print(f"The average of all best solutions over generations: {AVG_Best_Fitness}")

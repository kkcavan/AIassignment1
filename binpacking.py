import random
import csv




# Read data from CSV file
data_file = 'BinpackingProblems\BPP1.csv'

with open(data_file, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Extract information from the CSV data
problem_name = rows[0][0]
num_items = int(rows[1][0])
bin_capacity = int(rows[2][0])

# Extract item weights and numbers
item_weights = [int(row[0]) for row in rows[3:]]
item_numbers = [int(row[1]) for row in rows[3:]]

# Parameters
population_size = num_items
# string_length = 30
mutation_rate = 0.01
crossover_rate = 0.8
generations = 200


# Initialize population
population = item_weights[:population_size]
# population = [''.join(random.choice('01') for _ in range(num_items)) for _ in range(population_size)]

def bin_packing_fitness(individual, bin_capacity, item_numbers):
    num_bins = 1
    bin_weight = 0

    for i in range(0, len(individual), num_items):
        item_weight = sum(individual[i:i + num_items])
        bin_weight += item_weight * item_numbers[i // num_items]

        while bin_weight > bin_capacity:
            num_bins += 1
            bin_weight -= bin_capacity

    return num_bins

def mutate(individual):
    mutated_individual = individual.copy()

    for i in range(0, len(mutated_individual), num_items):
        if random.random() < mutation_rate:
            mutated_individual[i:i + num_items] = [random.randint(0, bin_capacity) for _ in range(num_items)]

    return mutated_individual

def crossover(parent1, parent2):
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) // num_items - 1) * num_items
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1, parent2
def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    selection_probabilities = [fitness / total_fitness for fitness in fitness_values]

    # Select individuals using Roulette Wheel Selection
    selected_indices = random.choices(range(len(population)), weights=selection_probabilities, k=len(population))

    # Return the selected individuals
    selected_population = [population[index] for index in selected_indices]
    return selected_population

# Main loop
# best_fitness_list = []
num_bins_used_list =[]

for generation in range(generations):
    # Calculate fitness for each individual
    fitness_values = [bin_packing_fitness(individual, bin_capacity,item_numbers) for individual in population]

    # Calculate best fitness
    best_fitness = min(fitness_values)  # Minimize the number of used bins
    # best_fitness_list.append(max(fitness_values))
    
    num_bins_used_list.append(best_fitness)
    # Print the number of bins used in each generation
    # print(f"Generation {generation + 1}: Number of Bins Used = {best_fitness}")
    
    # Select parents based on fitness values using Roulette Wheel Selection
    selected_population = roulette_wheel_selection(population, fitness_values) 

    # Create next generation
    new_population = []
    for i in range(0, len(selected_population), 2):
        parent1, parent2 = selected_population[i], selected_population[i+1]
        child1, child2 = crossover(parent1, parent2)
        child1 = mutate(child1)
        child2 = mutate(child2)
        new_population.extend([child1, child2])

    population = new_population

# Output fitness values
with open('binpacking.csv', 'w') as file:
    file.write("Generation,Number of Bins Used\n")
    for i, num_bins_used in enumerate(num_bins_used_list):
        file.write(f"{i+1},{num_bins_used}\n")






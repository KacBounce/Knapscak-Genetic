import random
import matplotlib.pyplot as plt

def generate_items(num_items):
    items = {}
    for i in range(1, num_items + 1):
        item = {
            'value': random.randint(1, 20),  # Generate random value
            'weight': random.randint(1, 20)  # Generate random weight
        }
        items[f'item{i}'] = item
    return items

#items with random weights
items = generate_items(20)

# Knapsack capacity
capacity = 100

# Genetic Algorithm parameters
population_size = 20
mutation_rate = 0.1
generations = 200

# Function to create initial population
def create_population():
    population = []
    for _ in range(population_size):
        chromosome = [random.choice([0, 1]) for _ in range(len(items))]
        population.append(chromosome)
    return population

# Function to calculate fitness of each chromosome
def fitness(chromosome):
    total_value = 0
    total_weight = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_value += items[f'item{i+1}']['value']
            total_weight += items[f'item{i+1}']['weight']
    if total_weight > capacity:
        return 0
    else:
        return total_value

# Function for selection (roulette wheel selection)
def selection(population):
    fitness_sum = sum(fitness(chromosome) for chromosome in population)
    selected = []
    for _ in range(population_size):
        pick = random.uniform(0, fitness_sum)
        current = 0
        for chromosome in population:
            current += fitness(chromosome)
            if current > pick:
                selected.append(chromosome)
                break
    return selected

# Function for crossover (single point crossover)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(items) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Function for mutation
def mutation(chromosome):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]  # Flip the bit
    return chromosome

# Main genetic algorithm function
def genetic_algorithm():
    population = create_population()
    fitness_values = []
    for _ in range(generations):
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(selection(population), k=2)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutation(child1))
            new_population.append(mutation(child2))
        population = new_population
        best_fitness = max([fitness(chromosome) for chromosome in population])
        fitness_values.append(best_fitness)
    best_solution = max(population, key=lambda chromosome: fitness(chromosome))
    return best_solution, fitness_values

# Run the genetic algorithm
best_solution, fitness_values = genetic_algorithm()
total_weight = 0
for i in range(len(best_solution)):
        if best_solution[i] == 1:
            total_weight += items[f'item{i+1}']['weight']
print("Best solution:", best_solution)
print("Best fitness:", fitness(best_solution))
print("Total solution weight:", total_weight)
# Plot fitness values
plt.plot(range(generations), fitness_values)
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Fitness Progression')
plt.show()

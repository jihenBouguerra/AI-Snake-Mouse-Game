from Genetic_Algorithm import *
from Genetic_Algorithm_mousse import * 
from Snake_Game import *

# n_x -> no. of input units
# n_h -> no. of units in hidden layer 1
# n_h2 -> no. of units in hidden layer 2
# n_y -> no. of output units

# The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
sol_per_pop = 50
num_weights = n_x*n_h + n_h*n_h2 + n_h2*n_y
num_weights_m = n_x_m*n_h_m + n_h_m*n_h2_m + n_h2*n_y_m

# Defining the population size.
pop_size = (sol_per_pop,num_weights)
pop_size_mousse=(sol_per_pop,num_weights_m)
#Creating the initial population.
new_population = np.random.choice(np.arange(-1,1,step=0.01),size=pop_size,replace=True)
new_population_mousse=np.random.choice(np.arange(-1,1,step=0.01),size=pop_size_mousse,replace=True)
num_generations = 100

num_parents_mating = 12
for generation in range(num_generations):
    print('##############        GENERATION ' + str(generation)+ '  ###############' )
    # Measuring the fitness of each chromosome in the population.
    
    fitness_mousse=cal_pop_fitness_mousse(new_population_mousse)
   # fitness = cal_pop_fitness(new_population)

    
#    print('#######  fittest chromosome in gneneration ' + str(generation) +' is having fitness value:  ', np.max(fitness))
    print('#######  fittest chromosome in gneneration mousse ' + str(generation) +' is having fitness value:  ', np.max(fitness_mousse))
    # Selecting the best parents in the population for mating.
   # parents = select_mating_pool(new_population, fitness, num_parents_mating)
    parents_mousse=select_mating_pool_mousse(new_population_mousse, fitness_mousse, num_parents_mating)

    # Generating next generation using crossover.
    #offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))
    offspring_crossover_mousse = crossover_mousse(parents_mousse, offspring_size=(pop_size_mousse[0] - parents_mousse.shape[0], num_weights_m))

    # Adding some variations to the offsrping using mutation.
    #offspring_mutation = mutation(offspring_crossover)
    offspring_mutation_mousse = mutation_mousse(offspring_crossover_mousse)

    # Creating the new population based on the parents and offspring.
   # new_population[0:parents.shape[0], :] = parents
    new_population_mousse[0:parents_mousse.shape[0], :] = parents_mousse
    #new_population[parents.shape[0]:, :] = offspring_mutation
    new_population_mousse[parents_mousse.shape[0]:, :] = offspring_mutation_mousse
    if generation == 99:
        # file_s = open("snake.txt", "w")
        # file_s.write(str(get_w(new_population[49])))
        # file_s.close()
        file_m = open("mousse.txt", "w")
        file_m.write(str(get_w_m(new_population_mousse[49])))
        file_m.close()
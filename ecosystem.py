import numpy as np
import random
import objects
import time

class ecosystem:

    def __init__( self, \
                  order,  \
                  initial_no=np.array([ 10, 1 ]), \
                  initial_hunger=np.array([ 100, 200 ]), \
                  hunger_rate=np.array([ 1, 1 ]), \
                  reproduction_threshold=np.array([ 50, 100 ]), \
                  reproduction_transfer=np.array([ 20, 40 ]), \
                  reproduction_rate=np.array([ 7, 20 ]), \
                  life_span=np.array([ 100, 100 ]), \
                  animal_max_hunger=np.array([ 100, 200 ]), \
                  animal_consume_rate=np.array([ 5, 20 ]), \
                  initial_food_distribution = [[0,0,0]], \
                  food_capacity=120, \
                  enable_draw=False, \
                ):
        '''
        input of initial_food_distribution is a list of 3-vector, with the first 2 elements the coordinates and the 3rd=amount of food.
        '''

        self.__space = [ [ None for _ in range(order) ] for _ in range(order) ]

        self.__animals = list()

        self.__preys = list()

        self.__predators = list()

        self.__space_order = order

        self.__food_capacity = food_capacity

        self.__total_food = 0.

        self.__animal_food = np.array([ 0., 0. ])

        self.__vege_food = 0.

        # Total no of preys, dead inclusive
        self.__animal_no = np.array([ 0, 0 ])

        self.__animal_life_no = np.array([ 0, 0 ])

        # parameters
        self.__initial_no = initial_no

        self.__initial_hunger = initial_hunger

        self.__life_span = life_span

        self.__hunger_rate = hunger_rate

        self.__reproduction_threshold = reproduction_threshold

        self.__reproduction_transfer = reproduction_transfer

        self.__reproduction_rate = reproduction_rate

        self.__animal_life_span = life_span

        self.__animal_max_hunger = animal_max_hunger

        self.__animal_consume_rate = animal_consume_rate

        self.__enable_draw = enable_draw

        # analysis variables
        self.__frame = 0

        self.__prey_no_array = np.array([])

        self.__predator_no_array = np.array([])

        self.__prey_gene1_array_high = np.array([])

        self.__prey_gene1_array_low = np.array([])

        self.__prey_gene2_array_high = np.array([])

        self.__prey_gene2_array_low = np.array([])

        self.__frame_array = np.array([])

        self.__prey_birth = 0

        self.__prey_natural_death = 0

        self.__prey_killed = 0

        self.__predator_birth = 0

        self.__predator_death = 0

        self.__prey_genes_tuple = list()



        # Construct space and initialize animals
        for i in range( order ):
            for j in range( order ):
                self.__space[i][j] = objects.space( [i,j] )

                animal_type = 0
                if i % 2 == 0 and j % 2 == 0 and not i == 0 and not j == 0:

                    start_gene_1 = random.uniform( 0, 20 )
                    start_gene_2 = random.uniform( 0, 20 )

                    self.add_animal( animal_type, \
                                     np.array([ i, j ]), \
                                     initial_hunger[animal_type], \
                                     animal_max_hunger[animal_type], \
                                     reproduction_threshold[animal_type], \
                                     reproduction_transfer[animal_type], \
                                     reproduction_rate[animal_type], \
                                     hunger_rate[animal_type], \
                                     life_span[animal_type], \
                                     animal_consume_rate[animal_type], \
                                     start_gene_1, \
                                     start_gene_2, \
                                     0, \
                                     0, \
                                     start_gene_2, \
                                     start_gene_1, \
                                     start_gene_2
                                    )



        #
        #     # Initialize food
        #     for food in initial_food_distribution:
        #         self.__space[food[0]][food[1]].add_food(food[2])

    def add_animal( self, \
                    animal_type, \
                    position, \
                    hunger, \
                    max_hunger,\
                    reproduction_threshold, \
                    reproduction_transfer, \
                    reproduction_rate, \
                    hunger_rate,\
                    life_span, \
                    consume_rate, \
                    hunger_rate_gene, \
                    reproduction_rate_gene, \
                    life_span_gene, \
                    consume_rate_gene, \
                    no_offspring_gene, \
                    fighting_gene, \
                    reproduction_threshold_gene, \
                    ):
        '''
        add ONE prey to the ecosystem
        '''
        if animal_type == 0:
            self.__preys.append( objects.prey( self.__animal_no[0], \
                                               position, \
                                               hunger, \
                                               max_hunger, \
                                               reproduction_threshold, \
                                               reproduction_transfer, \
                                               reproduction_rate, \
                                               hunger_rate,\
                                               life_span, \
                                               consume_rate, \
                                               hunger_rate_gene, \
                                               reproduction_rate_gene, \
                                               life_span_gene, \
                                               consume_rate_gene, \
                                               no_offspring_gene, \
                                               fighting_gene, \
                                               reproduction_threshold_gene, \
                                               ) )
            self.__animal_no += np.array([ 1, 0 ])
        if animal_type == 1:
            self.__predators.append( objects.predator( self.__animal_no[1], \
                                                       position, \
                                                       hunger, \
                                                       max_hunger,\
                                                       reproduction_threshold, \
                                                       reproduction_transfer, \
                                                       reproduction_rate, \
                                                       hunger_rate,\
                                                       life_span, \
                                                       consume_rate, \
                                                       hunger_rate_gene, \
                                                       reproduction_rate_gene, \
                                                       life_span_gene, \
                                                       consume_rate_gene, \
                                                       no_offspring_gene, \
                                                       fighting_gene, \
                                                       reproduction_threshold_gene, \
                                                       ) )
            self.__animal_no += np.array([ 0, 1 ])


    def add_food( self, position, value ):
        '''
        add food to the system
        '''
        self.__space[position[0]][position[1]].add_food(value)
        if self.__space[position[0]][position[1]].food() > self.__food_capacity:
            self.__space[position[0]][position[1]].set_food( self.__food_capacity )

    def update( self, ):
        '''
        Iteration function
        '''
        #


        self.__animals = self.__preys + self.__predators

        # Reproduce, starve, die
        for animal in self.__animals:
            # record the type of this animal
            animal_type = animal.animal_type()
            if not animal.death():
                # Reproduce
                if( animal.reproduction_check() ):
                    # Reproduction
                    for i in range( animal.no_offspring_value() ):
                        # Gene mutation control
                        # 1
                        gene_var_rate = 2
                        gene1_var = random.uniform( -gene_var_rate, gene_var_rate )
                        gene2_var = random.uniform( -gene_var_rate, gene_var_rate )
                        # 2

                        new_hunger_rate_gene = animal.hunger_rate_gene() + gene1_var
                        if new_hunger_rate_gene > 20:
                            new_hunger_rate_gene -= random.uniform( gene_var_rate, gene_var_rate+3 )
                        if new_hunger_rate_gene < 1:
                            new_hunger_rate_gene += random.uniform( gene_var_rate, gene_var_rate+3 )
                        new_fighting_gene = new_hunger_rate_gene

                        new_life_span_gene = animal.life_span_gene() + 0
                        new_consume_rate_gene = animal.consume_rate_gene() + 0


                        new_reproduction_threshold_gene = animal.reproduction_threshold_gene() + gene2_var
                        if new_reproduction_threshold_gene > 20:
                            new_reproduction_threshold_gene -= random.uniform( gene_var_rate, gene_var_rate+3 )
                        if new_reproduction_threshold_gene < 1:
                            new_reproduction_threshold_gene += random.uniform( gene_var_rate, gene_var_rate+3 )
                        new_reproduction_rate_gene = new_reproduction_threshold_gene
                        new_no_offspring_gene = new_reproduction_threshold_gene

                        transfer = animal.reproduction_transfer()*animal.hunger()/animal.no_offspring_value()

                        self.add_animal( animal_type, \
                                         animal.pos(), \
                                         transfer, \
                                         animal.max_hunger(), \
                                         animal.reproduction_threshold(), \
                                         animal.reproduction_transfer(), \
                                         animal.reproduction_rate(), \
                                         animal.hunger_rate(), \
                                         animal.life_span(), \
                                         animal.consume_rate() ,\
                                         new_hunger_rate_gene, \
                                         new_reproduction_rate_gene, \
                                         new_life_span_gene, \
                                         new_consume_rate_gene, \
                                         new_no_offspring_gene, \
                                         new_fighting_gene,\
                                         new_reproduction_threshold_gene, \
                                         )
                        if animal.animal_type() == 0:
                            self.__prey_birth += 1
                        if animal.animal_type() == 1:
                            self.__predator_birth += 1

                animal.reproduce()
                animal.starve()
                animal.aged()

                # Die
                if( animal.die_check() ):
                    pos = animal.pos()
                    self.__space[ pos[0] ][ pos[1] ].add_food( animal.hunger() )
                    animal.die()
                    if animal.animal_type() == 0:
                        self.__prey_natural_death += 1
                    if animal.animal_type() == 1:
                        self.__predator_death += 1

        # update animal list
        self.__animals = self.__preys + self.__predators

        # Dump the list
        self.__animals = [x for x in self.__animals if not x.death() ]

        # animal movement / consumption
        # reset occupancy
        for i in range(self.__space_order):
            for j in range(self.__space_order):
                self.__space[i][j].init_occupancy()
                self.__space[i][j].init_animal_food()

        # 1) Movement
        for animal in self.__animals:
            # state type of this animal
            animal_type = animal.animal_type()
            # proceed if the animal is not dead
            if not animal.death():
                # animal randomly move
                animal.set_pos( animal.pos() + self.animal_random_movement( animal.pos() )[1] )

                # Calculate no. of animals that are hungry- animals will share foods
                if not animal.full():
                    self.__space[ animal.pos()[0] ][ animal.pos()[1] ].add_hunger_occupancy( animal_type, 1 )
                pos = animal.pos()
                # Calculate the occupancy of animals for each square
                self.__space[ pos[0] ][ pos[1] ].add_occupancy( animal_type, 1 )

        # 2) Consumption
        # prey consumption / being consumed
        for prey in self.__preys:
            # preys share food
            if not prey.death():
                pos = prey.pos()
                predator_hunger_occupancy = self.__space[pos[0]][pos[1]].hunger_occupancy()[1]
                if predator_hunger_occupancy > 0:
                    if random.random() > prey.fighting_value():
                        # Calculate the food ready to be consumed by predator
                        self.__space[ pos[0] ][ pos[1] ].add_animal_food( prey.animal_type(), prey.hunger() )
                        # prey being consumed
                        self.__space[ pos[0] ][ pos[1] ].add_occupancy( prey.animal_type(), -1 )
                        self.__space[ pos[0] ][ pos[1] ].add_hunger_occupancy( prey.animal_type(), -1 )
                        self.__prey_killed += 1
                        prey.die()



                else:
                    # sharing food if there is not enough
                    if not prey.full():
                        prey_hunger_occupancy = self.__space[pos[0]][pos[1]].hunger_occupancy()[0]
                        food = self.__space[pos[0]][pos[1]].food()
                        if  food >= prey.consume_rate_value():
                            prey.eat( prey.consume_rate_value() )
                            self.__space[pos[0]][pos[1]].add_food( -prey.consume_rate_value() )
                        if food < prey.consume_rate_value():
                            prey.eat( food )
                            self.__space[pos[0]][pos[1]].set_food( 0 )

        # predator consumption
        for predator in self.__predators:
            # predators share food
            if not predator.death():
                pos = predator.pos()
                if not predator.full():
                    # consume next level animal( prey )
                    food = self.__space[ pos[0] ][ pos[1] ].animal_food()[ 0 ]
                    if  food >= predator.consume_rate_value():
                        predator.eat( predator.consume_rate_value() )
                        self.__space[pos[0]][pos[1]].add_animal_food( 0, -predator.consume_rate_value() )
                    if food < predator.consume_rate_value():
                        predator.eat( food )
                        self.__space[pos[0]][pos[1]].set_animal_food( 0, 0 )


        # Analysis part
        self.calculate_total_food()

        self.__prey_no_array[self.__frame] = self.calculate_alive_animal_no()[0]

        self.__predator_no_array[self.__frame] = self.calculate_alive_animal_no()[1]

        self.__prey_gene1_array_low[self.__frame], self.__prey_gene1_array_high[self.__frame] = self.calculate_animal_gene( 0, 1 )
        self.__prey_gene2_array_low[self.__frame], self.__prey_gene2_array_high[self.__frame] = self.calculate_animal_gene( 0, 2 )

        self.__frame_array[self.__frame] = self.__frame

        self.__frame += 1

        # investigate graphically
        if self.__enable_draw:
            self.draw()
            time.sleep(.5)

    def species_invasion( self, number ):
        animal_type = 1

        for i in range(number):
            x = random.randint( 0, self.__space_order-1 )
            y = random.randint( 0, self.__space_order-1 )
            self.add_animal( animal_type, \
                             np.array([ x, y ]), \
                             self.__initial_hunger[animal_type], \
                             self.__animal_max_hunger[animal_type], \
                             self.__reproduction_threshold[animal_type], \
                             self.__reproduction_transfer[animal_type], \
                             self.__reproduction_rate[animal_type], \
                             self.__hunger_rate[animal_type], \
                             self.__life_span[animal_type], \
                             self.__animal_consume_rate[animal_type], \
                             0, \
                             0, \
                             0, \
                             0, \
                             0, \
                             0, \
                             0
                            )

    def animal_no( self ):
        return self.__animal_no

    def animal_life_no( self ):
        return self.__animal_life_no

    def prey_gene1_high( self ):
        return self.__prey_gene1_array_high

    def prey_gene1_low( self ):
        return self.__prey_gene1_array_low

    def prey_gene2_high( self ):
        return self.__prey_gene1_array_high

    def prey_gene2_low( self ):
        return self.__prey_gene1_array_low

    def animal_food( self ):
        return self.__animal_food

    def vege_food( self ):
        return self.__vege_food

    def total_food( self ):
        return self.__total_food

    def food_capacity( self ):
        return self.__food_capacity

    def set_food_capacity( self, value ):
        self.__food_capacity = value

    def frame( self ):
        return self.__frame

    def prey_no_array( self ):
        return self.__prey_no_array

    def predator_no_array( self ):
        return self.__predator_no_array

    def frame_array( self ):
        return self.__frame_array

    def prey_hunger_rate( self ):
        hunger_rate_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                hunger_rate_array = np.append( hunger_rate_array, prey.hunger_rate_value() )
        return hunger_rate_array

    def prey_hunger_rate_genevalue( self ):
        hunger_rate_gene_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                hunger_rate_gene_array = np.append( hunger_rate_gene_array, prey.hunger_rate_gene() )
        return hunger_rate_gene_array

    def prey_reproduction_rate( self ):
        reproduction_rate_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                reproduction_rate_array = np.append( reproduction_rate_array, prey.reproduction_rate_value() )
        return reproduction_rate_array

    def prey_reproduction_rate_genevalue( self ):
        reproduction_rate_gene_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                reproduction_rate_gene_array = np.append( reproduction_rate_gene_array, prey.reproduction_rate_gene() )
        return reproduction_rate_gene_array

    def prey_life_span( self ):
        life_span_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                life_span_array = np.append( life_span_array, prey.life_span_value() )
        return life_span_array

    def prey_life_span_genevalue( self ):
        life_span_gene_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                life_span_gene_array = np.append( life_span_gene_array, prey.life_span_gene() )
        return life_span_gene_array

    def prey_consume_rate( self ):
        consume_rate_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                consume_rate_array = np.append( consume_rate_array, prey.consume_rate_value() )
        return consume_rate_array

    def prey_consume_rate_genevalue( self ):
        consume_rate_gene_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                consume_rate_gene_array = np.append( consume_rate_gene_array, prey.consume_rate_gene() )
        return consume_rate_gene_array

    def prey_no_offspring( self ):
        no_offspring_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                no_offspring_array = np.append( no_offspring_array, prey.no_offspring_value() )
        return no_offspring_array

    def prey_no_offspring_genevalue( self ):
        no_offspring_gene_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                no_offspring_gene_array = np.append( no_offspring_gene_array, prey.no_offspring_gene() )
        return no_offspring_gene_array

    def prey_fighting( self ):
        fighting_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                fighting_array = np.append( fighting_array, prey.fighting_value() )
        return fighting_array

    def prey_fighting_genevalue( self ):
        fighting_gene_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                fighting_gene_array = np.append( fighting_gene_array, prey.fighting_gene() )
        return fighting_gene_array

    def predator_hunger_rate( self ):
        hunger_rate_array = np.array([])
        for predator in self.__predators:
            if not predator.death():
                hunger_rate_array = np.append( hunger_rate_array, predator.hunger_rate() )
        return hunger_rate_array

    def prey_birth( self ):
        return self.__prey_birth

    def prey_natural_death( self ):
        return self.__prey_natural_death

    def predator_birth( self ):
        return self.__predator_birth

    def predator_death( self ):
        return self.__predator_death

    def prey_genes_tuple( self ):
        self.__prey_genes_tuple = []
        for prey in self.__preys:
            if not predator.death():
                self.__prey_genes_tuple.append( ( prey.hunger_rate_gene(), prey.reproduction_rate_gene() ) )
        return self.__prey_genes_tuple

    def prey_gene_no( self ):
        gene1_no = 0
        gene2_no = 0
        for prey in self.__preys:
            if prey.hunger_rate_gene() < 10:
                gene1_no +=1
            else:
                gene2_no +=1

        return gene1_no, gene2_no


    def initialize_data_array( self, iteration_number ):
        '''
        the argument is the no. of evolutions waited to be done
        '''
        self.__prey_no_array = np.append( self.__prey_no_array[:self.__frame], np.zeros( iteration_number ) )
        self.__predator_no_array = np.append( self.__predator_no_array[:self.__frame], np.zeros( iteration_number ) )
        self.__frame_array = np.append( self.__frame_array[:self.__frame], np.zeros( iteration_number ) )

        self.__prey_gene1_array_high = np.append( self.__prey_gene1_array_high[:self.__frame], np.zeros( iteration_number ) )
        self.__prey_gene1_array_low = np.append( self.__prey_gene1_array_low[:self.__frame], np.zeros( iteration_number ) )
        self.__prey_gene2_array_high = np.append( self.__prey_gene1_array_high[:self.__frame], np.zeros( iteration_number ) )
        self.__prey_gene2_array_low = np.append( self.__prey_gene1_array_low[:self.__frame], np.zeros( iteration_number ) )


    def animal_random_movement( self, animal_pos ):
        '''
        return a valid random movement vector
        uses input of original position to check movement validity
        '''
        direction = random.randint(1,4)

        if   direction == 1:
            if animal_pos[0] < self.__space_order-1:
                displacement = [ 1, 0 ]
            else:
                displacement = [ -self.__space_order + 1, 0 ]
        elif direction == 2:
            if animal_pos[1] < self.__space_order-1:
                displacement = [ 0, 1 ]
            else:
                displacement = [ 0, -self.__space_order + 1 ]
        elif direction == 3:
            if animal_pos[0] > 0:
                displacement = [ -1, 0 ]
            else:
                displacement = [ self.__space_order - 1, 0 ]
        elif direction == 4:
            if animal_pos[1] > 0:
                displacement = [ 0, -1 ]
            else:
                displacement = [ 0, self.__space_order - 1 ]

        return direction, displacement


    def calculate_total_food( self ):
        '''
        calculate food amount in the ecosystem
        '''
        self.__total_food = 0.
        self.__animal_food = np.array([ 0., 0. ])
        self.__vege_food = 0.
        for i in range(self.__space_order):
            for j in range(self.__space_order):
                self.__vege_food += self.__space[i][j].food()
        for prey in self.__preys:
            if not prey.death():
                self.__animal_food[prey.animal_type()] += prey.hunger()
        for predator in self.__predators:
            if not predator.death():
                self.__animal_food[predator.animal_type()] += predator.hunger()
        self.__total_food += np.sum( self.__animal_food, 0 ) + self.__vege_food

        return self.__total_food

    def calculate_alive_animal_no( self ):
        '''
        calculate alive animal no.
        distinction from total animal no.( dead inclusive )
        '''
        self.__animal_life_no = np.array([ 0, 0 ])
        for animal in self.__animals:
            if not animal.death():
                self.__animal_life_no[animal.animal_type()] += 1

        return self.__animal_life_no

    def calculate_animal_gene( self, animaltype, genetype ):
        '''
        calculate animal gene number
        genetype = 1: hunger rate
        genetype = 2: reproduction rate
        ( low_no, high_no )
        '''
        return_gene = np.array( [ 0, 0 ] )
        for animal in self.__animals:
            if animal.animal_type() == animaltype:
                if genetype == 1:
                    if animal.hunger_rate_gene() > 10:
                        return_gene[1] += 1
                    else: return_gene[0] += 1
                if genetype == 2:
                    if animal.reproduction_rate_gene() > 10:
                        return_gene[1] += 1
                    else: return_gene[0] += 1
        return return_gene



    def draw( self, ):
        '''
        1) information of the ecosystem
        2) draw the ecosystem with text
        '''
        output = [str()] * self.__space_order
        for i in range(self.__space_order):
            for j in range(self.__space_order):
                output[i] += ( self.__space[i][j].character().ljust(3) )

        # Print information
        for animal in self.__animals:
            if animal.death():
                print( animal )
                #print ( animal, 'dead', 'age', animal.age(), 'offspring', animal.offsprings(), animal.pos() )
            else:
                print ( animal )
                #print ( animal, 'hunger:', "{0:.2f}".format(animal.hunger()), 'age', animal.age(), 'offspring', animal.offsprings(), animal.pos() )

        print( 'animal / plant   ', sum(self.__animal_food), '/', self.__vege_food )
        print( 'total food       ', self.__total_food )

        # Print ecosystem
        for i in output:
            print( i )































            #

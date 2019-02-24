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
                  animal_speed=np.array([ 1, 3 ]), \
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

        self.__max_speed = 0.

        # Total no of preys, dead inclusive
        self.__animal_no = np.array([ 0, 0 ])

        self.__animal_life_no = np.array([ 0, 0 ])

        # parameters
        self.__initial_no = initial_no

        self.__hunger_rate = hunger_rate

        self.__reproduction_threshold = reproduction_threshold

        self.__reproduction_transfer = reproduction_transfer

        self.__reproduction_rate = reproduction_rate

        self.__animal_life_span = life_span

        self.__animal_speed = np.zeros( np.shape( animal_speed ) )

        self.__animal_max_hunger = animal_max_hunger

        self.__animal_consume_rate = animal_consume_rate

        self.__enable_draw = enable_draw

        # analysis variables
        self.__frame = 0

        self.__prey_no_array = np.array([])

        self.__predator_no_array = np.array([])

        self.__frame_array = np.array([])

        # Initializing prey and predator
        # for animal_type in range( 2 ):
        #     for i in range( self.__initial_no[animal_type] ):
        #         x = random.randint(0,order-1)
        #         y = random.randint(0,order-1)
        #         self.add_animal( animal_type, \
        #                          np.array([ x, y ]), \
        #                          initial_hunger[animal_type], \
        #                          animal_speed[animal_type], \
        #                          animal_max_hunger[animal_type], \
        #                          reproduction_threshold[animal_type], \
        #                          reproduction_transfer[animal_type], \
        #                          reproduction_rate[animal_type], \
        #                          hunger_rate[animal_type], \
        #                          life_span[animal_type], \
        #                          animal_consume_rate[animal_type], \
        #                          0, \
        #                          0, \
        #                          0, \
        #                          0, \
        #                         )

        # Construct space and initialize animals
        for i in range( order ):
            for j in range( order ):
                self.__space[i][j] = objects.space( [i,j] )

                if i % 2 == 0 and j % 2 == 0 and not i == 0 and not j == 0:
                    animal_type = 0
                    self.add_animal( animal_type, \
                                     np.array([ i, j ]), \
                                     initial_hunger[animal_type], \
                                     animal_speed[animal_type], \
                                     animal_max_hunger[animal_type], \
                                     reproduction_threshold[animal_type], \
                                     reproduction_transfer[animal_type], \
                                     reproduction_rate[animal_type], \
                                     hunger_rate[animal_type], \
                                     life_span[animal_type], \
                                     animal_consume_rate[animal_type], \
                                     5, \
                                     15, \
                                     5, \
                                     15, \
                                    )


        # Initialize food
        for food in initial_food_distribution:
            self.__space[food[0]][food[1]].add_food(food[2])

    def add_animal( self, \
                    animal_type, \
                    position, \
                    hunger, \
                    speed, \
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
                    ):
        '''
        add ONE prey to the ecosystem
        '''
        if animal_type == 0:
            self.__preys.append( objects.prey( self.__animal_no[0], \
                                               position, \
                                               hunger, \
                                               speed, \
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
                                               ) )
            self.__animal_no += np.array([ 1, 0 ])
            self.__max_speed = max( self.__preys[-1].speed_value(), self.__max_speed )
        if animal_type == 1:
            self.__predators.append( objects.predator( self.__animal_no[1], \
                                                       position, \
                                                       hunger, \
                                                       speed, \
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
                                                       ) )
            self.__animal_no += np.array([ 0, 1 ])
            self.__max_speed = max( self.__predators[-1].speed_value(), self.__max_speed )

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
                    animal.reproduce()

                    # Gene mutation control
                    hunger_rate_gene_var = random.uniform( -1, 1 )
                    reproduction_rate_gene_var = random.uniform( -1, 1 )
                    life_span_gene_var = hunger_rate_gene_var
                    consume_rate_gene_var = reproduction_rate_gene_var

                    # hunger_rate_gene_var = 0
                    # reproduction_rate_gene_var = 0
                    # life_span_gene_var = 0
                    # consume_rate_gene_var = 0

                    self.add_animal( animal_type, \
                                     animal.pos(), \
                                     animal.reproduction_transfer(), \
                                     animal.speed(), \
                                     animal.max_hunger(), \
                                     animal.reproduction_threshold(), \
                                     animal.reproduction_transfer(), \
                                     animal.reproduction_rate(), \
                                     animal.hunger_rate(), \
                                     animal.life_span(), \
                                     animal.consume_rate() ,\
                                     animal.hunger_rate_gene() + hunger_rate_gene_var, \
                                     animal.reproduction_rate_gene() + reproduction_rate_gene_var, \
                                     animal.life_span_gene() + life_span_gene_var, \
                                     animal.consume_rate_gene() + consume_rate_gene_var, \
                                     )

                animal.starve()
                animal.aged()
                animal.set_current_movement( 0 ) # reset action token

                # Die
                if( animal.die_check() ):
                    pos = animal.pos()
                    self.__space[ pos[0] ][ pos[1] ].add_food( animal.hunger() )
                    animal.die()

        # update animal list
        self.__animals = self.__preys + self.__predators

        # Dump the list
        self.__animals = [x for x in self.__animals if not x.death() ]

        # animal movement / consumption
        # repreat the process up to the highet speed of animals
        for action in range( int( self.__max_speed ) ):
            # reset occupancy
            for i in range(self.__space_order):
                for j in range(self.__space_order):
                    self.__space[i][j].init_occupancy()
                    self.__space[i][j].init_animal_food()

            # 1) Movement
            for animal in self.__animals:
                # state type of this animal
                animal_type = animal.animal_type()
                # proceed if the animal is not dead and has action token
                if not animal.death():
                    # animal randomly move
                    if animal.action_token() > 0:
                        animal.set_pos( animal.pos() + self.animal_random_movement( animal.pos() )[1] )

                        # Calculate no. of animals that are hungry- animals will share foods
                        if not animal.full():
                            self.__space[ animal.pos()[0] ][ animal.pos()[1] ].add_hunger_occupancy( animal_type, 1 )
                    pos = animal.pos()
                    # Calculate the occupancy of animals for each square
                    self.__space[ pos[0] ][ pos[1] ].add_occupancy( animal_type, 1 )
                    # Calculate the food worth value for this position
                    self.__space[ pos[0] ][ pos[1] ].add_animal_food( animal_type, animal.hunger() )

            # 2) Consumption
            # predator consumption
            for predator in self.__predators:
                # predator shares food
                if not predator.death() and predator.action_token() > 0 and not predator.full():
                    pos = predator.pos()
                    if not predator.full():
                        predator_hunger_occupancy = self.__space[pos[0]][pos[1]].hunger_occupancy()[1]
                        # consume next level animal( prey )
                        food = self.__space[ pos[0] ][ pos[1] ].animal_food()[ 0 ]
                        if  food >= predator.consume_rate_value():
                            predator.eat( predator.consume_rate_value() )
                            self.__space[pos[0]][pos[1]].add_animal_food( 0, -prey.consume_rate_value() )
                        if food < prey.consume_rate_value():
                            predator.eat( food )
                            self.__space[pos[0]][pos[1]].set_animal_food( 0, 0 )
                        # portion = food / predator_hunger_occupancy
                        # predator.eat( portion )
                    predator.set_current_movement( predator.current_movement() + 1 )

            # prey consumption / being consumed
            for prey in self.__preys:
                # prey shares food
                if not prey.death():
                    pos = prey.pos()
                    predator_hunger_occupancy = self.__space[pos[0]][pos[1]].hunger_occupancy()[1]
                    if predator_hunger_occupancy > 0:
                        # prey being consumed
                        self.__space[ pos[0] ][ pos[1] ].set_animal_food( prey.animal_type(), 0 )
                        self.__space[ pos[0] ][ pos[1] ].set_occupancy( prey.animal_type(), 0 )
                        self.__space[ pos[0] ][ pos[1] ].set_hunger_occupancy( prey.animal_type(), 0 )
                        prey.die()
                    elif prey.action_token() > 0:
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

                            # consume_rate = self.__animal_consume_rate[ prey.animal_type() ]
                            # if food >= prey_hunger_occupancy * consume_rate: # enough food
                            #
                            # else: # not enough food
                            #     portion = food / prey_hunger_occupancy
                            #     prey.eat( portion )
                        prey.set_current_movement( prey.current_movement() + 1 )

            # level 0 food (plant) being consumed
            # for i in range( self.__space_order ):
            #     for j in range( self.__space_order ):
            #         prey_hunger_occupancy = self.__space[i][j].hunger_occupancy()[0]
            #         # food being consumed
            #         if prey_hunger_occupancy > 0:
            #             self.__space[i][j].add_food( - prey_hunger_occupancy * self.__animal_consume_rate[ 0 ] )
            #             if self.__space[i][j].food() < 0 :
            #                 self.__space[i][j].set_food( 0 )



        # Analysis part
        self.calculate_total_food()

        self.__prey_no_array[self.__frame] = self.calculate_alive_animal_no()[0]

        self.__predator_no_array[self.__frame] = self.calculate_alive_animal_no()[1]

        self.__frame_array[self.__frame] = self.__frame

        self.__frame += 1

        # investigate graphically
        if self.__enable_draw:
            self.draw()
            time.sleep(.5)

    def animal_no( self ):
        return self.__animal_no

    def animal_life_no( self ):
        return self.__animal_life_no

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

    def prey_speed( self ):
        speed_array = np.array([])
        for prey in self.__preys:
            if not prey.death():
                speed_array = np.append( speed_array, prey.speed_value() )
        return speed_array

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

    def predator_hunger_rate( self ):
        hunger_rate_array = np.array([])
        for predator in self.__predators:
            if not predator.death():
                hunger_rate_array = np.append( hunger_rate_array, predator.hunger_rate() )
        return hunger_rate_array

    def initialize_data_array( self, iteration_number ):
        '''
        the argument is the no. of evolutions waited to be done
        '''
        self.__prey_no_array = np.append( self.__prey_no_array[:self.__frame], np.zeros( iteration_number ) )
        self.__predator_no_array = np.append( self.__predator_no_array[:self.__frame], np.zeros( iteration_number ) )
        self.__frame_array = np.append( self.__frame_array[:self.__frame], np.zeros( iteration_number ) )

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

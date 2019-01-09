import numpy as np
import random
import objects
import time

class ecosystem:

    def __init__( self, \
                  order,  \
                  initial_no=np.array([ 10, 1 ]), \
                  initial_hunger=np.array([ 100, 200 ]), \
                  starving_rate=np.array([ 1, 1 ]), \
                  reproduction_threshold=np.array([ 50, 100 ]), \
                  reproduction_transfer=np.array([ 20, 40 ]), \
                  reproduction_rate=np.array([ 7, 20 ]), \
                  life_span=np.array([ 100, 100 ]), \
                  animal_mobility=np.array([ 1, 3 ]), \
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

        self.__starving_rate = starving_rate

        self.__reproduction_threshold = reproduction_threshold

        self.__reproduction_transfer = reproduction_transfer

        self.__reproduction_rate = reproduction_rate

        self.__animal_life_span = life_span

        self.__animal_original_mobility = animal_mobility

        self.__animal_mobility = np.zeros( np.shape( animal_mobility ) )

        self.__animal_max_hunger = animal_max_hunger

        self.__animal_consume_rate = animal_consume_rate

        self.__enable_draw = enable_draw

        # putting in prey and predator
        for animal_type in range( 2 ):
            for i in range( self.__initial_no[animal_type] ):
                x = random.randint(0,order-1)
                y = random.randint(0,order-1)
                self.add_animal( animal_type, np.array([ x, y ]), initial_hunger[animal_type] )

        # Construct space
        for i in range( order ):
            for j in range( order ):
                self.__space[i][j] = objects.space( [i,j] )

        # Initialize food
        for food in initial_food_distribution:
            self.__space[food[0]][food[1]].add_food(food[2])

        if self.__enable_draw:
            self.draw()


    def add_animal( self, animal_type, position, hunger=20 ):
        '''
        add ONE prey to the ecosystem
        '''
        if animal_type == 0:
            self.__preys.append( objects.prey( position, self.__animal_no[0], hunger, self.__animal_mobility[0], self.__animal_max_hunger[0] ) )
            self.__animal_no += np.array([ 1, 0 ])
        if animal_type == 1:
            self.__predators.append( objects.predator( position, self.__animal_no[1], hunger, self.__animal_mobility[1], self.__animal_max_hunger[1] ) )
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

        # modify mobility according to animal no.
        for i in range( len( self.__animal_mobility ) ):
            if self.__animal_life_no[i] < 4 and self.__animal_life_no[i] > 0:
                self.__animal_mobility[i] = self.__animal_original_mobility[i] + 2
            elif self.__animal_life_no[i] < 20 and self.__animal_life_no[i] > 0:
                self.__animal_mobility[i] = self.__animal_original_mobility[i] + 1
            else:
                self.__animal_mobility[i] = self.__animal_original_mobility[i]

        # Reproduce, starve, die
        for animal in self.__animals:
            # record the type of this animal
            animal_type = animal.animal_type()
            if not animal.death():
                # Reproduce
                if( animal.age() % self.__reproduction_rate[ animal_type ] == 0 and \
                    not animal.age() == 0 and \
                    animal.hunger() >= self.__reproduction_threshold[ animal_type ] ):
                    animal.reproduce( self.__reproduction_transfer[ animal_type ] )
                    self.add_animal( animal_type, animal.pos(), self.__reproduction_transfer[ animal_type ] )

                # Starve
                animal.starve( self.__starving_rate[ animal_type ] )

                # Aged
                animal.add_age( 1 )

                # modify animal mobility
                animal.set_mobility( self.__animal_mobility[ animal_type ] )

                # reset action token
                animal.set_current_mobility( 0 )

                # Die
                if animal.hunger() <= 0 or animal.age() >= self.__animal_life_span[animal_type]:
                    pos = animal.pos()
                    self.__space[ pos[0] ][ pos[1] ].add_food( animal.hunger() )
                    animal.die()

        # update animal list
        self.__animals = self.__preys + self.__predators

        # animal movement / consumption
        # repreat the process up to the highet mobility of animals
        for action in range( int( max( self.__animal_mobility ) ) ):
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

                        # Calculate no. animals that are hungry- animals will share foods
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
                    predator_hunger_occupancy = self.__space[pos[0]][pos[1]].hunger_occupancy()[1]
                    # consume next level animal( prey )
                    food = self.__space[ pos[0] ][ pos[1] ].animal_food()[ predator.animal_type()-1 ]
                    portion = food / predator_hunger_occupancy
                    predator.eat( portion )
                    predator.set_current_mobility( predator.current_mobility() + 1 )

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
                            consume_rate = self.__animal_consume_rate[ prey.animal_type() ]
                            if food >= prey_hunger_occupancy * consume_rate: # enough food
                                prey.eat( consume_rate )
                            else: # not enough food
                                portion = food / prey_hunger_occupancy
                                prey.eat( portion )
                        prey.set_current_mobility( prey.current_mobility() + 1 )

            # level 0 food (plant) being consumed
            for i in range( self.__space_order ):
                for j in range( self.__space_order ):
                    prey_hunger_occupancy = self.__space[i][j].hunger_occupancy()[0]
                    # food being consumed
                    if prey_hunger_occupancy > 0:
                        self.__space[i][j].add_food( - prey_hunger_occupancy * self.__animal_consume_rate[ 0 ] )
                        if self.__space[i][j].food() < 0 :
                            self.__space[i][j].set_food( 0 )

        # calculate alive animal no.
        self.calculate_alive_animal_no()

        # Calculate total food in the system
        self.calculate_total_food()

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

    def animal_random_movement( self, animal_pos ):
        '''
        return a valid random movement vector
        uses input of original position to check movement validity
        '''
        allow_movement = False
        while not allow_movement:
            direction = random.randint(1,4)

            if   direction == 1 and animal_pos[0] < self.__space_order-1:
                displacement = [ 1, 0 ]
                allow_movement = True
            elif direction == 2 and animal_pos[1] < self.__space_order-1:
                displacement = [ 0, 1 ]
                allow_movement = True
            elif direction == 3 and animal_pos[0] > 0:
                displacement = [ -1, 0 ]
                allow_movement = True
            elif direction == 4 and animal_pos[1] > 0:
                displacement = [ 0, -1 ]
                allow_movement = True

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
                print ( animal, 'dead', 'age', animal.age(), 'offspring', animal.offsprings(), animal.pos() )
            else:
                print ( animal, 'hunger:', "{0:.2f}".format(animal.hunger()), 'age', animal.age(), 'offspring', animal.offsprings(), animal.pos() )

        print( 'animal / plant   ', sum(self.__animal_food), '/', self.__vege_food )
        print( 'total food       ', self.__total_food )

        # Print ecosystem
        for i in output:
            print( i )































            #

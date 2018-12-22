import numpy as np
import random
import objects
import time

class ecosystem:

    def __init__( self, \
                  order,  \
                  initial_no=[ 10, 1 ], \
                  initial_hunger=[ 100, 200 ], \
                  starving_rate=[ 1, 1 ], \
                  reproduction_threshold=[ 50, 100 ], \
                  reproduction_transfer=[ 20, 40 ], \
                  reproduction_rate=[ 7, 20 ], \
                  initial_food_distribution = [[0,0,0]], \
                ):
        '''
        input of initial_food_distribution is a list of 3-vector, with the first 2 elements the coordinates and the 3rd=amount of food.
        '''

        self.__space = [ [ None for _ in range(order) ] for _ in range(order) ]

        self.__animals = list()

        self.__preys = list()

        self.__predators = list()

        self.__space_order = order

        self.__total_food = 0.

        # Total no of preys, dead inclusive
        self.__animal_no = [ 0, 0 ]

        self.__initial_no = initial_no

        # putting in prey and predator
        for animal_type in range( 2 ):
            for i in range( self.__initial_no[animal_type] ):
                x = random.randint(0,order-1)
                y = random.randint(0,order-1)
                self.add_animal( animal_type, np.array([ x, y ]), initial_hunger[animal_type] )

        # parameters
        self.__starving_rate = starving_rate

        self.__reproduction_threshold = reproduction_threshold

        self.__reproduction_transfer = reproduction_transfer

        self.__reproduction_rate = reproduction_rate

        # Construct space
        for i in range( order ):
            for j in range( order ):
                self.__space[i][j] = objects.space( [i,j] )

        # Initialize food
        for food in initial_food_distribution:
            self.__space[food[0]][food[1]].add_food(food[2])

        for i in range(self.__space_order):
            for j in range(self.__space_order):
                self.__total_food += self.__space[i][j].food()
        for prey in self.__preys:
            self.__total_food += prey.hunger()

        self.draw()


    def add_animal( self, animal_type, position, hunger=20 ):
        '''
        add ONE prey to the ecosystem
        '''
        if animal_type == 0:
            self.__preys.append( objects.prey( position, self.__animal_no[0], hunger ) )
            self.__animal_no += np.array([ 1, 0 ])
        if animal_type == 1:
            self.__predators.append( objects.predator( position, self.__animal_no[1], hunger ) )
            self.__animal_no += np.array([ 0, 1 ])

    def add_food( self, position, value ):
        '''
        add food to the system
        '''
        self.__space[position[0]][position[1]].add_food(value)

    def update( self, ):
        '''
        Iteration function
        '''
        # Calculate total food in the system
        self.__total_food = 0
        for i in range(self.__space_order):
            for j in range(self.__space_order):
                self.__space[i][j].init()
                self.__total_food += self.__space[i][j].food()
        for prey in self.__preys:
            self.__total_food += prey.hunger()
        for predator in self.__predators:
            self.__total_food += predator.hunger()

        #
        self.__animals = self.__preys + self.__predators

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

                # Die
                if animal.hunger() <= 0 or animal.age() >= 100:
                    animal.die()

        # update animal list
        self.__animals = self.__preys + self.__predators

        # Movement
        for animal in self.__animals:
            # record the type of this animal
            animal_type = animal.animal_type()
            if not animal.death():

                allow_movement = False
                while not allow_movement:
                    direction = random.randint(1,4)

                    if   direction == 1 and animal.pos()[0] < self.__space_order-1:
                        displacement = [ 1, 0 ]
                        allow_movement = True
                    elif direction == 2 and animal.pos()[1] < self.__space_order-1:
                        displacement = [ 0, 1 ]
                        allow_movement = True
                    elif direction == 3 and animal.pos()[0] > 0:
                        displacement = [ -1, 0 ]
                        allow_movement = True
                    elif direction == 4 and animal.pos()[1] > 0:
                        displacement = [ 0, -1 ]
                        allow_movement = True
                animal.set_pos( animal.pos()+np.array(displacement) )

                # Calculate the occupancy of animals for each square - animals will share foods
                pos = animal.pos()
                self.__space[ pos[0] ][ pos[1] ].add_occupancy( animal_type, 1 )
                # Calculate the food worth value for this position
                self.__space[ pos[0] ][ pos[1] ].add_animal_food( animal_type, animal.hunger() )

        # Eat
        for predator in self.__predators:
            if not predator.death():
                pos = predator.pos()
                predator_occupancy = self.__space[pos[0]][pos[1]].occupancy()[1]
                # the predator will consume next level animal
                food = self.__space[ pos[0] ][ pos[1] ].animal_food()[ predator.animal_type()-1 ]
                portion = food / predator_occupancy
                predator.eat( portion )
                self.__space[ pos[0] ][ pos[1] ].set_occupancy( predator.animal_type()-1, 0 )

        for prey in self.__preys:
            if not prey.death():
                pos = prey.pos()
                prey_occupancy = self.__space[pos[0]][pos[1]].occupancy()[0]
                predator_occupancy = self.__space[pos[0]][pos[1]].occupancy()[1]
                if predator_occupancy > 0:
                    print( 'eaten' )
                    self.__space[ pos[0] ][ pos[1] ].set_animal_food( prey.animal_type(), 0 )
                    prey.die()
                else:
                    food = self.__space[pos[0]][pos[1]].food()
                    portion = food / prey_occupancy
                    prey.eat( portion )

        # for i in range( self.__space_order ):
        #     for j in range( self.__space_order ):
        #         prey_occupancy = self.__space[i][j].occupancy()[0]
        #         if not prey_occupancy == 0:
        #             self.__space[i][j].set_food = 0


        self.draw()
        # time.sleep(.5)


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
                print ( animal, 'dead', 'age', animal.age(), 'offspring', animal.offsprings() )
            else:
                print ( animal, 'hunger:', "{0:.2f}".format(animal.hunger()), 'age', animal.age(), 'offspring', animal.offsprings())

        print( 'total food: ', self.__total_food )

        # Print ecosystem
        for i in output:
            print( i )


































            #

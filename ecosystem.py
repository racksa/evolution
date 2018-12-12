import numpy as np
import random
import objects
import time

class ecosystem:

    def __init__( self, \
                  order,  \
                  initial_hunger=100, \
                  initial_food_distribution = [[0,0,0]], \
                  starving_rate=1, \
                  reproduction_threshold=50, \
                  reproduction_transfer=20, \
                  reproduction_rate=7, \
                ):
        '''
        input of initial_food_distribution is a list of 3-vector, with the first 2 elements the coordinates and the 3rd=amount of food.
        '''

        self.__space = [ [ None for _ in range(order) ] for _ in range(order) ]

        self.__bugs = list()

        self.__space_order = order

        self.__total_food = 0.

        # Total no of bugs, dead inclusive
        self.__bug_offspring = 0

        self.add_bug( np.array([ int(order/2), int(order/2) ]), initial_hunger )

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
        for bug in self.__bugs:
            self.__total_food += bug.hunger()

        self.draw()


    def add_bug( self, position, hunger=20 ):
        '''
        add ONE bug to the ecosystem
        '''
        self.__bugs.append( objects.bug( position, self.__bug_offspring, hunger ) )
        self.__bug_offspring += 1

    def add_food( self, position, value ):
        '''
        add food to the system
        '''
        self.__space[position[0]][position[1]].add_food(value)

    def update( self, ):
        '''
        Iteration function
        '''
        self.__total_food = 0
        for i in range(self.__space_order):
            for j in range(self.__space_order):
                self.__space[i][j].init()
                self.__total_food += self.__space[i][j].food()

        for bug in self.__bugs:
            self.__total_food += bug.hunger()
            
        # Reproduce, starve, die
        for bug in self.__bugs:
            if not bug.death():
                if bug.age() % self.__reproduction_rate == 0 and not bug.age() == 0 and bug.hunger() >= self.__reproduction_threshold:
                    bug.reproduce( self.__reproduction_transfer )
                    self.add_bug( bug.pos(), self.__reproduction_transfer )

                # Starve
                bug.starve( self.__starving_rate )

                # Aged
                bug.add_age( 1 )

                # Die
                if bug.hunger() <= 0 or bug.age() >= 100:
                    bug.die()


        # Move
        for bug in self.__bugs:
            if not bug.death():

                allow_movement = False
                while not allow_movement:
                    direction = random.randint(1,4)

                    if   direction == 1 and bug.pos()[0] < self.__space_order-1:
                        displacement = [ 1, 0 ]
                        allow_movement = True
                    elif direction == 2 and bug.pos()[1] < self.__space_order-1:
                        displacement = [ 0, 1 ]
                        allow_movement = True
                    elif direction == 3 and bug.pos()[0] > 0:
                        displacement = [ -1, 0 ]
                        allow_movement = True
                    elif direction == 4 and bug.pos()[1] > 0:
                        displacement = [ 0, -1 ]
                        allow_movement = True
                bug.set_pos( bug.pos()+np.array(displacement) )

                # Calculate the occupations of bugs for each square - bugs will share foods
                pos = bug.pos()
                self.__space[ pos[0] ][ pos[1] ].add_occupation( 1 )

        # Eat, aged, reproduce
        for bug in self.__bugs:
            if not bug.death():
                # Eat
                pos = bug.pos()
                occupation = self.__space[pos[0]][pos[1]].occupation()
                food = self.__space[pos[0]][pos[1]].food()
                portion = food / occupation
                bug.eat( portion )
                self.__space[pos[0]][pos[1]].init_food()

        self.draw()
        time.sleep(.5)


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
        for bug in self.__bugs:
            if bug.death():
                print ( 'bug', bug.id(), 'dead', 'age', bug.age(), 'offsprings', bug.offsprings() )
            else:
                print ( 'bug', bug.id(), 'hunger:', "{0:.2f}".format(bug.hunger()), 'age', bug.age(), 'offsprings', bug.offsprings())

        print( 'total food: ', self.__total_food )

        # Print ecosystem
        for i in output:
            print( i )


































            #

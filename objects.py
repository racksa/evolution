import numpy as np

class animal:

    def __init__( self, pos, id_no, hunger=20, mobility=1, max_hunger=100 ):

        self.__pos = pos

        self.__id = id_no

        self.__mobility = mobility

        self.__current_mobility = 0

        self.__hunger = hunger

        self.__max_hunger = max_hunger

        self.__last_displacement = np.array([])

        self.__age = 0

        self.__offspring = 0

        self.__death = False

    def pos( self ):
        return self.__pos

    def id( self ):
        return self.__id

    def mobility( self ):
        return self.__mobility

    def set_mobility( self, value ):
        self.__mobility = value

    def current_mobility( self ):
        return self.__current_mobility

    def set_current_mobility( self, value ):
        self.__current_mobility = value

    def action_token( self ):
        token = self.__mobility - self.__current_mobility
        return token

    def hunger( self ):
        return self.__hunger

    def max_hunger( self ):
        return self.__max_hunger

    def full( self ):
        return self.__max_hunger - self.__hunger <= 1.e-16

    def eat( self, value, ctype=1 ):
        self.__hunger += value

        return self.__hunger-value, self.__hunger

    def age( self ):
        return self.__age

    def add_age( self, value ):
        self.__age += value

    def offsprings( self ):
        return self.__offspring

    def last_displacement( self ):
        return self.__last_displacement

    def starve( self, value ):
        self.__hunger -= value
        if self.__hunger < 0:
            self.__hunger = 0

    def move( self, displacement, dis_type ):
        '''
        '''
        self.__pos += displacement

        self.__last_displacement = dis_type

        return self, self.__pos

    def set_pos( self, value ):
        self.__pos = value

    def death( self ):
        return self.__death

    def die( self ):
        self.__death = True
        self.__hunger = 0
        return 0

    def reproduce( self, value ):
        self.__hunger -= value
        self.__offspring += 1
        return 0

class prey(animal):

    def __repr__( self ):
        return 'prey' + str(self.id())

    def animal_type( self ):
        return 0

class predator(animal):

    def __repr__( self ):
        return 'predator' + str(self.id())

    def animal_type( self ):
        return 1

class space:

    def __init__( self, pos, food=0, _id='food' ):

        self.__pos = pos

        self.__id = _id

        self.__food = food

        self.__prey = list()

        self.__predator = list()

        self.__animal_food = np.array([ 0, 0 ])

        self.__occupancy = np.array([ 0, 0 ])

        self.__hunger_occupancy = np.array([ 0, 0 ])

    def pos( self ):
        return self.__pos

    def id( self ):
        return self.__id

    def food( self ):
        return self.__food

    def add_food( self, value ):
        self.__food += value

    def set_food( self, value ):
        self.__food = value

    def animal_food( self ):
        '''
        food worth value carried by animal
        '''
        return self.__animal_food

    def add_animal_food( self, index, value ):
        self.__animal_food[index] += value

    def set_animal_food( self, index, value ):
        self.__animal_food[index] = value

    def prey( self ):
        return self.__prey

    def add_prey( self, prey ):
        self.__prey.append( prey )

    def predator( self ):
        return self.__predator

    def add_predator( self, predator ):
        self.__predator.append( predator )

    def occupancy( self ):
        return self.__occupancy

    def add_occupancy( self, index, value ):
        self.__occupancy[index] += value

    def set_occupancy( self, index, value ):
        self.__occupancy[index] = value

    def hunger_occupancy( self ):
        return self.__hunger_occupancy

    def add_hunger_occupancy( self, index, value ):
        self.__hunger_occupancy[index] += value

    def set_hunger_occupancy( self, index, value ):
        self.__hunger_occupancy[index] = value

    def init_animal_food( self ):
        self.__animal_food = np.array([ 0., 0. ])

    def init_occupancy( self ):
        self.__occupancy = np.array([ 0., 0. ])
        self.__hunger_occupancy = np.array([ 0., 0. ])
        self.__prey = []
        self.__predator = []

    def character( self ):
        '''
        symbol used for this position
        '''
        character = '.'

        if not self.__food == 0:
            character = str( "{0:.0f}".format(self.__food) )

        if self.__occupancy[0] == 1:
            character = '@'
        elif self.__occupancy[0] == 2:
            character = '@@'
        elif self.__occupancy[0] > 2:
            character = '@@@'

        if self.__occupancy[1] == 1:
            character = '#'
        elif self.__occupancy[1] == 2:
            character = '##'
        elif self.__occupancy[1] > 2:
            character = '###'

        return character




























#

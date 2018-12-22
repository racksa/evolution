import numpy as np

class animal:

    def __init__( self, pos, id_no, hunger=20 ):

        self.__pos = pos

        self.__id = id_no

        self.__hunger =  hunger

        self.__last_displacement = np.array([])

        self.__age = 0

        self.__offspring = 0

        self.__death = False

    def pos( self ):
        return self.__pos

    def id( self ):
        return self.__id

    def hunger( self ):
        return self.__hunger

    def age( self ):
        return self.__age

    def add_age( self, value ):
        self.__age += value

    def offsprings( self ):
        return self.__offspring

    def last_displacement( self ):
        return self.__last_displacement

    def eat( self, value, ctype=1 ):
        self.__hunger += value

        return self.__hunger-value, self.__hunger

    def starve( self, value ):
        self.__hunger -= value

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

    def init( self ):
        self.__occupancy = [ 0, 0 ]
        self.__animal_food = [ 0, 0 ]
        self.__prey = []
        self.__predator = []

    def character( self ):
        '''
        symbol used for this position
        '''
        character = '.'

        if not self.__food == 0:
            character = str( self.__food )

        if self.__occupancy[0] == 1:
            character = '@'
        elif self.__occupancy[0] == 2:
            character = '&'
        elif self.__occupancy[0] > 2:
            character = '%'

        if self.__occupancy[1] > 0:
            character = '#'

        return character




























#

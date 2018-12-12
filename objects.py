import numpy as np

class bug:

    def __init__( self, pos, id_no, hunger=20 ):

        self.__pos = pos

        self.__id = id_no

        self.__hunger =  hunger

        self.__last_displacement = np.array([])

        self.__age = 0

        self.__offspring = 0

        self.__death = False

        self.__nonce = np.array([0])

    def __repr__( self ):
        return str(self.__id)

    def pos( self ):
        return self.__pos

    def nonce( self ):
        return self.__nonce

    def add_nonce( self, value ):
        self.__nonce += value

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

        self.__nonce += 1

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



class space:

    def __init__( self, pos, food=0, _id='food' ):

        self.__pos = pos

        self.__id = _id

        self.__food = food

        self.__occupation = int()


    def pos( self ):
        return self.__pos

    def id( self ):
        return self.__id

    def food( self ):
        return self.__food

    def add_food( self, value ):
        self.__food += value

    def init_food( self ):
        self.__food = 0

    def occupation( self ):
        return self.__occupation

    def add_occupation( self, value ):
        self.__occupation += value

    def init( self ):
        self.__occupation = 0

    def character( self ):
        '''
        symbol used for this square
        '''
        character = '.'

        if not self.__food == 0:
            character = str( self.__food )

        if self.__occupation == 1:
            character = '@'
        elif self.__occupation == 2:
            character = '&'
        elif self.__occupation > 2:
            character = '#'

        return character

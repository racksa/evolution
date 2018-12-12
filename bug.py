import numpy as np

class bug:

    def __init__( self, position, hunger=20, _id='bug' ):

        self.__position = position

        self.__id = _id

        self.__hunger =  hunger

        self.__last_displacement = np.array()

    def pos( self ):
        return self.__position

    def id( self ):
        return self.__id

    def hunger( self ):
        return self.__hunger

    def last_displacement( self ):
        return self.__last_displacement

    def hunger_change( self, value, ctype=1 ):
        '''
        Change the hunger value of the bug.
        +ve for food supple, -ve for starving
        '''
        self.__hunger += value

        return self.__hunger-value, self.__hunger

    def move( self, displacement ):
        '''
        '''
        self.__position += displacement

        self.__last_displacement = displacement

    def die( self ):
        return 0

    def reproduce( self, number=1 ):
        return 0

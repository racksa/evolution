import random
import bug

class ecosystem:

    def __init__( self, initial_bug_no ):

        self.__bugs = list()

        self.__foods = list()

        self.add_bug( np.array([0,0]) )

    def add_bug( self, position ):
        '''
        add ONE bug to the ecosystem
        '''
        self.__bugs.append( bug.bug( position, ) )

    def update( self, ):
        '''
        Iteration function
        '''

        # bug movement
        for bug in bugs:
            direction = random.randint(1,4)
            if direction == 1:
                displacement = np.array( [ 1, 0 ] )
            elif direction == 2:
                displacement = np.array( [ 0, 1 ] )
            elif direction == 3:
                displacement = np.array( [ -1, 0 ] )
            else:
                displacement = np.array( [ 0, -1 ] )

            bug.move( displacement )

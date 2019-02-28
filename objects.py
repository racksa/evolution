import numpy as np
import myMath
import random

class animal:

    def __init__( self, \
                  id_no, \
                  pos, \
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
        #
        self.__pos = pos

        self.__id = id_no

        # Gene values
        self.__hunger_rate_gene = hunger_rate_gene
        self.__hunger_rate = hunger_rate

        self.__reproduction_rate_gene = reproduction_rate_gene
        self.__reproduction_rate = reproduction_rate

        self.__life_span_gene = life_span_gene
        self.__life_span = life_span

        self.__consume_rate_gene = consume_rate_gene
        self.__consume_rate = consume_rate

        self.__no_offspring_gene = no_offspring_gene

        self.__fighting_gene = fighting_gene

        self.__reproduction_threshold_gene = reproduction_threshold_gene




        #Gaussian mapping
        # self.__hunger_rate_value = hunger_rate * myMath.gaussian( hunger_rate_gene, 0, 3 )
        #
        # self.__life_span_value = int( max( 1, life_span * myMath.gaussian( life_span_gene, 0, 3 ) ) )

        #Linear mapping
        if self.animal_type() == 0:
            self.__hunger_rate_value = max( 0, myMath.linear( hunger_rate_gene, .05, hunger_rate ) )

            self.__life_span_value = int( max( 1, myMath.linear( life_span_gene, 1, life_span ) ) )

            self.__reproduction_rate_value = max( 1, myMath.linear( reproduction_rate_gene, .5, reproduction_rate ) )

            self.__consume_rate_value = max( 0.1, myMath.linear( consume_rate_gene, consume_rate, 3 ) )

            self.__no_offspring_value = max( 1, int( (self.__no_offspring_gene ) ) )

            self.__fighting_value = 1. - 1./ fighting_gene**.5

            self.__reproduction_threshold_value = myMath.linear( reproduction_threshold_gene, 1., reproduction_threshold )

        if self.animal_type() == 1:
            self.__hunger_rate_value = max( 0.1, myMath.linear( hunger_rate_gene, 0., hunger_rate ) )

            self.__life_span_value = int( max( 1, myMath.linear( life_span_gene, 0, life_span ) ) )

            self.__reproduction_rate_value = max( 1, myMath.linear( reproduction_rate_gene, 0., reproduction_rate ) )

            self.__consume_rate_value = max( 0.1, myMath.linear( consume_rate_gene, 0, consume_rate ) )

            self.__no_offspring_value = 1

            self.__fighting_value = 0

            self.__reproduction_threshold_value = 60

        #
        self.__current_movement = 0

        self.__hunger = hunger

        self.__max_hunger = max_hunger

        self.__reproduction_threshold = reproduction_threshold

        self.__reproduction_transfer = reproduction_transfer







        #
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

    def max_hunger( self ):
        return self.__max_hunger

    def reproduction_transfer( self ):
        return self.__reproduction_transfer

    def reproduction_rate( self ):
        return self.__reproduction_rate

    def reproduction_rate_gene( self ):
        return self.__reproduction_rate_gene

    def reproduction_rate_value( self ):
        return self.__reproduction_rate_value

    def reproduction_threshold( self ):
        return self.__reproduction_threshold

    def reproduction_threshold_gene( self ):
        return self.__reproduction_rate_gene

    def reproduction_threshold_value( self ):
        return self.__reproduction_threshold_value

    def hunger_rate( self ):
        return self.__hunger_rate

    def hunger_rate_gene( self ):
        return self.__hunger_rate_gene

    def hunger_rate_value( self ):
        return self.__hunger_rate_value

    def no_offspring_gene( self ):
        return self.__no_offspring_gene

    def no_offspring_value( self ):
        return self.__no_offspring_value

    def life_span( self ):
        return self.__life_span

    def life_span_gene( self ):
        return self.__life_span_gene

    def life_span_value( self ):
        return self.__life_span_value

    def consume_rate( self ):
        return self.__consume_rate

    def consume_rate_gene( self ):
        return self.__consume_rate_gene

    def consume_rate_value( self ):
        return self.__consume_rate_value

    def fighting_gene( self ):
        return self.__fighting_gene

    def fighting_value( self ):
        return self.__fighting_value

    def full( self ):
        return self.__max_hunger - self.__hunger <= 1.e-16

    def eat( self, value, ctype=1 ):
        self.__hunger += value

        return self.__hunger-value, self.__hunger

    def age( self ):
        return self.__age

    def aged( self ):
        self.__age += 1

    def offsprings( self ):
        return self.__offspring

    def last_displacement( self ):
        return self.__last_displacement

    def starve( self ):
        self.__hunger -= self.__hunger_rate_value
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

    def set_pos_index( self, index, value ):
        self.__pos[ index ] = value

    def death( self ):
        return self.__death

    def death_state( self ):
        if self.death():
            return 'dead'
        return ''

    def die( self ):
        self.__death = True
        self.__hunger = 0
        return 0

    def die_check( self ):
        if self.__hunger <= 0 or self.__age >= self.__life_span_value:
            return True

    def reproduce( self ):
        self.__hunger -= self.__reproduction_transfer
        self.__offspring += self.__no_offspring_value
        return 0

    def reproduction_check( self ):
        nonce = random.uniform( 0, self.__reproduction_rate_value )
        if( nonce < 1 and \
            not self.age() == 0 and\
            self.hunger() >= self.reproduction_threshold() ):
            return True
        return False

        # if( self.age() % self.reproduction_rate() == 0 and \
        #     not self.age() == 0 and \
        #     self.hunger() >= self.reproduction_threshold() ):
        #     return True

class prey(animal):

    def __repr__( self ):
        return 'prey' + str( self.id() ) + ' ' + str( self.pos() ) + ' ' + \
                   'age ' + str( self.age() ) + '/' + str( self.life_span_value() ) + ' ' + \
                   'hunger: ' + "{0:.2f}".format( self.hunger() ) + '/' + "{0:.2f}".format( self.max_hunger() ) + ' ' + \
                   self.death_state()

    def info( self ):
        return 'prey' + str( self.id() ) + ' ' + str( self.pos() ) + ' ' + \
               'age ' + str( self.age() ) + '/' + str( self.life_span_value() ) + ' ' + \
               'hunger: ' + "{0:.2f}".format( self.hunger() ) + '/' + "{0:.2f}".format( self.max_hunger() ) + '\n' + \
               'rep_threshold: ' + str( self.reproduction_threshold() ) + '\n' + \
               'rep_transfer: ' + str( self.reproduction_transfer() ) + '\n' + \
               'rep_rate: ' + str( self.reproduction_rate() ) + '\n' + \
               'hunger_rate: ' + str( self.hunger_rate_value() ) + '\n' + \
               'consume_rate: ' + str( self.consume_rate_value() ) + '\n' + \
               self.death_state()

    def animal_type( self ):
        return 0

class predator(animal):

    def __repr__( self ):
        return 'predator' + str( self.id() ) + ' ' + str( self.pos() ) + ' ' + \
               'age ' + str( self.age() ) + '/' + str( self.life_span_value() ) + ' ' + \
               'hunger: ' + "{0:.2f}".format( self.hunger() ) + '/' + "{0:.2f}".format( self.max_hunger() ) + ' ' + \
               self.death_state()

    def info( self ):
        return 'prey' + str( self.id() ) + ' ' + str( self.pos() ) + ' ' + \
               'age ' + str( self.age() ) + '/' + str( self.life_span_value() ) + ' ' + \
               'hunger: ' + "{0:.2f}".format( self.hunger() ) + '/' + "{0:.2f}".format( self.max_hunger() ) + '\n' + \
               'rep_threshold: ' + str( self.reproduction_threshold() ) + '\n' + \
               'rep_transfer: ' + str( self.reproduction_transfer() ) + '\n' + \
               'rep_rate: ' + str( self.reproduction_rate() ) + '\n' + \
               'hunger_rate: ' + str( self.hunger_rate_value() ) + '\n' + \
               'consume_rate: ' + str( self.consume_rate_value() ) + '\n' + \
               self.death_state()

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

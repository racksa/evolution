import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import pickle
import copy
from scipy import optimize

import ecosystem

# Enable/disable loading
enable_loading = False
# index of the frame for loading
load_entry = -1

# The name of the file that you want to load
load_file = 'save_file'
# The name of the file that you want to save
save_file = 'save_file'

frame_number = 401
enable_draw = False
auto_stop_count = 0

# dimension of space
dimension = 10
# order of space
order = 20
# initial prey number
initial_prey_no = 0
# initial predator number
initial_predator_no = 0


def exponential( x, k ):
    return 1000*np.exp(k*x)

# condition for bugs to reproduce
prey_reproduction_threshold=20
# hunger transfered to offspring
prey_reproduction_transfer=.6
# every n cycle the bug will reproduce
prey_reproduction_rate=5
# hunger decresing rate
prey_hunger_rate=.1
# prey life span
prey_life_span=20
# prey max hunger
prey_max_hunger=30
# initial hunger value of prey
initial_prey_hunger=10
# max amount of food can be consumed
prey_consume_rate=.2

# condition for bugs to reproduce
predator_reproduction_threshold=80
# hunger transfered to offspring
predator_reproduction_transfer=.6
# every n cycle the predator will reproduce
predator_reproduction_rate=30
# hunger decresing rate
predator_hunger_rate=1.
# predator life span
predator_life_span=120
# predator max hunger
predator_max_hunger=120
# initial hunger value of predator
initial_predator_hunger = predator_max_hunger
# max amount of food can be consumed
predator_consume_rate=40


# food generation rate
food_generation_rate = 1
# no. of squares that receive food
food_generation_no = int( 200 * (order / 15.)**2 )
# amount of food generation per space
food_generation_amount = 1
# maximum food amounyt per square
food_capacity = 30

# initial food distribution
food_distribution = []

# information for repeat
population_ensemble = np.zeros( frame_number )
hunger_rate_ensemble = np.array([])
hunger_rate_gene_ensemble = np.array([])
life_span_ensemble = np.array([])
life_span_gene_ensemble = np.array([])
reproduction_rate_ensemble = np.array([])
reproduction_rate_gene_ensemble = np.array([])
hunger_rate_ensemble = np.array([])
hunger_rate_gene_ensemble = np.array([])


################################################################################
# Initialization
################################################################################
if ( not enable_loading ):
    # Create a list to store ecosystems
    system_list = list()
    # Create a new ecosystem
    ecosystem_instance = ecosystem.ecosystem  ( order=order,  \
                                              initial_no=[ initial_prey_no, initial_predator_no ], \
                                              initial_hunger=[ initial_prey_hunger, initial_predator_hunger ], \
                                              hunger_rate=[ prey_hunger_rate, predator_hunger_rate], \
                                              reproduction_threshold=[ prey_reproduction_threshold, predator_reproduction_threshold ], \
                                              reproduction_transfer=[ prey_reproduction_transfer, predator_reproduction_transfer ], \
                                              reproduction_rate=[ prey_reproduction_rate, predator_reproduction_rate ], \
                                              life_span=np.array([ prey_life_span, predator_life_span ]), \
                                              animal_max_hunger=np.array([ prey_max_hunger, predator_max_hunger ]), \
                                              animal_consume_rate=np.array([ prey_consume_rate, predator_consume_rate ]), \
                                              initial_food_distribution=food_distribution, \
                                              food_capacity=food_capacity, \
                                              enable_draw=enable_draw,\
                                              )
    ecosystem_instance.initialize_data_array( frame_number )
else:
    # Load the previous instance
    try:
        with open( load_file, 'rb' ) as input:
            system_list = pickle.load(input)
            # cut off the list after load entry index
            system_list = system_list[:load_entry]
            ecosystem_instance = system_list[ -1 ]
            ecosystem_instance.initialize_data_array( frame_number )
            print( 'Successfully loaded' )

    except:
        print( "Unexpected error:", sys.exc_info()[0] )
        raise

################################################################################
# Initialising figures
################################################################################
fig = plt.figure()
fig.suptitle( 'Geno\Phenotype distribution, iteration = ' + str( ecosystem_instance.frame() ) )
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

fig2 = plt.figure()
fig.suptitle( 'Geno\Phenotype distribution, iteration = ' + str( ecosystem_instance.frame() ) )
ax5 = fig2.add_subplot(221)
ax6 = fig2.add_subplot(222)
ax7 = fig2.add_subplot(223)
ax8 = fig2.add_subplot(224)

fig3 =plt.figure()



def draw_gene():
    '''
    plot gene pool
    '''

    ax1.hist(  ecosystem_instance.prey_hunger_rate(), bins = 30 )
    ax1.set_title( 'prey hunger rate' )
    # ax1.set_xlabel( 'hunger rate value' )
    ax1.set_ylabel( 'frequency' )
    # ax1.set_xlim([0, 2])

    ax2.hist(  ecosystem_instance.prey_hunger_rate_genevalue(), bins = 30 )
    ax2.set_title( 'prey hunger rate gene' )
    # ax2.set_xlabel( 'hunger rate genevalue' )
    ax2.set_ylabel( 'frequency' )
    # ax2.set_xlim([-4, 11])

    ax3.hist(  ecosystem_instance.prey_fighting(), bins = 30 )
    ax3.set_title( 'prey fighting power' )
    # ax3.set_xlabel( 'life_span value' )
    ax3.set_ylabel( 'frequency' )
    # ax3.set_xlim([0, 70])

    ax4.hist(  ecosystem_instance.prey_fighting_genevalue(), bins = 30 )
    ax4.set_title( 'prey fighting gene' )
    # ax4.set_xlabel( 'life_span gene value' )
    ax4.set_ylabel( 'frequency' )
    # ax4.set_xlim([-4, 11])

    fig.savefig( './fig/' + '1-' +str(frame) + '.png' )

    ax5.hist(  ecosystem_instance.prey_reproduction_rate(), bins = 30 )
    ax5.set_title( 'prey reproduction rate' )
    # ax5.set_xlabel( 'reproduction rate value' )
    ax5.set_ylabel( 'frequency' )
    # ax5.set_xlim([5, 14])

    ax6.hist(  ecosystem_instance.prey_reproduction_rate_genevalue(), bins = 30 )
    ax6.set_title( 'prey reproduction rate gene' )
    # ax6.set_xlabel( 'reproduction rate gene value' )
    ax6.set_ylabel( 'frequency' )
    # ax6.set_xlim([5, 25])

    ax7.hist(  ecosystem_instance.prey_no_offspring(), bins = 30 )
    ax7.set_title( 'no of offspring' )
    # ax6.set_xlabel( 'reproduction rate gene value' )
    ax7.set_ylabel( 'of of offspring' )
    # ax7.set_xlim([0, 12])

    ax8.hist(  ecosystem_instance.prey_no_offspring_genevalue(), bins = 30 )
    ax8.set_title( 'no of offspring gene' )
    # ax6.set_xlabel( 'reproduction rate gene value' )
    ax8.set_ylabel( 'frequency' )
    # ax8.set_xlim([5, 25])

    fig2.savefig( './fig/' + '2-' +str(frame) + '.png' )

    # ax_landscape.hist()
    ax_landscape = fig3.add_subplot(111)

    H, xedges, yedges = np.histogram2d(ecosystem_instance.prey_hunger_rate_genevalue(), ecosystem_instance.prey_reproduction_rate_genevalue(), bins=30 )
    H = H.T  # Let each row list bins with common y range.
    cax = ax_landscape.imshow(H, interpolation='nearest', origin='low', extent=[0, 15, 10, 30], vmin = 0, vmax = 25 )

    plt.colorbar( cax )
    fig3.savefig( './fig/' + '3-' +str(frame) + '.png' )

    plt.clf()

################################################################################
# Evoluting system
################################################################################
for frame in range( int(frame_number) ):
    print( '-----------', 'frame', frame ,'-----------' )

    # auto stop if any kind of animal is dead
    if auto_stop_count >= frame_number * .01 :
        nothing = None
        #break
    if 0 in ecosystem_instance.animal_life_no() :
        auto_stop_count += 1

    # Peoriodically add food to the system
    if( frame % food_generation_rate == 0 and \
        not frame == 0 ):

        # Randomly add food
        for t in range(food_generation_no):
            food_x = random.randint(0,order-1)
            food_y = random.randint(0,order-1)
            ecosystem_instance.add_food( [food_x, food_y], food_generation_amount )

    # system update
    ecosystem_instance.update()
    print( 'prey      / predator       ', "{0:.0f}".format( ecosystem_instance.animal_life_no()[0]), '/', "{0:.0f}".format( ecosystem_instance.animal_life_no()[1]) )
    print( 'prey food / predator food  ', "{0:.2f}".format( ecosystem_instance.animal_food()[0]), '/' , "{0:.2f}".format( ecosystem_instance.animal_food()[1]) )
    print( 'total                      ', "{0:.2f}".format( ecosystem_instance.total_food() )  )
    print( 'animal    / plant          ', "{0:.2f}".format( sum(ecosystem_instance.animal_food())), '/', "{0:.2f}".format(ecosystem_instance.vege_food())  )

    print( 'preybirth', ecosystem_instance.prey_birth() )
    print( 'preydeath', ecosystem_instance.prey_natural_death()  )
    print( 'predatorbirth', ecosystem_instance.predator_birth() )
    print( 'predatordeath', ecosystem_instance.predator_death()  )


    # store ecosystem to a list
    if frame == ( frame_number - 1 ):
        system_list.append( copy.deepcopy(ecosystem_instance) )

    # if frame % (frame_number/5) == 0 and not frame ==0:
    if ( (frame+1) % 10 == 0 ) or frame+1 == frame_number:
        draw_gene()

    if frame == 10:
        ecosystem_instance.species_invasion( 20 )
    #
    # if frame == 500:
    #     food_generation_no = int( food_generation_no* 2. )


print( '***Saving current session***' )
system_list.append( copy.deepcopy(ecosystem_instance) )

# save current instance
with open( save_file, 'wb' ) as output:
    pickle.dump( system_list, output, pickle.HIGHEST_PROTOCOL )

print( '***Session saved！***' )


################################################################################
# Analysis part
################################################################################
# plot


fig2 = plt.figure()
prey_plot, = plt.plot( ecosystem_instance.frame_array(), ecosystem_instance.prey_no_array(), label = 'Prey population' )
predator_plot, = plt.plot( ecosystem_instance.frame_array(), ecosystem_instance.predator_no_array(), label = 'Predator population' )
plt.legend( handles= [ prey_plot, predator_plot ], loc = 'upper right')
plt.xlabel( 'frame' )
plt.ylabel( 'animal no' )
plt.title( 'Animal population vs. time' )


# par, err = optimize.curve_fit( exponential, ecosystem_instance.frame_array(), ecosystem_instance.predator_no_array() )
# plt.plot( ecosystem_instance.frame_array(), exponential(ecosystem_instance.frame_array(),par[0]), label = 'Prey population' )
#
# print( par )


# fig2 = plt.figure()
# plt.
# plt.title( 'prey hunger rate' )
#
# fig2 = plt.figure()
# ax = fig2.add_subplot(111)
# plt.hist(  ecosystem_instance.prey_hunger_rate_genevalue(), bins = 15 )
# plt.title( 'prey hunger rate gene' )
#
# text = 'frame' + str( ecosystem_instance.frame() )
# plt.text(0.1, 0.9, text,
#      horizontalalignment='center',
#      verticalalignment='center',
#      transform = ax.transAxes)

'''
# prey life span
prey_life_span=300
# prey max hunger
prey_max_hunger=20
# initial hunger value of prey
initial_prey_hunger=10
# max amount of food can be consumed
prey_consume_rate=2

# condition for bugs to reproduce
predator_reproduction_threshold=50
# hunger transfered to offspring
predator_reproduction_transfer=15
# every n cycle the predator will reproduce
predator_reproduction_rate=1
# hunger decresing rate
predator_hunger_rate=3
# predator life span
predator_life_span=800
# predator max hunger
predator_max_hunger=100
# initial hunger value of predator
initial_predator_hunger = predator_max_hunger
# max amount of food can be consumed
predator_consume_rate=1



# food generation rate
food_generation_rate = 1
# no. of squares that receive food
food_generation_no = 10
# amount of food generation per space
food_generation_amount = 3
# maximum food amounyt per square
food_capacity = 15

'''
plt.show()














#

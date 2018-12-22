import numpy as np
import matplotlib.pyplot as plt
import random
import pickle

import ecosystem

fram_number = 501

# dimension of space
dimension = 2
# order of space
order = 100
# initial prey number
initial_prey_no = 500
# initial predator number
initial_predator_no = 200
# initial hunger value of the first prey
initial_prey_hunger = 100.
# initial hunger value of the first predator
initial_predator_hunger = 200.

# condition for bugs to reproduce
prey_reproduction_threshold=20
# hunger transfered to offspring
prey_reproduction_transfer=10
# every n cycle the bug will reproduce
prey_reproduction_rate=5
# hunger decresing rate
prey_starving_rate=1
# prey life span
prey_life_span = 100
# condition for bugs to reproduce
predator_reproduction_threshold=120
# hunger transfered to offspring
predator_reproduction_transfer=60
# every n cycle the bug will reproduce
predator_reproduction_rate=40
# hunger decresing rate
predator_starving_rate=2
# predator life span
predator_life_span=500


# food generation rate
food_generation_rate = 1
# no. of squares that receive food
food_generation_no = 1000
# (max) amount of food generation per space
food_generation_amount = 5

# initial food distribution
food_distribution = [#[x,y,amount]
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                              [random.randint(0,order-1), random.randint(0,order-1), random.randint(0,15)],
                    ]

food_distribution = []


# Create an ecosystem
current_instance = ecosystem.ecosystem(   order=order,  \
                                initial_no=[ initial_prey_no, initial_predator_no ], \
                                initial_hunger=[ initial_prey_hunger, initial_predator_hunger ], \
                                starving_rate=[ prey_starving_rate, predator_starving_rate], \
                                reproduction_threshold=[ prey_reproduction_threshold, predator_reproduction_threshold ], \
                                reproduction_transfer=[ prey_reproduction_transfer, predator_reproduction_transfer ], \
                                reproduction_rate=[ prey_reproduction_rate, predator_reproduction_rate ], \
                                life_span=np.array([ prey_life_span, predator_life_span ]), \
                                initial_food_distribution=food_distribution, \
                            )


# Statistics
prey_no = np.array([])
predator_no = np.array([])
frame_array = np.array([])

for i in range( fram_number ):
    print( '-----------', 'frame', i ,'-----------' )

    # system update
    current_instance.update()

    prey_no = np.append( prey_no, current_instance.animal_life_no()[0] )
    predator_no = np.append( predator_no, current_instance.animal_life_no()[1] )
    frame_array = np.append( frame_array, i )

    # Peoriodically add food to the system
    if( i % food_generation_rate == 0 and \
        not i == 0 ):
        for t in range(food_generation_no):
            food_x = random.randint(0,order-1)
            food_y = random.randint(0,order-1)
            current_instance.add_food( [food_x, food_y], food_generation_amount )

    print( current_instance.animal_life_no() )
    print( current_instance.animal_food() )

# save current instance
with open( 'saved_file', 'wb' ) as output:
    pickle.dump( current_instance, output, pickle.HIGHEST_PROTOCOL )

# load the saved instance
# try:
#     with open( load_file, 'rb' ) as input:
#         current_instance = pickle.load(input)
#         print( 'Successfully loaded' )
#
# except:
#     print( "Unexpected error:", sys.exc_info()[0] )
#     raise

# plot
fig = plt.figure()

prey_plot, = plt.plot( frame_array, prey_no, label = 'Prey population' )
predator_plot, = plt.plot( frame_array, predator_no, label = 'Predator population' )

plt.xlabel( 'frame' )
plt.ylabel( 'animal no' )
plt.title( 'Animal population vs. time' )
plt.legend( handles= [ prey_plot, predator_plot ], loc = 'upper right')

plt.show()














#

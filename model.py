import numpy as np
import matplotlib.pyplot as plt
import random
import pickle

import ecosystem

fram_number = 1
enable_draw = False
auto_stop_count = 0

# dimension of space
dimension = 2
# order of space
order = 20
# initial prey number
initial_prey_no = 250
# initial predator number
initial_predator_no = 7


# condition for bugs to reproduce
prey_reproduction_threshold=13
# hunger transfered to offspring
prey_reproduction_transfer=6
# every n cycle the bug will reproduce
prey_reproduction_rate=1
# hunger decresing rate
prey_starving_rate=1
# prey life span
prey_life_span=300
# prey mobility
prey_mobility=1
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
predator_starving_rate=3
# predator life span
predator_life_span=800
# predator mobility
predator_mobility=1
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
current_instance = ecosystem.ecosystem  ( order=order,  \
                                          initial_no=[ initial_prey_no, initial_predator_no ], \
                                          initial_hunger=[ initial_prey_hunger, initial_predator_hunger ], \
                                          starving_rate=[ prey_starving_rate, predator_starving_rate], \
                                          reproduction_threshold=[ prey_reproduction_threshold, predator_reproduction_threshold ], \
                                          reproduction_transfer=[ prey_reproduction_transfer, predator_reproduction_transfer ], \
                                          reproduction_rate=[ prey_reproduction_rate, predator_reproduction_rate ], \
                                          life_span=np.array([ prey_life_span, predator_life_span ]), \
                                          animal_mobility=np.array([ prey_mobility, predator_mobility ]), \
                                          animal_max_hunger=np.array([ prey_max_hunger, predator_max_hunger ]), \
                                          animal_consume_rate=np.array([ prey_consume_rate, predator_consume_rate ]), \
                                          initial_food_distribution=food_distribution, \
                                          food_capacity=food_capacity, \
                                          enable_draw=enable_draw,\
                                        )


# Statistics
prey_no = np.array([])
predator_no = np.array([])
frame_array = np.array([])

# for i in range( order ):
#     for j in range( order ):
#         current_instance.add_food( [i, j], food_generation_amount )

for frame in range( int(fram_number) ):
    print( '-----------', 'frame', frame ,'-----------' )

    # auto stop if any kind of animal is dead
    if auto_stop_count >= fram_number * .01 :
        break
    if 0 in current_instance.animal_life_no() :
        auto_stop_count += 1

    # Peoriodically add food to the system
    if( frame % food_generation_rate == 0 and \
        not frame == 0 ):
        # for t in range(food_generation_no):
        #     food_x = random.randint(0,order-1)
        #     food_y = random.randint(0,order-1)
        #     current_instance.add_food( [food_x, food_y], food_generation_amount )
        for i in range( order ):
            for j in range( order ):
                current_instance.add_food( [i, j], food_generation_amount )

    # system update
    current_instance.update()
    print( 'prey      / predator       ', "{0:.0f}".format( current_instance.animal_life_no()[0]), '/', "{0:.0f}".format( current_instance.animal_life_no()[1]) )
    print( 'prey food / predator food  ', "{0:.2f}".format( current_instance.animal_food()[0]), '/' , "{0:.2f}".format( current_instance.animal_food()[1]) )
    print( 'total                      ', "{0:.2f}".format( current_instance.total_food() )  )
    print( 'animal    / plant          ', "{0:.2f}".format( sum(current_instance.animal_food())), '/', "{0:.2f}".format(current_instance.vege_food())  )


    prey_no = np.append( prey_no, current_instance.animal_life_no()[0] )
    predator_no = np.append( predator_no, current_instance.animal_life_no()[1] )
    frame_array = np.append( frame_array, frame )



# save current instance
with open( 'saved_file', 'wb' ) as output:
    pickle.dump( current_instance, output, pickle.HIGHEST_PROTOCOL )

# load saved instances
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
text =  'prey_reproduction_threshold=13 \n' \
        'prey_reproduction_transfer=6 \n' \
        'prey_reproduction_rate=1 \n' \
        'prey_starving_rate=1'
plt.text( 0, -1, text, horizontalalignment = 'center' )

'''
# prey life span
prey_life_span=300
# prey mobility
prey_mobility=1
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
predator_starving_rate=3
# predator life span
predator_life_span=800
# predator mobility
predator_mobility=1
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

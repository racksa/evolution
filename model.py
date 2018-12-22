import numpy as np
import matplotlib.pyplot as plt
import random

import ecosystem


# dimension of space
dimension = 2
# order of space
order = 7
# initial prey number
initial_prey_no = 10
# initial predator number
initial_predator_no = 5
# initial hunger value of the first prey
initial_prey_hunger = 100
# initial hunger value of the first predator
initial_predator_hunger = 1000

# condition for bugs to reproduce
prey_reproduction_threshold=50
# hunger transfered to offspring
prey_reproduction_transfer=20
# every n cycle the bug will reproduce
prey_reproduction_rate=150
# hunger decresing rate
prey_starving_rate = 0
# condition for bugs to reproduce
predator_reproduction_threshold=100
# hunger transfered to offspring
predator_reproduction_transfer=40
# every n cycle the bug will reproduce
predator_reproduction_rate=200
# hunger decresing rate
predator_starving_rate = 0


# food generation rate
food_generation_rate = 10000
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
system = ecosystem.ecosystem(   order=order,  \
                                initial_no=[ initial_prey_no, initial_predator_no ], \
                                initial_hunger=[ initial_prey_hunger, initial_predator_hunger ], \
                                starving_rate=[ prey_starving_rate, predator_starving_rate], \
                                reproduction_threshold=[ prey_reproduction_threshold, predator_reproduction_threshold ], \
                                reproduction_transfer=[ prey_reproduction_transfer, predator_reproduction_transfer ], \
                                reproduction_rate=[ prey_reproduction_rate, predator_reproduction_rate ], \
                                initial_food_distribution=food_distribution, \
                            )

for i in range( 91 ):
    print( '-----------', 'frame', i ,'-----------' )

    # Peoriodically add food to the system
    if( i % food_generation_rate == 0 and \
        not i == 0 ):
        food_x = random.randint(0,order-1)
        food_y = random.randint(0,order-1)
        system.add_food( [food_x, food_y], 10 )

    system.update()

import numpy as np
import matplotlib.pyplot as plt
import random

import ecosystem


# dimension of space
dimension = 2
# order of space
order = 10
# initial hunger value of the first bug
initial_hunger = 100
# hunger decresing rate
starving_rate = 1
# condition for bugs to reproduce
reproduction_threshold=50
# hunger transfered to offspring
reproduction_transfer=20
# every n cycle the bug will reproduce
reproduction_rate=7
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

# Create an ecosystem
system = ecosystem.ecosystem(   order=order,  \
                                initial_hunger=initial_hunger, \
                                initial_food_distribution=food_distribution, \
                                starving_rate=starving_rate, \
                                reproduction_threshold=reproduction_threshold, \
                                reproduction_transfer=reproduction_transfer, \
                                reproduction_rate=reproduction_rate, \
                            )

for i in range( 200 ):
    print( '####', i ,'####' )

    # Peoriodically add food to the system
    if i % 1 == 0:
        food_x = random.randint(0,order-1)
        food_y = random.randint(0,order-1)
        system.add_food( [food_x, food_y], 10 )

    system.update()

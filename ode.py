import matplotlib.pyplot as plt

time_step=0.1
alpha=1.1
beta=0.4
sigma=0.1
gamma=0.4
ini_x=10
ini_y=10

x=ini_x
y=ini_y
x_list=[]
y_list=[]

for i in range(1000):
    rate_x=alpha*x-beta*x*y
    rate_y=sigma*x*y-gamma*y
    x_list.append(x)
    y_list.append(y)
    x_new=x+rate_x*time_step
    y_new=y+rate_y*time_step
    if x_new<0:
        x_new=0
    if y_new<0:
        y_new=0        
    x=x_new
    y=y_new
    
plt.plot(x_list,label='prey')
plt.plot(y_list, label='predator')
plt.ylabel('Number of population')
plt.xlabel('Time')
plt.legend()

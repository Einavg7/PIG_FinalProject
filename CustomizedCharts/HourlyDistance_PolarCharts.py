import matplotlib.pyplot as plt
import numpy as np


#=================POLAR CHARTS FOR HOURLY DISTANCE==========================

plt.figure(1)
x = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
theta = np.linspace(0.0, 2 * np.pi,24, endpoint=False)
offset = 2.0
R1=  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
width = np.pi /12

ax1 = plt.subplot(111, projection='polar')
ax1.set_theta_direction(-1)
ax1.bar(theta,R1,width=width, bottom=0.0, color=colors, alpha=0.5)

plt.show()



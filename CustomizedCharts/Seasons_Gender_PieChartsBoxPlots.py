import numpy as np
import matplotlib.pyplot as plt

# Some data
labels = 'Spring', 'Summer', 'Autumn', 'Winter'
fracs1 = [15, 30, 45, 10]
fracs2 = [40, 20, 50, 55]
fracsBoth = [50, 20, 40, 75]
# Make figure and axes
fig, axs = plt.subplots(3, 2)
axs[0,1].set_title("Seasons and Female")
# A standard pie plot
axs[0,1].pie(fracs1, labels=labels, autopct='%1.1f%%', shadow=True, counterclock = False )

# Shift the second slice using explode
axs[1,1].set_title("Seasons and Male")
axs[1,1].pie(fracs2, labels=labels, autopct='%.0f%%', shadow=True,
              explode=(0, 0.1, 0, 0), counterclock = False )
              
axs[2,1].set_title("Seasons and Male")
axs[2,1].pie(fracsBoth, labels=labels, autopct='%.0f%%', shadow=True,
                 counterclock = False )


# fake up some data
spread = np.random.rand(50) * 100
center = np.ones(25) * 50
flier_high = np.random.rand(10) * 100 + 100
flier_low = np.random.rand(10) * -100
data = np.concatenate((spread, center, flier_high, flier_low))
red_square = dict(markerfacecolor='r', marker='s')
axs[0,0].set_title('Shorter Whisker Length - Female')
axs[0,0].boxplot(data, flierprops=red_square, vert=False, whis=0.75)

axs[1,0].set_title('Shorter Whisker Length -Male')
axs[1,0].boxplot(data, flierprops=red_square, vert=False, whis=0.75)

axs[2,0].set_title('Shorter Whisker Length  - Both')
axs[2,0].boxplot(data, flierprops=red_square, vert=False, whis=0.75)

plt.show()
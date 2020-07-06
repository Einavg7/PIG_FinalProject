import matplotlib.pyplot as plt
import numpy as np
import random


n_bins = 20

x = np.random.uniform(low=0.5, high=10, size=(100,))

print(x)
fig, axs = plt.subplots(1, 1)
#, sharey=True, tight_layout=True
# We can set the number of bins with the `bins` kwarg
axs.hist(x, bins=n_bins)

plt.title('Frequency plot of Daily Distance')
plt.ylabel('Frequency')
plt.xlabel('Daily Distance in KM')
plt.show()
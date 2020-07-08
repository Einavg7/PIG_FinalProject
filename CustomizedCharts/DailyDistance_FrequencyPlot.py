import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import os
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
import matplotlib


def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'
    


#Define no. of classes/bins
n_bins = 50

#Set path to input file
summaryFolder="C:\\Users\\DELL\\Documents\\GitHub\\Project\\PIG_FinalProject\\summaryCSVs"
filename="dailyDistances.csv"
dailySummaryCSV=os.path.join(summaryFolder,filename)

dailySummary=pd.read_csv(dailySummaryCSV)
#read distance value from daily summary
total=dailySummary['Distance']
male_only=dailySummary[dailySummary['Gender']=="m"]['Distance']
female_only=dailySummary[dailySummary['Gender']=="f"]['Distance']
fig, axs = plt.subplots(1,2,sharey=False)

axs[0].hist(male_only, bins=n_bins)
axs[0].set_title("male owl")
axs[0].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=len(male_only)))
axs[1].hist(female_only, bins=n_bins)
axs[1].set_title("female owl")
axs[1].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=len(female_only)))

fig.suptitle('Frequency plot of Daily Distance')
#plt.ylabel('Frequency')
plt.xlabel('Daily Distance in Meters')
plt.show()
# We can set the number of bins with the `bins` kwarg


"""
The idea of this script is to simulate directly using the psychopy QUEST object in order to check the threshold estimate.

I don't know how to simulate from a weibull distribution (given that psychopy internally work in log10 units but within the experiment is in standard units 0-1)

Using a normal cdf function the estimation is quite good so for simulation purposes we can use a normal/logistic cdf
"""

# Modules

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from psychopy import data
import random as rd

# Functions

def psynorm(x, threshold, slope, guess = 0, lapses = 0):
    return guess + (1 - guess - lapses) * stats.norm.cdf(x, threshold, slope)

# Parameters

threshold = 0.5
slope = 0.2
guess = 0
lapses = 0
ntrials = 1000
xi = np.linspace(0, 1, 1000)

# Plotting

plt.plot(xi, psynorm(xi, threshold, slope))
plt.show()

# Creating Staircases

quest_50 = data.QuestHandler(0.5, 0.2, beta = 3.5,
    pThreshold=0.5, gamma=0, delta = 0,
    minVal=0, maxVal=1,
    ntrials = ntrials)

quest_70 = data.QuestHandler(0.5, 0.2, beta = 3.5,
    pThreshold=0.7, gamma=0, delta = 0,
    minVal=0, maxVal=1,
    ntrials = ntrials)

quest_80 = data.QuestHandler(0.5, 0.2, beta = 3.5,
    pThreshold=0.8, gamma=0, delta = 0,
    minVal=0, maxVal=1,
    ntrials = ntrials)

quest_list = [quest_50, quest_70, quest_80] # list

for trial in range(ntrials*len(quest_list)):
    which_quest = rd.randint(0,2) # select the staircase
    
    xi = quest_list[which_quest]._nextIntensity # trial contrast
    #pi = guess + (1 - lapses) * 1 - (1 - guess) * np.exp(-10**(beta * (np.log10(xi) - np.log10(threshold) + quest.epsilon)))
    
    # TODO check the weibull in order to simulate
    pi = psynorm(xi, threshold, slope) # get p(yes)
    ri = np.random.binomial(1, pi, 1)[0] # get 01 according to p
    quest_list[which_quest].addResponse(ri) # updating
    
means = [x.mean() for x in quest_list] # computing means
print(means)

# TODO check which values are presented in terms of variability
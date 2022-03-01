
from psychopy import data
import random as rd
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
from psy import staircase as mystair

ntrials = 1000

np.random.seed(100)

stair21 = data.StairHandler(0, nReversals=1, stepSizes=0.05, nTrials=ntrials, nUp=1, nDown=3, applyInitialRule=False, extraInfo=None, method='2AFC', stepType='lin', minVal=0, maxVal=1)

for xi in stair21:
    pi = norm.cdf(xi, loc = 0.5, scale = 0.2)
    ri = np.random.binomial(1, pi, size=1)[0]
    stair21.addResponse(ri)
    
print(np.average(stair21.reversalIntensities[2:]))
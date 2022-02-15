# Notes

The idea here is to apply the concept of the **subliminal perception window** to the unconscious WM effect. Given that we have to target an higher point on the psychometric function we need to change the `up/down` rule (you can find this on Garcia-Perez, 2000). In fact, the best approach would have been to use the Lesmes et al. (2015) approach that directly target a specific $d'$ level but the code is not open-source.

The problems are:

- which procedure to use:
  - QUEST: i don't like the parametrization (not easy to simulate)
  - PSY: not really useful to use *during* the experiment but for estimating the threshold and slope (in my case is not relevant)
  - Staircase: probably the best, maybe too slow

The idea is to interleave ~3 staircases that use a different `up/down` rule during the main experiment so not using a calibration approach. In this way the staircase should stabilize at a given % of visibility keeping the stimulus level variable but focused to the target point (variability according to the step size).

## Simulations

The important part to simulate:

- using Tel-Aviv data estimate the psych function and simulate with number of trials, starting point etc.
- try to simulate someting related to the **subliminal perception window** paper

## Experiment

- implement the experiment in psychopy

# References

- https://questplus.readthedocs.io/en/latest/psychometric_function.html
- https://psychtoolbox.discourse.group/t/problems-and-doubt-regard-quest-implementation/3123/2
- https://journal.r-project.org/archive/2016-1/linares-na.pdf
- http://www.cvrl.org/neur3001/Lecture%20Notes/Greenwood/Greenwood%20Advanced%20Psychophysics.PDF

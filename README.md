
<!-- README.md is generated from README.Rmd. Please edit that file -->

# Unconscious WM Behavioral

This repository contains the scripts to reproduce the experiment.

# Todo

    #> +- unconscious-wm-sdt
    #>    +- test
    #>    ¦  +- testing_quest.py
    #>    ¦     +- line 61: TODO check the weibull in order to simulate
    #>    ¦     +- line 69: TODO check which values are presented in terms of variability
    #>    +- experiment.py
    #>    ¦  +- line 19: TODO check if is correct to set the test ori in this way doubt about the clock/anticlock
    #>    ¦  +- line 159: TODO check the pas translation
    #>    ¦  +- line 293: TODO set better values for gamma/delta
    #>    ¦  +- line 310: TODO icrease the quest 0.80 to 0.85
    #>    +- utils.py
    #>       +- line 19: TODO check if the with open statment is too slow
    #>       +- line 161: TODO set the same number of catch for each staircase

# Note

    #> - The QUEST estimation is good. The only problem is the spread of the psychometric function. If too low, the $p(yes)$ saturate very fast.
    #> - The maximum point should be ~0.85. More than that have a PAS 1 rate too low
    #> - I can reduce the number of catch trials in order to have more valid trials even with high $p(yes)$


<!-- README.md is generated from README.Rmd. Please edit that file -->

# Unconscious WM Behavioral

This repository contains the scripts to reproduce the experiment.

# Todo

    #> +- unconscious-wm-sdt
    #>    +- modules
    #>    ¦  +- utils.py
    #>    ¦     +- line 18: TODO check if the with open statment is too slow
    #>    +- test
    #>    ¦  +- testing_quest.py
    #>    ¦     +- line 61: TODO check the weibull in order to simulate
    #>    ¦     +- line 69: TODO check which values are presented in terms of variability
    #>    +- experiment.py
    #>       +- line 166: TODO check the pas translation
    #>       +- line 316: TODO set better values for other parameters
    #>       +- line 383: TODO add the catch for the uncued side of memory. Check if the test was always mask-cued and not random(mask or ori)-cued
    #>       +- line 416: TODO adding jittering

# Note

    #> # Notes
    #> 
    #> - the mask (catch) should be present on the uncued side. Set a random integer from 0 to length ORI + mask and set the target (and ori) or only the mask.
    #> - check if not using deepcopy is a problem
    #> - maybe removing the mask as target is a problem

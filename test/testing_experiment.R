# --- Script to check data

# Packages

library(dplyr)
library(psycho)

# Functions

test_passed <- function(test_name) {
    cli::cli_alert_success(sprintf("Test %s passed!", test_name))
}

test_failed <- function(test_name) {
    cli::cli_alert_danger(sprintf("Test %s failed!", test_name))
}

test <- function(test_name, expr) {
    if(expr) {
        test_passed(test_name)
    }else{
        test_failed(test_name)
    }
}

# Vars

catch_valid_ratio <- 2/3
ntrials_cond <- 7
test_key <- c("change" = "f", "same" = "j") # keys for the change detection task

# Loading Data

dat <- read.csv("data/csv/10_(2022-03-10_19-08-49).csv")

# Check total trials valid and catch

test_catch_valid_ratio <- dat %>%
    count(trial_type) %>% # the prop should be the same as the experiment script
    pull(n)

test("Catch Ratio",
    (test_catch_valid_ratio[1]/test_catch_valid_ratio[2]) == catch_valid_ratio
)

# Check contrast for catch trials

test_catch_contrast <- dat$contrast[dat$trial_type == "catch"]

test("Contrast catch = 0", all(test_catch_contrast == 0))

# Check number of catch for each quest

test_catch_quest <- dat %>%
    filter(trial_type == "catch") %>% 
    count(quest)

test("Equal ncatch for each quest", length(unique(test_catch_quest$n)) == 1)

# Check Number of trials per condition

test_ntrials_cond <- dat %>%
    filter(trial_type == "valid") %>%
    count(memory_ori, trial_type, quest, type, which_change)

test("Ntrials cond per cond", all(test_ntrials_cond$n == ntrials_cond))

# Check PAS and staircase match

test_pas_vis <- dat %>%
    select(pas, vis) %>%
    # all should be true
    mutate(check = case_when(pas == 1 & vis == 0 ~ TRUE,
                             pas > 1 & vis == 1 ~ TRUE,
                             TRUE ~ FALSE))

test("Pas and Vis convertion", all(test_pas_vis$check))

# Check test and memory ori

test_memory_test_ori <- dat %>%
    filter(trial_type == "valid") %>%
    mutate(check = case_when(
        type == "change" & (test_ori != memory_ori) ~ TRUE,
        type == "same" & (test_ori == memory_ori) ~ TRUE,
        TRUE ~ FALSE)
    )

test("Memory and Test ori match", all(test_memory_test_ori$check))

# check if probe keypress match the stimulus

test("Probe key and Probe type match", all(unname(test_key[dat$test]) == dat$test_key))

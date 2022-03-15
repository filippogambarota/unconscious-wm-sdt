# Packages

library(tidyverse)

# Data

dat <- read.csv("data/csv/10_(2022-03-10_19-08-49).csv")

# Functions

ppsy <- function(q, threshold, slope, guess, lapses) {
    guess + (1 - guess - lapses) * pnorm(q, threshold, slope)
}

dpsy <- function(p, threshold, slope, guess, lapses) {
    guess + (1 - guess - lapses) * qnorm(p, threshold, slope)
}

get_d <- function(sdt_tab) {
    psycho::dprime(sdt_tab["hit"],
                sdt_tab["fa"],
                sdt_tab["miss"],
                sdt_tab["cr"])
} 

# QUEST Parameters

threshold <- 0.5
slope <- 0.2
guess <- 0
lapses <- 0

# Check QUEST

dat %>%
    filter(trial_type == "valid") %>%
    group_by(quest) %>%
    mutate(trialq = 1:n()) %>%
    ungroup() %>%
    ggplot(aes(x = trialq, y = contrast)) +
    facet_wrap(~quest, ncol = 1) +
    geom_point() +
    ylim(c(0, 1))

# Check SDT
# Here the dprime should be higher according to quest

sdt <- dat %>%
    select(vis, trial_type, quest) %>%
    mutate(trial_type = ifelse(trial_type == "valid", 1, 0),
           sdt = case_when(
               vis == 1 & trial_type == 1 ~ "hit",
               vis == 1 & trial_type == 0 ~ "fa",
               vis == 0 & trial_type == 0 ~ "cr",
               TRUE ~ "miss"
           )) %>%
    group_by(quest) %>%
    nest() %>%
    mutate(sdt_tab = map(data, function(x) table(x$sdt))) %>%
    ungroup()

# Check number of trials PAS 1 per QUEST

dat %>%
    filter(trial_type == "valid") %>%
    group_by(quest) %>%
    summarise(pyes = mean(vis == 0),
              nvalid = pyes * nrow(dat_fit)/3)

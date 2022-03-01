library(quickpsy)

fa_rate <- c(0, 0.1, 0.2, 0.3)

sim_obs <- function(fa_rate, ntrials, x_signal, p = c(0.5, 0.1), nsim = 1){
  psy_fun <- create_psy_fun(cum_normal_fun, fa_rate, 0)
  
  dat <- expand.grid(
    is_signal = c(1, 0),
    trial = 1:ntrials
  )
  
  dat$x <- ifelse(dat$is_signal == 1,
                  x_signal, 0)
  
  dat$xi <- psy_fun(dat$x, p)
  dat$y <- rbinom(nrow(dat), 1, dat$xi)

  dat$sdt <- case_when(dat$is_signal == 1 & dat$y == 1 ~ "hit",
                       dat$is_signal == 1 & dat$y == 0 ~ "miss",
                       dat$is_signal == 0 & dat$y == 1 ~ "fa",
                       TRUE ~ "cr")
  
  sdt <- table(dat$sdt)
  sdt_m <- c("hit", "miss", "fa", "cr")
  missing <- sdt_m[!sdt_m %in% names(sdt)]
  sdt_missing <- rep(0, length(missing))
  names(sdt_missing) <- missing
  sdt <- c(sdt, sdt_missing)
  
  res <- psycho::dprime(sdt["hit"], sdt["fa"], sdt["miss"], sdt["cr"])
  res$acc <- mean(dat$y[dat$is_signal == 1])
  res
}

sim <- vector(mode = "list", length = length(fa_rate))

for(i in 1:length(fa_rate)){
  sim[[i]] <- sapply(1:1000, function(x) sim_obs(fa_rate[i], 100, 0.7)$dprime)
}

names(sim) <- fa_rate

bind_cols(sim) %>% 
  apply(., 2, mean)

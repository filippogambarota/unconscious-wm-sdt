find_reversals <- function(resp){
  rev <- vector(mode = "logical", length = length(resp))
  for(i in 1:(length(resp)-1)){
    if(resp[i] != resp[i + 1]){
      rev[i + 1] <- TRUE
    }
  }
  rev
}

sim_stair <- function(ntrials, psy_fun, params,
                      nup = 1, ndown = 1, step,
                      x, max_x = 1, min_x = 0){
  respn <- 0
  xi <- vector(mode = "numeric", length = ntrials)
  respi <- vector(mode = "integer", length = ntrials)
  
  for(i in 1:ntrials){
    p <- psy_fun(x, p = params)
    respi[i] <- rbinom(1, 1, p)
    if(respi[i] == 1){
      respn <- respn + 1
      if(respn == ndown){
        x <- x - step
        x <- ifelse(x < min_x, min_x, x)
        respn <- 0
      }
    }else{
      x <- x + step
      x <- ifelse(x > max_x, max_x, x)
    }
    xi[i] <- x
  }
  data.frame(xi, respi)
}

ntrials <- 100
x <- 0
step <- 0.05
nsim <- 1000
psy_fun <- quickpsy::create_psy_fun(cum_normal_fun, guess = 0, lapses = 0)

sim <- lapply(1:nsim, function(i){
  sim_stair(ntrials = ntrials, psy_fun = psy_fun, params = c(0.3, 0.2), 
            nup = 1, ndown = 3, step = 0.05, x = x, max_x = 1, min_x = 0)
})

th <- sapply(sim, function(x) mean(x$xi[find_reversals(x$respi)]))

psy_fun(median(th), c(0.3, 0.2))


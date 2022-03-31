revert_cdt <- function(data, id_to_revert){
  data %>% 
    mutate(test = case_when(
      subject %in% id_to_revert & test == "same" ~ "change",
      subject %in% id_to_revert & test == "change" ~ "same",
      TRUE ~ test))
}

get_sdt <- function(data, sdt_col){
  sdt_col <- rlang::enexpr(sdt_col)
  data %>% 
    pivot_wider(names_from = !!sdt_col, values_from = n) %>% 
    mutate(fa_rate = fa/(fa + cr),
           hit_rate = hit/(hit + miss),
           dprime = qnorm(hit_rate) - qnorm(fa_rate),
           crit = -((qnorm(hit_rate) + qnorm(fa_rate))/2))
}

compile_report <- function(subject, upload = FALSE){
  suppressMessages({suppressWarnings({
      html <- rmarkdown::render(here("analysis", "single_subject_report.Rmd"), 
                        output_dir = here("analysis", "reports"),
                        output_file = paste0("subject_", subject),
                        output_format = "all",
                        params = list(id = subject), 
                        quiet = TRUE, 
                        clean = TRUE)
  })
  })
  cli::cli_alert_success(paste("Report for subject", subject, "compiled!"))
  if(upload){
    upload_report(html, subject)
  }
}

upload_report <- function(file, subject){
  folder <- "https://drive.google.com/drive/u/0/folders/1p87OlKrDBcdN5E5CRTTlArmEs_QQ65sp"
  folder <- googledrive::as_dribble(folder)
  pdf <- pagedown::chrome_print(file)
  googledrive::drive_upload(pdf, path = folder, verbose = FALSE, overwrite = TRUE)
  cli::cli_alert_info(paste("Report for subject", subject, "uploaded!"))
}
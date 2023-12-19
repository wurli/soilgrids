args      <- commandArgs(trailingOnly = TRUE)
csv       <- paste(args, collapse = "\\r\\n")
soilgrids <- read.csv(text = args)

model <- lm(
  clay + sand + silt ~ ocs,
  data = soilgrids,
  na.action = na.omit
)

summary(model)

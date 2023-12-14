args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 1L) {
  stop("Please supply exactly one trailing argument")
}

soilgrids_summary <- read.csv(text = args)

model <- lm(
  clay + sand + silt ~ ocs,
  data = soilgrids_summary,
  na.action = na.omit
)

summary(model)

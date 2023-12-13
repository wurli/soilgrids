args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 1L) {
  stop("Please supply exactly one trailing argument")
}

input_data <- read.csv(text = args)
model <- lm(clay + sand + silt ~ ocs, data = input_data)

summary(model)

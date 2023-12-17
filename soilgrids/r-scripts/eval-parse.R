# This script simply evaluates the command line arguments as R code. It is used
# for testing purposes only.
args <- commandArgs(trailingOnly = TRUE)

for (line in args) {
  eval(parse(text = line))
}
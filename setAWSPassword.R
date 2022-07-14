# Simple yet important password and credentials practice
# Allows me to share code without my password (removed it)
# Ask for the password once in every session of app.R Rshiny server loading
pwd <- "PASSWORD"
# Store it in options()
options(AWSPassword=pwd)
# Once any user closes their R session, the password is forgotten and not stored
rm(pwd)
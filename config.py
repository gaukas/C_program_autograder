# This is the config file.
path = "./test5/" # Relative Dir to files/directories/zips to be graded
stdpath = "./test5std/"
filepath = "./file/"
mode = "FILE" # DIR, FILE, ZIP. Only file is supported for now
target = "{}_{}.c" # Name probing format

# Compile
#gcc -Wall -Wextra test.c -o exec_out
compiler = "gcc"
comparg = "-Wall -Wextra" 
exec_out = "exec_out.exe"

# Running
exec_timeout = 1 #second

# Grading
# Student will not receive grades lower than 0.
# 0 - Disable Compliation Warning Penalty. 1 - Dock all points off.
warning_penalty = 0 # Range 0~1
return_penalty = 0
stdout_penalty = 0
fileout_penalty = 0
halt_penalty = 0 # If not halting, stdout and return won't be checked.
# 3rd party
#from parse import parse
import sys
import shlex
import os.path
import copy
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
# Self-defined
from config import *
from rubric import *

###########################################################################
#                               Instructions                              #
###########################################################################
#   This module is encapsulated and requires:
#       1. Copy and rename the source code file (.c) to config.path as 
# listed in prob[] of rubric.py.
#       2. Prepare stdin, desired stdout file in config.stdpath. Name as
# listed in test_stdin[]/test_stdout[] of rubric.py
#       3. Each call to grade() will return the total grade for 1 student. 
# You shall prepare the file for each student before each call to grade()
###########################################################################
#   Alternative:
#       Call altgrade(list_of_files) as relative directory to grading.py
#       list_of_files[] must not be longer than following lists to 
# prevent undefined behavior: 
#           points_breakup[] 
#           test_args[] 
#           test_stdin[] 
#           return_val[] 
#           test_stdout[]
###########################################################################

# Compilation
def _compile(filename):
    #outname = parse("{}.c", filename)
    cmd = str(compiler+" "+comparg+" "+filename+" -o "+path+exec_out)
    process = Popen(shlex.split(cmd), stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    #(output, err) = process.communicate()
    output = process.stdout.read()
    exit_code = process.wait()
    if(exit_code!=0):
        #print(output)
        return 1
    if(output!=""):
        #print(output)
        return 2
    return 0

# Compilation Test Func
def compile(filename):
    ret=_compile(filename)
    if(ret==1):
        print("Compilation Error.")
    elif(ret==2):
        print("Compilation Warning.")
    else:
        print("Compilation Complete.")

# Test Case Run, call per testcase
### Inputs
# tc_exec = RELATIVE DIR TO EXEC # sys.path[0] will be inserted automatically
# args = "-a -b"
# stdin_path = "./TestData/stdin"
# retval = 0
# out_sol = "stdout.txt"    # Checking stdout
#   out_sol = ""            # Not Checking stdout
# fileout = ["sol_out1.txt", "out1.txt"] # Checking fileout
#   fileout = []                         # Not checking fileout
### Return
# 0 - Worked perfectly
# 1 - Return value is wrong
# 2 - Stdout does not match
# 4 - File Output does not match
# 8 - Program does not terminate itself (STDOUT won't be checked. RET val can't be checked.)
# Return the compounds of any occured error
def tc_run(tc_exec, stdin_path, retval, out_sol, fileout):
    status = 0
    process=0
    forcekilled=False
    stdin_data=""
    stdout_data=""
    
    # PreCheck: Delete old file if exist
    if(len(fileout)==2 and fileout[0]!="" and fileout[1]!=""):
        if os.path.exists(fileout[1]):
            os.remove(fileout[1]) # Delete fileoutput to prevent usage of old file    
    
    print(tc_exec)

    process = Popen(tc_exec, stdin=PIPE, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    
    # CHECK: Self-terminating
    if(stdin_path!=""): # STDIN is requested
        stdin_file = open(stdpath+stdin_path, 'r') 
        stdin_data = stdin_file.read()
        try:
            stdout_data = process.communicate(input=stdin_data, timeout=exec_timeout)[0]
        except TimeoutExpired:
            #print("Prog does not terminate in "+str(exec_timeout)+" second(s)")
            process.kill()
            forcekilled=True
            status+=8
        else: # Validate returncode if not timeout
            if process.returncode!=retval: # Return val is wrong
                status+=1
    else: # STDIN is not requested
        try:
            stdout_data = process.communicate(timeout=exec_timeout)[0]
        except TimeoutExpired:
            #print("Prog does not terminate in "+str(exec_timeout)+" second(s)")
            process.kill()
            forcekilled=True
            status+=8
        else: # Validate returncode if not timeout
            if process.returncode!=retval: # Return val is wrong
                status+=1
    
    # CHECK: STDOUT
    if(out_sol!="" and not forcekilled): # Only check when not force-killed
        stdoutsol_file = open(stdpath+out_sol, 'r') 
        stdout_sol =  stdoutsol_file.read()
        # Check STDOUT
        if(stdout_data!=stdout_sol and stdout_sol!="ANY"):
            #print("Prog out: " + stdout_data + "\n")
            #print("Solution: " + stdout_sol)
            status+=2
        elif(stdout_sol=="ANY" and stdout_data==""):
            status+=2

    # CHECK: File Output(Write-to-File)
    if(len(fileout)==2 and fileout[0]!="" and fileout[1]!=""):
        if os.path.exists(fileout[1]):
            filesol=""
            filetxt=""
            with open(filepath+fileout[0]) as fp0:
                filesol = fp0.read()
            with open(fileout[1]) as fp1:
                filetxt = fp1.read()
            os.remove(fileout[1]) # Delete fileoutput to prevent usage of old file
            if(filesol!=filetxt):
                #print("File Output Does Not Match")
                status+=4
        else:
            #print("File Output Does Not Exist")
            status+=4

    return status

# Return: A list of grade for each test
# Example:
#       When running against the example points_breakup,
#       with second test for prob1 and third test for prob2 failed.
#       _rubric()
#       > [[20, 0], [15, 5, 0]]
#       
def _rubric(problem_list):
    # For each .c file
    list_of_grades = copy.deepcopy(points_breakup)
    student_report = [] # Format: [[p1.compile, p1.t1, p1.t2,...], [p2.compile, p2.t1, ...],...]
    for p in range(len(problem_list)):
        problem_report = []
        # Check size of points_breakup
        if len(points_breakup[p]) > min([len(test_args[p]), len(test_stdin_path[p]), len(return_val[p]), len(test_stdout_sol_path[p])]):
            print("Fatal Error: Length of points_breakup[" + str(p) + "] is longer than at least one of the other configure lists.")
            exit()
        # Compile only once per problem.
        compret = _compile(problem_list[p])
        problem_report.append(compret)
        if(compret==1):
            # If failed compilation, receive 0.
            for x in range(len(list_of_grades[p])):
                list_of_grades[p][x] = 0
        elif(compret==2):
            # If warning in compilation, deduct max possible points for each test case
            for x in range(len(list_of_grades[p])):
                list_of_grades[p][x] -= points_breakup[p][x]*warning_penalty
        #elif(compret==0), compiled without warning.

        # Start testing current problem problem_list[p] with each tc(test case)
        for tc in range(len(list_of_grades[p])):
            if list_of_grades[p][tc]==0:# Usually caused by: Compilation Error.
                #problem_report.extend(-1,0) # Status = -1, Grade = 0 for this testcase
                problem_report.append(-1)
            else:
                # Fetch and append status_code
                cmd = str(path+exec_out+" "+test_args[p][tc])
                start_list = shlex.split(cmd)
                start_list[0]=sys.path[0] + "/" + start_list[0]
                status_code=tc_run(start_list, test_stdin_path[p][tc], return_val[p][tc], test_stdout_sol_path[p][tc], test_fileout[p][tc])
                
                problem_report.append(status_code)
                # Parse status_code
                # bad_return = 0
                # bad_stdout = 0
                # bad_fileout = 0
                # bad_halt = 0
        
                # if status_code | 1:
                #     bad_return=1
                # if status_code | 2:
                #     bad_stdout=1
                # if status_code | 4:
                #     bad_fileout=1
                # if status_code | 8:
                #     bad_halt=1

                # Grade Deduction
                # list_of_grades[p][tc]-=bad_return*return_penalty
                # list_of_grades[p][tc]-=bad_stdout*stdout_penalty
                # list_of_grades[p][tc]-=bad_fileout*fileout_penalty
                # list_of_grades[p][tc]-=bad_halt*halt_penalty
                
                # Negative Grade Correction
                # if(list_of_grades[p][tc]<0):
                #     list_of_grades[p][tc]=0
                
                # Append into report
                # problem_report.append(list_of_grades[p][tc])

            # Conclusion append into student_report
        student_report.append(problem_report)
    return student_report

def grade():
    problem_list = prob
    for n in range(len(problem_list)):
        problem_list[n] = path+problem_list[n]

    # Checking size of lists
    if len(problem_list) > min([len(points_breakup), len(test_args), len(test_stdin_path), len(return_val), len(test_stdout_sol_path)]):
        print("Fatal Error: Length of problem list is longer than at least one of the configure lists.")
        exit()
    # Checking existence of all solution file
    for p in range(len(problem_list)):
        for tc in range(len(points_breakup[p])):
            if(test_stdin_path[p][tc]!="" and not os.path.exists(stdpath+test_stdin_path[p][tc])):
                print("Fatal Error: STDIN file \""+stdpath+test_stdin_path[p][tc]+"\" not found.")
                exit()
            if(test_stdout_sol_path[p][tc]!="" and not os.path.exists(stdpath+test_stdout_sol_path[p][tc])):
                print("Fatal Error: STDOUT solution file \""+stdpath+test_stdout_sol_path[p][tc]+"\" not found.")
                exit()
            if(len(test_fileout[p][tc])==2 and not os.path.exists(filepath+test_fileout[p][tc][0])):
                print("Fatal Error: File Output solution file \""+filepath+test_fileout[p][tc][0]+"\" not found.")
                exit()

    report = _rubric(problem_list)
    #print(report)
    return report

def altgrade(list_of_files):
    problem_list = list_of_files
    # Checking size of lists
    if len(problem_list) > min([len(points_breakup), len(test_args), len(test_stdin_path), len(return_val), len(test_stdout_sol_path)]):
        print("Fatal Error: Length of problem list is longer than at least one of the configure lists.")
        exit()
    # Checking existence of all solution file
    for p in range(len(problem_list)):
        for tc in range(len(points_breakup[p])):
            if(test_stdin_path[p][tc]!="" and not os.path.exists(stdpath+test_stdin_path[p][tc])):
                print("Fatal Error: STDIN file \""+stdpath+test_stdin_path[p][tc]+"\" not found.")
                exit()
            if(test_stdout_sol_path[p][tc]!="" and not os.path.exists(stdpath+test_stdout_sol_path[p][tc])):
                print("Fatal Error: STDOUT solution file \""+stdpath+test_stdout_sol_path[p][tc]+"\" not found.")
                exit()
            if(len(test_fileout[p][tc])==2 and not os.path.exists(filepath+test_fileout[p][tc][0])):
                print("Fatal Error: File Output solution file \""+filepath+test_fileout[p][tc][0]+"\" not found.")
                exit()

    report = _rubric(problem_list)
    #print(report)
    return report

######### TEST #########
# print("Error Test: ")
# compile("compe.c")
# print("Warning Test: ")
# compile("compw.c")
# print("Succ Test: ")
# compile("comp.c")
######### END #########
#grade()
#(tc_exec, args, stdin_path, retval, out_sol, fileout):
# print("Running in default mode: Grade the file listed in rubric.py. (For 1 student)")
# print("Student feedback:")
# print(grade())
# print("\n")
# print("Running in alternative mode: Grade the list passed to the func.")

# alt_prob = [
#     './test/good.c', # ./TestData/good.c
#     './test/warning.c', 
#     './test/error.c',
#     './test/badret.c', 
#     './test/badstdout.c',
#     './test/badfile.c',
#     './test/badhalt.c'
# ]
# print("Student feedback:")
# print(altgrade(alt_prob))
import os
import shlex, subprocess
from parse import *
from zipfile import ZipFile
# Local file import
from config import *
from grading import *

dir_list = os.listdir(path)

def _file_probing():
    f = open("report.csv", "w")
    # Assume: .c files in $path
    for n in range(len(dir_list)):
        graded_list = []
        name = parse(target, dir_list[n])
        if(name != None):
            name=name.fixed
            #print("Student: "+name[0])
            graded_list.append(name[0])
            #print(graded_list)
            #graded_list.extend([0,1,2,3])
            graded_list.extend(altgrade([path+dir_list[n]])[0])
            #print(graded_list)
            report_str= ','.join(map(str, graded_list)) 
            f.write(report_str+"\n")
    f.close()

def probing():
    if(mode=="ZIP"):
        # NOT SUPPORTED
        print("Please specify an implemented mode.")
        exit()
    elif(mode=="FILE"):
        _file_probing()
    elif(mode=="DIR"):
        # NOT SUPPORTED
        print("Please specify an implemented mode.")
        exit()
    else:
        # Default case
        print("Please specify an implemented mode.")
        exit()



# Name Probing Process
## Unzip .zip files into directories.
# if(mode=="ZIP"):
#     for n in range(len(dir_list)):
#         r = parse(target, dir_list[n])

#         with ZipFile(path+'test.zip', 'r') as zipObj:
#             # Extract all the contents of zip file in different directory
#             zipObj.extractall('temp')
# exit()
# print(dir_list) 
# for n in range(len(dir_list)):
#     r = parse(target, dir_list[n])
#     if(r!=None and r.fixed[0]=="1"):
#         print("Firstname: "+r.fixed[2].capitalize())
#         print("Lastname: "+r.fixed[1].capitalize())

probing()
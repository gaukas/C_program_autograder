# Just a rubric file

# config.path/prob[] = Actual File Path
prob = [
    'begleralex_335202_15335751_statistics.c', # ./TestData/good.c
    # 'warning.c', 
    # 'error.c',
    # 'badret.c', 
    # 'badstdout.c',
    # 'badfile.c',
    # 'badhalt.c'
]

points_breakup = [
    #[first_test, second_test, ...]
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
]

test_args = [
    # prob1.c
    [
        "-echo",
        "-echo",
        "-echo",
        "-echo",
        "-echo",
        "-echo",
        "-echo",
        "-echo",
        "-author",  # author test
        "-help"     # help test
    ]
]

# config.stdpath/test_stdin_path[] = Actual Input File Path
test_stdin_path = [
    #prob1.c
    [
        "datain1.txt", 
        "datain1.txt", 
        "datain2.txt", 
        "datain2.txt", 
        "datain3.txt", 
        "datain3.txt", 
        "datain4.txt", 
        "datain4.txt", 
        "",
        "",
    ]
]

return_val = [
    # good.c
    [
        0, # Return 0 for GOOD
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]
]

# config.stdpath/test_stdout_sol_path[] Path to expected stdout
test_stdout_sol_path = [
    # good.c
    [
        "datao1.txt", 
        "dataol1.txt", 
        "datao2.txt", 
        "dataol2.txt", 
        "datao3.txt", 
        "dataol3.txt", 
        "datao4.txt", 
        "dataol4.txt", 
        "anyout.txt",
        "help.txt",
    ]
]

# config.filepath/test_fileout[][][0] Path to expected file output
# ./test_fileout[][][1] Path to program file output
test_fileout= [
    # good.c
    [
        #["file_sol_good.txt", "file/out_good.txt"]
        [],   # Solution path, Output path
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]
]
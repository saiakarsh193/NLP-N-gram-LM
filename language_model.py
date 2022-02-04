import sys

if(len(sys.argv) == 4):
    n_count = int(sys.argv[1])
    smooth_type = int(sys.argv[2])
    path_corpus = int(sys.argv[3])
else:
    print("Invalid number of parameters")
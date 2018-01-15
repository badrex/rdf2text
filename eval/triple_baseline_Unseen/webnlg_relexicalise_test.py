import sys
import getopt
ONLINE = False
from Unseen_input import input_ONefile


def main(argv):
    usage = 'usage:\npython3 gener_relex.py -i <data-directory> -n <name> -f <prediction-file>' \
           '\ndata-directory is the directory where all preprocessing files of currently triple size are' \
 '\n name, the name of evaluation state either triple size or category name'\
            '\n prediction-file is the path to the generated file baseline_predictions.txt' 
    try:
        opts, args = getopt.getopt(argv, 'i:n:f:', ['inputdir=','name=', 'filedir='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    input_data = False
    input_filepath = False
    for opt, arg in opts:
        if opt in ('-i', '--inputdir'):
            inputdir = arg
            input_data = True
        elif opt in ('-n', '--name'):
            name = arg
            input_data = True
        elif opt in ('-f', '--filedir'):
            filepath = arg
            input_data = True
        else:
            print(usage)
            sys.exit()
    if not input_data:
        print(usage)
        sys.exit(2)
    print('Input directory is', inputdir)
    print('Path to the file is', filepath)
    input_ONefile(inputdir,name,filepath, relex=True)

if __name__ == "__main__":
    main(sys.argv[1:])

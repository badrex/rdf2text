import sys
import getopt
ONLINE = False
from webnlg_baseline_test_input import input_ONefile


def main(argv):
    usage = 'usage:\npython3 gener_relex.py -i <data-directory> -f <prediction-file>' \
           '\ndata-directory is the directory where all preprocessing files of currently triple size are' \
            '\nprediction-file is the path to the generated file baseline_predictions.txt' \
            ' (e.g. documents/baseline_predictions.txt)'
    try:
        opts, args = getopt.getopt(argv, 'i:f:', ['inputdir=', 'filedir='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    input_data = False
    input_filepath = False
    for opt, arg in opts:
        if opt in ('-i', '--inputdir'):
            inputdir = arg
            input_data = True
        elif opt in ('-f', '--filedir'):
            filepath = arg
            input_filepath = True
        else:
            print(usage)
            sys.exit()
    if not input_data or not input_filepath:
        print(usage)
        sys.exit(2)
    print('Input directory is', inputdir)
    print('Path to the file is', filepath)
# call input_files from webnlg_baseline_input  and this in here turne while call relexicalise() and it will generate file 
#'relexicalised_predictions.txt
#python3 webnlg_relexicalise.py -i <data-directory> -f <OpenNMT-directory>/baseline_predictions.txt
#all-notdelex-source.triple and dev-webnlg-all-notdelex.triple must already be in the directory
    input_ONefile(inputdir, filepath, relex=True)

if __name__ == "__main__":
    main(sys.argv[1:])

import sys
import getopt
ONLINE = False
from baseline_dev_category import input_files

# we assum here that each pred.txt in corresponding triple size file 
# and we open it within the input_files method
def main(argv):
    usage = 'usage:\npython3 webnlg_relexicalise_dev.py -i <data-directory>' \
           '\ndata-directory is the directory where dev dataset is'
    try:
        opts, args = getopt.getopt(argv, 'i:', ['inputdir='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    input_data = False
    for opt, arg in opts:
        if opt in ('-i', '--inputdir'):
            inputdir = arg
            input_data = True
        else:
            print(usage)
            sys.exit()
    if not input_data:
        print(usage)
        sys.exit(2)
    print('Input directory is ', inputdir)
    input_files(inputdir,relex=True)
    
# call input_files from webnlg_baseline_input  and this in here turn will call relexicalise() and it will generate file 
#'relexicalised_predictions.txt

    

if __name__ == "__main__":
    main(sys.argv[1:])

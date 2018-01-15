import os
import sys
import getopt

# pass max ref number as parameter ,and directory of each triple size ,modify 
# the code the write output files in current triple size folder

#maindir the directory where all folders of different tiple size are 
def get_ref_maxref(maindir):

    max_ref_list=[5,3,3,3,3]
    size=1
    for i in max_ref_list:
        tripledir='triple'+str(size)+'Unseen_Baseline/'
        print('current triple size is '+tripledir)
        prepare_files_ter(tripledir,i,size)
        size+=1
        

#inputdir path of current triple size folder
#ref_max number of reference for current triple size
#size of current triple
def prepare_files_ter(inputdir,ref_max,size):
    """
    Generate files for METEOR and TER input.
    :param inputdir: directory with bleu files
    :ref_max: the max number of references for current triple size
    : size: the size of current triple set 
    :return:
    """
    references = []  # each element is a list of references # for Ter
    pure_references = [] # for Meteor
    initialref = inputdir + 'all-notdelex-reference0.lex'
    # complete refs with references for all sents
    # take all lines from reference 0
    with open(initialref, 'r') as f:
        for i, line in enumerate(f):
            references.append([line.strip() + ' (id' + str(i) + ')\n'])
            pure_references.append([line])

    # create a file with all reference for TER
    #and write it in the folder of triple size folder
    with open(inputdir+'all-notdelex-oneref-ter.txt', 'w+') as f:
        for ref in references:
            f.write(''.join(ref))
    # get lines from all another reference files belonging to current triple size
    files = [(inputdir, filename) for filename in os.listdir(inputdir)]
    for filepath in files:
        if 'all-notdelex-reference' in filepath[1] and 'reference0' not in filepath[1]:
            with open(filepath[0]+filepath[1], 'r') as f:
                for i, line in enumerate(f):
                    if line != '\n':  #if line not empty take it 
                        references[i].append(line.strip() + ' (id' + str(i) + ')\n')
                        pure_references[i].append(line)

    with open(inputdir+'all-notdelex-refs-ter.txt', 'w+') as f:
        for ref in references:
            f.write(''.join(ref))

    # prepare generated hypotheses
    with open(inputdir+'relexicalised_predictions.txt', 'r') as f:
        geners = [line.strip() + ' (id' + str(i) + ')\n' for i, line in enumerate(f)]
    with open(inputdir+'relexicalised_predictions-ter.txt', 'w+') as f:
        f.write(''.join(geners))

    # data for meteor
    # For N references, it is assumed that the reference file will be N times the length of the test file,
    # containing sets of N references in order.
    # For example, if N=4, reference lines 1-4 will correspond to test line 1, 5-8 to line 2, etc.
    with open(inputdir+'all-notdelex-refs-meteor.txt', 'w+') as f:
        for ref in pure_references:
            empty_lines = ref_max - len(ref)  # calculate how many empty lines to add (for example 8 max references)
            f.write(''.join(ref))
            if empty_lines > 0:
                f.write('\n' * empty_lines)
    print('Input files for METEOR and TER generated successfully.')

def main(argv):
    usage = 'usage:\npython3 metrics.py -i <data-directory>' \
           '\ndata-directory is the directory where all folders of different triple size'
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
    get_ref_maxref(inputdir)

    

if __name__ == "__main__":
    main(sys.argv[1:])

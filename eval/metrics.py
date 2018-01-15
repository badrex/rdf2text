import os
import sys
import getopt

# pass max ref number as parameter ,and directory of unseen preprocess files 

def prepare_files_ter(inputdir,dataType,predFile):
    """
    Generate files for METEOR and TER input.
    :param inputdir: directory with all reference files
    :param dataType: the name of current evaluated data e.g. dev or test
    :param predFile: the directory for prediction file
    :return:
    """
    references = []  # each element is a list of references # for Ter
    pure_references = [] # for Meteor
    initialref = inputdir+dataType+'.ref1'
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
    # get lines from all another reference files belonging to current dataType
    files = [(inputdir, filename) for filename in os.listdir(inputdir)]
    refName=dataType+'.ref'
    for filepath in files:
        if refName in filepath[1] and '.ref1' not in filepath[1]:
            with open(filepath[0]+filepath[1], 'r') as f:
                for i, line in enumerate(f):
                    if line != '\n':  #if line not empty take it 
                        references[i].append(line.strip() + ' (id' + str(i) + ')\n')
                        pure_references[i].append(line)

    with open(inputdir+'all-notdelex-refs-ter.txt', 'w+') as f:
        for ref in references:
            f.write(''.join(ref))

    # prepare generated hypotheses
    # get prediction from predFile and put id to each line
    with open(predFile, 'r') as f:
        geners = [line.strip() + ' (id' + str(i) + ')\n' for i, line in enumerate(f)]
    with open(inputdir+'relexicalised_predictions-ter.txt', 'w+') as f:
        f.write(''.join(geners))

    # data for meteor
    # For N references, it is assumed that the reference file will be N times the length of the test file,
    # containing sets of N references in order.
    # For example, if N=4, reference lines 1-4 will correspond to test line 1, 5-8 to line 2, etc.
    #In our new system our max_ref is 3, so for each tested line, it will combines with 3 lines in reference file
    with open(inputdir+'all-notdelex-refs-meteor.txt', 'w+') as f:
        for ref in pure_references:
            empty_lines = 3 - len(ref)  # calculate how many empty lines to add (for example 8 max references)
            f.write(''.join(ref))
            if empty_lines > 0:
                f.write('\n' * empty_lines)
    print('Input files for METEOR and TER generated successfully.')

def main(argv):
    usage = 'usage:\npython3 metrics.py -i <data-directory> -d dataType -p predFile' \
           '\ndata-directory is where all reference filesare,directory should ends with /' \
            '\n dataType, the name of current evaluated dataset e.g. dev ' \
            '\n  predFile, the directory of predictions file '

    try:
        opts, args = getopt.getopt(argv, 'i:d:p:', ['inputdir=', '=dataType','=predFile'])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    input_data = False
    for opt, arg in opts:
        if opt in ('-i', '--inputdir'):
            inputdir = arg
            input_data = True
        elif opt in ('-d', '--dataType'):
            datatype = arg
        elif opt in ('-p', '--predFile'):
            pred=arg
        else:
            print(usage)
            sys.exit()
    if not input_data:
        print(usage)
        sys.exit(2)
    print('Input directory is', inputdir)
    print('current evaluated data type is ',datatype)
    print('The directory of predictions file is', pred)
    prepare_files_ter(inputdir,datatype,pred)

if __name__ == "__main__":
    main(sys.argv[1:])

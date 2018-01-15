import os
import sys
import getopt
import csv


def predictionFinder(filePath,fileName):
    """
    Extract predictions for input file, put them in another file i.e. outputFile
    :param filePath: the directory of the file we want to extract predictions from
    :param fileName: the name of the file we want to put extracted predictions in  
    :return
    """
    folder='ExtractedPred'
    if not os.path.exists(folder):
       os.makedirs(folder)
    outputFile=folder+'/'+fileName+'_predictions.txt'
    with open(filePath) as tsvfile,open(outputFile, 'w+') as tsvout:
        tsvReader = csv.reader(tsvfile, delimiter='\t')
        #for each row in the tsvFile get the prediction
        for row in tsvReader:
        #put extracted prediction in outputFile
             tsvout.write(row[4]+'\n')

def main(argv):
    usage = 'usage:\npython3 predFinder.py -i <file-directory> -f fileName' \
           '\nfile-directory is the directory where the file we want to extract predictions from ' \
            '\n fileName is the name of generated file with extracted predictions' 
    try:
        opts, args = getopt.getopt(argv, 'i:f:', ['inputdir=', 'output='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    input_data = False
    for opt, arg in opts:
        if opt in ('-i', '--inputdir'):
            inputdir= arg
            input_data = True
        elif opt in ('-f', '--output'):
            output=arg
            input_data = True
        else:
            print(usage)
            sys.exit()
    if not input_data:
        print(usage)
        sys.exit(2)
    print('Input directory is', inputdir)
    print('Output file name is', output)
    predictionFinder(inputdir,output)

if __name__ == "__main__":
    main(sys.argv[1:])


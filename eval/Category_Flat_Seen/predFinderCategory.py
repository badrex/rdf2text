import os
import sys
import getopt
import csv


def predictionFinder(filePath,category):
    """
    Extract predictions from general predections file, that corresponding to current category
    :param filePath: the directory of the file we want to extract predictions from
    :param category: the name of current category we want to get its predictions
    :return
    """

    if not os.path.exists(category):
       os.makedirs(category)
    #get all references from general reference files, store them in list of tuple(line number,line) separetly
    with open('../ref/dev.ref1', 'r') as f1:
        refin1= [(i,line) for i, line in enumerate(f1)]
    with open('../ref/dev.ref2', 'r') as f2:
        refin2 = [(i,line) for i, line in enumerate(f2)]
    with open('../ref/dev.ref3', 'r') as f3:
        refin3 = [(i,line) for i, line in enumerate(f3)]
    #create files for extracted predictions&references for current category
    outputFile=category+'/'+category+'_predictions.txt'
    refout1=category+'/'+category+'.ref1'
    refout2=category+'/'+category+'.ref2'
    refout3=category+'/'+category+'.ref3'
    with open(filePath) as tsvfile,open(outputFile, 'w+') as tsvout,open(refout1, 'w+') as ref1,open(refout2, 'w+') as ref2,open(refout3, 'w+') as ref3:
        tsvReader = csv.reader(tsvfile, delimiter='\t')
        #for each row in the tsvFile get the prediction for current category
        for row in tsvReader:
            if row[2]==category:
        #put extracted prediction in outputFile
                tsvout.write(row[4]+'\n')
                 #get the id(number)of current row minus one becuase it start with 1 not 0
                currentId=int(row[0])-1
                 #search in each reference file for corresponding line for this id
                for item in refin1:
                    if item[0]==currentId:
                        ref1.write(item[1])
                for item in refin2:
                    if item[0]==currentId:
                        ref2.write(item[1])
                for item in refin3:
                    if item[0]==currentId:
                        ref3.write(item[1])


def main(argv):
    usage = 'usage:\npython3 predFinderTriple.py -i <file-directory> -f categoryName' \
           '\nfile-directory is the directory where the file we want to extract predictions from ' \
            '\n categoryName, the name of current category we want to evaluate' 
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
    print('The current category name is', output)
    predictionFinder(inputdir,output)

if __name__ == "__main__":
    main(sys.argv[1:])


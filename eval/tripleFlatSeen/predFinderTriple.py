import os
import sys
import getopt
import csv


def predictionFinder(filePath,size):
    """
    Extract predictions from input file, which corresponding to passed triple size
    :param filePath: the directory of the file we want to extract predictions from
    :param size: the size of triple we want to get its predictions
    :return
    """
    tripleSize='triple'+size
    if not os.path.exists(tripleSize):
       os.makedirs(tripleSize)
    #get all references from general reference files, store them in list of tuple(line number,line)
    with open('../ref/dev.ref1', 'r') as f1:
        refin1= [(i,line) for i, line in enumerate(f1)]
    with open('../ref/dev.ref2', 'r') as f2:
        refin2 = [(i,line) for i, line in enumerate(f2)]
    with open('../ref/dev.ref3', 'r') as f3:
        refin3 = [(i,line) for i, line in enumerate(f3)]
    #create files for extracted predictions&references for current triple size
    outputFile=tripleSize+'/'+tripleSize+'_predictions.txt'
    refout1=tripleSize+'/'+tripleSize+'.ref1'
    refout2=tripleSize+'/'+tripleSize+'.ref2'
    refout3=tripleSize+'/'+tripleSize+'.ref3'
    with open(filePath) as tsvfile,open(outputFile, 'w+') as tsvout,open(refout1, 'w+') as ref1,open(refout2, 'w+') as ref2,open(refout3, 'w+') as ref3:
        tsvReader = csv.reader(tsvfile, delimiter='\t')
        #for each row in the tsvFile get the prediction for current triple size
        for row in tsvReader:
            if row[1]==size:
        #put extracted prediction in outputFile
                tsvout.write(row[4]+'\n')
                 #get the id(number)of current row minus one becuase it start with 1 not 0
                currentId=int(row[0])-1
                #print("id is "+str(currentId))
                 #search in each reference file for corresponding line for this id
                for item in refin1:
                    if item[0]==currentId:
                        #print("reference row id is"+str(item[0]))
                        ref1.write(item[1])
                for item in refin2:
                    if item[0]==currentId:
                        ref2.write(item[1])
                for item in refin3:
                    if item[0]==currentId:
                        ref3.write(item[1])

def main(argv):
    usage = 'usage:\npython3 predFinderTriple.py -i <file-directory> -f size' \
           '\nfile-directory is the directory where the file we want to extract predictions from ' \
            '\n size, the size of triple' 
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
    print('The cuurent size of triple is', output)
    predictionFinder(inputdir,output)

if __name__ == "__main__":
    main(sys.argv[1:])


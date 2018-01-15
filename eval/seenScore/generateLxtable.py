import sys
import getopt
import re
import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat
from pylatex.utils import *
from pylatex.utils import italic
import os

####Note####
# This script depends on pylatex, you can install it by writing in the terminal
#pip install pylatex 
#############

#this function get 2 digits after the decimal point
def get2decimal(fValue):
    dec="{:0.2f}".format(float(fValue))
    return dec

def searchScores(filepath=None):
    """
    This function take score file as input, search for Bleu, Meteor, Ter scores and 
    return them as list
    :param filepath: the directory of the score file
    return
    """
    #list to put all scores in it (blue ,meteor ,ter)
    scores=[]
    # the key words we want to search for in our score file 
    regexpBleu = re.compile(r'BLEU.*?([0-9.-]+)')
    regexpMeteor = re.compile(r'Final score:.*?([0-9.-]+)')
    regexpTer = re.compile(r'Total TER:.*?([0-9.-]+)')
 
    with open(filepath) as f:
        for line in f:
            #search for Bleu score        
            searchBlue = regexpBleu.search(line)
            if searchBlue:
                bleu=get2decimal(searchBlue.group(1))
                scores.append(bleu)
                #print("BLeu score "+get2decimal(dec))
            #search for Meteor score            
            searchMeteor = regexpMeteor.search(line)
            if searchMeteor:
                meteor=get2decimal(searchMeteor.group(1))
                scores.append(meteor)
                #print("Meteor score "+get2decimal(dec))
            #search for Ter score        
            searchTer = regexpTer.search(line)
            if searchTer:
                ter=get2decimal(searchTer.group(1))
                scores.append(ter)
                #print("Ter score is "+get2decimal(dec)) 
    return scores


def generateTex(filepath=None):
    #read all score files for seen and store them in lists 
   #scores ordered in list as: BLEU METEOR TER
    mdBaseLine=searchScores('baselineSeen-Score.txt')
    flat=searchScores('flatseen-score.txt')
    str1=searchScores('str1seen-score.txt')
    str2=searchScores('str2seen-score.txt')

    geometry_options = {"tmargin": "1cm", "lmargin": "5cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('The evaluation scores for Seen set')):
        doc.append(italic('========================================\n'))
        doc.append(italic('We mean by system the extended system which contain 3 model: flat,str1,str2\n'))
        doc.append(italic('baseline the basic baseline of webnlg challeng \n'))
        doc.append(italic('modify baseline the modified baseline of webnlg challeng \n'))

        with doc.create(Subsection('Table of Evaluation in term of BLEU \n')):
            with doc.create(Tabular('|r|c|')) as table:
                table.add_hline()
                table.add_row((bold("System"),bold("Bleu")))
                table.add_hline()
                #table.add_row(("system",ScoreList[0], bold(ScoreList[1]),ScoreList[2]))
                #table.add_empty_row()
                table.add_row(("baseline","54.03"))
                table.add_hline()
                table.add_row(("Modify baseline",mdBaseLine[0]))
                table.add_hline()
                table.add_row(("Flat",bold(flat[0])))
                table.add_hline()
                table.add_row(("Structure1",str1[0]))
                table.add_hline()
                table.add_row(("Structure2",str2[0]))
                table.add_hline()
        with doc.create(Subsection('Table of Evaluation in term of METEOR \n')):
            with doc.create(Tabular('|r|c|')) as table:
                table.add_hline()
                table.add_row((bold("System"),bold("METEOR")))
                table.add_hline()
                #table.add_row(("system",ScoreList[0], bold(ScoreList[1]),ScoreList[2]))
                #table.add_empty_row()
                table.add_row(("baseline","0.39"))
                table.add_hline()
                table.add_row(("Modify baseline",mdBaseLine[1]))
                table.add_hline()
                table.add_row(("Flat",bold(flat[1])))
                table.add_hline()
                table.add_row(("Structure1",str1[1]))
                table.add_hline()
                table.add_row(("Structure2",str2[1]))
                table.add_hline()
        with doc.create(Subsection('Table of Evaluation in term of TER \n')):
            with doc.create(Tabular('|r|c|')) as table:
                table.add_hline()
                table.add_row((bold("System"),bold("TER")))
                table.add_hline()
                #table.add_row(("system",ScoreList[0], bold(ScoreList[1]),ScoreList[2]))
                #table.add_empty_row()
                table.add_row(("baseline","0.40"))
                table.add_hline()
                table.add_row(("Modify baseline",mdBaseLine[2]))
                table.add_hline()
                table.add_row(("Flat",bold(flat[2])))
                table.add_hline()
                table.add_row(("Structure1",str1[2]))
                table.add_hline()
                table.add_row(("Structure2",str2[2]))
                table.add_hline()
               # table.add_row(("baseline","06.13","0.07","0.80"))
    doc.generate_pdf('SeenSetEvaluation ', clean_tex=False)


def main(argv):
  """  usage = 'usage:\npython3 generateLxtable.py -i <score file directory>' \
           '\n score file directory where your text file of evaluation score is '
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
    print('Input directory for evaluation file is  ', inputdir)"""
generateTex()


if __name__ == "__main__":
    main(sys.argv[1:])

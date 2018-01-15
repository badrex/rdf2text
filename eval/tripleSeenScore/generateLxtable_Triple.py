import sys
import getopt
import re
import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat,MultiColumn,MultiRow
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
    This function take score file name as input, search for Bleu, Meteor, Ter scores and 
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
    #read all score files for different triple size and store them in lists 
   #scores ordered in list as: BLEU METEOR TER
# get triple1 score
    mdBaseTripl1=searchScores('baseTriple1_score.txt')
    flatTripl1=searchScores('flattriple1_score.txt')
# get triple2 score
    mdBaseTripl2=searchScores('baseTriple2_score.txt')
    flatTripl2=searchScores('flattriple2_score.txt')
# get triple3 score
    mdBaseTripl3=searchScores('baseTriple3_score.txt')
    flatTripl3=searchScores('flattriple3_score.txt')
# get triple4 score
    mdBaseTripl4=searchScores('baseTriple4_score.txt')
    flatTripl4=searchScores('flattriple4_score.txt')
# get triple5 score
    mdBaseTripl5=searchScores('baseTriple5_score.txt')
    flatTripl5=searchScores('flattriple5_score.txt')
# get triple6 score
    mdBaseTripl6=searchScores('baseTriple6_score.txt')
    flatTripl6=searchScores('flattriple6_score.txt')
# get triple7 score
    mdBaseTripl7=searchScores('baseTriple7_score.txt')
    flatTripl7=searchScores('flattriple7_score.txt')
  

    geometry_options = {"tmargin": "1cm", "lmargin": "5cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('The evaluation scores for different triple size of Seen dataset')):
        doc.append(italic('========================================\n'))
        doc.append(italic('We mean by flat one model from the extended system which contains 3 model:flat,str1,str2\n'))
        doc.append(italic('Where we evaluate just this model in term of different triple size, because the result of other models i.e. str1&str2 for the dataset seen and unseen not very good comparing by this model\n'))
        doc.append(italic('We mean by "Modify baseline" the modified baseline of webnlg challeng \n'))

        with doc.create(Subsection('Table of Evaluation in term of BLEU \n')):
            with doc.create(Tabular('|c|c|c|')) as table:
                table.add_hline()
                table.add_row(bold("Triple size"),bold("Model"),bold("Bleu"))
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 1'), "Modify Baseline",mdBaseTripl1[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl1[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 2'), "Modify Baseline",mdBaseTripl2[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl2[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 3'), "Modify Baseline",mdBaseTripl3[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl3[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 4'), "Modify Baseline",mdBaseTripl4[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl4[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 5'), "Modify Baseline",mdBaseTripl5[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl5[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 6'), "Modify Baseline",mdBaseTripl6[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl6[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 7'), "Modify Baseline",mdBaseTripl7[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl7[0])))
                table.add_hline()
# Generate METEOR score table
        with doc.create(Subsection('Table of Evaluation in term of METEOR \n')):
            with doc.create(Tabular('|c|c|c|')) as table:
                table.add_hline()
                table.add_row(bold("Triple size"),bold("Model"),bold("METEOR"))
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 1'), "Modify Baseline",mdBaseTripl1[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl1[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 2'), "Modify Baseline",mdBaseTripl2[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl2[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 3'), "Modify Baseline",mdBaseTripl3[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl3[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 4'), "Modify Baseline",mdBaseTripl4[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl4[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 5'), "Modify Baseline",mdBaseTripl5[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl5[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 6'), "Modify Baseline",mdBaseTripl6[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl6[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 7'), "Modify Baseline",mdBaseTripl7[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl7[1])))
                table.add_hline()
# Generate TER score table
        with doc.create(Subsection('Table of Evaluation in term of TER \n')):
            with doc.create(Tabular('|c|c|c|')) as table:
                table.add_hline()
                table.add_row(bold("Triple size"),bold("Model"),bold("TER"))
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 1'), "Modify Baseline",mdBaseTripl1[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl1[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 2'), "Modify Baseline",mdBaseTripl2[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl2[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 3'), "Modify Baseline",mdBaseTripl3[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl3[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 4'), "Modify Baseline",mdBaseTripl4[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl4[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 5'), "Modify Baseline",mdBaseTripl5[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl5[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 6'), "Modify Baseline",mdBaseTripl6[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl6[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Triple 7'), "Modify Baseline",mdBaseTripl7[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatTripl7[2])))
                table.add_hline()
    doc.generate_pdf('TripleSize_SeenSetEvaluation ', clean_tex=False)
    #doc.generate_tex('TripleSize_SeenSetEvaluation')#Generate a .tex file for the document.


def main(argv):
    generateTex()


if __name__ == "__main__":
    main(sys.argv[1:])

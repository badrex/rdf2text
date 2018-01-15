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
# get Astronaut score
    mdBase_Athlete=searchScores('Athlete_score.txt')
    flat_Athlete=searchScores('flat_Athlete_score.txt')
# get City score
    mdBase_Artist=searchScores('Artist_score.txt')
    flat_Artist=searchScores('flat_Artist_score.txt')
# get Food score
    mdBase_Politician=searchScores('Politician_score.txt')
    flat_Politician=searchScores('flat_Politician_score.txt')


  

    geometry_options = {"tmargin": "1cm", "lmargin": "5cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('The evaluation scores for different DBpedia categories of Unseen dataset:')):
        doc.append(italic('=============================================\n'))
        doc.append('Comparing the evaluation scores between two model: (flat, modify baseline) according to different DBpedia categories, which are:Athlete,Artist,Politician \n')
        doc.append(italic('We mean by "flat" one model from the extended system which contains 3 model:flat,str1,str2\n'))
        doc.append(italic('Where we evaluate just this model in term of different DBpedia categories, because the result of other models i.e. str1&str2 for the whole dataset unseen and unseen not very good comparing by this model\n'))
        doc.append(italic('We mean by "Modify baseline" the modified baseline of webnlg challeng \n'))

        with doc.create(Subsection('Table of Evaluation in term of BLEU \n')):
            with doc.create(Tabular('|c|c|c|')) as table:
                table.add_hline()
                table.add_row(bold("Category Name"),bold("Model"),bold("BLEU"))
                table.add_hline()
                table.add_row((MultiRow(3, data='Athlete'), "Modify Baseline",mdBase_Athlete[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flat_Athlete[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Artist'), "Modify Baseline",mdBase_Artist[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flat_Artist[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Politician'), "Modify Baseline",mdBase_Politician[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flat_Politician[0])))
                table.add_hline()
                table.add_hline()
           
         
# Generate METEOR score table
        with doc.create(Subsection('Table of Evaluation in term of METEOR \n')):
            with doc.create(Tabular('|c|c|c|')) as table:
                table.add_hline()
                table.add_row(bold("Category Name"),bold("Model"),bold("METEOR"))
                table.add_hline()
                table.add_row((MultiRow(3, data='Athlete'), "Modify Baseline",mdBase_Athlete[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flat_Athlete[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Artist'), "Modify Baseline",mdBase_Artist[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flat_Artist[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Politician'), "Modify Baseline",mdBase_Politician[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flat_Politician[1])))
                table.add_hline()
                table.add_hline()
# Generate TER score table
        with doc.create(Subsection('Table of Evaluation in term of TER \n')):
            with doc.create(Tabular('|c|c|c|')) as table:
                table.add_hline()
                table.add_row(bold("Category Name"),bold("Model"),bold("TER"))
                table.add_hline()
                table.add_row((MultiRow(3, data='Athlete'), "Modify Baseline",mdBase_Athlete[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flat_Athlete[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Artist'), "Modify Baseline",mdBase_Artist[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flat_Artist[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Politician'), "Modify Baseline",mdBase_Politician[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flat_Politician[2])))
                table.add_hline()
                table.add_hline()
    doc.generate_pdf('Category_Unseen_Evaluation ', clean_tex=False)
    #doc.generate_tex('Category_Unseen_Evaluation')#Generate a .tex file for the document.


def main(argv):
    generateTex()


if __name__ == "__main__":
    main(sys.argv[1:])

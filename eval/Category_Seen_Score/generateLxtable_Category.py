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
    mdBaseAstronaut=searchScores('baseAstronaut_score.txt')
    flatAstronaut=searchScores('flatAstronaut_score.txt')
# get City score
    mdBaseCity=searchScores('baseCity_score.txt')
    flatCity=searchScores('flatCity_score.txt')
# get Food score
    mdBaseFood=searchScores('baseFood_score.txt')
    flatFood=searchScores('flatFood_score.txt')
# get SportTeam score
    mdBaseSportTeam=searchScores('baseSportsTeam_score.txt')
    flatSportTeam=searchScores('flatSportsTeam_score.txt')
# get University score
    mdBaseUniversity=searchScores('baseUniversity_score.txt')
    flatUniversity=searchScores('flatUniversity_score.txt')

  

    geometry_options = {"tmargin": "1cm", "lmargin": "5cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('The evaluation scores for different DBpedia categories of Seen dataset:')):
        doc.append(italic('=============================================\n'))
        doc.append('Comparing the evaluation scores between two model: (flat, modify baseline) according to different DBpedia categories, which are: Astronaut,City,University,Food,SportsTeam.\n')
        doc.append(italic('We mean by "flat" one model from the extended system which contains 3 model:flat,str1,str2\n'))
        doc.append(italic('Where we evaluate just this model in term of different DBpedia categories, because the result of other models i.e. str1&str2 for the whole dataset seen and unseen not very good comparing by this model\n'))
        doc.append(italic('We mean by "Modify baseline" the modified baseline of webnlg challeng \n'))

        with doc.create(Subsection('Table of Evaluation in term of BLEU \n')):
            with doc.create(Tabular('|c|c|c|')) as table:
                table.add_hline()
                table.add_row(bold("Category Name"),bold("Model"),bold("BLEU"))
                table.add_hline()
                table.add_row((MultiRow(3, data='Astronaut'), "Modify Baseline",mdBaseAstronaut[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatAstronaut[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='City'), "Modify Baseline",mdBaseCity[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatCity[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Food'), "Modify Baseline",mdBaseFood[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatFood[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='SportTeam'), "Modify Baseline",mdBaseSportTeam[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatSportTeam[0])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='University'), "Modify Baseline",mdBaseUniversity[0]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatUniversity[0])))
                table.add_hline()
         
# Generate METEOR score table
        with doc.create(Subsection('Table of Evaluation in term of METEOR \n')):
            with doc.create(Tabular('|c|c|c|')) as table:
                table.add_hline()
                table.add_row(bold("Category Name"),bold("Model"),bold("METEOR"))
                table.add_hline()
                table.add_row((MultiRow(3, data='Astronaut'), "Modify Baseline",mdBaseAstronaut[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatAstronaut[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='City'), "Modify Baseline",mdBaseCity[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatCity[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Food'), "Modify Baseline",mdBaseFood[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatFood[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='SportTeam'), "Modify Baseline",mdBaseSportTeam[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatSportTeam[1])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='University'), "Modify Baseline",mdBaseUniversity[1]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatUniversity[1])))
                table.add_hline()
# Generate TER score table
        with doc.create(Subsection('Table of Evaluation in term of TER \n')):
            with doc.create(Tabular('|c|c|c|')) as table:
                table.add_hline()
                table.add_row(bold("Category Name"),bold("Model"),bold("TER"))
                table.add_hline()
                table.add_row((MultiRow(3, data='Astronaut'), "Modify Baseline",mdBaseAstronaut[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatAstronaut[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='City'), "Modify Baseline",mdBaseCity[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatCity[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='Food'), "Modify Baseline",mdBaseFood[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatFood[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='SportTeam'), "Modify Baseline",mdBaseSportTeam[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatSportTeam[2])))
                table.add_hline()
                table.add_hline()
                table.add_row((MultiRow(3, data='University'), "Modify Baseline",mdBaseUniversity[2]))
                table.add_hline(2, 3)
                table.add_row(('',"Flat",bold(flatUniversity[2])))
                table.add_hline()
    doc.generate_pdf('Category_SeenSetEvaluation ', clean_tex=False)
    #doc.generate_tex('Category_SeenSetEvaluation')#Generate a .tex file for the document.


def main(argv):
    generateTex()


if __name__ == "__main__":
    main(sys.argv[1:])

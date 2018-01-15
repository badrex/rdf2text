
# 1- separate unseen.xml according to triple size
## where in unseen dataset there are triple from size 1 to 5 
# runing this script give us the set of triple for each size in xml file
 python3 separateTripleSize.py -i unseen_lex.xml -s 1
 python3 separateTripleSize.py -i unseen_lex.xml -s 2
 python3 separateTripleSize.py -i unseen_lex.xml -s 3
 python3 separateTripleSize.py -i unseen_lex.xml -s 4
 python3 separateTripleSize.py -i unseen_lex.xml -s 5

where
# -i the path of the whole unseen dataset file
# -s the current size of triple we want to separate according to

## 2- preprocess unseen dataset according to different triple size:
# runing this script will create seperate folder folder for each tiple size, inside of it the preprocessing files and references

python3 Unseen_input.py -i unseenTriple1.xml -n triple1

python3 Unseen_input.py -i unseenTriple2.xml -n triple2

python3 Unseen_input.py -i unseenTriple3.xml -n triple3

python3 Unseen_input.py -i unseenTriple4.xml -n triple4

python3 Unseen_input.py -i unseenTriple5.xml -n triple5

where
# -i  is the directory where is current triple size data

# -n name, the name of evaluation state either triple size or category name


## 3-Translate:
 put the script translate_all_triple.sh in OpenNMT folder, to get in each triple size folder its corresponding baseline_pred.txt
#in OpemNMT we run the next command
$ ./translate_all_triple.sh


# 4- Relexicalisation: we come back to triple_baseline_Unseen folder
we run the script (relex_triple_unseen.sh) to do relexicalisation on all prediction for all triple size, by usnig the script(webnlg_relexicalise_test.py)
python3 webnlg_relexicalise_test.py -i <data-directory> -n <name> -f <directory>
Example:
python3 webnlg_relexicalise_test.py -i unseenTriple1.xml -n triple1  -f triple1Unseen_Baseline/baseline_pred.txt


# 5- Prepare files for Meteor & Ter

python3 metrics.py -i  <data-directory>
data-directory is the directory where all files of different triple size, in our case it's the main directory.
When we run this script we got all files for Meteor, Ter evaluation in the folder of each triple size .

python3 metrics.py -i ./

# 6-Execute automatic evaluation :
In each triple size directory we put the script (evaluat_metrics_tripleN.sh) with multi-bleu.prel,where N the size of current triple, i.e. N take value from 1 to 5 sequentially.
Then we run it, to get the evaluation score file of each triple size, in the
seperate folder (triple_unseenScore)
# in triple1Unseen_Baseline
./evaluat_metrics_triple1.sh > ../../triple_unseenScore/baseTriple1_score.txt
# in triple2Unseen_Baseline
./evaluat_metrics_triple2.sh > ../../triple_unseenScore/baseTriple2_score.txt
# in triple3Unseen_Baseline
./evaluat_metrics_triple3.sh > ../../triple_unseenScore/baseTriple3_score.txt
# in triple4Unseen_Baseline
./evaluat_metrics_triple4.sh > ../../triple_unseenScore/baseTriple4_score.txt
# in triple5Unseen_Baseline
./evaluat_metrics_triple5.sh > ../../triple_unseenScore/baseTriple5_score.txt

#===============================================

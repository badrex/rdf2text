## In this folder we prepare seen dataset of modified baseline, to evaluate according to input data of various length (i.e. different triple size)


## we put the folder that contians(dav dataset) in tripleBaselineSeen folder ,which contains the following scripts (metrics_dev.py,spreate_Seen.py,webnlg_baseline_dev_input.py,webnlg_relexicalise_dev.py)

## Also, surly we suppose that, meteor-1.5, tercom-0.7,OpenNMT folders are in the same directory with tripleBaselineSeen

#1-webnlg_baseline_dev_input.py :
preprocess each triple size and create new folder for its preprocessing files .

python3 webnlg_baseline_dev_input.py -i dev

#2-Translate:
 put the script translate_all_triple.sh in OpenNMT folder
 Run the script translate_all_triple.sh to get in each triple size folder its corresponding baseline_predictions.txt .
#in OpemNMT we run the next command
$ ./translate_all_triple.sh


#3- Relexicalisation
# We return to tripleBaselineSeen folder, and we run webnlg_relexicalise_dev.py, to do relexicalisation.
python3 webnlg_relexicalise_dev.py -i <data-directory>
'data-directory' is the directory where dev set is .

python3 webnlg_relexicalise_dev.py -i dev


#4- Prepare files for Meteor & Ter

python3 metrics_dev.py -i  <data-directory>
data-directory is the directory where all folders of different triple size
When we run this script we got all files for Meteor, Ter evaluation in the corresponding triple size folder.
# in our case all folders for different triple size in the same directory of script metrics_dev.py
python3 metrics_dev.py -i ./


#5-Execute automatic evaluation :
In each triple size directory we put the script (evaluat_metrics_tripleN.sh) with multi-bleu.prel,where N the size of current triple, i.e. N take value from 1 to 7 sequentially.
Then we run it, to get the evaluation score file of each triple size, in the
seperate folder (tripleSeenScore)
# in dev_triple1
./evaluat_metrics_triple1.sh > ../../tripleSeenScore/baseTriple1_score.txt
# in dev_triple2
./evaluat_metrics_triple2.sh > ../../tripleSeenScore/baseTriple2_score.txt
# in dev_triple3
./evaluat_metrics_triple3.sh > ../../tripleSeenScore/baseTriple3_score.txt
# in dev_triple4
./evaluat_metrics_triple4.sh > ../../tripleSeenScore/baseTriple4_score.txt
# in dev_triple5
./evaluat_metrics_triple5.sh > ../../tripleSeenScore/baseTriple5_score.txt
# in dev_triple6
./evaluat_metrics_triple6.sh > ../../tripleSeenScore/baseTriple6_score.txt
# in dev_triple7
./evaluat_metrics_triple7.sh > ../../tripleSeenScore/baseTriple7_score.txt
#===============================================








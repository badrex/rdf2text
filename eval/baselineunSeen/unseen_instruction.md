## In this folder, we prepare the wholde UnSeen dataset of modified baseline for evaluation, where the evaluation score after executing the script (metrics_test.sh) we find it in the folder (unseenScore) with the score of unseen dataset from other other models.

# All the output files from all the following scripts will be in the folder (unseen_baseline) inside the current folder baselineunSeen
#1- preprocess unseen test data 
python3 webnlg_baseline_test_input.py -i unseen_lex.xml

#2- Translate :in the folder OpenNMT-py-master, we execute this script

python3 translate.py -model baseline-model_acc_69.57_ppl_3.56_e13.pt -src   ../baselineunSeen/unseen_baseline/unseen_all-delex.triple -output  ../baselineunSeen/unseen_baseline/baseline_pred.txt

#3- Relexicalisation: come back to baselineunseen folder

python3 webnlg_relexicalise_test.py -i <data-directory> -f <directory>/baseline_predictions.txt
Example:
python3 webnlg_relexicalise_test.py -i unseen_lex.xml  -f unseen_baseline/baseline_pred.txt


#4- Prepare files for Meteor & Ter

python3 metrics_test.py -i  <data-directory>
data-directory is the directory where all files of unseen test 
When we run this script we got all files for Meteor, Ter evaluation in the directory of unseen set directory .
Example
python3 metrics_test.py -i unseen_baseline/


#5-Execute automatic evaluation :
In unseen_baseline directory we put the script evaluat_metrics_test.sh,
Then we run it to get the evaluation score of each automatic metrics.

./evaluat_metrics_test.sh  > ../unseenScore/baselineUnseen-score.txt 

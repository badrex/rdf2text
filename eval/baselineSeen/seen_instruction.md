## In this folder, we prepare the wholde Seen (dev) dataset of modified baseline, for evaluation, where the evaluation score after executing the script (seen_evaluat_metrics.sh) we find it in the folder (seenScore) with the score of seen dataset from other other models.
 
#1- preprocess seen test data 

python3 webnlg_baseline_input.py -i challenge_data_train_dev/

#2- Translate :in the folder OpenNMT-py-master, we execute this script

$ python3 translate.py -model baseline-model_acc_69.57_ppl_3.56_e13.pt -src ../baselineSeen/dev-webnlg-all-delex.triple -output ../baselineSeen/baseline_pred.txt


#3- Relexicalisation

python3 webnlg_relexicalise.py -i <data-directory> -f <directory/baseline_predictions.txt>
Example:
python3 webnlg_relexicalise.py -i challenge_data_train_dev/  -f baseline_pred.txt


#4- Prepare files for Meteor & Ter

python3 metrics.py -i  <data-directory>
data-directory is the directory where all files of seen (dev) test are
When we run this script, we will got all files for Meteor, Ter, in the directory of baseline.
Example
python3 metrics.py -i challenge_data_train_dev/


#5-Execute automatic evaluation :
In seen_baseline directory we put the script seen_evaluat_metrics.sh with multi-bleu.prel,
Then we run it to get the evaluation score of each automatic metrics.

./seen_evaluat_metrics.sh > ../seenScore/baselineSeen-Score.txt

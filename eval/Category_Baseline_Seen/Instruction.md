##############################################################

# Input data with different category name (Modified-baseline model)
# This folder prepare seen dataset of the model Modified-baseline to be evaluated according to  different DBPedia category name, where we choose five categories from seen dataset, which are: Astronaut,City,University,Food,SportsTeam

## Also, we put all the folders: baseline, meteor-1.5, tercom-0.7,OpenNMT in the same directory with (Category_Baseline_Seen) 


#1- preprocess dev(Seen) dataset for different DBPedia categories:

 python3 baseline_dev_category.py -i <data-directory>
   data-directory is the directory where is dev dataset
# When we run the script (baseline_dev_category.py) a folder for each choosen  DBPedia category will be generated,inside of it the reference and preprocessing files.
   python3 baseline_dev_category.py -i dev

# Translate: do translate for each category in the OpenNMT folder
python3 translate.py -model baseline-model_acc_69.57_ppl_3.56_e13.pt -src ../Category_Baseline_Seen/dev_Astronaut/dev-triple-all-delex.triple -output ../Category_Baseline_Seen/dev_Astronaut/baseline_pred.txt

python3 translate.py -model baseline-model_acc_69.57_ppl_3.56_e13.pt -src ../Category_Baseline_Seen/dev_City/dev-triple-all-delex.triple -output ../Category_Baseline_Seen/dev_City/baseline_pred.txt

python3 translate.py -model baseline-model_acc_69.57_ppl_3.56_e13.pt -src ../Category_Baseline_Seen/dev_Food/dev-triple-all-delex.triple -output ../Category_Baseline_Seen/dev_Food/baseline_pred.txt

python3 translate.py -model baseline-model_acc_69.57_ppl_3.56_e13.pt -src ../Category_Baseline_Seen/dev_SportsTeam/dev-triple-all-delex.triple -output ../Category_Baseline_Seen/dev_SportsTeam/baseline_pred.txt

python3 translate.py -model baseline-model_acc_69.57_ppl_3.56_e13.pt -src ../Category_Baseline_Seen/dev_University/dev-triple-all-delex.triple -output ../Category_Baseline_Seen/dev_University/baseline_pred.txt

#3- Relexicalisation: we return to the directory (Category_Baseline_Seen)
# and we generate relex-predictions for every selected category,by the command
 python3 webnlg_relexicalise_Category.py -i <data-directory> 
 data-directory is the directory where is dev dataset
# Example
 python3 webnlg_relexicalise_Category.py -i dev
Where the corresponding prediction file wil be located in each category folder

#4- Prepare files for Meteor & Ter for every choosen category
$ python3 metrics_category.py -i <data-directory>
data-directory is the directory where all folders of different choosen category
When we run this script we got all files for Meteor, Ter evaluation in every category directory .
(in our case all category folder in the same directory with metrics_category.py)
Example:$ python3 metrics_category.py -i ./ 

#5-Execute automatic evaluation :
In each category directory we put the script evaluat_metrics_categoryName.sh ,where categoryName the name of current category.
Then we run it to get the evaluation score of each automatic metrics, where all scores we find them in the folder Category_Seen_Score

## in Astronaut folder
./evaluat_metrics_Astronaut.sh > ../../Category_Seen_Score/baseAstronaut_score.txt
## in SportTeam
./evaluat_metrics_SportsTeam.sh  > ../../Category_Seen_Score/baseSportsTeam_score.txt
## in Food 
 ./evaluat_metrics_Food.sh  > ../../Category_Seen_Score/baseFood_score.txt
## in City folder
 ./evaluat_metrics_City.sh  > ../../Category_Seen_Score/baseCity_score.txt
## in University
./evaluat_metrics_University.sh  > ../../Category_Seen_Score/baseUniversity_score.txt
#===============================================









## 1- separate unseen.xml according to category name
# There are 5 unseen categories (Athlete, Artist, MeanOfTransportation, CelestialBody, Politician), we will do the evaluation on Athlete, Artist, Politician.

 python3 separateCategory.py -i unseen_lex.xml -c Athlete

 python3 separateCategory.py -i unseen_lex.xml -c Artist

 python3 separateCategory.py -i unseen_lex.xml -c Politician

# -i the path of the whole unseen dataset file
# -c the current name of category we want to separate according to


## 2- preprocess unseen dataset according to different triple size:
# runing this script will create seperate folder folder for each tiple size, inside of it the preprocessing files and references

# commands as follow ,or run the script (preprocessingRUN.sh)
python3 Unseen_input.py -i unseenAthlete.xml -n Athlete

python3 Unseen_input.py -i unseenArtist.xml -n Artist

python3 Unseen_input.py -i unseenPolitician.xml -n Politician


where
# -i  is the directory where is current category data

# -n name, the name of evaluation state either triple size or category name


## 3-Translate:
 put the script translate_all_triple.sh in OpenNMT folder, to get in each triple size folder its corresponding baseline_pred.txt
#in OpemNMT we run the next command
$ ./translate_all_triple.sh



## 4- Relexicalisation: we come back to Category_Baseline_unseen folder
we run the script (relex_category_unseen.sh) to do relexicalisation on all prediction for all choosen categories, by usnig the script(webnlg_relexicalise_test.py)
python3 webnlg_relexicalise_test.py -i <data-directory> -n <name> -f <directory>
Example:
python3 webnlg_relexicalise_test.py -i unseenAthlete.xml -n Athlete  -f AthleteUnseen_Baseline/baseline_pred.txt

## 5- Prepare files for Meteor & Ter

python3 metrics.py -i  <data-directory>
data-directory is the directory where all files of different categories, in our case it's the main directory.
When we run this script we got all files for Meteor, Ter evaluation in the folder of each category.

python3 metrics.py -i ./

## 6-Execute automatic evaluation :
In each category directory we put the script (evaluat_metrics_categoryN.sh) with multi-bleu.prel,where N the name of current category, i.e. N=(Athlete,Artist,Politician) sequentially.
Then we run it, to get the evaluation score file of each category, in the
seperate folder (Category_unseen_Score)
# in AthleteUnseen_Baseline
./evaluat_metrics_Athlete.sh > ../../Category_unseen_Score/Athlete_score.txt
# in ArtistUnseen_Baseline
./evaluat_metrics_Artist.sh > ../../Category_unseen_Score/Artist_score.txt
# in PoliticianUnseen_Baseline
./evaluat_metrics_Politician.sh > ../../Category_unseen_Score/Politician_score.txt

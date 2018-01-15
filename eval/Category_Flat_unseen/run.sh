 python3 predFinderCategory.py -i ../preds/flat_unseen.pred -f Athlete

 python3 predFinderCategory.py -i ../preds/flat_unseen.pred -f Artist

 python3 predFinderCategory.py -i ../preds/flat_unseen.pred -f Politician

python3 metrics.py -i Athlete/ -d Athlete -p Athlete/Athlete_predictions.txt

 python3 metrics.py -i Artist/ -d Artist -p Artist/Artist_predictions.txt

 python3 metrics.py -i Politician/ -d Politician -p Politician/Politician_predictions.txt

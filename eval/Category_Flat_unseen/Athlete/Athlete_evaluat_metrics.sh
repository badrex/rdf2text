#!/bin/bash

# compute BLEU

export TEST_TARGETS_REF0=Athlete.ref1
export TEST_TARGETS_REF1=Athlete.ref2
export TEST_TARGETS_REF2=Athlete.ref3

printf " \n Blue score \n "
./multi-bleu.perl ${TEST_TARGETS_REF0} ${TEST_TARGETS_REF1} ${TEST_TARGETS_REF2}  < Athlete_predictions.txt

cd ..
cd ..
cd meteor-1.5
printf "\n Meteor score \n"
#compute METEOR
# The two files relexicalised_predictions.txt and all-notdelex-refs-meteor.txt must be in the folder meteor-1.5
java -Xmx2G -jar meteor-1.5.jar ../Category_Flat_unseen/Athlete/Athlete_predictions.txt ../Category_Flat_unseen/Athlete/all-notdelex-refs-meteor.txt -l en -norm -r 3

cd ..
cd tercom-0.7.25
printf "\n TER score \n"
#compute TER
# The two files relexicalised_predictions-ter.txt and all-notdelex-refs-ter.txt must be in the folder tercom-0.7.25
java -jar tercom.7.25.jar -h ../Category_Flat_unseen/Athlete/relexicalised_predictions-ter.txt -r ../Category_Flat_unseen/Athlete/all-notdelex-refs-ter.txt


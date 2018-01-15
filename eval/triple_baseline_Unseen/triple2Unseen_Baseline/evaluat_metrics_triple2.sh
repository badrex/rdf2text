#!/bin/bash

# compute BLEU

export TEST_TARGETS_REF0=all-notdelex-reference0.lex
export TEST_TARGETS_REF1=all-notdelex-reference1.lex
export TEST_TARGETS_REF2=all-notdelex-reference2.lex

printf " \n Blue score \n "
./multi-bleu.perl ${TEST_TARGETS_REF0} ${TEST_TARGETS_REF1} ${TEST_TARGETS_REF2}  < relexicalised_predictions.txt

cd ..
cd ..
cd meteor-1.5
printf "\n Meteor score \n"
#compute METEOR
# The two files relexicalised_predictions.txt and all-notdelex-refs-meteor.txt must be in the folder meteor-1.5
java -Xmx2G -jar meteor-1.5.jar ../triple_baseline_Unseen/triple2Unseen_Baseline/relexicalised_predictions.txt ../triple_baseline_Unseen/triple2Unseen_Baseline/all-notdelex-refs-meteor.txt -l en -norm -r 3

cd ..
cd tercom-0.7.25
printf "\n TER score \n"
#compute TER
# The two files relexicalised_predictions-ter.txt and all-notdelex-refs-ter.txt must be in the folder tercom-0.7.25
java -jar tercom.7.25.jar -h ../triple_baseline_Unseen/triple2Unseen_Baseline/relexicalised_predictions-ter.txt -r ../triple_baseline_Unseen/triple2Unseen_Baseline/all-notdelex-refs-ter.txt


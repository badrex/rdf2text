#!/bin/bash

# compute BLEU

export TEST_TARGETS_REF0=unseen_baseline/all-notdelex-reference0.lex
export TEST_TARGETS_REF1=unseen_baseline/all-notdelex-reference1.lex
export TEST_TARGETS_REF2=unseen_baseline/all-notdelex-reference2.lex
export TEST_TARGETS_REF3=unseen_baseline/all-notdelex-reference3.lex
export TEST_TARGETS_REF4=unseen_baseline/all-notdelex-reference4.lex


printf " \n Blue score \n "
./multi-bleu.perl ${TEST_TARGETS_REF0} ${TEST_TARGETS_REF1} ${TEST_TARGETS_REF2} ${TEST_TARGETS_REF3} ${TEST_TARGETS_REF4}  < unseen_baseline/relexicalised_predictions.txt

cd ..
cd meteor-1.5
printf "\n Meteor score \n"
#compute METEOR
# The two files relexicalised_predictions.txt and all-notdelex-refs-meteor.txt must be in the folder meteor-1.5
java -Xmx2G -jar meteor-1.5.jar ../baselineunSeen/unseen_baseline/relexicalised_predictions.txt ../baselineunSeen/unseen_baseline/all-notdelex-refs-meteor.txt -l en -norm -r 5

cd ..
cd tercom-0.7.25
printf "\n TER score \n"
#compute TER
# The two files relexicalised_predictions-ter.txt and all-notdelex-refs-ter.txt must be in the folder tercom-0.7.25
java -jar tercom.7.25.jar -h ../baselineunSeen/unseen_baseline/relexicalised_predictions-ter.txt -r ../baselineunSeen/unseen_baseline/all-notdelex-refs-ter.txt


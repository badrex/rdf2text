#!/bin/bash

# compute BLEU

export TEST_TARGETS_REF0=all-notdelex-reference0.lex
export TEST_TARGETS_REF1=all-notdelex-reference1.lex
export TEST_TARGETS_REF2=all-notdelex-reference2.lex
export TEST_TARGETS_REF3=all-notdelex-reference3.lex
export TEST_TARGETS_REF4=all-notdelex-reference4.lex
export TEST_TARGETS_REF5=all-notdelex-reference5.lex
export TEST_TARGETS_REF6=all-notdelex-reference6.lex

printf " \n Blue score \n "
./multi-bleu.perl ${TEST_TARGETS_REF0} ${TEST_TARGETS_REF1} ${TEST_TARGETS_REF2} ${TEST_TARGETS_REF3} ${TEST_TARGETS_REF4} ${TEST_TARGETS_REF5} ${TEST_TARGETS_REF6} < relexicalised_predictions2.txt

cd ..
cd ..
cd meteor-1.5
printf "\n Meteor score \n"
#compute METEOR
java -Xmx2G -jar meteor-1.5.jar ../baseline/dev_triple2/relexicalised_predictions2.txt ../baseline/dev_triple2/all-notdelex-refs-meteor.txt -l en -norm -r 7

cd ..
cd tercom-0.7.25
printf "\n TER score \n"
#compute TER
java -jar tercom.7.25.jar -h ../baseline/dev_triple2/relexicalised_predictions-ter.txt -r ../baseline/dev_triple2/all-notdelex-refs-ter.txt


#!/bin/bash

# compute BLEU

export TEST_TARGETS_REF0=all-notdelex-reference0.lex
export TEST_TARGETS_REF1=all-notdelex-reference1.lex
export TEST_TARGETS_REF2=all-notdelex-reference2.lex
export TEST_TARGETS_REF3=all-notdelex-reference3.lex


printf " \n Blue score \n "
./multi-bleu.perl ${TEST_TARGETS_REF0} ${TEST_TARGETS_REF1} ${TEST_TARGETS_REF2} ${TEST_TARGETS_REF3} < relexicalised_predictions3.txt

cd ..
cd ..
cd meteor-1.5
printf "\n Meteor score \n"
#compute METEOR
java -Xmx2G -jar meteor-1.5.jar ../tripleBaselineSeen/dev_triple3/relexicalised_predictions3.txt ../tripleBaselineSeen/dev_triple3/all-notdelex-refs-meteor.txt -l en -norm -r 4

cd ..
cd tercom-0.7.25
printf "\n TER score \n"
#compute TER
java -jar tercom.7.25.jar -h ../tripleBaselineSeen/dev_triple3/relexicalised_predictions-ter.txt -r ../tripleBaselineSeen/dev_triple3/all-notdelex-refs-ter.txt


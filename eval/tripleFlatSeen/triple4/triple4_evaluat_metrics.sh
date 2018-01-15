#!/bin/bash

# compute BLEU

export TEST_TARGETS_REF0=triple4.ref1
export TEST_TARGETS_REF1=triple4.ref2
export TEST_TARGETS_REF2=triple4.ref3

printf " \n Blue score \n "
./multi-bleu.perl ${TEST_TARGETS_REF0} ${TEST_TARGETS_REF1} ${TEST_TARGETS_REF2}  < triple4_predictions.txt

cd ..
cd ..
cd meteor-1.5
printf "\n Meteor score \n"
#compute METEOR
# The two files relexicalised_predictions.txt and all-notdelex-refs-meteor.txt must be in the folder meteor-1.5
java -Xmx2G -jar meteor-1.5.jar ../tripleFlatSeen/triple4/triple4_predictions.txt ../tripleFlatSeen/triple4/all-notdelex-refs-meteor.txt -l en -norm -r 3

cd ..
cd tercom-0.7.25
printf "\n TER score \n"
#compute TER
# The two files relexicalised_predictions-ter.txt and all-notdelex-refs-ter.txt must be in the folder tercom-0.7.25
java -jar tercom.7.25.jar -h ../tripleFlatSeen/triple4/relexicalised_predictions-ter.txt -r ../tripleFlatSeen/triple4/all-notdelex-refs-ter.txt


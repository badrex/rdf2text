# Learning to generate text from RDF fact graphs with seq2seq models

#### Project work by Badr Abdullah, François Buet, and Reem Mathbout.

This project is still under development. All modules in this project have been developed
and tested with python 3.6. There are only two non-core Python libraries required to run the modules: NLTK and SPARQLWrapper.

For now, the code can be used to parse RDF data from XML files,
apply text preprocessing, retrieve semantic types for RDF entities, perform
delexicalization on the target sentences and generate datasets to be used for
training and evaluations sequence to sequence models for NLG from fact graphs.

## Generating Training Datasets
To use the module for generating training datasets, use:

###### Flat sequences in the source side
```
mkdir ../datasets
python generate_train_dataset.py \
  -path ../challenge_data_train_dev/train \
  -src_mode  flat \
  -src ../datasets/train.src \
  -tgt ../datasets/train.tgt
```

Example: the pair {*triple:* Albany , Oregon | country | United States, *text:* "Albany , Oregon is in the U.S."} would be represented as follows:
```
src: ENTITY_1 CITY country ENTITY_2 COUNTRY

tgt: ENTITY_1 is in the ENTITY_2  .
```


###### Structured sequences in the source side
```
python generate_train_dataset.py \
  -path ../challenge_data_train_dev/train \
  -src_mode  structured \
  -src ../datasets/train.src \
  -tgt ../datasets/train.tgt
```

Example: the pair (triple: Albany , Oregon | country | United States, "Albany , Oregon is in the U.S.") would be represented as follows:
```
src: ( ( ENTITY_1 CITY ( country ( ENTITY_2 COUNTRY ) ) ) )

tgt: ENTITY_1 is in the ENTITY_2  .
```

## Generating Evaluation Datasets
To use the module for generating evaluation (dev and test) datasets, use:

(Running this script would generate 5 files: dev.src, dev.tgt, dev.ref1, dev.ref2, dev.ref3, and dev.relex)

###### Flat sequences in the source side
```
mkdir ../datasets
python generate_eval_dataset.py \
  -path ../challenge_data_train_dev/dev \
  -src_mode  flat \
  -src ../datasets/dev.src \
  -tgt ../datasets/dev.tgt \
  -ref ../datasets/dev.ref \
  -relex ../datasets/dev.relex
```

###### Structured sequences in the source side
```
python generate_eval_dataset.py \
  -path ../challenge_data_train_dev/dev \
  -src_mode  structured \
  -src ../datasets/dev.src \
  -tgt ../datasets/dev.tgt \
  -ref ../datasets/dev.ref-ref \
  -relex ../datasets/dev.relex
```

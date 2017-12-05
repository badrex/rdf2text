# Learning to generate text from knowledge graphs with Seq2Seq models

This project is still under development. All modules in this project have been developed
and tested with python 3.6. The only non-core library that is required is NLTK.

For now, the code can be used to parse RDF data from XML files,
apply some text preprocessing, retrieve semantic types for RDF entities, performance
delexicalization on the target sentences and generate datasets to be used for
training and evaluations sequence to sequence models for NLG from fact graphs.

## Generating Training Datasets
To use the module for generating training datasets, use:

### Flat sequences in the source side
```
mkdir ../datasets
python generate_train_dataset.py \
  -path ../challenge_data_train_dev/train \
  -src_mode  flat \
  -src ../datasets/train.src \
  -tgt ../datasets/train.tgt
```

Example: the pair (triple: Albany , Oregon | country | United States, "Albany , Oregon is in the U.S.") would be represnted as follows
src: ENTITY_1 CITY | country | ENTITY_2 COUNTRY
tgt: ENTITY_1 is in the ENTITY_2  .


### Structured sequences in the source side
```
python generate_train_dataset.py \
  -path ../challenge_data_train_dev/train \
  -src_mode  structured \
  -src ../datasets/train.src \
  -tgt ../datasets/train.tgt
```

Example: the pair (triple: Albany , Oregon | country | United States, "Albany , Oregon is in the U.S.") would be represnted as follows

src: ( ( ENTITY_1 CITY ( country ( ENTITY_2 COUNTRY ) ) ) )

tgt: ENTITY_1 is in the ENTITY_2  .

## Generating Evaluation Datasets
To use the module for generating evaluation (dev and test) datasets, use:
(Running this script would generate 5 files: dev.src, dev.tgt, dev.ref1, dev.ref2, and dev.ref3)

### Flat sequences in the source side
```
mkdir ../datasets
python generate_eval_dataset.py \
  -path ../challenge_data_train_dev/dev \
  -src_mode  flat \
  -src ../datasets/dev.src \
  -tgt ../datasets/dev.tgt \
  -ref ../datasets/dev.ref
```

### Structured sequences in the source side
```
python generate_eval_dataset.py \
  -path ../challenge_data_train_dev/dev \
  -src_mode  flat \
  -src ../datasets/dev.src \
  -tgt ../datasets/dev.tgt \
  -ref ../datasets/dev.ref
```

## TODO:
1. Write code for relexicalization procedure (to be used after training).
2. Improve the evaluation module (development already started, but not in GitLab yet).
3. Run some experiments with seq2seq model in OpenNMT-Lua.
4. Perform error analysis.
5. Write the report.

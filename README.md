# Learning to generate text from RDF fact graphs with seq2seq models

#### Project work by Badr Abdullah, François Buet, and Reem Mathbout.

The repository contains code to prepare data for training models that generate natural language text from RDF triples using the WebNLG data (more info about the data can be found in this paper: http://webnlg.loria.fr/pages/webnlg-challenge-report.pdf). All modules in this project have been developed
and tested with python 3.6. There are only two non-core Python libraries required to run the modules: NLTK and SPARQLWrapper.

For now, the code can be used to parse RDF data from XML files, apply text preprocessing, retrieve semantic types for RDF entities, perform delexicalization on the target sentences and generate datasets to be used for
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
  -ref ../datasets/dev.ref \
  -relex ../datasets/dev.relex
```

## Using OpenNTM
Once we have the data, we can train a seq2seq model. We show how to use OpenNMT for this task:
(probably you would want to move the datasets directory to where you have installed OpenNMT)

### 1. Preprocess the data.

```
th preprocess.lua \
    -train_src datasets/train.src \
    -train_tgt datasets/train.tgt \
    -valid_src datasets/dev.src \
    -valid_tgt datasets/dev.tgt \
    -save_data datasets/data_tensor
```

### 2. Train a model.
```
th train.lua -data datasets/data_tensor-train.t7 -save_model s2s_model
```

### 3. Use the model for inference.
```
th translate.lua -model s2s_model_epochX_PPL.t7 -src datasets/dev.src -output predictions.dev
```

### 4. Relexicalize predictions.
```
python relex_preditions.py \
    -pred predictions.dev \
    -relex datasets/dev.relex \
    -output predictions.relex
```

### 5. Evaluate with BLEU script.
```
multi-bleu.perl  datasets/dev.ref < predictions.relex
```

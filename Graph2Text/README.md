# Learning to generate text from knowledge graphs with Seq2Seq models

This project is under development. So far, it has been developed
and tested with python 3.6.

For now, the code can be used to parse RDF data from XML files,
apply some preprocessing, and generate datasets to be used for
sequence to sequence models.

To use the module for generating datasets (either training or dev):

For flat sequences in the source side
```
python generate_dataset.py \
  -path ../challenge_data_train_dev/train \
  -input_mode  flat \
  -src ../datasets/train.src \
  -tgt ../datasets/train.tgt
```

Source sequences will be like:
```ENTITY-1 WORK author ENTITY-2 PERSON```

NOTE: The module is still under development. For now, the source sequence would be like this example:

```ENTITY-1 AGENT author ENTITY-2 PATIENT```


For structured sequences in the source side
```
python generate_dataset.py \
  -path ../challenge_data_train_dev/train \
  -input_mode  structured \
  -src ../datasets/train.src \
  -tgt ../datasets/train.tgt 
```

Source sequences will be like:
```¹( ²( ENTITY-1 WORK ³( author ^( ENTITY-2 PERSON )^ )³ )² )¹```

NOTE: The module is still under development. For now, the source sequence would be like this example:

```¹( ²( ENTITY-1 AGENT ³( author ^( ENTITY-2 PATIENT )^ )³ )² )¹```

The target sequences would be the original target sentences (target sentence delexicalization is still under development).

## TODO:
1. Develope a SPARQL module (in utils) for communicating with DBpedia.
2. Get semantic types from DBpedia (using property schema?).
3. Build offline dictionaries for property schemas, entity aliases, etc.  
4. Implement delexicalize_sentence() method with text matching.
5. Develop evaluation module.
6. Run some experiments with seq2seq model.

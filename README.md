To use the modules for generating datasets (either training or dev):

1. For flat sequence in the source side
``` python generate_dataset.py \
  -path ../challenge_data_train_dev/train \
  -input_mode  flat \
  -src ../datasets/train.src \
  -tgt ../datasets/train.tgt
```

Source sequences will be like:

```ENTITY-1 WORK ENTITY-2 PERSON```

NOTE: The module is still under development. For now, the source sequence would be like this example:

```ENTITY-1 AGENT ENTITY-2 PATIENT```

```
python generate_dataset.py \
  -path ../challenge_data_train_dev/train \
  -input_mode  structured \
  -src ../datasets/train.src \
  -tgt ../datasets/train.tgt \
```

Source sequences will be like:

```( ( ENTITY-1 WORK ( author ( ENTITY-2 PERSON ) ) ) )```

NOTE: The module is still under development. For now, the source sequence would be like this example:

```( ( ENTITY-1 AGENT ( author ( ENTITY-2 PATIENT ) ) ) )```

The target sequences would be the original target sentences (target sentence delexicalization is still under development).

TODO:
1. Develope a SPARQL module (in utils) for communicating with DBpedia.
2. Get semantic types from DBpedia (using property schema?).
3. Build offline dictionaries for property schemas, entity aliases, etc.  
4. Implement delexicalize_sentence() method with text matching.

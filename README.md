To use the modules for generating datasets (either training or dev):

1. For linear sequence in the source side
```
python generate_dataset.py \
  -path ../challenge_data_train_dev/train \
  -input_mode  linear \
  -src ../datasets/train.src \
  -tgt ../datasets/train.tgt
```
Source sequences will be like:
```
ENTITY-1 BOOK author ENTITY-2 PERSON
```

2. For structured sequence in the source side
``` 
python generate_dataset.py \
  -path ../challenge_data_train_dev/train
  -input_mode  structured
  -src ../datasets/train.src
  -tgt ../datasets/train.tgt
```
Source sequences will be like:
```
( ( ENTITY-1 BOOK ( author ( ENTITY-2 PERSON ) ) ) )
```

TODO:
1. Develope a SPARQL module (in utils) for communicating with DBpedia.
2. Get semantic types from DBpedia (using property schema?). 
3. Build offline dictionaries for property schemas, entity aliases, etc.  
4. Implement delexicalize_sentence() method with text matching.

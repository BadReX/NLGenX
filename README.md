To use the modules for generating datasets (either training or dev):

1. For linear sequence in the source side
>>> python generate_dataset.py \
  -path ../challenge_data_train_dev/train
  -input_mode  linear
  -src ../datasets/train.src
  -tgt ../datasets/train.tgt

Source sequences will be like:
>>> ENTITY-1 BOOK ENTITY-2 AUTHOR

2. For structured sequence in the source side
>>> python generate_dataset.py \
  -path ../challenge_data_train_dev/train
  -input_mode  structured
  -src ../datasets/train.src
  -tgt ../datasets/train.tgt

  Source sequences will be like:
  >>> ( ( ENTITY-1 BOOK ( author ( ENTITY-2 AUTHOR ) ) ) )

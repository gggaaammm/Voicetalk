#construct dictionary for zhckip

import os
import sys

# Suppress as many warnings as possible
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# from tensorflow.python.util import deprecation
# deprecation._PRINT_DEPRECATION_WARNINGS = False
# import tensorflow as tf
# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

# Load model without GPU
ws = WS("./data")
pos = POS("./data")
ner = NER("./data")

# Load model with GPU
# ws = WS("./data", disable_cuda=False)
# pos = POS("./data", disable_cuda=False)
# ner = NER("./data", disable_cuda=False)

# Create custom dictionary
word_to_weight = {
    "2號電扇": 1,
    "打開": 1,
    "風速": 2,
    "虛擬裝置": 1,
    "定時器": 1,
    "分鐘": 1,
}
dictionary = construct_dictionary(word_to_weight)
print(dictionary)

sentence_list = [
        "設定虛擬裝置的定時器為2分30秒"
    ]
word_sentence_list = ws(sentence_list, coerce_dictionary=dictionary)
pos_sentence_list = pos(word_sentence_list)
entity_sentence_list = ner(word_sentence_list, pos_sentence_list)


del ws
del pos
del ner

print("[word]", word_sentence_list)



# after token classifying, remove the keyword and get the va
sentence =  ' '.join(word_sentence_list[0])
print("[sentence] [", sentence,"]")
print("[pos]",pos_sentence_list )
print("[entity]",entity_sentence_list)
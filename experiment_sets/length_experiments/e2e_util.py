import torch
from transformers import AutoModelForCausalLM, \
  AutoTokenizer
# from torch import nn
import numpy as np

import random as rng

def tokenize(full_eng, toker, model):
    """Parse out the seed and the tokens from the provided english"""   
    bundle = full_eng.split(" ",1)
    seed = bundle[0]
    eng = " "+bundle[1]
    if seed[-1] == ",":
        eng = ","+eng
        seed = seed[:-1]
    inpts = toker(eng, return_tensors="pt")
    inpt_ids = inpts["input_ids"]
    tokens = []
    for tid in inpt_ids[0]:
        word = toker.decode(tid)
        tokens.append(word)
    return seed, tokens



def sample_seed():
    """ Sample a random seed from our pre-configured seed set"""
    seed_data = ['Although', 'As', 'Because', 'Before', 'If', 'Since', 'Unless', 'Until', 'When', 'While', 'I', 'You', 'He', 'She', 'We', 'They', 'It', 'Do', 'What', 'Where', 'Why', 'Could', 'The', 'Because', 'Does', 'So', 'This', 'That', 'My', 'Your', 'His', 'Her', 'Their', 'Our', 'Its', 'Dogs', 'Cats', 'Cheese', 'Trump', 'Biden', 'Democrats', 'Republicans', 'How', 'People', 'A', 'Pizza', 'Chinese', 'To', 'Have', 'Maybe']
    rand_index = rng.randint(0, len(seed_data)-1)
    return seed_data[rand_index]


def extract_iv_ct(raw_bytes):
    if len(raw_bytes) < 32:
        return raw_bytes, raw_bytes
    iv = raw_bytes[:16]
    ct = raw_bytes[16:]
    extra_pads = -1 * (len(ct) % 16)
    real_ct = ct[:extra_pads]
    return iv, real_ct

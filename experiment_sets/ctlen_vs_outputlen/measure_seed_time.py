#!/usr/bin/env python3
""" English-to-English(E2E) Encryption Tool """
import binascii as binascii
from termcolor import colored
import crypto.util as crypto
import gpt2_arthm_coding.encoderGPT2 as en_gpt2
import gpt2_arthm_coding.decoderGPT2 as de_gpt2

import e2e_util as util

import time

import getopt
import sys

import torch
from transformers import AutoModelForCausalLM, \
  AutoTokenizer


from datetime import datetime


def initialize_GPT2():
    toker = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    return toker, model


def run_encryption(secret_msg, my_l, initial_seed, include_iv = False):

    t0 = time.perf_counter()
    toker, model = initialize_GPT2()
    t1 = time.perf_counter()
    key = crypto.obtain_key("e2e")
    iv, ct = crypto.encrypt_aes_cbc(key, secret_msg)
    t2 = time.perf_counter()

    if include_iv:
        code = iv+ct
    else:
        code = ct
    fl = len(code)
    print(fl)
    assert len(code) == fl
    print("We have obtained our "+str(fl)+" total ciphertex")
    data_dump = {}
    data_dump[0] = []
    data_dump[2] = []
    data_dump[3] = []
    data_dump[4] = []
 
    initial_seed = util.pad(initial_seed)
    seed_back = initial_seed

    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=initial_seed, toker=toker, model=model, rotater_len=0, time_data_dump = data_dump)
    de.decode()
    print("done")
    assert len(code) == fl
    print(initial_seed)
    assert initial_seed == seed_back 

    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=initial_seed, toker=toker, model=model, rotater_len=2, time_data_dump = data_dump)
    de.decode()
    print("done")
    assert len(code) == fl
    assert initial_seed == seed_back

    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=initial_seed, toker=toker, model=model, rotater_len=3, time_data_dump = data_dump)
    de.decode()
    print("done")
    assert len(code) == fl
    assert initial_seed == seed_back

    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=initial_seed, toker=toker, model=model, rotater_len=4, time_data_dump = data_dump)
    de.decode()
    print("done")
    assert len(code) == fl
    assert initial_seed == seed_back

    print()
    print()
    print("full previous")
    for d in data_dump[0]:
        print(d)
    print()
    print()
    print("1 sentence")
    for d in data_dump[2]:
        print(d)
    print()
    print()
    print("2 sentences")
    for d in data_dump[3]:
        print(d)
    print()
    print()
    print("3 sentences")
    for d in data_dump[4]:
        print(d)



    







if __name__ == "__main__":
    msg = "This is a graduate-level course on Advanced Computer Security and Privacy. We will meet three times a week MWF 8-9:15 am"
    run_encryption(msg, 32, "I", include_iv = True)
           

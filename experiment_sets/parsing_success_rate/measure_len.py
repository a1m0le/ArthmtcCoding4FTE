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


def run_encryption(secret_msg, my_l, initial_seed, include_iv = False, data_dump=None):

    t0 = time.perf_counter()
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
    toker, model = initialize_GPT2()
    assert len(code) == fl
    initial_seed = util.pad(initial_seed)
    seed_back = initial_seed


    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=initial_seed, toker=toker, model=model, rotater_len=2)
    T = de.decode()
    all_T = [initial_seed] + T
    eng = "".join(all_T)
    if len(code) not in data_dump:
        data_dump[len(code)] = []
    data_dump[len(code)].append(len(eng))



    







if __name__ == "__main__":
    msg = "YYesYesYesYesYes"
    data_dump = {}
    for i in range(0,1):
        run_encryption(msg, 32, "I", include_iv = True, data_dump=data_dump)
        msg = msg+"Yes"
    print()
    print("---------------------------------------------------------------------------------------------")
    print()
    print("AES ct total length","output sentence char length")
    for k in data_dump:
        for d in data_dump[k]:
            print(str(k)+","+str(d))


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


def run_encryption(secret_msg, my_l, initial_seed, include_iv = False, data_dump=None, toker=None, model=None):

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
    print(str(fl)+" is "+secret_msg, flush=True)
    assert len(code) == fl


    initial_seed = util.pad(initial_seed)
    seed_back = initial_seed


    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=initial_seed, toker=toker, model=model, rotater_len=2)
    T = de.decode()
    all_T = [initial_seed] + T

    eng = "".join(all_T)
    re_T = util.tokenize(eng, toker, model)
    if re_T != all_T:
        bad = 1
        good = 0
    else:
        bad = 0
        good = 1



    if len(code) not in data_dump:
        data_dump[len(code)] = {"good":0, "bad":0}
    data_dump[len(code)]["good"] += good
    data_dump[len(code)]["bad"] += bad



    







if __name__ == "__main__":
    toker, model = initialize_GPT2()
    msg = "YesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYesYes"
    data_dump = {}
    for i in range(0,1):
        for j in range(0, 100):
            run_encryption(msg, 32, "They", include_iv = True, data_dump=data_dump, toker=toker, model=model)
        msg = msg+"YesYesYesYesYes"
    print()
    print("---------------------------------------------------------------------------------------------")
    print()
    print("AES ct total length","output sentence char length")
    for k in data_dump:
        print(str(k)+","+str(data_dump[k]["good"])+","+str(data_dump[k]["bad"]))


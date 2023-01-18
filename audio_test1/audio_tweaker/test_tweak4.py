import os
import random


def sampling_all(frames_list):
    return sampling(0, len(frames_list), frames_list)


def sampling(st,frames_ct, frames_list):

    new_data = ""
    bgF = st
    for i in range(bgF, bgF+frames_ct):
        k = i
        if k == 0:
            continue
        nstr = "11111111111"+frames_list[k]
        new_data += nstr

    ct = 0
    new_hex_data = ""

    while ct < len(new_data):
        eachB = new_data[ct:ct+8]
        hexBstr = hex(int(eachB,2))
        new_hex_data += hexBstr[2:].zfill(2)
        ct += 8
    
    return new_hex_data



if __name__ == "__main__":

    pieces = {}
    pc_ct = 0
    for file in os.listdir("weapon"):
        with open("weapon/"+file,"rb") as note_file:
            raw_note = note_file.read()
            hex_data = raw_note.hex()

            ct = 0
            bin_data = ""
            while ct < len(hex_data):
                eachB = hex_data[ct]+hex_data[ct+1]
                binBstr = (str(bin(int(eachB,16)))[2:]).zfill(8)
                bin_data += binBstr
                ct += 2

            frames_list = bin_data.split("11111111111")
            samp = sampling_all(frames_list)
            pieces[str(pc_ct)] = bytes.fromhex(samp)
            pc_ct += 1

    print(pc_ct)
    #sequence = "12345678"
    begin = "0"
    length = 20
    sequence = ""
    for i in range(0,20):
        next_c = str(random.randint(0,pc_ct-1))
        sequence += next_c
    #sequence = "bcde"
    new_file = pieces[begin]
    for c in sequence:
        new_file += pieces[c]



    #for i in range(0, len(bin_data)):
    #    if bin_data[i] != new_data[i]:
    #        print("bad-"+str(i))

    #print(new_file)
    miredo = open("war_compose.mp3","wb+")
    miredo.write(new_file)
    miredo.close()

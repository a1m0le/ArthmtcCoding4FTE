



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
    doremi = open("basic.mp3","rb")

    raw_cont = doremi.read()

    hex_data = raw_cont.hex()

    ct = 0
    bin_data = ""
    while ct < len(hex_data):
        eachB = hex_data[ct]+hex_data[ct+1]
        binBstr = (str(bin(int(eachB,16)))[2:]).zfill(8)
        bin_data += binBstr
        ct += 2
        if ct < 10:
            print(binBstr)

    frames_list = bin_data.split("11111111111")

    print()
    print(len(frames_list))

    doremi.close()


    s1 = sampling(0,25,frames_list)
    s2 = sampling(25,25,frames_list)
    s3 = sampling(50,25,frames_list)
    s4 = sampling(75,25,frames_list)
    s5 = sampling(100,25,frames_list)
    s6 = sampling(125,25,frames_list)
    s7 = sampling(150,25,frames_list)
    s8 = sampling(175,25,frames_list)

    #all_hex = s1+s2+s3+s4+s5+s6+s7+s8
    all_hex = s3

    new_file = bytes.fromhex(all_hex)



    #for i in range(0, len(bin_data)):
    #    if bin_data[i] != new_data[i]:
    #        print("bad-"+str(i))

    #print(new_file)
    miredo = open("compose.mp3","wb+")
    miredo.write(new_file)
    miredo.close()

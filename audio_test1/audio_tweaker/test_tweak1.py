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


new_data = ""
bgF = 100
frames_ct = 100
for i in range(bgF, bgF+frames_ct):
    k = i
    if k == 0:
        continue
    nstr = "11111111111"+frames_list[k]
    new_data += nstr

ct = 0
new_hex_data = ""

print("--------")
while ct < len(new_data):
    eachB = new_data[ct:ct+8]
    hexBstr = hex(int(eachB,2))
    new_hex_data += hexBstr[2:].zfill(2)
    ct += 8
    if ct < 50:
        print(eachB)
        print(hexBstr)

#print(new_hex_data)
new_file = bytes.fromhex(new_hex_data+new_hex_data)


print(new_hex_data[0:64])
print(hex_data[0:64])

#for i in range(0, len(bin_data)):
#    if bin_data[i] != new_data[i]:
#        print("bad-"+str(i))

#print(new_file)
miredo = open("test_miredo.mp3","wb+")
miredo.write(new_file)
miredo.close()

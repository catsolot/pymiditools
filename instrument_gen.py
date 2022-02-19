# Script used to process instrument text in inst.txt
#with open("ins_list.txt", "r") as f:
#    a = f.read()
#
#instruments = a.split("\n")
#for i in range(len(instruments)):
#    instruments[i].strip()
#    for j in range(len(instruments[i])):
#        if (instruments[i][j] == '.'):
#            instruments[i] = instruments[i][j+1:]
#            break
#new_list = []
#print(instruments)
#for i in range(0, len(instruments), 2):
#    new_list.append(instruments[i])
#
#for i in range(1, len(instruments), 2):
#    new_list.append(instruments[i])
#
#    
#
#with open("out.txt", "w") as f:
#    for i in new_list:
#        f.write(i + "\n")

with open("ins_list.txt", "r") as f:
    instruments = f.read().split("\n")


dictionary = "instruments = {"

for i in range(128):
    string = str(hex(i))
    string = string[2:]
    if (len(string) != 2):
        string = "0" + string

    dictionary += '"{}": "{}", '.format(string, instruments[i])
dictionary += '"{}": "{}" '.format("80", "Gunshot")
dictionary += "}"
with open("instrument_lookup.py", "w") as f:
    f.write(dictionary + "\n")
    # { "key": "value" ... }

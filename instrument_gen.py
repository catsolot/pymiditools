#Acknowledgement:
#This document was originally distributed in text format by The International MIDI Association. I have updated it and added new Appendices.
#© Copyright 1999 David Back.
#Web: http://midimusic.github.io
#This document may be freely copied in whole or in part provided the copy contains this Acknowledgement.
# midi instrument names and hex values come from this site.
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

for i in range(127):
    string = str(hex(i))
    string = string[2:]
    if (len(string) != 2):
        string = "0" + string

    dictionary += '"{}": "{}", '.format(string, instruments[i])
dictionary += '"{}": "{}" '.format("7f", "Gunshot")
dictionary += "}"

ack = "#Acknowledgement:\n#This document was originally distributed in text format by The International MIDI Association. I have updated it and added new Appendices.\n#© Copyright 1999 David Back.\n#Web: http://midimusic.github.io\n#This document may be freely copied in whole or in part provided the copy contains this Acknowledgement.\n# midi instrument names and hex values come from this site."
with open("instrument_lookup.py", "w") as f:
    f.write(ack + "\n")
    f.write(dictionary + "\n")
    # { "key": "value" ... }

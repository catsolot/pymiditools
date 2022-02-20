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


dictionary1 = "hex_to_instrument = {"
dictionary2 = "instrument_to_hex = {"

for i in range(127):
    hex_string = str(hex(i))
    hex_string = hex_string[2:]
    if (len(hex_string) != 2):
        hex_string = "0" + hex_string

    dictionary1 += '"{}": "{}", '.format(hex_string, instruments[i])
    dictionary2 += '"{}": "{}", '.format(instruments[i], hex_string)
dictionary1 += '"{}": "{}" '.format("7f", "Gunshot")
dictionary2 += '"{}": "{}"'.format("Gunshot", "7f")
dictionary1 += "}"
dictionary2 += "}"

ack = "#Acknowledgement:\n#This document was originally distributed in text format by The International MIDI Association. I have updated it and added new Appendices.\n#© Copyright 1999 David Back.\n#Web: http://midimusic.github.io\n#This document may be freely copied in whole or in part provided the copy contains this Acknowledgement.\n# midi instrument names and hex values come from this site."
with open("instrument_lookup.py", "w") as f:
    f.write(ack + "\n")
    f.write(dictionary1 + "\n")
    f.write(dictionary2 + "\n")
    # { "key": "value" ... }

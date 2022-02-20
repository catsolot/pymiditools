from instrument_lookup import hex_to_instrument, instrument_to_hex

class MIDIFile:

    def __init__(self):
        self.hex_array = []

    def read_file(self, input_file):
        """ Read a midi file and store it into the object."""
        with open(input_file, "rb") as input_file:
            binary_string = input_file.read()
        hex_string = binary_string.hex(" ")
        self.hex_array = hex_string.split(" ")

    def hexarray_to_binary(self):
        """Converts an array of HEX values into a binary sting."""
        hex_string = ''.join(self.hex_array)
        binary_string = bytes.fromhex(hex_string)
        return binary_string
    
    def write_file(self, output_file):
        """Writes the MIDI object to the output file."""
        with open(output_file, "wb") as output_file:
            output_file.write(self.hexarray_to_binary()) 
    
    def find_start_track(self, start_index):
        """Returns the index after the start track and length of the track."""
        #print("searching")
        while start_index < len(self.hex_array):
            if (self.hex_array[start_index] == "4d" and 
                self.hex_array[start_index+1] == "54" and 
                self.hex_array[start_index+2] == "72" and 
                self.hex_array[start_index+3] == "6b"):
                    #print("found")
                    #print(self.hex_array[start_index+8]) 
                    return start_index+7    

            start_index = start_index + 1
        return -1

    def find_end_track(self, start_index):
        """ Returns the index right after an end of track sequence."""
        for i in range(start_index, len(self.hex_array)):
            if (self.hex_array[i] == "ff" and self.hex_array[i+1] == "2f" 
                and self.hex_array[i+2] == "00"):
                #print(self.hex_array[i+3])
                return i+3
    
    def list_instruments(self):
        """ Returns the instrument titles being used in the midi file in a list.
        """
        strings = {}
        search_index = self.find_end_track(0)
        search_index = self.find_start_track(search_index)
        while search_index < len(self.hex_array):
            #print(search_index, self.hex_array[search_index])
            if (search_index == -1):
                break
            if (self.hex_array[search_index][0] == "c"):
                channel = self.hex_array[search_index]
                instrument_type = self.hex_array[search_index+1]
                strings[channel] =  hex_to_instrument[instrument_type]
                search_index = self.find_start_track(search_index)
            else:
                search_index = search_index + 1
        return strings

    def change_instrument(self, channel, instrument_name):
        """Changes the instrument for a channel to the specified instrument."""
        if (len(instrument_name) != 2):
            instrument_name = instrument_to_hex[instrument_name]
        search_index = self.find_end_track(0)
        search_index = self.find_start_track(search_index)

        while search_index < len(self.hex_array):
            if (self.hex_array[search_index] == "54"):
                search_index = search_index + 7

            if (self.hex_array[search_index] == channel):
                self.hex_array[search_index+1] = instrument_name
                return
            search_index = search_index + 1

if __name__ == "__main__":
    a = MIDIFile()

    a.read_file("jd.mid")
    print(a.list_instruments())
    #print(a)
    #write_midi("mary3.mid", a)

from instrument_lookup import instruments

class MIDI_File:

    def __init__(self):
        self.hex_array = []
    def read_file(self, input_file):
        """ Read a midi file and returns a list of HEX values representing the bytes."""
        with open(input_file, "rb") as input_file:
            binary_string = input_file.read()
        hex_string = binary_string.hex(" ")
        self.hex_array = hex_string.split(" ")
        #return hex_array
    
    def write_file_helper(self, output_file, data):
        """Overwrites output_file with data."""
        with open(output_file, "wb") as output_file:
            lines = output_file.write(data)
        return lines 
    
    def hexarray_to_binary(self):
        """Converts an array of HEX values into a binary sting."""
        hex_string = ''.join(self.hex_array)
        binary_string = bytes.fromhex(hex_string)
        return binary_string
    
    def write_midi(self, output_file):
        write_file_helper(output_file, hexarray_to_binary(self.hex_array))
    
    def find_end_of_track(self):
        """ Returns the index right after an end of track sequence."""
        for i in range(len(self.hex_array)):
            if (self.hex_array[i] == "ff" and self.hex_array[i+1] == "2f" and self.hex_array[i+2] == "00"):
                return i+2
    
    def list_instruments(self):
        """ Returns the instrument titles being used in the midi file in a list."""
        strings = []
        start_search_index = self.find_end_of_track()
        for i in range(start_search_index, len(self.hex_array)):
            if (self.hex_array[i][0] == "c"):
                channel = self.hex_array[i]
                instrument_type = self.hex_array[i+1]
                string = "{} {}".format(channel, instruments[instrument_type])
                strings.append(string) 
        return strings


if __name__ == "__main__":
    a = MIDI_File()

    a.read_file("mary.mid")
    print(a.list_instruments())
    #print(a)
    #write_midi("mary3.mid", a)

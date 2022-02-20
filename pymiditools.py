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

    def find_end_of_track(self):
        """ Returns the index right after an end of track sequence."""
        for i in range(len(self.hex_array)):
            if (self.hex_array[i] == "ff" and self.hex_array[i+1] == "2f" 
                and self.hex_array[i+2] == "00"):
                return i+2
    
    def list_instruments(self):
        """ Returns the instrument titles being used in the midi file in a list.
        """
        strings = []
        start_search_index = self.find_end_of_track()
        for i in range(start_search_index, len(self.hex_array)):
            if (self.hex_array[i][0] == "c"):
                channel = self.hex_array[i]
                instrument_type = self.hex_array[i+1]
                string = "{} {}".format(channel, hex_to_instrument[instrument_type])
                strings.append(string) 
        return strings

    def change_instrument(self, channel, instrument_name):
        """Changes the instrument for a channel to the specified instrument."""
        start_search_index = self.find_end_of_track()
        for i in range(start_search_index, len(self.hex_array)):
            if (self.hex_array[i] == channel):
                self.hex_array[i+1] = instrument_to_hex[instrument_name]
                return

if __name__ == "__main__":
    a = MIDIFile()

    a.read_file("mary.mid")
    print(a.list_instruments())
    #print(a)
    #write_midi("mary3.mid", a)

import sys
from instrument_lookup import hex_to_instrument, instrument_to_hex

class MIDIFile:

    MTrk = ["4d", "54", "72", "6b"]
    MThd = ["4d", "54", "68", "06"]
    END_TRACK = ["ff", "2f", "00"]

    def __init__(self):
        self.hex_array = []


    def read_file(self, input_file):
        """ Read a midi file and store it into the MIDIFile instance."""
        with open(input_file, "rb") as input_file:
            binary_string = input_file.read()
        hex_string = binary_string.hex(" ")
        self.hex_array = hex_string.split(" ")
        self.read_header()

    def read_header(self):
        """Reads header information into format, ntracks, and tickdiv.""" 
        position = 4
        header_string = ""
        for hex_byte in self.read_bytes(4, 4):
            header_string = header_string + hex_byte
        position = 8
        header_length = int(header_string, 16)
        header_data = self.read_bytes(8, header_length)
        self.format = self.htoi("".join(header_data[0:2]))
        self.num_tracks = self.htoi("".join(header_data[2:4]))
        timing = self.htoi("".join(header_data[4:6]))
        # The top bit of a 16-bit number determines the timing format. 
        if (timing  > 32768):
            self.timing = "timecode"
            timing = timing - 32768
        else:
            self.timing = "metrical"
        self.tickdiv = timing            

    def hexarray_to_binary(self):
        """Converts an array of HEX values into a binary sting."""
        hex_string = ''.join(self.hex_array)
        binary_string = bytes.fromhex(hex_string)
        return binary_string
    
    def write_file(self, output_file):
        """Writes the MIDIFile instance to the output file."""
        with open(output_file, "wb") as output_file:
            output_file.write(self.hexarray_to_binary()) 
    
    def find_start_track(self, start):
        """Returns the index after the start track and length of the track."""
        #print("searching")
        for index in range(start, len(self.hex_array) - 4):
            if self.read_bytes(index, 4) == self.MTrk: 
                    return index + 7    
        return -1

    def find_end_track(self, start):
        """ Returns the index right after an end of track sequence."""
        for index in range(start, len(self.hex_array) - 3):
            if (self.read_bytes(index, 3) == self.END_TRACK):
                return index + 3
        return -1
    
    def list_instruments(self):
        """ Returns the instrument titles being used in the midi file in a list.
        """
        strings = {}
        search_index = self.find_end_track(0)
        search_index = self.find_start_track(search_index)
        while search_index < len(self.hex_array):
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
    
    def read_bytes(self, start_position, number_of_bytes):
        """Read a certain number of bytes from the hex_array starting at
        start position."""
        output = []
        end_position = start_position + number_of_bytes 
        for i in range(start_position, end_position):
            output.append(self.hex_array[i]) 
        return output
    
    def htoi(self, hex_string):
        """Converts a hex_string to an integer."""
        return int(hex_string, 16)


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        if (sys.argv[1] == "inst"):
            a = MIDIFile()
            a.read_file(sys.argv[2])
            #print(a.list_instruments())
            
            print(a.list_instruments())
            print(a.format, a.num_tracks, a.timing, a.tickdiv)
    else: 
        a = MIDIFile()
        a.read_file("mary.mid")
        print(a.read_bytes(0,6))
        print(a.read_bytes(0,5))
        #print(a.format, a.num_tracks, a.timing, a.tickdiv)

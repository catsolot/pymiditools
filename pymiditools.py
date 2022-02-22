import sys
from instrument_lookup import hex_to_instrument, instrument_to_hex

class MIDIFile:

    MTrk = ["4d", "54", "72", "6b"]
    MThd = ["4d", "54", "68", "06"]
    END_TRACK = ["ff", "2f", "00"]

    def __init__(self):
        self.hex_array = []
        self.meta_events = {}


    def read_file(self, input_file_name: str) -> None:
        """ Read a midi file and store it into the MIDIFile instance."""
        with open(input_file_name, "rb") as input_file:
            binary_string = input_file.read()
        hex_string = binary_string.hex(" ")
        self.hex_array = hex_string.split(" ")
        self.read_header()

    def read_header(self) -> None:
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

    def hexarray_to_binary(self) -> bytes:
        """Converts an array of HEX values into a binary sting."""
        hex_string = ''.join(self.hex_array)
        binary_string = bytes.fromhex(hex_string)
        return binary_string
    
    def write_file(self, output_file_name: str) -> None:
        """Writes the MIDIFile instance to the output file."""
        with open(output_file_name, "wb") as output_file:
            output_file.write(self.hexarray_to_binary()) 
    
    def find_start_track(self, start: int) -> int:
        """Returns the index after the start track and length of the track."""
        #print("searching")
        for index in range(start, len(self.hex_array) - 4):
            if self.read_bytes(index, 4) == self.MTrk: 
                    return index + 7    
        return -1

    def find_end_track(self, start: int) -> int:
        """ Returns the index right after an end of track sequence."""
        for index in range(start, len(self.hex_array) - 3):
            if (self.read_bytes(index, 3) == self.END_TRACK):
                return index + 3
        return -1
    
    def find_byte_sequence(self, start: int, byte_sequence: list) -> int:
        """Returns the index after the start track and length of the track."""
        #print("searching")
        for index in range(start, len(self.hex_array) - len(byte_sequence)):
            if self.read_bytes(index, len(byte_sequence)) == byte_sequence: 
                    return index    
        return -1
    def list_instruments(self) -> dict:
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

    def change_instrument(self, channel: str, instrument_name: str) -> None:
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
    
    def read_bytes(self, start_position: int, number_of_bytes: int) -> list:
        """Read a certain number of bytes from the hex_array starting at
        start position."""
        output = []
        end_position = start_position + number_of_bytes 
        for i in range(start_position, end_position):
            output.append(self.hex_array[i]) 
        return output
    
    def htoi(self, hex_string: str) -> int:
        """Converts a hex_string to an integer."""
        return int(hex_string, 16)

    def read_meta_events(self):
        """Reads all meta events into a dictionary."""
        for type_byte in MetaEvent.TEXT_EVENTS:
            event = MetaEvent(type_byte)
            if (event.read_event(self)):
                self.meta_events[type_byte] = event.data 

class Event:
    """This is a representation of a single event that can be found in a MIDI
    file."""

    def __init__(self, start_byte: str) -> None:
        self.start_byte = start_byte
    
    def htoi(self, hex_string: str) -> int:
        """Converts a hex_string to an integer."""
        return int(hex_string, 16)
    def hex_to_char(self, hex_string: str) -> str:
        """Converts a hex_string to an Unicode charater (string)."""
        return chr(self.htoi(hex_string))

class MIDIEvent(Event):
    """A single MIDI Event."""

    def __init__(self, start_byte: str) -> None:
        super().__init__(start_byte)

class SysExEvent(Event):
    """A single system exclusive Event."""

    def __init__(self, start_byte: str) -> None:
        super().__init__(start_byte)

class MetaEvent(Event):
    """A single Meta Event."""
    #Meta events are of the form ff type length data
   
    TEXT_EVENTS = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]

    def __init__(self, type_byte: str) -> None:
        super().__init__("ff")
        #if type(length) == str:
        #    self.length_hex = length
        #    length = self.htoi(length)
        #else:
        #    self.length_hex = hex(length)[2:]
        self.type = type_byte
        #self.length = length

    def read_event(self, midi: MIDIFile) -> bool:
        """Reads the meta-event from MIDIFile midi."""
        if (self.type in self.TEXT_EVENTS):
            return self.read_event_text(midi)
        else:
            return self.read_event_numeric(midi)

    def read_event_text(self, midi: MIDIFile) -> bool:
        """Reads a text meta-event from MIDIFile midi."""
        #search = [self.start, self.type, self.length_hex]
        search = [self.start_byte, self.type]
        hex_array = midi.hex_array
        start = midi.find_start_track(0)
        position = start
        index = midi.find_byte_sequence(start, search)
        if index == -1:
            return False
        length = self.htoi(midi.hex_array[index + 2])
        data = midi.read_bytes(index + 3, length)
        for i in range(len(data)):
            data[i] = self.hex_to_char(data[i])
        self.data = "".join(data)
        return True

    def read_event_numeric(self, midi: MIDIFile) -> bool:
        """Reads a numeric meta-event from MIDIFile midi."""
        return False


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

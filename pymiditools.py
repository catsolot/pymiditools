from instrument_lookup import instruments

def read_file(input_file):
    """ Read a midi file and returns a list of HEX values representing the bytes."""
    with open(input_file, "rb") as input_file:
        binary_string = input_file.read()
    hex_string = binary_string.hex(" ")
    hex_array = hex_string.split(" ")
    return hex_array

def write_file_helper(output_file, data):
    """Overwrites output_file with data."""
    with open(output_file, "wb") as output_file:
        lines = output_file.write(data)
    return lines 

def hexarray_to_binary(hex_array):
    """Converts an array of HEX values into a binary sting."""
    hex_string = ''.join(hex_array)
    binary_string = bytes.fromhex(hex_string)
    return binary_string

def write_midi(output_file, hex_array):
    write_file_helper(output_file, hexarray_to_binary(hex_array))

def print_instruments(hex_array):


if __name__ == "__main__":
    a = read_file("mary.mid")
    print(a)
    write_midi("mary3.mid", a)

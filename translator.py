def text_to_bits(txt):

    """
    text_to_bits() converts a given text into binary format and returns a variable length list with the text along with its length.
    Each element in the list represents a bit.
    Format of returned list: [<16 bits for length>, <8 bits for first character>, <8 bits of second character>,...]
    """

    steg_lst =[]
    lengt = len(txt)
    binary_lengt = f"{lengt:016b}"                  # Convert the given text's length into binary
    
    for i in binary_lengt:
        steg_lst.append(int(i))

    for i in txt:
        binary_char = f"{ord(i):08b}"
        for j in binary_char:
            steg_lst.append(int(j))

    return steg_lst


def bits_to_text(lst):

    """
    bits_to_text() takes a list of format: [<16 bits for length>, <8 bits for first character>, <8 bits of second character>,...] (Each element in the list represents a bit).
    It converts the given list into the original text that was embedded into the image.
    """

    real_text = []
    length = ""

    for i in range(0, 16):              # Read the first 16 bits to get the length of hidden text
        length += str(lst[i])
    length = int(length, 2)

    total_needed_bits = 16 + length * 8

    if len(lst) < total_needed_bits:
        raise ValueError(
            f"Header indicates length {length} ({total_needed_bits} bits), "
            f"but image only has {len(lst)} bits available. Data may be corrupted."
        )

    for i in range(16, total_needed_bits, 8):
        binary_str = ""

        for j in range(0, 8):
            binary_str += str(lst[i+j])
            
        binary_str = chr((int(binary_str, 2)))
        real_text.append(binary_str)

    real_text = "".join(real_text)
    
    return real_text

if __name__ == "__main__":
    test_msg = "Hello World!"
    encoded = text_to_bits(test_msg)
    decoded = bits_to_text(encoded)
    print("Test passed:", test_msg == decoded)
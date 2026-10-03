def text_to_bits(txt):

    """
    The given function converts a given text into binary format and returns a variable length list with the text along with its length.
    Each element in the list represents a bit.
    Format of returned list: [<16 bits for length>, <8 bits for first character>, <8 bits of second character>,...]
    """

    steg_lst =[]
    lengt = len(txt)
    binary_lengt = f"{lengt:016b}"                  # Convert the given 
    
    for i in binary_lengt:
        steg_lst.append(int(i))

    for i in txt:
        binary_char = f"{ord(i):08b}"
        for j in binary_char:
            steg_lst.append(int(j))

    return steg_lst

print(text_to_bits("Hello!"))
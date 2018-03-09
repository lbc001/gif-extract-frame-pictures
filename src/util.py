'''
define some function to use.
'''

def bytes_to_int(bytes_string, order_type):
    '''
    the bind of the int.from_bytes function.
    '''
    return int.from_bytes(bytes_string, byteorder=order_type)

def bits_to_int(bit_string):
    '''
    the bind of int(string, 2) function.
    '''
    return int(bit_string, 2)
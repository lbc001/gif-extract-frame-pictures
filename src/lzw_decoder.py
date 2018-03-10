'''
the impl of the  decoder of the gif lzw alogrithm.
'''
from .util import bits_to_int

class Decoder:
    '''
    the decoder source code
    '''
    def __init__(self, lzw_minium_size, bytes_string):
        self._lzw_minium_size = lzw_minium_size
        self._bytes_string = bytes_string
        self._current_code_size = self._lzw_minium_size + 1
        self._decode_result = []
        self.generate_code_table()
        self.unpack_code_stream()

    def find_dict_number(self, ch, current_dict):
        '''
        to find the dict number with values
        '''
        for index in current_dict:
            if current_dict[index] == ch:
                return index

    def generate_code_table(self):
        '''
        generate the code table in gif lzw alogrithm.
        '''
        self._clear_code_index = 2**self._lzw_minium_size
        self._end_code_index = 2**self._lzw_minium_size + 1
        self._code_table = dict([(i, [i]) for i in range(self._clear_code_index)])
        self._code_table[self._clear_code_index] = "CLEAR"
        self._code_table[self._end_code_index] = "END"
        self._current_code_table_key_index = self._end_code_index
        self._stream_current_value = ""
        self._stream_prev_value = ""
        self._stream_current_index = 0
        self._stream_prev_index = 0

    def unpack_code_stream(self):
        '''
        unpack the code stream to the bit string.
        '''
        self._unpacked_bit_string = (''.join([format(b, "08b") for b in self._bytes_string]))
        self._length = len(self._unpacked_bit_string)
    
    def decode(self, value):
        '''
        decode the value and store the value in the decode result.
        '''
        if self._stream_current_value == ""  and self._stream_prev_value == "":
            self._stream_prev_value = self._stream_current_value = self._code_table[value]
            self._stream_prev_index = self._stream_current_index = value
            self._decode_result += self._stream_current_value
        else:
            self._stream_current_index = value
            if self._stream_current_index == self._end_code_index:
                return
            if self._stream_current_index in self._code_table:
                self._stream_prev_value = self._code_table[self._stream_prev_index]
                self._stream_current_value = self._code_table[self._stream_current_index][0]
            else:
                self._stream_prev_value = self._code_table[self._stream_prev_index]
                self._stream_current_value = self._code_table[self._stream_prev_index][0]             
            pc_sum = self._stream_prev_value + [self._stream_current_value]
            self._current_code_table_key_index += 1
            self._code_table[self._current_code_table_key_index] = pc_sum
            self._decode_result += self._code_table[self._stream_current_index]
            self._stream_prev_index = self._stream_current_index

    def start(self):
        '''
        seperate the bit string and start the lzw decode process.
        '''
        current = -1 - self._current_code_size + 1
        prev = current
        begin_code = bits_to_int(self._unpacked_bit_string[current:])
        assert(begin_code == self._clear_code_index)
        while abs(current) <= self._length:
            if self._current_code_table_key_index >= (2**self._current_code_size - 1):
                self._current_code_size += 1
            current -= self._current_code_size
            bits_value = self._unpacked_bit_string[current:prev]
            if bits_value == "" or len(bits_value) < self._current_code_size:
                break
            value = bits_to_int(self._unpacked_bit_string[current:prev])
            self.decode(value)
            prev = current
        
    def get_result(self):
        '''
        return the decode result.
        '''
        return self._decode_result

'''
the impl of the gif lzw algorithm. just for a test.
'''
class lzw:
    def __init__(self, data, base_dict):
        self._data = data
        self._dict = base_dict
        self._dict_key = len(base_dict) - 1
        
    def find_dict_number(self, ch, current_dict):
        '''
        to find the dict number with values
        '''
        for index in current_dict:
            if current_dict[index] == ch:
                return index

    def encode(self):
        '''
        encode the data
        '''
        encode_list = []
        encode_dict = dict(self._dict)
        encode_dict_key = self._dict_key
        previous = ""
        current = ""
        for ch in self._data:
            current = ch
            pc_sum = previous + current
            if pc_sum in encode_dict.values():
                previous = pc_sum
            else:
                encode_dict_key += 1
                encode_dict[encode_dict_key] = pc_sum
                encode_list.append(self.find_dict_number(previous, encode_dict))
                previous = current
        encode_list.append(self.find_dict_number(previous, encode_dict))
        return encode_list

    def decode(self, encode_list):
        '''
        decode the packed data.
        '''
        decode_string = ""
        decode_dict = dict(self._dict)
        decode_dict_key = self._dict_key
        previous = current = decode_dict[encode_list[0]]
        p_index = c_index = encode_list[0]
        decode_string += current
        for index in encode_list[1:]:
            c_index = index
            if c_index in decode_dict:
                previous = decode_dict[p_index]
                current = decode_dict[c_index][0]
            else:
                previous = decode_dict[p_index]
                current = decode_dict[p_index][0]
            pc_sum = previous + current
            decode_dict_key += 1
            decode_dict[decode_dict_key] = pc_sum
            decode_string += decode_dict[c_index]
            p_index = c_index
        return decode_string



if __name__ == "__main__":
    import random
    for _ in range(10000):
        example_string = ''.join([chr(random.randint(48, 49)) for _ in range(100)])
        example = lzw(example_string, {0:"0", 1:"1"})
        assert(example.decode(example.encode()) == example_string)
    print("test passed!")

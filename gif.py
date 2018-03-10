#!/usr/bin/env python3
'''
test the gif file structure
'''
import math
import argparse
from PIL import Image
from src import logical_screen_description_block, global_color_table, local_color_table, image_descriptor
from src import plain_text_extension, application_extension, graphic_control_extension, comment_extension
from src import bytes_to_int
from src import Decoder
from src import BEGIN, END, EXTENTION_INTRODUCER


class Reader:
    '''
    read the gif file
    '''
    def __init__(self, file_name):
        self._data = open(file_name, "rb").read()
        self._begin = 0
        self._picture_index = 0

    def read_until(self, end_value):
        while True:
            if self._data[self._begin] == end_value:
                break
            self._begin += 1

    def header_assert(self):
        '''
        assert the file is the gif file
        '''
        assert(self._data[0] == ord("G"))
        assert(self._data[1] == ord("I"))
        assert(self._data[2] == ord("F"))
        self._version = self._data[3:6].decode("utf-8")

    def save_pictures(self, width, height, decode_result, picture_name):
        '''
        save the decoded .gif static data to the .jpg data. 
        '''
        background_color_index = self._logical_screen_description_block.background_color_index
        img = Image.new("RGB", (width, height), self._global_color_table.rgb_list[background_color_index])
        pixels = img.load()
        for i in range(width):
            for j in range(height):
                if self._image_descriptor.local_color_table_flag:
                    pixels[i, j] = self._local_color_table.rgb_list[decode_result[width*i+j]]
                else:
                    pixels[i, j] = self._global_color_table.rgb_list[decode_result[width*i+j]]
        img.save(picture_name)

    def start(self):
        '''
        begin to parse the gif picture.
        '''
        self.header_assert()
        self._logical_screen_description_block = logical_screen_description_block(self._data)
        self._global_color_table_bytes_size = 3 * 2**(self._logical_screen_description_block.global_color_table_size+1)
        self._global_color_table_data = self._data[13:13+self._global_color_table_bytes_size]
        self._global_color_table = global_color_table(self._global_color_table_data, self._global_color_table_bytes_size)
        self._begin = 13 + self._global_color_table_bytes_size
        if self._version == "89a":
            while True:
                if self._data[self._begin] == EXTENTION_INTRODUCER:
                    self._begin += 1
                    if self._data[self._begin] == 0xff:
                        self._application_extension = application_extension(self._data, self._begin)
                        self._begin += 18 # add one \x0 end
                    elif self._data[self._begin] == 0xf9:
                        self._graphic_control_extension = graphic_control_extension(self._data, self._begin)
                        self._begin += 7 # add one \x0 end
                    elif self._data[self._begin] == 0x01:
                        self._plain_text_extension = plain_text_extension(self._data, self._begin)
                        self._begin = self._plain_text_extension.current
                    elif self._data[self._begin] == 0xfe:
                        self._comment_comment_extension = comment_extension(self._data, self._begin)
                        self._begin = self._comment_comment_extension.current
                elif self._data[self._begin] == BEGIN:
                    self._begin += 1
                    self._image_descriptor = image_descriptor(self._data, self._begin)
                    self._begin += 9
                    if self._image_descriptor.local_color_table_flag:
                        self._local_color_table_bytes_size = 3 * 2**(self._image_descriptor.size_of_local_color_table+1)
                        self._local_color_table_data = self._data[self._begin:self._begin+self._local_color_table_bytes_size]
                        self._local_color_table = local_color_table(self._local_color_table_data, self._local_color_table_bytes_size)
                        self._begin += local_color_table_bytes_size
                elif self._data[self._begin] == END:
                    break
                else:
                    blocks_data = b""
                    lzw_minium_size = self._data[self._begin]
                    self._begin += 1
                    while True:
                        block_size = self._data[self._begin]
                        if block_size == 0:
                            break
                        sub_blocks_data = self._data[self._begin+1:self._begin+block_size+1]
                        blocks_data += sub_blocks_data
                        self._begin += block_size + 1
                    self._begin += 1
                    decoder = Decoder(lzw_minium_size, blocks_data[::-1])
                    decoder.start()
                    decode_result = decoder.get_result()
                    assert(len(decode_result) == self._image_descriptor.get_size())
                    self.save_pictures(self._image_descriptor.image_width, self._image_descriptor.image_height, decode_result, "output_{}.jpg".format(self._picture_index))
                    self._picture_index += 1

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--input", help="enter the input file path")
    args = arg_parser.parse_args()
    reader = Reader(args.input)
    reader.start()
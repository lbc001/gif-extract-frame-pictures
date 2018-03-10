'''
api entrance.
'''
from .structure import logical_screen_description_block, global_color_table, local_color_table, application_extension, graphic_control_extension, image_descriptor
from .structure import plain_text_extension, comment_extension
from .lzw_decoder import Decoder
from .util import bytes_to_int

EXTENTION_INTRODUCER = 0x21
BEGIN = 0x2c
END = 0x3b
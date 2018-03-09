'''
define chunk structure
'''
from .util import bytes_to_int

class logical_screen_description_block:
    '''
    define logical screen description block structure.
    '''
    def __init__(self, data):
        self.width = bytes_to_int(data[6:8], "little")
        self.height = bytes_to_int(data[8:10], "little")
        self.package_fields = data[10]
        self.global_color_table_flag = (self.package_fields & 0x80) >> 7
        self.color_plan = (self.package_fields & 0x70) >> 4 
        self.short_flag = (self.package_fields & 0x8) >> 3
        self.global_color_table_size = self.package_fields & 0x7
        self.background_color_index = data[11]
        self.pixel_aspect_ratio = data[12]


class global_color_table:
    '''
    define the global color table structure, usually for rgb list.
    '''
    def __init__(self, data, size):
        self.rgb_list = []
        for i in range(size//3):
            red = data[3*i]
            green = data[3*i+1]
            blue = data[3*i+2]
            self.rgb_list.append((red, green, blue))

class local_color_table:
    '''
    define the local color table structure, usually for rgb list.
    '''
    def __init__(self, data, size):
        self.rgb_list = []
        for i in range(size//3):
            red = data[3*i]
            green = data[3*i+1]
            blue = data[3*i+2]
            self.rgb_list.append((red, green, blue))

class application_extension:
    '''
    define the appliacation extension block structure.
    '''
    def __init__(self, data, begin):
        self.block_size = data[begin+1]
        assert(self.block_size == 11)
        self.application_identifier = data[begin+2:begin+10]
        self.application_proof_code = data[begin+10:begin+13]
        self.sub_block_size = data[begin+13]
        assert(self.sub_block_size == 3)
        assert(data[begin+14] == 0x1)
        self.number_of_loop_time = bytes_to_int(data[begin+15:begin+17], "little")
        assert(data[begin+17] == 0x0)


class graphic_control_extension:
    '''
    define the graphic control extension structure.
    '''
    def __init__(self, data, begin):
        self.block_size = data[begin+1]
        assert(self.block_size == 4)
        self.package_fields = data[begin+2]
        self.reserved = (self.package_fields & 0xc0) >> 6
        self.diposal_method = (self.package_fields & 0x3c) >> 2
        self.user_input_flag = (self.package_fields & 0x2) >> 1
        self.transparent_color_flag = self.package_fields & 0x1
        self.delay_time = bytes_to_int(data[begin+3:begin+5], "little")
        self.transparent_color_index = data[begin+5]
        assert(data[begin+6] == 0x0)

class plain_text_extension:
    '''
    define the plain text extension structure.
    '''
    def __init__(self, data, begin):
        self.sub_blocks = []
        self.current = begin + 1
        while True:
            block_size = data[self.current]
            if block_size == 0:
                break
            self.sub_blocks.append(data[self.current+1:self.current+block_size+1])
            self.current += block_size + 1
        self.current += 1
        
class image_descriptor:
    '''
    define the image descriptor structure.
    '''
    def __init__(self, data, begin):
        self.image_left_position = bytes_to_int(data[begin:begin+2], "little")
        self.image_right_position = bytes_to_int(data[begin+2:begin+4], "little")
        self.image_width = bytes_to_int(data[begin+4:begin+6], "little")
        self.image_height = bytes_to_int(data[begin+6:begin+8], "little")
        self.package_fields = data[begin+8]
        self.local_color_table_flag = (self.package_fields & 0x80) >> 7
        self.interlace_flag = (self.package_fields & 0x40) >> 6
        self.sort_flag = (self.package_fields & 0x20) >> 5
        self.reserved = (self.package_fields & 0x18) >> 3
        self.size_of_local_color_table = self.package_fields & 0x7
    
    def get_size(self):
        '''
        return the pixel nums.
        '''
        return self.image_width * self.image_height
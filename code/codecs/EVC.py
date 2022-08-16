from Codec import Codec
import os
import re
class EVC(Codec):

    def __init__(self, bit_stream_path, output_path):
        super().__init__(bit_stream_path, output_path)


    def encode(self,input,output,preset):

        os.system(f'xeve_app -i RAW_files/{input} -v 3 --preset {preset} -o encoded_files/{output} > TXTs/{input}temp.txt')


    def decode(self,input,output,preset):
        
        os.system(f'xevd_app -i encoded_files/{input} -o decoded_files/{preset}_{output}')
    
    def parse(self):

        pattern = re.compile(r"\d+\s+\d{0,4}\s+\([IB]\)\s+\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\s+\d+")
        parameters_lines = []

        with open(f'TXTs/{self.__output_path}.txt') as temp:

            text = temp.read()
            result = pattern.findall(text)

            for line in range(len(result)):

                    original_data = result[line].split()
                    parsed_data = ([int(original_data[0])]+[original_data[2][1]]+original_data[3:9])
                    parameters_lines.append((parsed_data))

        return sorted(parameters_lines)

    def gen_config(self):
        pass


class Video():
    def __init__(self):
        pass

    def get_format():
        pass

    def yuv_to_y4m(self,input, output):
        ffmpegpath = ''
        input_path = input
        output_path = output
        width = ''
        height = ''
        frate = ''
        pfmt = ''
        cmdline = ffmpegpath + ' -f rawvideo -vcodec rawvideo -s ' + width + 'x' + height + ' -r ' + frate + ' -pix_fmt ' + pfmt
        cmdline += ' -i ' +  input_path + ' ' + output_path + ' -y'
        print(cmdline)
        #os.system(cmdline)
    
    def parse_y4m():
        pass

    def gen_config():
        pass
    
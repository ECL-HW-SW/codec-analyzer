import json

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
    
    def parse_y4m(self, file, name):
        try:
            with open(file, 'rb') as f:
                a = f.readline()
                w = a[a.find(ord('W'))+1 :]
                w = w[:w.find(ord(' '))]
                width = int(w) # get width
                h = a[a.find(ord('H'))+1 :]
                h = h[:h.find(ord(' '))]
                height = int(h) # get height
                fps = a[a.find(ord('F'))+1 :]
                fps = fps[:fps.find(ord(' '))] #get fps
                #print(height, width, fps)
                
        except Exception as e:
            print(f'Erro: {e}')
        
        data = {
            "path": file,
            "name": name,
            "resolution": str(width) + 'x' + str(height),
            "fps": str(fps),
            "framesnumber": 0,
            "format": "YUV420"
        }

        json_object = json.dumps(data, indent=4)
        with open(name+".JSON", "w") as outfile:
            outfile.write(json_object)

    def gen_config():
        pass

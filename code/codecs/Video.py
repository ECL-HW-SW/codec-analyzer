import json
import os

class Video():
    def __init__(self):
        pass

    def get_format():
        pass

    def yuv_to_y4m(self, input, output, res, frate, pfmt="yuv420p"):
        part1 = 'ffmpeg -hide_banner -loglevel error -f rawvideo -vcodec rawvideo '
        part2 = f'-s {res} -r {frate} -pix_fmt {pfmt} -i {input} {output} -y'
        os.system(part1+part2)
    
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

        f = eval(str(fps)[2:-1].replace(':', '/'))
        data = {
            "path": file,
            "name": name,
            "resolution": str(width) + 'x' + str(height),
            "fps": str("%.2f" % f),
            "framesnumber": 0, # contar no arquivo?
            "format": "YUV420" # qual o padrão?
        }

        json_object = json.dumps(data, indent=4)
        with open(name+".JSON", "w") as outfile:
            outfile.write(json_object)

    def gen_config():
        pass

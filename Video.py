import json
import os

from GlobalPaths import GlobalPaths

class Video():

    def __init__(self, video_cfg_path):
        paths = GlobalPaths().get_paths()
        video_data = json.load(open(video_cfg_path, "r"))
        self.__name = video_data["name"]
        self.__resolution = video_data["resolution"]
        self.__fps = video_data["fps"]
        self.__framesnumber = video_data["framesnumber"]
        self.__format = video_data["format"]
        self.__rel_path = video_data["rel_path"].lower()
        self.__abs_path = os.path.join(paths["raw_videos_path"], self.__rel_path)

    def get_format(self):
        return self.__format

    def get_abs_path(self):
        return self.__abs_path

    def get_name(self):
        return self.__name
    
    def get_resolution(self):
      return  self.__resolution 
    
    def get_fps(self):
      return  self.__fps

    def get_framesnumber(self):
      return  self.__framesnumber

    def to_y4m(self):
        output_path = self.__abs_path.replace(".yuv", ".y4m")
        part1 = 'ffmpeg -hide_banner -loglevel error -f rawvideo -vcodec rawvideo '
        part2 = f'-s {self.__resolution} \
                  -r {self.__fps} \
                  -pix_fmt {pfmt} \
                  -i {self.__abs_path} {output_path} -y'
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

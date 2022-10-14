import os

def create_output_dirs(paths, codec_name, *sub_dirs):
    output_dir = os.path.join(paths["output_dir"], codec_name)
    if len(sub_dirs) == 0: sub_dirs = ["default"]
    
    os.makedirs(output_dir, exist_ok = True)      

    for sub_dir in sub_dirs:
        dirs = [_ for _ in paths.keys() if "_dir"  in _ and output_dir not in _]
        
        paths[codec_name] = {}
        for dir in dirs:
            dir_path = os.path.join("./", output_dir, sub_dir, dir )
            paths[codec_name][dir] = dir_path
            os.makedirs(dir_path, exist_ok = True)



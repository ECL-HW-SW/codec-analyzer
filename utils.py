import os

def create_output_dirs(paths, codec_name, video, mode, *sub_dirs):
    output_dir = os.path.join(paths["output_dir"], codec_name)
    if len(sub_dirs) == 0: sub_dirs = ["default"]
    
    os.makedirs(output_dir, exist_ok = True)
    
    if mode == "metrics":
        for metric in ["VMAF","XPSNR", "LPIPS", "MSSIM"]:
            os.makedirs(os.path.join("./", output_dir,"metrics", metric, video), exist_ok=True)
            if metric == "VMAF":
                os.makedirs(os.path.join("./", output_dir,"metrics", metric, video,"averageVMAFs"), exist_ok=True)

    else:    
        for sub_dir in sub_dirs:
            dirs = [paths[_] for _ in paths.keys() if "_dir"  in _ and output_dir not in _]
            paths[codec_name] = {}
            for dir in dirs:
                dir_path = os.path.join("./", output_dir, sub_dir, dir, video)
                paths[codec_name][dir+"_dir"] = dir_path
                os.makedirs(dir_path, exist_ok = True)


###############################################################################
#CHANGE LOG: the name of the directories now are defined by the values instead of the keys of the PATHS JSON.
#The resulting files will now be stored inside a folder named after the video
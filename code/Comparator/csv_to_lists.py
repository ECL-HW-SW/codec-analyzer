import csv
import os
from importlib.resources import path
 #returns 2 lists, the first one with the bitrates, and the second with the psnr
 #mode 1 gets a csv list with values from more than 1 video, the video name must be the first value in each line, and must be specified as an argument
 #mode 0 gets a path with a bunch of lists, each containing the values of only one video, where bitrate is in the first position and psnr is in te second
def csv2lists(csv_path,mode = 0, video_name = ''):
    bitrate = []
    psnr = []
    if mode == 1:
        with open(csv_path, 'r') as csv_input:
            csv_reader = csv.DictReader(csv_input, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    if row != []:
                        if row['video'] == video_name:
                            bitrate.append(row['bitrate'])
                            psnr.append(row['psnr'])
                line_count += 1
    else:
        for filecod in os.listdir(csv_path):
            if path.endswith("/"):
                fullpath = path + filecod
            else:
                fullpath = path + '/' + filecod
            with open(fullpath, 'r') as csv_input:
                csv_reader = csv.DictReader(csv_input, delimiter=',')
                for row in csv_reader:
                    bitrate.append(row["bitrate"])
                    psnr.append(row["psnr"])
    floats_bitrate = [float(x) for x in bitrate]
    floats_psnr = [float(x) for x in psnr]         
    return floats_bitrate, floats_psnr
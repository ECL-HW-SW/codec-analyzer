import csv
import os

class ParserVTM_VVcodec:
    """Class for parsing VTM and VVcodec text outputs"""
    
    def __init__(self):
        pass

    def parse(self, textpath):
        with open(textpath, 'r') as txt:
            text = txt.read().split("\n")
            for line in text:
                if "YUV-PSNR" in line.split():
                    data_line = text[text.index(line)+1].split()
                    break
            txt.close()
            bitrate = data_line[2]
            psnr = data_line[6]
            line_time = text[-2].split()
            total_time = line_time[2]

        return bitrate, psnr, total_time

    def add_to_csv(self, csvpath, video, res,
                    nframes, qsize, bitrate, psnr,
                    optional_settings, total_time):
        with open(csvpath, 'a') as csv:
            writer_object = csv.writer(csv)

            if os.stat(csvpath).st_size() == 0:
                writer_object.writerow(["VTM", "Video Name", "Resolution",
                                            "Number of Frames", "Quantization Parameter",
                                            "Bitrate", "YUV-PSNR", "Optional Settings",
                                            "Total Time Taken to Encode"])

            writer_object.writerow(["VTM", video, res, nframes, qsize, bitrate, psnr,
                                        optional_settings, total_time])
            csv.close()           

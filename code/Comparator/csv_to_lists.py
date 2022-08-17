import csv
 #returns 2 lists, the first one with the bitrates, and the second with the psnr
 #mode 1 gets a csv list with values from more than 1 video, the video name must be the first value in each line, and must be specified as an argument
 #mode 0 gets a path with a bunch of lists, each containing the values of only one video, where bitrate is in the first position and psnr is in te second
def csv2lists(csv_path,mode = 0, video_name = ''):
    bitrate = []
    psnr = []
    if (not (mode == 1)):
        for file in csv_path:
            with open(file, 'r') as csv_input:
                csv_reader = csv.reader(csv_input, delimiter=',')
                for row in csv_reader:
                    bitrate.append(row[0])
                    psnr.append(row[1])
    if mode == 1:
        with open(csv_path, 'r') as csv_input:
            csv_reader = csv.reader(csv_input, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    if row != []:
                        if row[2] == video_name:
                            bitrate.append(row[4])
                            psnr.append(row[3])
                line_count += 1
    floats_bitrate = [float(x) for x in bitrate]
    floats_psnr = [float(x) for x in psnr]         
    return floats_bitrate, floats_psnr
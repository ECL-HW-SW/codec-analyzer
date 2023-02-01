import csv
import numpy as np
import scipy.interpolate
import os
from importlib.resources import path
from pathlib import Path

class CodecComparator():

    def __init__(self):
        pass

    def bdrate(self, input1, input2):
        bitrate1 , psnr1 = self.csv2lists(input1)
        print("BITRATE1, PSNR1:",bitrate1, psnr1)
        bitrate2, psnr2 = self.csv2lists(input2)
        print("BITRATE2, PSNR2:",bitrate2, psnr2)        
        bdrate = self.BD_RATE(bitrate1,psnr1,bitrate2,psnr2)
        return bdrate

    def bdpsnr(self, input1, input2):
        bitrate1 , psnr1 = self.csv2lists(input1)
        bitrate2, psnr2 = self.csv2lists(input2)
        bdpsnr = self.BD_PSNR(bitrate1,psnr1,bitrate2,psnr2)
        return bdpsnr

#the methods bellow are used by the previous ones

    def csv2lists(self,csv_path,mode = 0, video_name = ''):
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
            p = Path('~').expanduser()
            csv_path = csv_path.replace("~",str(p))
            for filecod in os.listdir(csv_path):
                if csv_path.endswith("/"):
                    fullpath = csv_path + filecod
                else:
                    fullpath = csv_path + '/' + filecod
                with open(fullpath, 'r') as csv_input:
                    csv_reader = csv.DictReader(csv_input, delimiter=',')
                    for row in csv_reader:
                        bitrate.append(row["bitrate"])
                        psnr.append(row["psnr"])
                        break
        floats_bitrate = [float(x) for x in bitrate]
        floats_psnr = [float(x) for x in psnr]         
        
        return floats_bitrate, floats_psnr

#the following code was taken from https://github.com/shengbinmeng/Bjontegaard_metric/blob/master/bjontegaard_metric.py

    def BD_PSNR(self,R1, PSNR1, R2, PSNR2, piecewise=0):
        lR1 = np.log(R1)
        lR2 = np.log(R2)

        p1 = np.polyfit(lR1, PSNR1, 3)
        p2 = np.polyfit(lR2, PSNR2, 3)

        # integration interval
        min_int = max(min(lR1), min(lR2))
        max_int = min(max(lR1), max(lR2))

        # find integral
        if piecewise == 0:
            p_int1 = np.polyint(p1)
            p_int2 = np.polyint(p2)

            int1 = np.polyval(p_int1, max_int) - np.polyval(p_int1, min_int)
            int2 = np.polyval(p_int2, max_int) - np.polyval(p_int2, min_int)
        else:
            # See https://chromium.googlesource.com/webm/contributor-guide/+/master/scripts/visual_metrics.py
            lin = np.linspace(min_int, max_int, num=100, retstep=True)
            interval = lin[1]
            samples = lin[0]
            v1 = scipy.interpolate.pchip_interpolate(np.sort(lR1), np.sort(PSNR1), samples)
            v2 = scipy.interpolate.pchip_interpolate(np.sort(lR2), np.sort(PSNR2), samples)
            # Calculate the integral using the trapezoid method on the samples.
            int1 = np.trapz(v1, dx=interval)
            int2 = np.trapz(v2, dx=interval)

        # find avg diff
        avg_diff = (int2-int1)/(max_int-min_int)

        return avg_diff


    def BD_RATE(self,R1, PSNR1, R2, PSNR2, piecewise=0):
        lR1 = np.log(R1)
        lR2 = np.log(R2)

        # rate method
        p1 = np.polyfit(PSNR1, lR1, 3)
        p2 = np.polyfit(PSNR2, lR2, 3)

        # integration interval
        min_int = max(min(PSNR1), min(PSNR2))
        max_int = min(max(PSNR1), max(PSNR2))

        # find integral
        if piecewise == 0:
            p_int1 = np.polyint(p1)
            p_int2 = np.polyint(p2)

            int1 = np.polyval(p_int1, max_int) - np.polyval(p_int1, min_int)
            int2 = np.polyval(p_int2, max_int) - np.polyval(p_int2, min_int)
        else:
            lin = np.linspace(min_int, max_int, num=100, retstep=True)
            interval = lin[1]
            samples = lin[0]
            v1 = scipy.interpolate.pchip_interpolate(np.sort(PSNR1), np.sort(lR1), samples)
            v2 = scipy.interpolate.pchip_interpolate(np.sort(PSNR2), np.sort(lR2), samples)
            # Calculate the integral using the trapezoid method on the samples.
            int1 = np.trapz(v1, dx=interval)
            int2 = np.trapz(v2, dx=interval)

        # find avg diff
        avg_exp_diff = (int2-int1)/(max_int-min_int)
        avg_diff = (np.exp(avg_exp_diff)-1)*100

        return avg_diff


from subprocess import run
from statistics import mean
#from skvideo.measure import msssim
import PIL.Image as im
import numpy as np
import os
import csv
#import cv2

class MetricsCalculator():
    """ 
    Class for calculating image/video comparison metrics
    such as MSSSIM, VMAF, LPIPS, X-PNSR, and others.
    """

    def __init__(self):
        pass

#XPSNR CURRENTLY NOT WORKING
    def xpsnr(self, videoref: str, videodis: str, output: str) -> float:
        ffmpegpath = 'ffmpeg'
        cmdline = ffmpegpath + " -i " + videoref + " -i " + videodis + ' -lavfi xpsnr="stats_file=' + output + '.log" -f null -'
        os.system(cmdline)   

    def vmaf(self, videoref: str , videodis: str, output: str) -> float:
        vmafpath = 'vmaf'
        cmdline = vmafpath + " -r " + videoref + " -d " + videodis + " -o " + output + ".csv --csv"
        os.system(cmdline)

    def vmaf_parse(self, ogcsvpath):
        data = []
        for csvfile in os.listdir(ogcsvpath):
            if csvfile.endswith(".csv"):
                with open(os.path.join(ogcsvpath,csvfile), newline="") as csv_input:
                    spamreader = csv.reader(csv_input, delimiter=",", quotechar="|")
                    next(spamreader)
                    vmaf_values = []
                    for row in spamreader:
                        vmaf_values.append(float(row[-2]))          
                    avg_vmaf = mean(vmaf_values)
                    string = os.path.splitext(csvfile)[0]+","+ str(avg_vmaf)
                    data += [tuple(i.split(",")) for i in string.split("\n") if i]
                    csv_input.close()
        with open(ogcsvpath+"/averageVMAFs/pathavg_vmaf.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["name","avg_vmaf"])
            writer.writerows(data)
            csvfile.close()    

    def lpips(self, videoref: str, videodis: str) -> float:
        cmdline = f"python3.7 ~/VC/tools/PerceptualSimilarity/lpips_2imgs.py \
                        -p0  {videoref} -p1 {videodis}"
        lpips = run([cmdline], shell=True, capture_output=True).stdout\
                    .decode('utf-8').split('\n')[-2].split()[-1]        
        return lpips

    """
    Calculates the Multi-Scale Structural Similarity Index for Motion Detection (MS-SSIM).

    Given the paths of original and decoded frames, transforms said frames into luminance arrays
    and then calculates their MS-SSIM.

    @param imref: path for the original frame
    @param imdis: path for the decoded frame
    @return MS-SSIM
    """
#    def msssim(self, imref: str, imdis: str) -> float:
#        original_array_luminance = self.__get_image_array(imref, "y", "cv2")
#        decoded_array_luminance = self.__get_image_array(imdis, "y", "cv2")
#
#        ssim_ms = msssim(original_array_luminance, decoded_array_luminance, 'product')[0]
#        return ssim_ms
#
#    """
#    Private methods below           
#    """
#
#    def __get_image_array(self, path, color_space, package = 'PIL'):
#        """Acquires numpy array from an image using either PIL or CV2"""
#
#        if package.lower() == 'pil':
#            if color_space.lower() == "rgb":
#                imgArray = np.array(im.open(path))
#            elif color_space.lower() == "ycbcr":
#                imgArray = np.array(im.open(path).convert('YCbCr'))
#            else:
#                print("That is not a valid color space.")
#        elif package.lower() == 'cv2':
#            if color_space.lower() == "rgb":
#                imgArray = cv2.imread(path, 1)
#            elif color_space.lower() == "ycbcr":
#                imgArray = cv2.cvtColor(cv2.imread(path, 1), cv2.COLOR_BGR2YCR_CB)
#            elif color_space.lower() == "y":
#                imgArray = cv2.cvtColor(cv2.imread(path, 1), cv2.COLOR_BGR2YCR_CB)
#                return imgArray[:,:,0]
#            else:
#                print("That is not a valid color space.")
#        
#        return imgArray
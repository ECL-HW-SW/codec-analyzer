import csv
from csv_to_lists import csv2lists
import bjoontegaard_metric 
class comparator():

    def __init__(self):
        pass

    def bdrate(self, input1, input2):
        bitrate1 , psnr1 = csv2lists(input1)
        bitrate2, psnr2 = csv2lists(input2)
        bdrate = bjoontegaard_metric.BD_RATE(bitrate1,psnr1,bitrate2,psnr2)
        return bdrate

    def bdpsnr(self, input1, input2):
        bitrate1 , psnr1 = csv2lists(input1)
        bitrate2, psnr2 = csv2lists(input2)
        bdpsnr = bjoontegaard_metric.BD_PSNR(bitrate1,psnr1,bitrate2,psnr2)
        return bdpsnr

    
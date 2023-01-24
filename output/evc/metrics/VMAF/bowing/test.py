import csv
import os
from statistics import mean

ogcsvpath = "output/evc/metrics/VMAF/bowing"

for csvfile in os.listdir(ogcsvpath):
    if csvfile.endswith(".csv"):
        with open(os.path.join(ogcsvpath,csvfile), newline="") as csv_input:
            spamreader = csv.reader(csv_input, delimiter=",", quotechar="|")
            next(spamreader)
            vmaf_values = []
            for row in spamreader:
                vmaf_values.append(float(row[-2]))          
            avg_vmaf = mean(vmaf_values)
        print(os.path.splitext(csvfile)[0]+" VMAF: "+ str(avg_vmaf))
    
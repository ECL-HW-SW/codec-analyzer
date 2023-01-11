
texto = "safoda/bowing_22qp_30fr.txt"

def parse(pt1,pt2):
    BR_STRING = 'Total Frames	Average QP  	Y-PSNR   	U-PSNR   	V-PSNR		| 	Y-PSNR   	U-PSNR   	V-PSNR   	|	Y-SSIM   	U-SSIM   	V-SSIM   	|	Bitrate\n'
    with open(pt1, 'r') as output_text:
        out_string = output_text.readlines()
        results_index = (out_string.index(BR_STRING) + 1)
        bitrate = float(out_string[results_index].split()[20])
        psnry = float(out_string[results_index].split()[2])
        psnru = float(out_string[results_index].split()[4])
        psnrv = float(out_string[results_index].split()[6])
        psnryuv = float("{:.2f}".format((4*psnry + psnru +psnrv)/6))

    with open(pt2, 'rt') as outtime_text:
        outtime_string = outtime_text.readlines()
    for strtime in outtime_string:
        if not strtime.startswith("Total Encoding Time"):
            continue
        timems_string = float(strtime.split()[3])
    return bitrate*1024, psnryuv, psnry, psnru, psnrv, timems_string

print(parse(texto))
def parse_svt_output(pt1,pt2):
    BR_STRING = 'Total Frames	Average QP  	Y-PSNR   	U-PSNR   	V-PSNR		| 	Y-PSNR   	U-PSNR   	V-PSNR   	|	Y-SSIM   	U-SSIM   	V-SSIM   	|	Bitrate\n'
    with open(pt1, 'rt') as output_text:
        out_string = output_text.readlines()
        results_index = (out_string.index(BR_STRING) + 1)
        bitrate_string = out_string[results_index].split()[20]
        psnr_string = out_string[results_index].split()[2]
    with open(pt2, 'rt') as outtime_text:
        outtime_string = outtime_text.readlines()
    for strtime in outtime_string:
        if not strtime.startswith("Total Encoding Time"):
            continue
        timems_string = strtime.split()[3]
    return float(bitrate_string)*1024, float(psnr_string) , float(timems_string)

def parse_aom_output(st):
    with open(st, 'rt') as output_text:
        out_string = output_text.readlines()
        for line in out_string:
            if (line.startswith("Stream")):
                bitrateaom_string = line.split()[9]
                psnr_stringaom = line.split()[5]
                ms_stringaom = line.split()[11]
    return float(bitrateaom_string), float(psnr_stringaom), float(ms_stringaom)
import os

cmdline = "ffmpeg -i teste/akiyo_27qp_30fr_29.97fps_medium-preset_4t.y4m -i teste/bowing_cif.y4m -lavfi xpsnr=stats_file=xpsnr.log - f null -" 
os.system(cmdline)
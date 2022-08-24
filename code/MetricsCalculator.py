class metrics():

    def __init__(self):
        pass

    def xpsnr(self,rawvideo, y4m_decoded, output):
        videoref = rawvideo
        videodis = y4m_decoded
        ffmpegpath = ''
        output = output
        cmdline = ffmpegpath + " -i " + videoref + " -i " + videodis + ' -lavfi xpsnr="stats_file=' + output + '" -f null -'
        print(cmdline)
        #os.system(cmdline)    

    def vmaf(self, y4m_decoded, output):
        videoref = self.raw
        videodis = y4m_decoded
        vmafpath = ''
        output = output
        cmdline = vmafpath + " -r " + videoref + " -d " + videodis + " -o " + output +  " --csv"
        print(cmdline)
        #os.system(cmdline)
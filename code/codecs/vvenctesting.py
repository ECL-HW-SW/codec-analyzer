from VVcodec import VVcodec

vvenc = VVcodec("~/VC/data/video-samples/BasketballPass_416x240_50.yuv")
vvenc.encode("BasketballPass_416x240_50.yuv", "vvencout_BasketballPass.bin", "faster")
print("encoded")
vvenc.decode("vvencout_BasketballPass.bin", "decoded_BasketballPass.yuv", "faster")
print("decoded\n\n\n")

bitrate, psnr, timems = vvenc.parse("BasketballPass_416x240_50.yuv.txt", "faster")
vvenc.add_to_csv(bitrate, psnr, timems)

print("End of tests.")
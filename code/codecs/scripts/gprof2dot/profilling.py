import os

os.system("sudo perf record -g -- ~/VC/tools/vvenc/bin/debug-static/vvencapp")
os.system("perf script | c++filt | gprof2dot -f perf | dot -Tpng -o vvenc_methods.png")
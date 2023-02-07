#from EVC import EVC
from video_codecs.VVcodec import VVcodec
from GlobalPaths import GlobalPaths
import utils
from Video import Video
from HttpContent import HttpContent
from video_codecs.EncodingConfig import EncodingConfig

"""
NOTE: 
This is a sample script for performing a series of encoding operations, then sending the information to the server.
The http operations of authenticating and logging out SHOULD NOT BE CHANGED! They are necessary to ensure working conditions.
Change the parameters and configurations if needed, or add/remove some Codecs.
"""

# NOTE: declaring PATHS should be the first thing, or else the script breaks
# (we should probably change that) 
PATHS = GlobalPaths("config/Paths.JSON").get_paths()

# stores video information to be used in the encoding process
video = Video("config/Bowing.JSON")
# the codecs 
vvenc = VVcodec("config/VVEnc.JSON", "ec44ee022959410f9596175b9424d9fe1ece9bc8", video=video)

# declaring configs, paths, and codecs to be used 
CODECS = [vvenc]
QPS = [22,27,32,37]
NFRAMES = 30
NTHREADS = 2
# PRESETS = ["faster", "fast", "medium", "slow", "slower"]
PRESETS = ["faster"]
FPS = 29.97

# http for sending queries to the server
http = HttpContent("http://localhost:8080/api/codec-database")

http.authenticate("creds.json")

for codec in CODECS:
    codec.set_threads(NTHREADS)
    
    for preset in PRESETS:
        utils.create_output_dirs(PATHS, codec.get_codec(), preset, "")
        
        for qp in QPS:
            # EncodingConfig is a dataclass that stores all relevant configs  
            config = EncodingConfig(qp, NFRAMES, FPS, preset, NTHREADS, "")
            
            codec.set_encoding_config(config)
            codec.set_video(video)

            # hasEntry returns an empty response body if there is no entry - this is equivalent to a `False` value
            # -------
            # check docstring on HttpContent or the docs on codec-analyzer-api (github, not the same repo)
            # to see why these params are important
            response = http.hasEntry(
                codec.get_commit_hash(),
                codec.get_video().get_unique_attrs(),
                codec.get_encoding_config().get_unique_attrs()
            )

            # if there is no response (empty body), encode video 
            if not response:
                codec.encode(force_rerun=1)
                # codec.add_to_csv(video) 
                # info = codec.get_encoding_info()

                # POSTs the encoding result into the server, prints the response (200 = OK)
                response = http.POST_encoding_result(codec, codec.get_results())
                print(response)

# Prints all the saved results in JSON format 
print(http.GET_all_encoding_results())
# Logs out of the server (THIS IS IMPORTANT!)
http.logout()

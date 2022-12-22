import requests
import json
import ast

class HttpContent:
    """
    A Class for handling all the HTTP requests to the Codec Analyzer Database.

    It works by gathering the input in the form of a list and transforming it into a Python dict 
    so that it can then be parsed as JSON and sent.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def GET(self) -> list:
        response = requests.get(self.base_url)
        return ast.literal_eval(response.text)

    def POST(self, codec: str, video: str, resolution: str,
                fps: float, nframes: int, qp: int, ypsnr: float,
                upsnr: float, vpsnr: float, yuvpsnr: float,
                bitrate: float, time: float) -> requests.Response:
        payload = json.dumps({
            "codec": codec,
            "video": video,
            "resolution": resolution,
            "fps": fps,
            "nFrames": nframes,
            "qp": qp,
            "yPSNR": ypsnr,
            "uPSNR": upsnr,
            "vPSNR": vpsnr,
            "yuvPSNR": yuvpsnr,
            "bitrate": bitrate,
            "time": time
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", self.base_url, headers=headers, data=payload)
        return response
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


    def POST(self, info: dict) -> requests.Response:
        payload = json.dumps({
            "codec": info["codec"],
            "video": info["video"],
            "resolution": info["resolution"],
            "fps": info["fps"],
            "nFrames": info["nFrames"],
            "qp": info["qp"],
            "yPSNR": info["ypsnr"],
            "uPSNR": info["upsnr"],
            "vPSNR": info["vpsnr"],
            "yuvPSNR": info["yuvpsnr"],
            "bitrate": info["bitrate"],
            "time": info["time"]
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", self.base_url, headers=headers, data=payload)
        return response
    

    def PUT(self, id: str, info: dict) -> requests.Response:
        payload = json.dumps({
            "codec": info["codec"],
            "video": info["video"],
            "resolution": info["resolution"],
            "fps": info["fps"],
            "nFrames": info["nFrames"],
            "qp": info["qp"],
            "yPSNR": info["ypsnr"],
            "uPSNR": info["upsnr"],
            "vPSNR": info["vpsnr"],
            "yuvPSNR": info["yuvpsnr"],
            "bitrate": info["bitrate"],
            "time": info["time"]
        })
        url = self.base_url + f"/{id}"
        headers = {'Content-Type': 'application/json'}
        response = requests.request("PUT", url, headers=headers, data=payload)
        return response
    

    def DELETE(self, id: str) -> requests.Response:
        url = self.base_url + f"/{id}"
        headers = {'Content-Type': 'application/json'}
        response = requests.request("DELETE", url, headers=headers)
        return response

    
    """
    GETTERS AND SETTERS BELOW
    """

    def set_base_url(self, base_url: str) -> None:
        self.base_url = base_url

    def get_base_url(self) -> str:
        return self.base_url
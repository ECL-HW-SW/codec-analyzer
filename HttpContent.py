import requests
import json
import ast


"""A Class for handling all the HTTP requests to the Codec Analyzer Server"""
class HttpContent:
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.__access_token = None
        self.__refresh_token = None


    """
    Logs out of the server. Must be used after all the other methods, to ensure safety and functionality.

    @returns the request status code (204 if successful)
    """
    def logout(self) -> int:
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", "http://localhost:8080/logout", headers=headers)
        return response.status_code 


    """
    Refreshes the access token using the refresh token

    @returns the request status code (200 if successful)
    """
    def refresh_token(self) -> int:
        headers = {'Content-Type': 'application/json'}
        payload = {'refreshToken': self.__refresh_token}
        response = requests.request("POST", f"{self.base_url}/auth/refresh", headers=headers, data=payload)
        json_response = json.loads(response.content)
        self.__refresh_token = json_response["refreshToken"]
        self.__access_token = json_response["token"]
        return response.status_code

    
    """
    Method used for user authentication in the API

    @params credentials: filename where the credentials (email and password) are stored. 
        |--> can't risk other people seeing credentials on an open source project :P
             NOTE: must be in JSON format! 
    """
    def authenticate(self, credentials: str) -> None:
        with open(credentials, "r") as creds:
            json_creds = json.loads(creds.read())
            self.__POST_auth(json_creds)


    """
    Private method used to send the authentication request to the API
    This is only meant to be used inside `self.authenticate()`

    @params creds: the JSON-style string, read from the credentials file
    """
    def __POST_auth(self, creds: dict) -> None:
        url = f"http://localhost:8080/login"
        payload = json.dumps({
          "email": creds["email"],
          "password": creds["password"]
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)       
        response = json.loads(response.content)
        self.__access_token = response["token"]
        self.__refresh_token = response["refreshToken"]


    """
    Checks if there is an entry with the given parameters as columns in the Database
    
    @param str unique_config: unique configuration string to represent the codification process
    @param str commit_hash: the github commit hash for the codec
    @returns bool
    """
    def hasEntry(
        self, commitHash, uniqueVideoAttrs, uniqueConfigAttrs
    ) -> dict:
        url = f"{self.base_url}/encoding-results/has-entry/{uniqueVideoAttrs}/{uniqueConfigAttrs}/{commitHash}"
        headers = {'Authorization': f'Bearer {self.__access_token}'}
        response = requests.request("GET", url, headers=headers, data={})
        return json.loads(response.content or 'null')

    # NOTE to self:
    # should the Codec class really be the one containing the Video and EncodingResult? 
    # would it not be better for them to be separate? Something to think about.

    """
    Saves the EncodingResult on the database, 
    mapping the entities with their respective Python classes in a 1:1 relationship.

    @params codec: Codec
    @params results: EncodingResult
    @returns requests.Response 
    """
    def POST_encoding_result(self, codec, results) -> requests.Response: 
        video = codec.get_video()
        encoding_config = codec.get_encoding_config()

        payload = json.dumps({
            "codec": codec.to_dict(),
            "video": encoding_config.to_dict(),
            "encodingConfig": encoding_config.to_dict(),
            "ypsnr": results["ypsnr"],
            "upsnr": results["upsnr"],
            "vpsnr": results["vpsnr"],
            "yuvpsnr": results["yuvpsnr"],
            "bitrate": results["bitrate"],
            "time": results["time"],
            "energyConsumption": results["energyConsumption"] 
        })
        headers = {
            'Authorization': f'Bearer {self.__access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", f"{self.base_url}/encoding-results", headers=headers, data=payload)
        return response


    """
    Gets all the saved EncodingResults from the Database and returns them in the form of of a list

    @returns list of all available EncodingResults
    """
    def GET_all_encoding_results(self) -> list:
        headers = {'Authorization': f'Bearer {self.__access_token}'}
        response = requests.request("GET", f"{self.base_url}/encoding-results", headers=headers)
        return json.loads(response.text)
    

    """
    Deletes an EncodingResult from the Database. 
    This should only be done in case of a wrong configuration, or something of the sort,
    so that the data goes unaldutered. 

    @param id: the specific EncoidngResult ID, generated by the server
    @returns the status code of the response 
    """
    def DELETE_encoding_result(self, id: str) -> int:
        url = self.base_url + f"/{id}"
        headers = {
            'Authorization': f'Bearer {self.__access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("DELETE", url, headers=headers)
        return response.status_code
    

    """GETTERS AND SETTERS"""
    def set_base_url(self, base_url: str) -> None:
        self.base_url = base_url


    def get_base_url(self) -> str:
        return self.base_url


    def is_authenticated(self) -> bool:
        return True if self.__access_token else False
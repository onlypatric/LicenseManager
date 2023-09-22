from requests import post

class ClientWrapper:
    def __init__(self,url) -> None:
        self.url = url
    def checkLicense(self, uuid):
        return post(f"{self.url}/activate/{uuid}").json()
import json

class Image:
    url: str

    def __init__(self, url):
        self.url = url
    
    def __repr__(self):
        return { "url": self.url }

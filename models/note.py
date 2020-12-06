import json

class Note:
    title: str
    description: str

    def __init__(self, title, description):
        self.title = title
        self.description = description
    
    def __repr__(self):
        return { "title": self.title, "description": self.description }

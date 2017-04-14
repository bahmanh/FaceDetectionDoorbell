import requests 
from facepy import GraphAPI
import json

class Facebook(object):

    def __init__(self, token):
        self.token = token
        self.graph = GraphAPI(self.token)

    def upload_photo(self, filepath):
        try:
            response = self.graph.post(path='me/photos', source=open(filepath, 'rb'))
        except Exception as e:
            raise e
        return response

    def delete_photo(self, post_id):
        try:
            response = self.graph.delete(path=post_id)
        except Exception as e:
            raise e
        return response

    def recognize_faces(self, filepath):
        post_id = upload_photo(filepath)['id']
        delete_photo(post_id)


    def parse_names(fb_response):



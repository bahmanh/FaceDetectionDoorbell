from facepy import GraphAPI
import requests 
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

    def recognize_faces(self, filepath, cookie, fb_dtsg):
        post_id = self.upload_photo(filepath)['id']
        URL = "https://www.facebook.com/photos/tagging/recognition/"
        headers = {
                'accept':'*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language':'en-US,en;q=0.8',
                'content-type':'application/x-www-form-urlencoded',
                'cookie':'l',
                'origin':'https://www.facebook.com',
                'referer':'https://www.facebook.com/',
                'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'x_fb_background_state':'1'
        }
        payload = {
                'dpr':'1',
                'recognition_project':'composer_facerec',
                'photos[0]':post_id,
                'target':'',
                'is_page':'false',
                'include_unrecognized_faceboxes':'false',
                'include_face_crop_src':'false',
                'include_recognized_user_profile_picture':'false',
                'include_low_confidence_recognitions':'true',
                '__a':'1',
                'fb_dtsg': fb_dtsg
            }

        response = requests.post(URL, headers=headers, data=payload)
        names = self.parse_names(response.text)
        self.delete_photo(post_id)
        

    def parse_names(fb_response):
        return



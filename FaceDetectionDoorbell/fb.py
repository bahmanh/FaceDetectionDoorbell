from facepy import GraphAPI
import requests 
import json
import time

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
                'accept-encoding': 'gzip, deflate',
                'accept-language':'en-US,en;q=0.8',
                'content-type':'application/x-www-form-urlencoded',
                'cookie':cookie,
                'origin':'https://www.facebook.com',
                'referer':'https://www.facebook.com/',
                'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'x_fb_background_state':'1'
        }
        params = {
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

        payload = None
        
        while not payload:
            response = requests.post(URL, headers=headers, data=params)
            # [9:] in order to skip 'for (;;);' to make string JSON compatible
            payload = json.loads(response.text[9:])['payload']
            response.raise_for_status()
            time.sleep(1)

        self.delete_photo(post_id)
        return self.parse_names(payload[0])
        

    def parse_names(self, fb_response):
        names = {}
        faceboxes = fb_response['faceboxes']
        for face in faceboxes:
            for recognition in face['recognitions']:
                names[recognition['user']['name']]= recognition['certainty'] 
        return names

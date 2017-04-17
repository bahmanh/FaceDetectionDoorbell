import picamera
from fb import Facebook
from messenger import Messenger
from credentials import FB_KEY, FB_COOKIE, FB_DTSG


phone_number = 0000000000;
camera = picamera.PiCamera()
camera.capture('image.jpg')

fb = Facebook(FB_KEY)
names = fb.recognize_faces('image.jpg', FB_COOKIE, FB_DTSG)

message = '\n'.join(names.keys())

if len(names.keys()) == 1:
    message += '\nis at the door.'
elif len(names.keys()) > 1:
    message += '\nare at the door'
elif len(names.keys()) == 0:
    message += 'Unrecognized person(s) at the door'

mess = Messenger()
mess.send_text(message, phone_number)

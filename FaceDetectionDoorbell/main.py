import picamera
from fb import Facebook
from messenger import Messenger
from credentials import FB_KEY, FB_COOKIE, FB_DTSG
from scapy.all import *

MAC_ADDRESS = '' # enter Dash Button's MAC Address here.
phone_number = 0000000000 #enter phone number to send text to here. Must be verified with Twilio
camera = picamera.PiCamera()

def transaction():
    camera.capture('image.jpg')
    print "Photo taken"

    fb = Facebook(FB_KEY)
    names = fb.recognize_faces('image.jpg', FB_COOKIE, FB_DTSG)

    message = '\n'.join(names.keys())

    if len(names.keys()) == 1:
        message += '\nis at the door.'
    elif len(names.keys()) > 1:
        message += '\nare at the door'
    elif len(names.keys()) == 0:
        message += 'Unrecognized person(s) at the door'

    print message
    mess = Messenger()
    mess.send_text(message, phone_number)

def detect_button(pkt):
    if pkt.haslayer(DHCP) and pkt[Ether].src == MAC_ADDRESS:
            print "Button Press Detected"
            transaction()

sniff(prn=detect_button, filter="(udp and (port 67 or 68))", store=0)
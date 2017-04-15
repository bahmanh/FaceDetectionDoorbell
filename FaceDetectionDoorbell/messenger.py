from twilio.rest import Client
from credentials import ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER

class Messenger():
	
	def __init__(self):
		self.client = Client(ACCOUNT_SID, AUTH_TOKEN)
	
	# message you wish to send, target phone number
	# phone number must be verified through twilio
	def send_text(self,msg,mynum):
		message = self.client.messages.create(
			body=msg,
			to=mynum,
			from_= TWILIO_NUMBER
		)
		print(message.sid)
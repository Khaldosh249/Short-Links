import requests
import os
from dotenv import load_dotenv
load_dotenv()


def send_reset_password(email:str , link:str ):
    requests.post(
		"https://api.mailgun.net/v3/eltech.sd/messages",
		auth=("api", os.getenv('MAIL_GUN_API_KEY')),
		data={"from": "Confirm <confirm@eltech.sd>",
			"to": [email], #"kha09128857@gmail.com"
			"subject": "Reset your Password",
			"text": f"Click here {link}"})
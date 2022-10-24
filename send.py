import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

def time_run_notification(minutes):
	second = 60
	cal = second * minutes
	return cal

time_run_notification(4)

def telegram_bot_sendtext(bot_message):
   bot_token  = os.environ.get("BOT_TOKEN")
   bot_chatID = os.environ.get("BOT_CHATID")
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + bot_message

   response = requests.get(send_text)
   return response.json()


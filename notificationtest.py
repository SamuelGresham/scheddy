import consts
import requests

url = 'https://api.pushover.net/1/messages.json'
myobj = {'token': consts.API_KEY_Pushover,
         'user': consts.USER_KEY_Pushover,
         'message': "This is a test"}

x = requests.post(url, json = myobj)

print(x.text)

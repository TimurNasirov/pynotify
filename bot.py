from requests import get

def send(message, userid):
    print(f'https://api.telegram.org/bot7070717396:AAFstYu8WGqGuWR3sD9q36_8z0zBucOu1kg/sendMessage?chat_id={userid}&text={message}')
    get(f'https://api.telegram.org/bot7070717396:AAFstYu8WGqGuWR3sD9q36_8z0zBucOu1kg/sendMessage?chat_id={userid}&text={message}')
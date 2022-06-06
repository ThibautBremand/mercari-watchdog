import requests


def send_telegram_message(bot_message, bot_token, bot_chat_id):
    msg = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + \
          '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(msg)

    return response.json()

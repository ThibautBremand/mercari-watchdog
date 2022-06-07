# mercari-watchdog

![japaneselanguage](https://user-images.githubusercontent.com/9871294/155874389-eac9c024-c0df-4c40-b164-89dd34e2f119.jpeg)

It automatically and regularly scrapes predefined [mercari.jp](https://jp.mercari.com) listing pages, and 
sends notifications to a configured Telegram bot when new listings are found, with basic data.  
Whenever a new listing appears on a search page, you will be notified, on mobile and on desktop.

![watchdoge](https://user-images.githubusercontent.com/9871294/123490445-4d546a80-d614-11eb-9889-520df15e594e.jpg)

## Quick start
- Make sure Python3 is installed on your machine.
- Clone the repository
- Set up the mercari search keywords in the `config.toml` file (more details below)
- Set up your Telegram credentials in the `.env` file (more details below)
- Install the dependencies in `requirements.txt`
- Run `git submodule update --init --recursive` to init the mercari submodule
- Run the main file `main.py` to launch the program.

### Config.toml

#### Search keywords
To add a new keyword to scrape, add the following lines into the `config.toml` file:
```
[[searches]]
keywords = "your keywords"
```

Add as much as you want:  
```
[[searches]]
keywords = "shirts"

[[searches]]
keywords = "カーハート"
```

Other parameters:  
- `delay`: period, in seconds, between two scraping loops. Keep it reasonably high.
- `changerate`: rate that will be applied to the original prices in yen, so they will be displayed in a currency that 
  you are familiar. If you are fine with the yen currency, you can set the changerate at zero and only display the 
  prices in yen in the Telegram messages template in `config.toml`.
- `downloadphotos`: 
  - if set to `true`, then the photo of each listing will be downloaded, and the messages to Telegram will be sent as "photo with caption" instead of raw text. This is useful if Telegram doesn't display the URLs previews.
  - if set to `false`, then the messages will be sent to Telegram as raw text.

### Telegram and .env
- First, you need to create a [Telegram account](https://desktop.telegram.org/).
- Then, for the following steps, you need to download and use the desktop version.  

You can create a new Telegram bot [via this link](https://t.me/BotFather). 
- Send the `/newbot` command to BotFather, and
follow the steps to create a new bot. Once the bot is created, you will receive a token.
- Set the `TELEGRAM_TOKEN` variable in the `.env` file with your token.
```
TELEGRAM_TOKEN="your token"
```

Then, you need to find your chat ID.
- Paste the following link in your browser. Replace `<Telegram-token>` with the Telegram token.
```
https://api.telegram.org/bot<Telegram-token>/getUpdates?offset=0
```
- Send a message to your bot in the Telegram application. The message text can be anything. Your chat history must include at least one message to get your chat ID.
- Refresh your browser.
- Identify the numerical chat ID by finding the id inside the chat JSON object. In the example below, the chat ID is 123456789.
```json
{  
   "ok":true,
   "result":[  
      {  
         "update_id":987654321,
         "message":{  
            "message_id":2,
            "from":{  
               "id":123456789,
               "first_name":"Mushroom",
               "last_name":"Kap"
            },
            "chat":{  
               "id":123456789,
               "first_name":"Mushroom",
               "last_name":"Kap",
               "type":"private"
            },
            "date":1487183963,
            "text":"hi"
         }
      }
   ]
}
```
- Set the `TELEGRAM_CHAT_ID` variable in the `.env` file with this value.
```
TELEGRAM_CHAT_ID=123456789
```
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from sent_backend.models import Tweet

count = 0

all_tweets = Tweet.objects.all()

for t in all_tweets:
    try:
        url = 'https://twitter.com/anyuser/status/{}'.format(t.tweet_id)
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        tweet = soup.find('div', 'permalink-tweet')

        text =tweet.find('p', 'tweet-text') or ""
        emoji = re.findall(r'<img alt="(\S+)" aria-label="Emoji: .+" class="Emoji Emoji--forText" draggable="false" src="\S+" title=".+"\/>', str(text))

        text = text.text 

        if len(emoji):
            print('found an emoji')
            for e in emoji:
                text += " " + emoji[0] + " "
            print('new text = ' + text)
            t.tweet_class = 99
            t.text = text
            t.save()
            count += 1
    except:
        print("an error occured")

print('added emojis to ', count, ' tweets')
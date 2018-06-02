from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from sent_backend.models import Tweet

count = 0

all_tweets = Tweet.objects.filter(emoji_checked=0)

print("starting emoji check for ", all_tweets.count(), " tweets")

for t in all_tweets:
    try:
        url = 'https://twitter.com/anyuser/status/{}'.format(t.tweet_id)
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        tweet = soup.find('div', 'permalink-tweet')

        text = tweet.find('p', 'tweet-text') or ""
        emoji = re.findall(r'<img alt="(\S+)" aria-label="Emoji: .+" class="Emoji Emoji--forText" draggable="false" src="\S+" title=".+"\/>', str(text))

        print(str(text))
        
        text = text.text 

        if len(emoji):
            print('found an emoji')
            for e in emoji:
                text += " " + emoji[0] + " "
            print('new text = ' + text)
            t.tweet_class = 99
            t.text = text
            count += 1
        else:
            print("tweet has no emoji")
        t.emoji_checked = 1
        t.save()
    except:
        print("an error occured")
        t.emoji_checked = 1
        t.save()

print('added emojis to ', count, ' tweets')
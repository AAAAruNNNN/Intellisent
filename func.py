import pandas as pd
import sys
import re

def clean_tweets(text, show):
    text = re.sub(r'http\S+', ' <url> ', text.lower())
    text = re.sub(r'@[\S]+', ' <HANDLE> ', text)
    text = text.replace(',', ' ')
    text = re.sub(r'#(\S+)', r' \1 ', text)
    text = re.sub(r'\brt\b', '', text)
    text = re.sub(r'\.{2,}', ' ', text)
    text = re.sub(show.lower(), ' <SHOW_NAME> ', text)	
    show_words = show.lower().split(' ')
    text = re.sub(''.join(show_words), ' <SHOW_NAME> ', text)
    text = text.strip(' "\'')
    text = re.sub(r'\s+', ' ', text)

    clean_text = []
    for i in text.split():
        i = i.strip('\'"?!,.():;')
        i = re.sub(r'(.)\1+', r'\1\1', i)
        i = re.sub(r'(-|\')', '', i)
        clean_text.append(i)

    return ' '.join(clean_text)

def keep_required(csv_file):
    df = pd.read_csv(csv_file)
    df = df[['tweet_id', 'tweet_class', 'text', 'query']]

    smallest_len = min( len(df[df['tweet_class'] == 1]),
                        len( df[df['tweet_class'] == -1]),
                        len( df[df['tweet_class'] == 0]),
                        len( df[df['tweet_class'] == 2]),
                        )

    data = pd.DataFrame()
    data = data.append(df[df['tweet_class']==-1])
    data = data.append(df[df['tweet_class']==0])
    data = data.append(df[df['tweet_class']==1])
    data = data.append(df[df['tweet_class']==2])

    df = data.copy()

    df = df.sample(frac=1)

    df['clean']  = df.apply(lambda x: clean_tweets(x['text'], x['query']), axis=1)

    df['text'] = df['clean']

    df = df.drop(['clean'], axis=1)

    df.loc[df.tweet_class == -1, 'tweet_class'] = 3

    amt = int(len(df)*.8)

    df1 = df[:amt]
    df2 = df[amt:]
    df1 = df1.drop(['query'], axis=1)
    df3 = df2.drop(['query'], axis=1)
        
    df1.to_csv(csv_file[:-4] + "_train.csv", index=False)
    df3.to_csv(csv_file[:-4] + "_test.csv", index=False)
    # df2.to_csv(csv_file[:-4] + "_test_labels.csv", index=False)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('Usage: python func.py ')
		exit()
	keep_required(sys.argv[1])
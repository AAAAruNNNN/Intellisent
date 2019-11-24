import sqlite3
import pandas as pd

# connection to sqlLite DB
conn = sqlite3.connect('db.sqlite3')

df = pd.read_sql_query('select * from sent_backend_tweet;', conn);

df.to_csv('tweets_new.csv')

conn.close()



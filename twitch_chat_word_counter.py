import pandas as pd
import os
from collections import Counter


class ChattyLog:
    def __init__(self, logfile):
        self.twitch_channel = os.path.basename(logfile)[:-4].strip('#')
        with open(logfile, 'r', encoding='utf-8') as f:
            raw_contents = f.readlines()
        self.df = self.to_dataframe(raw_contents)

    def to_dataframe(self, raw_contents):
        """
        Read file buffer into pandas DataFrame
        """
        s = pd.Series(raw_contents)
        s = s[s.str.contains('<')]
        df = s.str.extract('\[(.*?)\]', expand=True)
        df.columns = ['timestamp']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['username'] = s.str.extract('<(.*?)>', expand=True)
        df['content'] = s.str.extract('> (.*?)$', expand=True)
        df['content'] = df['content'].fillna['']  # strip NaN values if exist

        return df

    def gen_counter(self, df=None, split_words=True):
        if df is None:
            words = self.df['content']
        else:
            words = df

        if split_words:
            words = words.str.split()
            words = [w for sublist in words for w in sublist]

        return Counter(words)

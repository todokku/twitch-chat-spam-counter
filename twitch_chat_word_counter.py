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
        # s = s[s.str.contains(r'^(?=.*<|# Log)')]  # remove non user messages

        # dates_logged = s[s.str.contains('# Log')]
        # dates_logged = dates_logged.str.split(expand=True)[3]
        # dates_logged.index = fix_dates_logged_ind(dates_logged)
        s = s[s.str.contains('<')]
        df = s.str.extract('\[(.*?)\]', expand=True)
        df.columns = ['timestamp']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['username'] = s.str.extract('<(.*?)>', expand=True)
        df['content'] = s.str.extract('> (.*?)$', expand=True)

        return df

    def gen_counter(self, df=None, split_words=True):
        if not df:
            words = self.df['content']
        else:
            words = df

        if split_words:
            words = words.str.split()
            words = [w for sublist in words for w in sublist]

        return Counter(words)

    def get_timeslice(self, slice=10):
        """
        Get index values of ChattyLog dataframe corresponding to slice of time.

        Parameters
        ----------
        slice : int, default 10
        """
        pass

    def parse_dates(self):
        pass


def fix_dates_logged_ind(dates_logged):
    l = [0] * len(dates_logged)
    l[::2] = dates_logged.index[::2] + 1
    l[1::2] = dates_logged.index[1::2] - 1

    return l

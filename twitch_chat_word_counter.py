import pandas as pd
import os
from collections import Counter


class ChattyLog:

    """
    Parser and basic manipulator class for reading plaintext Chatty log files.

    Attributes
    ----------
    df : pandas.DataFrame
        pandas.DataFrame Parsed logfile with 3 column names: timestamp,
        username, and content. NaN values are replaced with empty strings,
        extraneous chat info is stripped as well (log open and close lines,
        mod announcements and bans.)
    twitch_channel : str
        Username of twitch channel, derived from Chatty logfile name.
    """

    def __init__(self, logfile):
        self.twitch_channel = os.path.basename(logfile)[:-4].strip('#')
        with open(logfile, 'r', encoding='utf-8') as f:
            raw_contents = f.readlines()
        self.df = self.to_dataframe(raw_contents)

    def to_dataframe(self, raw_contents):
        """
        Parse file buffer into pandas DataFrame

        Parameters
        ----------
        raw_contents : list
            Raw output of logfile file buffer. No processing has been done at
            this point. Read in with utf-8 encoding to best deal with variety
            of characters.

        Returns
        -------
        df : pandas.DataFrame Parsed logfile with 3 column names: timestamp,
            username, and content. NaN values are replaced with empty strings,
            extraneous chat info is stripped as well (log open and close
            lines, mod announcements and bans.)
        """
        s = pd.Series(raw_contents)
        s = s[s.str.contains('<')]
        df = s.str.extract('\[(.*?)\]', expand=True)
        df.columns = ['timestamp']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['username'] = s.str.extract('<(.*?)>', expand=True)
        df['content'] = s.str.extract('> (.*?)$', expand=True)
        df['content'] = df['content'].fillna('')  # strip NaN values if exist

        return df

    def gen_counter(self, df=None, split_words=False):
        """
        Generate Counter object from pandas series of twitch chat messages.

        Parameters
        ----------
        df : {None, pandas.Series}, optional
            Series containing chat messages. If parameter is left blank will
            default to the 'content' column of the instances dataframe (i.e.
            df['content']).

        split_words : Boolean, optional
            If true, will split each chat message into single words using
            whitespace as delimiter. Can be useful if you're only interested
            in single word spam like emotes. Default value is False.

        Returns
        -------
        out : collections.Counter
            Counter object from python collections module, using your
            dataframe input.
        """
        if df is None:
            words = self.df['content']
        else:
            words = df

        if split_words:
            words = words.str.split()
            words = [w for sublist in words for w in sublist]

        return Counter(words)

import pandas as pd
from geeksrus import LOGGER
from geeksrus.utils.dbconn import read_mongo
from geeksrus.utils.dbconn import write_mongo
from geeksrus import dbcon
from geeksrus import cfg

import nltk
from nltk.corpus import stopwords
from datetime import datetime

import traceback

stop = stopwords.words('english')
stop.extend(('.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','/','-', '@', '#','://', 'https', 'RT', 'co', '&', '...'))


class WordCloud:

    def getTokenFrequency(self, count_cutoff=10, min_length=3):
        try:
            data_df = read_mongo(dbcon, cfg['collection'])
            frequency_words_wo_stop = {}
            for data in data_df['text']:
                tokens = nltk.wordpunct_tokenize(data)
                for token in tokens:
                    if token.lower() not in stop:
                        if token in frequency_words_wo_stop:
                            count = frequency_words_wo_stop[token]
                            count = count + 1
                            frequency_words_wo_stop[token] = count
                        else:
                            frequency_words_wo_stop[token] = 1

            wordcloud= []
            for key, value in frequency_words_wo_stop.items():
                word_freq = {}
                if value > count_cutoff and len(key) >= min_length:
                    word_freq['text'] = key
                    word_freq['size'] = value
                    wordcloud.append(word_freq)


            # {'text': 'word', 'size' : count}
            mongo_doc = {}
            mongo_doc['word_cloud'] = wordcloud
            mongo_doc['timestamp'] = datetime.now()

            write_mongo(db_conn=dbcon, collection=cfg['word_cloud_collection'], document=mongo_doc)

        except Exception as e:
            LOGGER.error(traceback.format_exc())


if __name__ == "__main__":
    wc = WordCloud()
    wc.getTokenFrequency()

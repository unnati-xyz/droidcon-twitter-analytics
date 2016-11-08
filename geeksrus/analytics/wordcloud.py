from datetime import datetime
import traceback
import re
from operator import itemgetter

import pandas as pd
import nltk
from nltk.corpus import stopwords

from geeksrus import LOGGER
from geeksrus.utils.dbconn import read_mongo, write_mongo, read_mongo_projection, find_and_sort_desc
from geeksrus import dbcon
from geeksrus import cfg


stop = stopwords.words('english')
stop.extend(('.', ',', '"', "'", '?', '!', ':', ';',
             '(', ')', '[', ']', '{', '}','/','-', '@', '#','://',
             'https', 'RT', 'co', '&', '...'
             , 'say', 'says'))


class WordCloud:

    def getTokenFrequency(self, count_cutoff=2, min_length=3):
        try:
            data_df = read_mongo(dbcon, cfg['collection'])
            frequency_words_wo_stop = {}
            max = 1
            min = 1
            for data in data_df['text']:
                data = re.sub("http\S*\s*", ' ', data)
                data = re.sub("t.co\S*\s*", ' ', data)
                data = re.sub("bit.ly\S*\s*", ' ', data)
                data = re.sub("\W", ' ', data)
                tokens = nltk.wordpunct_tokenize(data)
                for token in tokens:
                    token = token.strip()
                    if len(token) > 0 and token.lower() not in stop:
                        if token in frequency_words_wo_stop:
                            count = frequency_words_wo_stop[token]
                            count = count + 1
                            if count > max:
                                max = count
                            if count < min:
                                min = count
                            frequency_words_wo_stop[token] = count
                        else:
                            frequency_words_wo_stop[token] = 1
            wordcloud= []

            if max == min:
                max = max + 1

            for key, value in frequency_words_wo_stop.items():
                word_freq = {}
                if value > count_cutoff and len(key) >= min_length:
                    word_freq['text'] = key
                    normalized_value = ((max - value)/ (max - min)) * 100.0
                    normalized_value = normalized_value + 1.0
                    word_freq['size'] = normalized_value
                    wordcloud.append(word_freq)


            sorted_wordcloud= sorted(wordcloud, reverse=True, key=itemgetter('size'))


            # {'text': 'word', 'size' : count}
            mongo_doc = {}
            mongo_doc['word_cloud'] = sorted_wordcloud
            mongo_doc['timestamp'] = datetime.now()

            write_mongo(db_conn=dbcon, collection=cfg['word_cloud_collection'], document=mongo_doc)

        except Exception as e:
            LOGGER.error(traceback.format_exc())

    def getMentionsFrequency(self):
        try:
            projection = []
            projection.append('entities.user_mentions')
            data = read_mongo_projection(dbcon, cfg['collection'], query=projection)
            normalized_df = pd.io.json.json_normalize(data.entities, 'user_mentions')


            grouped_df = normalized_df.groupby(by=['screen_name'], as_index=False)['id'].count()
            grouped_df_screen_count = grouped_df[['screen_name','id']]
            grouped_df_screen_count = grouped_df_screen_count.sort(columns='id', ascending=False).reset_index()
            grouped_df_screen_count = grouped_df_screen_count.ix[:20,]

            max = grouped_df_screen_count.id.max()
            min = grouped_df_screen_count.id.min()

            count_data = []
            for row in grouped_df_screen_count.iterrows():
                screen_count = {}
                screen_count["text"] = "@" + row[1]['screen_name']
                normalized_value = ((max - row[1]['id'])/ (max - min)) * 100.0
                screen_count["size"] = normalized_value
                count_data.append(screen_count)

            sorted_wordcloud= sorted(count_data, reverse=True, key=itemgetter('size'))
            mongo_doc = {}
            mongo_doc['word_cloud']=sorted_wordcloud
            mongo_doc['timestamp'] = datetime.now()

            write_mongo(db_conn=dbcon, collection=cfg['mentions_collection'], document=mongo_doc)

        except Exception as e:
            LOGGER.error(traceback.format_exc())

    def getMaximumUserCount(self):
        try:
            projection = []
            projection.append('user.screen_name')
            projection.append('user.id')
            data = read_mongo_projection(dbcon, cfg['collection'], query=projection)
            column_df = data.apply(self.generate_columns_from_dict, axis=1)
            grouped_df = column_df.groupby(by=['screen_name'], as_index=False)['id'].count()
            grouped_df_screen_count = grouped_df[['screen_name','id']]
            grouped_df_screen_count = grouped_df_screen_count.sort(columns='id', ascending=False).reset_index()
            grouped_df_screen_count = grouped_df_screen_count.ix[:20,]
            count_data = []

            max = grouped_df_screen_count.id.max()
            min = grouped_df_screen_count.id.min()

            for row in grouped_df_screen_count.iterrows():
                screen_count = {}
                screen_count["text"] = "@" + row[1]['screen_name']
                normalized_value = ((max - row[1]['id'])/ (max - min)) * 100.0
                screen_count["size"] = normalized_value
                count_data.append(screen_count)

            sorted_wordcloud= sorted(count_data, reverse=True, key=itemgetter('size'))
            mongo_doc = {}
            mongo_doc['word_cloud'] = sorted_wordcloud
            mongo_doc['timestamp'] = datetime.now()

            write_mongo(db_conn=dbcon, collection=cfg['users_collection'], document=mongo_doc)

        except Exception as e:
            LOGGER.error(traceback.format_exc())

    def generate_columns_from_dict(self, row):
        user_dict = dict(row['user'])
        return pd.Series({'screen_name': user_dict['screen_name'], 'id': user_dict['id']})

    def get_current_wordcloud(self, collection):
        try:
            data = find_and_sort_desc(db_conn=dbcon, collection=collection, field='timestamp')
            wordcloud = data.ix[(0,1)]
            return wordcloud
        except:
            LOGGER.error(traceback.format_exc())




if __name__ == "__main__":
    wc = WordCloud()
    wc.getTokenFrequency()
    wc.getMentionsFrequency()
    wc.getMaximumUserCount()
    wc.get_current_wordcloud('word_cloud')

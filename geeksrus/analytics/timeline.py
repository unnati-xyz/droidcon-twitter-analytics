
from geeksrus import cfg, dbcon
from geeksrus.utils.dbconn import find_with_project_and_sort
from geeksrus import LOGGER

import traceback
import pandas as pd

class TimeLine:

    def get_recent_timeline(self, last_timestamp):
        try:
            projection = []
            projection.append('text')
            projection.append('timestamp_ms')
            projection.append('user.screen_name')
            projection.append('user.name')
            projection.append('user.profile_image_url_https')
            data = find_with_project_and_sort(db_conn=dbcon, collection=cfg['collection'], query=projection, field='timestamp_ms')
            data_df = data.apply(self.generate_columns_from_dict, axis=1)

            max_timestamp = data_df.timestamp.max()
            timeline = []
            tweets = {}
            if max_timestamp > last_timestamp:

                data_df = data_df[(data_df.timestamp > last_timestamp)]

                for row in data_df.iterrows():
                    tweet = {}
                    tweet['name'] = row[1]['name']
                    tweet['screen_name'] = row[1]['screen_name']
                    tweet['text'] = row[1]['text']
                    tweet['dp'] = row[1]['dp']
                    tweet['timestamp'] = row[1]['timestamp']
                    timeline.append(tweet)

            tweets['tweets'] = timeline
            tweets['max_time'] = str(max_timestamp)

            return tweets

        except:
            LOGGER.error(traceback.format_exc())

    def generate_columns_from_dict(self, row):
        user_dict = dict(row['user'])
        #return pd.Series({'text': row['text'], 'timestamp': row['timestamp_ms'], 'screen_name': user_dict['screen_name'], 'name': user_dict['name']})
        return pd.Series({'text': row['text'], 'screen_name': user_dict['screen_name'], 'name': user_dict['name']
                             , 'dp':user_dict['profile_image_url_https'], 'timestamp': row['timestamp_ms']})

if __name__=="__main__":

    tl = TimeLine()
    tl.get_recent_timeline()


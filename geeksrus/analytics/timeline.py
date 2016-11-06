
from geeksrus import cfg, dbcon
from geeksrus.utils.dbconn import find_with_project_and_sort
from geeksrus import LOGGER

import traceback
import pandas as pd

class TimeLine:

    def get_recent_timeline(self):
        try:
            projection = []
            projection.append('text')
            projection.append('timestamp_ms')
            projection.append('user.screen_name')
            projection.append('user.name')
            data = find_with_project_and_sort(db_conn=dbcon, collection=cfg['collection'], query=projection, field='timestamp_ms')
            data_df = data.apply(self.generate_columns_from_dict, axis=1)
            maxlen = 10
            data_df = data_df.loc[:maxlen, :]

            timeline = []
            for row in data_df.iterrows():
                tweet = {}
                tweet['name'] = row[1]['name']
                tweet['screen_name'] = row[1]['screen_name']
                tweet['text'] = row[1]['text']
                timeline.append(tweet)

            return timeline

        except:
            LOGGER.error(traceback.format_exc())

    def generate_columns_from_dict(self, row):
        user_dict = dict(row['user'])
        #return pd.Series({'text': row['text'], 'timestamp': row['timestamp_ms'], 'screen_name': user_dict['screen_name'], 'name': user_dict['name']})
        return pd.Series({'text': row['text'], 'screen_name': user_dict['screen_name'], 'name': user_dict['name']})

if __name__=="__main__":

    tl = TimeLine()
    tl.get_recent_timeline()


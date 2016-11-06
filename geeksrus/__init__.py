from geeksrus.utils.logger import Logger
from geeksrus.utils.dbconn import connect_mongo, read_mongo
from geeksrus.config import config as cfg

LOGGER = Logger().get()
API_LOGGER = Logger(module='api').get()

dbcon = connect_mongo(cfg['db'], host=cfg['host'], port=cfg['port'])

from nltk.corpus import stopwords

stop = stopwords.words('english')
stop.extend(('.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','/','-', '@', '#','://', 'https', 'RT', 'co', '&', '...'))

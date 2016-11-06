import traceback
from flask import jsonify, request, render_template, send_from_directory

from . import app
from geeksrus import API_LOGGER as LOGGER
from geeksrus.analytics.wordcloud import WordCloud
from geeksrus.analytics.timeline import TimeLine
from geeksrus import cfg





@app.route("/health")
def get_health():
    return "Health OK"

@app.route("/api/cloud/token")
def get_token_freq():
    try:
        result = WordCloud().get_current_wordcloud(cfg['word_cloud_collection'])
        LOGGER.info(type(result))
        return jsonify(result)
    except Exception:
        LOGGER.error(traceback.format_exc())

@app.route("/api/cloud/users")
def get_user_freq():
    try:
        result = WordCloud().get_current_wordcloud(cfg['users_collection'])
        LOGGER.info(type(result))
        return jsonify(result)
    except Exception:
        LOGGER.error(traceback.format_exc())

@app.route("/api/cloud/mentions")
def get_mention_freq():
    try:
        result = WordCloud().get_current_wordcloud(cfg['mentions_collection'])
        LOGGER.info(type(result))
        return jsonify(result)
    except Exception:
        LOGGER.error(traceback.format_exc())

@app.route("/api/timeline")
def get_timeline():
    try:
        result = TimeLine().get_recent_timeline()
        LOGGER.info(type(result))
        return jsonify(result)
    except Exception:
        LOGGER.error(traceback.format_exc())

@app.route("/")
def index_page():
    return render_template('index.html')

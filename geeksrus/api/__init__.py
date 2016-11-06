import os

from flask import Flask
from flask_cors import CORS, cross_origin
from geeksrus import config as cfg

cwd = os.getcwd()
our_static_folder = os.path.join(cwd, 'geeksrus', 'api', 'static')

#auth_key = cfg["flask_auth_key"]
app = Flask(__name__, static_folder=our_static_folder)
CORS(app)


from . import routes

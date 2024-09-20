import os
from flask import Flask

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static'),
    static_url_path='/static'
)

from app import routes
from app import create_app
from db import *
import config

db.create_all(app=create_app(config))

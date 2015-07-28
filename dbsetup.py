from src.app import create_app
from src.db import *
import src.config as config

db.create_all(app=create_app(config))

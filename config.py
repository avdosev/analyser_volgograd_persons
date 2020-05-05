import os
from os.path import join
from pathlib import Path


APP_PATH = Path(__file__).parents[0]
DATA_PATH = join(APP_PATH, "data")

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
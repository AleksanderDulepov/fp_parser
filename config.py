import os


class Config():
    DEBUG=True
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    JSON_AS_ASCII=False
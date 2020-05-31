import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MONGO_URI = '{}/{}?retryWrites=true&w=majority'.format(os.getenv('DB_CONNECTION_URL'),os.getenv("DB_NAME"))

    MONGO_1 = '{}'.format(os.getenv("CLUSTER_1"))
    MONGO_2 = '{}'.format(os.getenv("CLUSTER_2"))
    MONGO_3 = '{}'.format(os.getenv("CLUSTER_3"))
    MONGO_4 = '{}'.format(os.getenv("CLUSTER_4"))

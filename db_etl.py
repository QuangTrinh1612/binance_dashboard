import pymongo
import configparser

# Get MONGODB_URI from .ini file
config = configparser.ConfigParser()
config.read('keys.ini')
mongodb_uri = config['mongodb_URI']['mongodb_uri']

# MongoDB Client
client = pymongo.MongoClient(mongodb_uri)

# Retrieve Database
db = client['binance_analysis']

binance_schema = {
    'symbol': {
        'type': 'string',
        'required': True
    },
    'open_date': {
        'type': 'date',
        'required': True
    },
    'open': {
        'type': 'decimal',
        'required': False
    },
    'high': {
        'type': 'decimal',
        'required': False
    },
    'low': {
        'type': 'decimal',
        'required': False
    },
    'close': {
        'type': 'decimal',
        'required': False
    },
    'volume':{
        'type': 'long',
        'required': False
    },
    'num_trades': {
        'type': 'long',
        'required': False
    },
    'taker_base_vol': {
        'type': 'long',
        'required': False
    },
    'taker_quote_vol': {
        'type': 'long',
        'required': False
    }
}
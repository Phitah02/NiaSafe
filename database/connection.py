from pymongo import MongoClient
from datetime import datetime

# Establish connection to local MongoDB instance
client = MongoClient('localhost', 27017)

# Create database 'niasafe'
db = client['niasafe']

# Create collection 'flagged_comments'
collection = db['flagged_comments']

# Define schema as dictionary structure for documents
schema = {
    'comment_text': str,
    'severity_scores': {
        'toxic': float,
        'severe_toxic': float,
        'obscene': float,
        'threat': float,
        'insult': float,
        'identity_hate': float
    },
    'predicted_category': str,
    'timestamp': datetime,
    'alert_triggered': bool
}

def get_collection():
    return collection
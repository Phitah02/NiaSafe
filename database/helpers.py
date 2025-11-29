from datetime import datetime
from database.connection import collection

def save_flagged_comment(comment_text, severity_scores, predicted_category):
    document = {
        'comment_text': comment_text,
        'severity_scores': severity_scores,
        'predicted_category': predicted_category,
        'timestamp': datetime.now(),
        'alert_triggered': False
    }
    result = collection.insert_one(document)
    return result.inserted_id

def get_recent_comments(limit=20):
    documents = collection.find().sort('timestamp', -1).limit(limit)
    return list(documents)

def get_comments_by_category(category):
    documents = collection.find({'predicted_category': category})
    return list(documents)
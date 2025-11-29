from database.connection import collection

severity_thresholds = {'threat': 0.8, 'severe_toxic': 0.7}

def check_and_trigger_alert(doc_id, severity_scores):
    triggered_keys = []
    for key in severity_thresholds:
        if severity_scores.get(key, 0) > severity_thresholds[key]:
            triggered_keys.append(key)

    if triggered_keys:
        # Update the document to set alert_triggered to True
        collection.update_one({'_id': doc_id}, {'$set': {'alert_triggered': True}})

        # Determine severity_level
        if len(triggered_keys) > 1:
            severity_level = 'multiple'
        else:
            severity_level = triggered_keys[0]

        # Call send_alert
        send_alert('Alert: High severity comment detected', severity_level)

        return True
    else:
        return False

def send_alert(message, severity_level):
    print(message, severity_level)
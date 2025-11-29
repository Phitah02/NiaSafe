from flask import Flask, request, jsonify
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
from database.helpers import save_flagged_comment
from backend.alerts import check_and_trigger_alert

app = Flask(__name__)

# Load model and tokenizer
try:
    model = DistilBertForSequenceClassification.from_pretrained('./models/')
    tokenizer = DistilBertTokenizer.from_pretrained('./models/')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    tokenizer = None

def predict_toxicity(text):
    if model is None or tokenizer is None:
        raise Exception("Model not loaded")
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.sigmoid(logits).squeeze().tolist()
    
    labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    return dict(zip(labels, probs))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text field'}), 400
        
        text = data['text']
        predictions = predict_toxicity(text)
        predicted_category = max(predictions, key=predictions.get)
        doc_id = save_flagged_comment(text, predictions, predicted_category)
        alert_triggered = check_and_trigger_alert(doc_id, predictions)
        return jsonify({'text': text, 'predictions': predictions, 'alert_triggered': alert_triggered})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
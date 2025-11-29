import pandas as pd
import re
from transformers import DistilBertTokenizer
from sklearn.utils.class_weight import compute_class_weight
import json
import pickle

# Load datasets
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
test_labels = pd.read_csv('data/test_labels.csv')

# Merge test with labels
test = test.merge(test_labels, on='id')

# Preprocess text function
def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# Preprocess train and test
train['comment_text'] = train['comment_text'].apply(preprocess_text)
test['comment_text'] = test['comment_text'].apply(preprocess_text)

# Tokenize
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# For train
train_texts = train['comment_text'].tolist()
train_tokenized = tokenizer(train_texts, truncation=True, padding=True, max_length=512, return_tensors='pt')

# For test, filter valid labels (not -1)
test_valid = test[test['toxic'] != -1]
test_texts = test_valid['comment_text'].tolist()
test_tokenized = tokenizer(test_texts, truncation=True, padding=True, max_length=512, return_tensors='pt')

# Compute class weights
label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
class_weights = {}
for col in label_cols:
    y = train[col].values
    weights = compute_class_weight('balanced', classes=[0, 1], y=y)
    class_weights[col] = weights.tolist()

# Save
# Save class weights
with open('data/class_weights.json', 'w') as f:
    json.dump(class_weights, f)

# Save tokenized train
with open('data/train_tokenized.pkl', 'wb') as f:
    pickle.dump(train_tokenized, f)

# Save train labels
train_labels = train[label_cols].values
with open('data/train_labels.pkl', 'wb') as f:
    pickle.dump(train_labels, f)

# Save tokenized test
with open('data/test_tokenized.pkl', 'wb') as f:
    pickle.dump(test_tokenized, f)

# Save test labels
test_labels = test_valid[label_cols].values
with open('data/test_labels.pkl', 'wb') as f:
    pickle.dump(test_labels, f)

# Also save preprocessed csv if needed
train.to_csv('data/train_preprocessed.csv', index=False)
test.to_csv('data/test_preprocessed.csv', index=False)

print("Preprocessing complete")
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import pickle
import json
import numpy as np

# Load data
with open('data/train_tokenized.pkl', 'rb') as f:
    train_tokenized = pickle.load(f)

with open('data/train_labels.pkl', 'rb') as f:
    train_labels = pickle.load(f)

# Use subset for faster training
subset_size = 1000
train_tokenized = {k: v[:subset_size] for k, v in train_tokenized.items()}
train_labels = train_labels[:subset_size]

with open('data/class_weights.json', 'r') as f:
    class_weights = json.load(f)

label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

# Pos weights for BCE
pos_weights = torch.tensor([class_weights[col][1] for col in label_cols], dtype=torch.float)

# Model
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=6, problem_type="multi_label_classification")

# Loss
loss_fn = torch.nn.BCEWithLogitsLoss(pos_weight=pos_weights)

# Dataset
class ToxicityDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.float)
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = ToxicityDataset(train_tokenized, train_labels)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=16, shuffle=True)

# Optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
pos_weights = pos_weights.to(device)

# Training
epochs = 1
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in train_loader:
        batch_inputs = {k: v.to(device) for k, v in batch.items() if k != 'labels'}
        labels = batch['labels'].to(device)
        outputs = model(**batch_inputs)
        loss = loss_fn(outputs.logits, labels)
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    avg_loss = total_loss / len(train_loader)
    print(f'Epoch {epoch+1}/{epochs}, Average Loss: {avg_loss:.4f}')

# Save model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model.save_pretrained('./models/')
tokenizer.save_pretrained('./models/')

print("Training completed. Model and tokenizer saved to models/ folder.")
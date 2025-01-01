

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

df  = data = pd.read_csv("data.csv")
df['SMA10'] = df['last'].rolling(window=10).mean()
df['SMA50'] = df['last'].rolling(window=50).mean()

df['Signal'] = 0
df['Signal'][df['SMA10'] > df['SMA50']] = 1  # Buy signal
df['Signal'][df['SMA10'] < df['SMA50']] = -1  # Sell signal


df['SMA_Diff'] = df['SMA10'] - df['SMA50']
features = ['SMA10', 'SMA50', 'SMA_Diff']
X = df.dropna()[features]
y = df.dropna()['Signal']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LogisticRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

cm = confusion_matrix(y_test, y_pred)
print('Confusion Matrix:')
print(cm)

cr = classification_report(y_test, y_pred)
print('Classification Report:')
print(cr)


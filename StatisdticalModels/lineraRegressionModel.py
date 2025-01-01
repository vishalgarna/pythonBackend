import pandas as pd
import numpy as np
import talib as tb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler

# Load the data
data = pd.read_csv("data.csv")

# Calculate technical indicators
data["sma10"] = tb.SMA(data["last"], timeperiod=10)
data["sma50"] = tb.SMA(data["last"], timeperiod=50)
data["rsi"] = tb.RSI(data["last"], timeperiod=14)
data["macd"], data["macdsignal"], data["macdhist"] = tb.MACD(data["last"], fastperiod=12, slowperiod=26, signalperiod=9)
# Drop rows with NaN values
data = data.dropna()

# Create binary target labels (1 for price increase, 0 for price decrease)

target = data["last"]

# Select features and target
features = data[["sma10", "sma50", "volume", "rsi", "macd"]]

# print(features["sma10"].to_string())
# print(features["sma50"].to_string())
print(target.to_string())

# Scale the features
# scaler = StandardScaler()
# scaled_features = scaler.fit_transform(features)

# Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(scaled_features, target, test_size=0.2, random_state=42)

# # Initialize and train the logistic regression model
# model = LogisticRegression()
# model.fit(X_train, y_train)

# # Make predictions
# predictions = model.predict(X_test)

# # Evaluate the model
# accuracy = accuracy_score(y_test, predictions)
# conf_matrix = confusion_matrix(y_test, predictions)
# class_report = classification_report(y_test, predictions)
# print(f"Accuracy: {accuracy:.2f}")
# print("Confusion Matrix:")
# print(conf_matrix)
# print("Classification Report:")
# print(class_report)

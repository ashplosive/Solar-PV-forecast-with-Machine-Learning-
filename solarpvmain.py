# -*- coding: utf-8 -*-
"""solarpvmain.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lVfrPxcrxI4i1NsVrkN6hUCajgFfz_Tc

# Importing Dependencies
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

"""# Loading data from the Dataset"""

filepath = '/content/Plant_1_Generation_Data.csv' #load the filepath from the files section
df = pd.read_csv(filepath)

# printing the first few rows of the csv file to identify the features
print(df.head(-50))

#assigning net current to total yeild column of the csv dataset
net_current = df["TOTAL_YIELD"]

"""# Scaling data between 0 and 1"""

scaler = MinMaxScaler(feature_range=(0,1))
scaled_net_current = scaler.fit_transform(net_current.values.reshape(-1,1))

"""Defining Parameters"""

look_back = 10
epochs = 100

"""Create sequences for training"""

X, Y = [], []
for i in range(look_back, len(scaled_net_current)):
  X.append(scaled_net_current[i-look_back:i,0])
  Y.append(scaled_net_current[i,0])

X = np.array(X)
Y = np.array(Y)

"""Reshape input for LSTM"""

model = Sequential()
model.add(LSTM(50, return_sequences = True, input_shape = (X.shape[1], 1)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss="mse", optimizer="adam")

"""Train the model"""

model.fit(X,Y,epochs=epochs, batch_size=32)

"""Make predictions on new data"""

new_data = scaled_net_current[-look_back:]  # Last look_back values for prediction
new_data = new_data.reshape(1, look_back, 1)
predicted_net_current = model.predict(new_data)

"""Invert scaling for predicted current and original current"""

predicted_net_current = scaler.inverse_transform(predicted_net_current)
original_net_current = scaler.inverse_transform(scaled_net_current)

"""Prepare data for plotting"""

time_steps = range(len(original_net_current))

"""Plot the historical data, forecast and predicted data"""

plt.plot(time_steps[:look_back], original_net_current[:look_back], color='blue', label='Historical Data')
plt.plot(time_steps[-1], predicted_net_current[0][0], marker='o', color='red', label='Predicted Value')
plt.xlabel('Net Curent')
plt.ylabel('')
plt.legend()
plt.show()
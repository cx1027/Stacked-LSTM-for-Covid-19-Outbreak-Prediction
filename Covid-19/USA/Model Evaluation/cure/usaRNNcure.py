# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:56:04 2020

@author: Aparajita Das
"""
# Part 1 -Preprocessing

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
np.random.seed(35)

# Importing the training set
dataset_train = pd.read_csv('usa1.csv')
training_set = dataset_train.iloc[:, 1:2].values

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Creating a data structure
X_train = []
y_train = []
for i in range(50, 100):
    X_train.append(training_set_scaled[i-50:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))



# Part 2 - Building the RNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initialising the RNN
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 45, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

# Adding a second LSTM layer nd some Dropout regularisation
regressor.add(LSTM(units = 45, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 45, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 45))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units = 1))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
regressor.fit(X_train, y_train, epochs = 150 , batch_size = 40)



# Part 3 - Making the predictions 

# Getting the real data
dataset_test = pd.read_csv('usa2.csv')
real_confirmed_rate = dataset_test.iloc[:, 1:2].values

# Getting the predicted data
dataset_total = pd.concat((dataset_train['Cured'], dataset_test['Cured']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 50:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(50, 62):
    X_test.append(inputs[i-50:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_confirmed_rate = regressor.predict(X_test)
predicted_confirmed_rate = sc.inverse_transform(predicted_confirmed_rate)




# Part 4 - Visualising the results

# Close Comparision of Actual and Real
import matplotlib.dates as mdates
import datetime 
dates = list(dataset_test.iloc[:, 0].values)
x_values = [datetime.datetime.strptime(d,"%d-%m-%Y").date() for d in dates]
y_values = list(real_confirmed_rate)
ax = plt.gca()
formatter = mdates.DateFormatter("%d-%m-%Y")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.DayLocator()
ax.xaxis.set_major_locator(locator)

plt.plot(x_values, y_values, color = 'red', label = 'Real Covid19 Cured Case')
plt.plot(x_values, predicted_confirmed_rate, color = 'blue', label = 'Predicted Covid19 Cured Case')
plt.title('USA Covid19 Daywise Cured Prediction')
plt.xlabel('Days')
plt.ylabel('Cases')
plt.legend()
plt.show()


# Making structure to help visualize
df = pd.read_csv('usa-daily.csv', usecols = ['Cured'])
df2 = pd.read_csv('usa-daily.csv', usecols = ['Date'])

# Visualizing actual Data
datelist = list(df2.iloc[:, 0].values)
df['Date'] = datelist 
df = df.set_index(['Date'])
df.plot()

df_old = pd.read_csv('usa1.csv', usecols = ['Date', 'Cured'])
df_pred = pd.read_csv('usa2.csv', usecols = ['Date'])
df_pred['Cured'] = predicted_confirmed_rate
frames = [df_old, df_pred]
df_result = pd.concat(frames)

copy = df_result
copy = copy.drop('Date', axis=1)
copy_df_date = df_result
copy_df_date = copy_df_date.drop('Cured', axis=1)

# Visualizing predicted Data
datelist2 = list(copy_df_date.iloc[:, 0].values)
copy['Date'] = datelist2 
copy = copy.set_index(['Date'])
copy.plot()

# Visualization for Comparing actual and predicted
plt.plot(df, color = 'red', label = 'Real Covid19 Cured Case')
plt.plot(copy, color = 'blue', label = 'Predicted Covid19 Cured Case')
plt.title('USA Covid19 Daywise Cured Prediction')
plt.xticks(rotation=60)
plt.tight_layout()
plt.xlabel('Days')
plt.ylabel('Cases')
plt.legend()
plt.show()
 

df_3 = pd.DataFrame(predicted_confirmed_rate)
df_4 = dates
df_3['Date'] = df_4
df_3 = df_3.set_index(['Date'])
df_54 = copy[:100].copy(deep = True)
df_54.plot()

#visualization of future forecast/prediction
plt.plot(df_54, color = 'blue', label = 'Real Covid19 Cured Case')
plt.plot(copy, color = 'red', label = 'Predicted Covid19 Cured Case', alpha = 0.4)
plt.title('USA Covid19 Daywise Cured Prediction')
plt.xticks(rotation=60)
plt.tight_layout()
plt.xlabel('Days')
plt.ylabel('Cases')
plt.legend()
plt.show()







































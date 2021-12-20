import pandas as pd
import os
import constants
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler


df_1 = pd.read_csv(constants.PROJECT_PATH+'/all_data_first_half.csv')
df_2 = pd.read_csv(constants.PROJECT_PATH+'/all_data_second_half.csv')

df = df_1.append(df_2)

bad_rows = df[df['NAs'] > 5].index

df.drop(bad_rows, inplace=True)
df.pop('zeros')
df.pop('NAs')
values = df.values

num_values = len(values)
split_index = num_values//5

scaler = MinMaxScaler(feature_range=(0,1))
values = scaler.fit_transform(values)

random.shuffle(values)


test = values[:split_index, :]
train = values[split_index:, :]


train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

# reshape input to be 3D [samples, timesteps, features]
#train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
#test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)



model = Sequential()
model.add(Dense(50, input_shape=train_X.shape))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam', metrics=['acc'])

# fit network
history = model.fit(train_X, train_y, epochs=50, validation_data=(test_X, test_y), verbose=1, shuffle=False)

import os
import time
import argparse
import pandas as pd

from sklearn.preprocessing import StandardScaler
from keras.models import model_from_json
from keras.utils import multi_gpu_model
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard

argparser = argparse.ArgumentParser(description='Continue training the model')
argparser.add_argument('-m', '--model', help='model json file path')
argparser.add_argument('-w', '--weights', help='model weights file path')
argparser.add_argument('-r', '--results', help='output directory path')
argparser.add_argument('--train', help='train dataset path')
argparser.add_argument('--test', help='test dataset path')

args = argparser.parse_args()

# parse arguments
model = args.model
weights = args.weights
results_dir = args.results
train_dataset = args.train
test_dataset = args.test

df_train = pd.read_csv(train_dataset)
df_test = pd.read_csv(test_dataset)

X_train = df_train[['xmin', 'ymin', 'xmax', 'ymax']].values
y_train = df_train[['distance']].values

# standardized data
scalar = StandardScaler()
X_train = scalar.fit_transform(X_train)
y_train = scalar.fit_transform(y_train)

# load json and create model
json_file = open(model, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# load weights into new model
model.load_weights(weights)
print("Loaded model from disk")

# compile and train model
parallel_model = multi_gpu_model(model, gpus=2)
parallel_model.compile(loss='mean_squared_error', optimizer='adam')

modelname = "model@{}".format(int(time.time()))
tensorboard = TensorBoard(log_dir="logs/{}".format(modelname))

parallel_model.fit(X_train, y_train, validation_split=0.1, epochs=5000,
                   batch_size=2048, callbacks=[tensorboard], verbose=1)

# save model and weights
model_json = model.to_json()
with open(os.path.join(results_dir, "{}.json".format(modelname)), "w") as json_file:
    json_file.write(model_json)

model.save_weights(os.path.join(results_dir, "{}.h5".format(modelname)))
print("Saved model to disk")

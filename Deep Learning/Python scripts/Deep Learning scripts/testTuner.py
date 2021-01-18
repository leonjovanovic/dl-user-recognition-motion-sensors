import tensorflow as tf
from tensorflow import keras
import IPython
import kerastuner as kt
from sklearn.utils import shuffle
import os

from CreateDataset import *
path2 = r"D:\Users\Leon Jovanovic\Desktop\GyroData\VectorData50Hz"
input_type = "Acceleration"
output_type = "Lang"

data_vector_input, data_vector_output = create_vector_dataset(path2, input_type, output_type)

DATASET_SIZE = data_vector_output.shape[0]#315
train_size = int(0.6 * DATASET_SIZE)#252
test_size = int(0.2 * DATASET_SIZE)#63

data_vector_input_norm = data_vector_input
data_vector_output_norm = data_vector_output
#Shuffle
data_vector_input_norm, data_vector_output_norm = shuffle(data_vector_input_norm, data_vector_output_norm, random_state=0)
#Normalize
mi = np.sum(data_vector_input_norm,axis = 0)/data_vector_input_norm.shape[0]
data_vector_input_norm = data_vector_input_norm - mi
sigma = np.sum(data_vector_input_norm**2,axis = 0)/data_vector_input_norm.shape[0]
data_vector_input_norm = data_vector_input_norm/np.sqrt(sigma)

train_examples = data_vector_input_norm[:train_size,:]
train_labels = data_vector_output_norm[:train_size,:]

val_examples = data_vector_input_norm[train_size:train_size+test_size,:]
val_labels = data_vector_output_norm[train_size:train_size+test_size,:]

test_examples = data_vector_input_norm[train_size+test_size:,:]
test_labels = data_vector_output_norm[train_size+test_size:,:]



#---------------Create model with hyperparameters------------------------------
def model_builder(hp):
  model = keras.Sequential()
  # Choose an optimal value between 32-512
  hp_units = hp.Int('units', min_value = 32, max_value = 512, step = 32)
  
  model.add(keras.layers.Dense(units = hp_units, input_shape=(2997,)))
  
  for lay in range(9):
      model.add(keras.layers.Dense(units = hp_units, activation = 'relu', kernel_regularizer=keras.regularizers.l2(0.001)))
      model.add(keras.layers.Dropout(0.5))
      
  model.add(keras.layers.Dense(3, activation='softmax'))

  # Tune the learning rate for the optimizer 
  # Choose an optimal value from 0.01, 0.001, or 0.0001
  hp_learning_rate = hp.Choice('learning_rate', values = [1e-2, 1e-3, 1e-4]) 
  
  model.compile(optimizer = keras.optimizers.Adam(learning_rate = hp_learning_rate),
                loss = keras.losses.SparseCategoricalCrossentropy(from_logits = True), 
                metrics = [tf.keras.metrics.SparseCategoricalAccuracy()])
  
  return model
#The Keras Tuner has four tuners available - RandomSearch, Hyperband, 
#BayesianOptimization, and Sklearn. In this tutorial, you use the Hyperband tuner. 
#---------------------------Init Hyperband tuner-------------------------------
#To instantiate the Hyperband tuner, you must specify the hypermodel, 
#the objective to optimize and the maximum number of epochs to train (max_epochs).
tuner = kt.BayesianOptimization(model_builder,
                     objective = 'val_sparse_categorical_accuracy', 
                     max_trials = 200,
                     directory = os.path.normpath('C:/'),
                     project_name = 'overwrite=True')                       
#The Hyperband tuning algorithm uses adaptive resource allocation and 
#early-stopping to quickly converge on a high-performing model. This is done 
#using a sports championship style bracket. The algorithm trains a large number 
#of models for a few epochs and carries forward only the top-performing half of 
#models to the next round. Hyperband determines the number of models to train 
#in a bracket by computing 1 + logfactor(max_epochs) and rounding it up to the nearest integer.

#---Callback to clear the training outputs at the end of every training step---
class ClearTrainingOutput(tf.keras.callbacks.Callback):
  def on_train_end(*args, **kwargs):
    IPython.display.clear_output(wait = True)
#---------------------------------Run------------------------------------------
#Search is same as model.fit (same params)
tuner.search(train_examples,
             train_labels, 
             epochs = 200, 
             validation_data = (val_examples, val_labels), 
             callbacks = [ClearTrainingOutput()])

# Get the optimal hyperparameters
best_hps = tuner.get_best_hyperparameters(num_trials = 1)[0]


model = tuner.hypermodel.build(best_hps)
model.fit(train_examples, train_labels, epochs = 200, validation_data = (val_examples, val_labels))

loss1, accuracy = model.evaluate(test_examples, test_labels)
print("Loss: ", loss1)
print("Accuracy: ", accuracy)
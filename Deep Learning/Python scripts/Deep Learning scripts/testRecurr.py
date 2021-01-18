from CreateDataset import *
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import regularizers
import tensorflow_docs as tfdocs
import tensorflow_docs.modeling
import tensorflow_docs.plots

from sklearn.utils import shuffle

from  IPython import display
from matplotlib import pyplot as plt
import numpy as np
import pathlib
import shutil
import tempfile
#----------------------------Preprocess data-----------------------------------
path1 = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Data50Hz"
path2 = r"D:\Users\Leon Jovanovic\Desktop\GyroData\VectorData50Hz"
input_type = "GyroscopeRotRate"
output_type = "#F"
#Input types: "Acceleration|GyroscopeRotRate|GyroscopeAttitude
#Output types: BgNoise|Lang|Dist|#Pers|#M|#F|Y(1	Y2	Y3	Y4	Y5	Y6)|L/W(etter/Num/Word..)
data_input, data_output = create_dataset(path1, input_type, output_type)
data_vector_input, data_vector_output = create_vector_dataset(path2, input_type, output_type)
DATASET_SIZE = data_vector_output.shape[0]#315

#Split dataset into train, validation and test sets
train_size = int(0.8 * DATASET_SIZE)#252
test_size = int(0.2 * DATASET_SIZE)#63

#----------------Shuffle, normalize and split vector input---------------------
data_vector_input_norm = data_vector_input
data_vector_output_norm = data_vector_output

data_vector_input, data_vector_output_norm = shuffle(data_vector_input_norm, 
                                                     data_vector_output_norm, 
                                                     random_state=3)

mi = np.sum(data_vector_input_norm,axis = 0)/data_vector_input_norm.shape[0]
data_vector_input_norm = data_vector_input_norm - mi
sigma = np.sum(data_vector_input_norm**2,axis = 0)/data_vector_input_norm.shape[0]
data_vector_input_norm = data_vector_input_norm/np.sqrt(sigma)


train_vector_examples = data_vector_input_norm[:train_size,:]
train_vector_labels = data_vector_output_norm[:train_size,:]

test_vector_examples = data_vector_input_norm[train_size:,:]
test_vector_labels = data_vector_output_norm[train_size:,:]
#---------------------Adding dimension for LSTM RNN----------------------------
train_vector_examples = train_vector_examples[..., np.newaxis]
test_vector_examples = test_vector_examples[..., np.newaxis]
#------------------------------------------------------------------------------
l = 0
a = 0
for i in range(10):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(10, 
                                    activation='tanh', 
                                    input_shape=(2997, 1),
                                    recurrent_activation="sigmoid",
                                    recurrent_dropout=0,
                                    unroll=False,
                                    use_bias=True,
                                    return_sequences=True,
                                    kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.LSTM(10, 
                                    activation='tanh', 
                                    input_shape=(2997, 1),
                                    recurrent_activation="sigmoid",
                                    recurrent_dropout=0,
                                    unroll=False,
                                    use_bias=True,
                                    return_sequences=False,
                                    kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(layers.Dropout(0.5))
    for js in range(5) :
        model.add(layers.Dense(1024, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
        model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1, activation='sigmoid'))
    
    model.compile(optimizer=tf.keras.optimizers.Adam(clipvalue=0.5), 
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics = ['accuracy'])
    
    history = model.fit(train_vector_examples, 
              train_vector_labels, 
              validation_split = 0.2,
              epochs=20, 
              verbose=1)    
    
    loss1, accuracy = model.evaluate(test_vector_examples, test_vector_labels)
        

    print("Loss: ", loss1)
    print("Accuracy: ", accuracy)
    print("Iteration: ", i)
    l = l+loss1
    a = a+accuracy

print("Loss: ", l/10)
print("Accuracy: ", a/10)
    
    #alfa
    lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
      0.0008,
      decay_steps=200,
      decay_rate=1,
      staircase=True)
    
    
    callbacks = [
                 tf.keras.callbacks.EarlyStopping(
                     monitor='val_loss', patience = 20
                 )
    ]

    history_dict = history.history
    history_dict.keys()
    #acc = history_dict['sparse_categorical_accuracy']
    #val_acc = history_dict['val_sparse_categorical_accuracy']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
    
    epochs = range(1, len(loss) + 1)
    # "bo" is for "blue dot"
    plt.plot(epochs, loss, 'bo', label='Training loss')
    # b is for "solid blue line"
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

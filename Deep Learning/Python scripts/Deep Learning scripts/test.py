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
import numpy as np
#----------------------------Preprocess data-----------------------------------
path1 = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Data50Hz"
path2 = r"D:\Users\Leon Jovanovic\Desktop\GyroData\VectorData50Hz"
pathOut = r"D:\Users\Leon Jovanovic\Desktop\GyroData\Results"
freq = 50
input_type = "Acceleration"
output_type = "Lang"
#Input types: "Acceleration|GyroscopeRotRate|GyroscopeAttitude
#Output types: BgNoise|Lang|Dist|#Pers|#M|#F|Y(Y1	Y2	Y3	Y4	Y5	Y6)|L/W(Letter/Num/Word..)
data_input, data_output = create_dataset(path1, input_type, output_type)
data_vector_input, data_vector_output = create_vector_dataset(path2, input_type, output_type)
#----------------------------------Plotting------------------------------------
    
def plot_data(data, num, s):
    plt.plot(data, 'bx', label='')
    plt.title(s)
    plt.xlabel('Test number')
    plt.ylabel('Value')
    plt.savefig('plot'+str(num)+'.png', dpi=300)
    plt.show()
    
#plot_data(data_input[:,:,0],1,"Acceleration value on X axis")
#plot_data(data_input[:,:,1],2,"Acceleration value on Y axis")
#plot_data(data_input[:,:,2],3,"Acceleration value on Z axis")
#plot_data(data_vector_input,4,"Acceleration vector value")
#plot_data(data_vector_output,5,"Output")

DATASET_SIZE = data_vector_output.shape[0]#315
#Split dataset into train, validation and test sets
train_size = int(0.8 * DATASET_SIZE)#252
test_size = int(0.2 * DATASET_SIZE)#63


#-------------------------Shuffle, normalize and split coord input------------------------------------------
data_input_norm = data_input
data_output_norm = data_output

rnd = 3
data_input_norm, data_output_norm = shuffle(
                                            data_input_norm, 
                                            data_output_norm, 
                                            random_state=rnd
                                            )

mi = np.sum(data_input_norm,axis = 0)/data_input_norm.shape[0]
data_input_norm = data_input_norm - mi
sigma = np.sum(data_input_norm**2,axis = 0)/data_input_norm.shape[0]
data_input_norm = data_input_norm/np.sqrt(sigma)

train_examples = data_input_norm[:train_size,:,:]
train_labels = data_output_norm[:train_size,:]

test_examples = data_input_norm[train_size:,:,:]
test_labels = data_output_norm[train_size:,:]

train_examples = np.reshape(train_examples, (train_size,8991), order='F')
test_examples = np.reshape(test_examples, (test_size,8991), order='F')
#------------------------Shuffle, normalize and split vector input--------------------------------------
data_vector_input_norm = data_vector_input
data_vector_output_norm = data_vector_output

data_vector_input_norm, data_vector_output_norm = shuffle(data_vector_input_norm, 
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
#------------------------------------------------------------------------------
np.random.seed(1337) 

def plot_learning_rate(ep,alfa):
    step = np.linspace(0,20*ep)
    lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
          alfa,
          decay_steps=200,
          decay_rate=1,
          staircase=False) 
    lr = lr_schedule(step)
    plt.figure(figsize = (8,6))
    plt.plot(step/20, lr)
    plt.ylim([0,max(plt.ylim())])
    plt.xlabel('Epoch')
    _ = plt.ylabel('Learning Rate')
    
def train(totalLoops, activF, i_size, numLayers, numUnits, outputUnits, alfa, optFlag, optim, pat, train_e, train_l, test_e, test_l, epoch, verb, mini_batch):
    l = 0
    a = 0
    smallest_l = 5
    biggest_a = 0
    for i in range(totalLoops):
        model = tf.keras.Sequential()    
        model.add(layers.Dense(numUnits, activation=activF,input_shape = (i_size,), kernel_regularizer=regularizers.l2(0.001)))
        model.add(layers.Dropout(0.5))
        for js in range(numLayers) :
            model.add(layers.Dense(numUnits, activation=activF, kernel_regularizer=regularizers.l2(0.001)))
            model.add(layers.Dropout(0.5))
    
        model.add(layers.Dense(outputUnits, activation='softmax'))
        
        #alfa
        lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
          alfa,
          decay_steps=200,
          decay_rate=1,
          staircase=False)    
        
        callbacks = [
                     tf.keras.callbacks.EarlyStopping(
                         monitor='val_loss', patience = pat, restore_best_weights=True
                     )
        ]
        if(optFlag):
            if(optim == 'adam'):
                optimizer1=tf.keras.optimizers.Adam(learning_rate = lr_schedule)
            if(optim == 'adamax'):
                optimizer1=tf.keras.optimizers.Adamax(learning_rate = lr_schedule)
            if(optim == 'rmsprop'):
                optimizer1=tf.keras.optimizers.RMSprop(learning_rate = lr_schedule)
            if(optim == 'sgd'):
                optimizer1=tf.keras.optimizers.SGD(learning_rate = lr_schedule)
        else:
            if(optim == 'adam'):
                optimizer1=tf.keras.optimizers.Adam(learning_rate = alfa)
            if(optim == 'adamax'):
                optimizer1=tf.keras.optimizers.Adamax(learning_rate = alfa)
            if(optim == 'rmsprop'):
                optimizer1=tf.keras.optimizers.RMSprop(learning_rate = alfa)
            if(optim == 'sgd'):
                optimizer1=tf.keras.optimizers.SGD(learning_rate = alfa, momentum=0.9)
                
        model.compile(optimizer=optimizer1, 
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
                      metrics = [tf.keras.metrics.SparseCategoricalAccuracy()])#tf.keras.metrics.SparseCategoricalAccuracy()
        
        history = model.fit(
            train_e,
            train_l,
            validation_split = 0.25,
            epochs =epoch,
            callbacks=callbacks,
            verbose=verb,
            shuffle=False,
            batch_size = mini_batch
            )    
        
        loss1, accuracy = model.evaluate(test_e, test_l)
        
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
        plt.savefig('plot10.png', dpi=300)
        plt.show()
        
        
        print("Epochs: ", epochs.__len__())
        print("Loss: ", loss1)
        print("Accuracy: ", accuracy)
        l = l+loss1
        a = a+accuracy
        if(accuracy>biggest_a):biggest_a = accuracy
        if(loss1<smallest_l):smallest_l = loss1  
        print("Iteration: ", i)
    a = a/totalLoops
    l = l/totalLoops
    print("Loss: ", l)
    print("Average accuracy: ", a)      
    print("Best accuracy: ", biggest_a)
    plot_learning_rate(epoch,alfa)
    s = str(freq) + '\t' + input_type + '\t' + ('Coords' if train_e.shape[1]>train_vector_examples.shape[1] else 'Vector') + '\t' + "60|20|20" + '\t' + "Yes" + '\t' + str(rnd) + '\t' + "Yes" + '\t' + str(numLayers) + '\t' + str(numUnits) + '\t' + "0.001" + '\t' + "0.5" + '\t' + activF + '\t' + str(outputUnits) + '\t' + "Sigmoid" + '\t' + optim + '\t' + str(alfa) + '\t' + ('200\t1' if optFlag else '/\t/') + '\t' + "BinaryCrossentropy\tAccuracy" + '\t' + str(epoch) + '\t' + str(pat) + '\t' + str(smallest_l) + '\t' + str(biggest_a*100) + '\t' + str(a*100) + '\t\n'
    return s

for o in range(3):
    s = train(
          totalLoops = 10,
          activF = 'relu',              #activation function for hidden layers
          i_size = 2997,                #flatten input size in first layer
          numLayers = 3,                #Number of hidden layers after first hidden layer
          numUnits = 1024,              #number of units in each hidden layer
          outputUnits = 3,              #number of output units
          alfa = 0.0011,                #step size
          optFlag = True,               #learning rate decay (True) or static lr (False)
          optim = "rmsprop",                   #optimization algorithm
          pat = 11,                            #early stopping patience
          train_e = train_vector_examples,     #training data vector or coords
          train_l = train_vector_labels,       #training data vector or coords
          test_e = test_vector_examples,       #test data vector or coords
          test_l = test_vector_labels,         #test data vector or coords
          epoch = 120,                  #number of epochs
          verb = 0,                     #print output on console for every epoch or not
          mini_batch = 63               #split data into mini_batches with size
          )              
    print(s)
    with open(pathOut+"\\"+str(output_enums(output_type))+".txt", 'a') as fin:
        fin.write(s)
        

    
    
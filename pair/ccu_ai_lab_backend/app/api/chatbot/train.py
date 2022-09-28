#Used in Tensorflow Model
import numpy as np
#import tensorflow as tf
#from tensorflow.python.framework import ops
#ops.reset_default_graph()
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import tflearn
import random

#Usde to for Contextualisation and Other NLP Tasks.
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#Other
import json
import pickle
import warnings
import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

warnings.filterwarnings("ignore")

#curses is not supported on this machine (please install/reinstall curses for an optimal experience)

#print("Processing the Intents.....")
with open(os.path.join(script_dir, 'intents.json')) as json_data:
    intents = json.load(json_data)

#Processing the Intents.....

words = []
classes = []
documents = []
ignore_words = ['?','!', '-', '.', '/', '\'', 'to', 'a', 'the', 'of', 'it', 'at'] 
#print("Looping through the Intents to Convert them to words, classes, documents and ignore_words.......")
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#Looping through the Intents to Convert them to words, classes, documents and ignore_words.......

#print("Stemming, Lowering and Removing Duplicates.......")
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

#print (len(documents), "documents")
#print (len(classes), "classes", classes)
#print (len(words), "unique stemmed words", words)

#Stemming, Lowering and Removing Duplicates.......
#27 documents
#9 classes ['goodbye', 'greeting', 'hours', 'mopeds', 'opentoday', 'payments', 'rental', 'thanks', 'today']
#48 unique stemmed words ["'d", "'s", 'a', 'acceiv', 'anyon', 'ar', 'bye', 'can', 'card', 'cash', 'credit', 'day', 'do', 'doe', 'good', 'goodby', 'hav', 'hello', 'help', 'hi', 'hour', 'how', 'i', 'is', 'kind', 'lat', 'lik', 'mastercard', 'mop', 'of', 'on', 'op', 'rent', 'see', 'tak', 'thank', 'that', 'ther', 'thi', 'to', 'today', 'we', 'what', 'when', 'which', 'work', 'yo', 'you']

#print("Creating the Data for our Model.....")
training = []
output = []
#print("Creating an List (Empty) for Output.....")
output_empty = [0] * len(classes)

#print("Creating Traning Set, Bag of Words for our Model....")
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    #print("pattern words", pattern_words)
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    #print("pattern words", pattern_words)
    # create our bag of words array
    for w in words:
        #print("words", w)
        bag.append(1) if w in pattern_words else bag.append(0)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])
    #print("output_row", output_row)
    
#Creating the Data for our Model.....
#Creating an List (Empty) for Output.....
#Creating Traning Set, Bag of Words for our Model....

#print("Shuffling Randomly and Converting into Numpy Array for Faster Processing......")
random.shuffle(training)
training = np.array(training)

#print("Creating Train and Test Lists.....")
train_x = list(training[:,0])
train_y = list(training[:,1])

#print("train_x", train_x)
#print("train_y", train_y)


#print("Building Neural Network for Out Chatbot to be Contextual....")
#print("Resetting graph data....")
tf.reset_default_graph()

#Shuffling Randomly and Converting into Numpy Array for Faster Processing......
#Creating Train and Test Lists.....
#Building Neural Network for Out Chatbot to be Contextual....
#Resetting graph data....

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
#print("Training....")

#Training....

model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
#print("Training the Model.......")
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
#print("Saving the Model.......")
model.save('model.tflearn')

#Training Step: 3999  | total loss: 0.06984 | time: 0.011s
#| Adam | epoch: 1000 | loss: 0.06984 - acc: 0.9976 -- iter: 24/27
#Training Step: 4000  | total loss: 0.07164 | time: 0.014s
#| Adam | epoch: 1000 | loss: 0.07164 - acc: 0.9978 -- iter: 27/27
#--
#Saving the Model.......
#INFO:tensorflow:E:\FreeBirdsCrew\Chatbot\model.tflearn is not in all_model_checkpoint_paths. Manually adding it.

#print("Pickle is also Saved..........")
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )

#Pickle is also Saved..........

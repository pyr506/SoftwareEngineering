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
curr_path = os.getcwd()
#print(curr_path)
os.chdir('./app/api/chatbot')

warnings.filterwarnings("ignore")

#curses is not supported on this machine (please install/reinstall curses for an optimal experience)

print("Processing the Intents.....")
with open('intents.json') as json_data:
    intents = json.load(json_data)

#Processing the Intents.....

words = []
classes = []
documents = []
ignore_words = ['?','!', '-', '.', '/', '\'']
print("Looping through the Intents to Convert them to words, classes, documents and ignore_words.......")
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

print("Stemming, Lowering and Removing Duplicates.......")
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)

#Stemming, Lowering and Removing Duplicates.......
#27 documents
#9 classes ['goodbye', 'greeting', 'hours', 'mopeds', 'opentoday', 'payments', 'rental', 'thanks', 'today']
#48 unique stemmed words ["'d", "'s", 'a', 'acceiv', 'anyon', 'ar', 'bye', 'can', 'card', 'cash', 'credit', 'day', 'do', 'doe', 'good', 'goodby', 'hav', 'hello', 'help', 'hi', 'hour', 'how', 'i', 'is', 'kind', 'lat', 'lik', 'mastercard', 'mop', 'of', 'on', 'op', 'rent', 'see', 'tak', 'thank', 'that', 'ther', 'thi', 'to', 'today', 'we', 'what', 'when', 'which', 'work', 'yo', 'you']

print("Creating the Data for our Model.....")
training = []
output = []
print("Creating an List (Empty) for Output.....")
output_empty = [0] * len(classes)

print("Creating Traning Set, Bag of Words for our Model....")
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

    training.append([bag, output_row]) # [單字, tag]
    #print("output_row", output_row)
    
#Creating the Data for our Model.....
#Creating an List (Empty) for Output.....
#Creating Traning Set, Bag of Words for our Model....

print("Shuffling Randomly and Converting into Numpy Array for Faster Processing......")
random.shuffle(training)
training = np.array(training)

print("Creating Train and Test Lists.....")
train_x = list(training[:,0])
train_y = list(training[:,1])

print("train_x", train_x)
print("train_y", train_y)

#[:,0]是numpy中数组的一种写法，表示对一个二维数组，取该二维数组第一维中的所有数据，第二维中取第0个数据，直观来说，[:,0]就是取所有行的第0个数据, [:,1] 就是取所有行的第1个数据。

print("Building Neural Network for Out Chatbot to be Contextual....")
print("Resetting graph data....")
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
print("Training....")

#Training....

model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
print("Training the Model.......")
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
print("Saving the Model.......")
model.save('model.tflearn')

#Training Step: 3999  | total loss: 0.06984 | time: 0.011s
#| Adam | epoch: 1000 | loss: 0.06984 - acc: 0.9976 -- iter: 24/27
#Training Step: 4000  | total loss: 0.07164 | time: 0.014s
#| Adam | epoch: 1000 | loss: 0.07164 - acc: 0.9978 -- iter: 27/27
#--
#Saving the Model.......
#INFO:tensorflow:E:\FreeBirdsCrew\Chatbot\model.tflearn is not in all_model_checkpoint_paths. Manually adding it.

print("Pickle is also Saved..........")
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )

#Pickle is also Saved..........

print("Loading Pickle.....")
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']


with open('intents.json') as json_data:
    intents = json.load(json_data)
    
print("Loading the Model......")
# load our saved model
model.load('./model.tflearn')

#Loading Pickle.....
#Loading the Model......
#INFO:tensorflow:Restoring parameters from E:\FreeBirdsCrew\Chatbot\model.tflearn

def clean_up_sentence(sentence):
    # It Tokenize or Break it into the constituents parts of Sentense.
    sentence_words = nltk.word_tokenize(sentence)
    # Stemming means to find the root of the word.
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# Return the Array of Bag of Words: True or False and 0 or 1 for each word of bag that exists in the Sentence
def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

# create a data structure to hold user context
context = {}
userID = 123
context[userID] = ""


ERROR_THRESHOLD = 0.25
print("ERROR_THRESHOLD = 0.25")

def classify(sentence):
    # Prediction or To Get the Posibility or Probability from the Model
    results = model.predict([bow(sentence, words)])[0]
    # Exclude those results which are Below Threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # Sorting is Done because heigher Confidence Answer comes first.
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1])) #Tuppl -> Intent and Probability
    return return_list
salary = "d_2"
proj_type = "d_1"
flag = 0
def response(sentence, userID, show_details=False):
    results = classify(sentence)
    # That Means if Classification is Done then Find the Matching Tag.
    if results:
        # Long Loop to get the Result.
        while results:
            for i in intents['intents']:
                # Tag Finding
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']
                        #print('context', context[userID])
                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        if('context_filter' in i and i['context_filter'] == context[userID]):
                            context[userID] = "" 
                        tmp_response = random.choice(i['responses'])
                        fileName = "my-data.json"    
                        jsonString = '{ "flag": "d_0", "project_types": "d_1", "salary": "d_2", "time": "d_3", "group_member": "d_4" , "other":"d_5" , "response":"d_6"}'
                        jsonString = jsonString.replace("d_6", tmp_response)
                        #jsonString = jsonString.replace("d_1", i['tag']) #
                        if(i['tag']== "AI"):
                            global proj_type
                            proj_type = i['tag']
                            #jsonString = jsonString.replace("1", i['tag'])
                            #jsonString = jsonString.replace("d_1", proj_type)
                            #jsonString = jsonString.replace("d_0","1")
                        if(i['tag'] == "Salary"):
                            output=sentence.split()
                            global salary
                            salary = output[1]
                            jsonString = jsonString.replace("d_2",output[1])

                        if(i['tag'] == "AI_Info"):
                            jsonString = jsonString.replace("d_1", proj_type) #d_1
                        if(i['tag']=="Result"):
                            global flag
                            flag=1
                        if(flag==1):
                            jsonString = jsonString.replace("d_0","1")
                            jsonString = jsonString.replace("d_1", proj_type)
                            jsonString = jsonString.replace("d_2",salary)
                            flag=0 #
                        jsonString = json.loads(jsonString)
                        file = open(fileName, "a")
                        json.dump(jsonString, file)
                        file.write('\n')
                        file.close()
                        return tmp_response #print(tmp_response)
            results.pop(0)
            
#ERROR_THRESHOLD = 0.25

#das


#while True:
#    input_data = input("You- ")
#    answer = response(input_data, userID)
 #   answer

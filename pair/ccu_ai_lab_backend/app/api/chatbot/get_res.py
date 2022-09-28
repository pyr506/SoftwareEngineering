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
warnings.filterwarnings("ignore")
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
#print("Loading Pickle.....")
data = pickle.load( open( os.path.join(script_dir, 'training_data'), "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

with open(os.path.join(script_dir, 'intents.json')) as json_data:
    intents = json.load(json_data)
    
#print("Loading the Model......")
# load our saved model
model.load(os.path.join(script_dir, 'model.tflearn'))

#Loading Pickle.....
#Loading the Model......
#INFO:tensorflow:Restoring parameters from E:\FreeBirdsCrew\Chatbot\model.tflearn

get_result = 0
proj_type = " "
department     = " "
time = " "
member = " "
country = " "
flag = 0
jsonString = '{ "flag": " ", "project_types": " ", "department": " ", "time": " ", "member": " " , "country":" " , "response":" "}'
jsonString = json.loads(jsonString, strict=False)

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
                
    return(np.array(bag))

# create a data structure to hold user context
context = {}
match = {}
userID = 0
context[userID] = ""
match[userID] = ""

type_switch = 0
ERROR_THRESHOLD = 0.25
#print("ERROR_THRESHOLD = 0.25")

def init(userID):
    global get_result
    global flag
    global jsonString
    jsonString['flag'] = " "
    jsonString['project_types'] = " "
    jsonString['department'] = " "
    jsonString['time'] = " "
    jsonString['member'] = " "
    jsonString['country'] = " "
    

def classify(sentence):
    # Prediction or To Get the Posibility or Probability from the Model
    results = model.predict([bow(sentence, words)])[0]
    # Exclude those results which are Below Threshold
    global type_switch
    if type_switch == 0:
        #print('---switch=0---')
        results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    if type_switch == 1:
        #print('---switch=1---')
        results = [[i,r] for i,r in enumerate(results)]
    # Sorting is Done because heigher Confidence Answer comes first.
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1])) #Tuppl -> Intent and Probability
    return return_list



def response(sentence, userID, show_details=False):
    global get_result
    global flag
    global jsonString
    if (jsonString['flag'] == "2" or jsonString['flag'] == "1") :
        #flag=0
        jsonString['flag'] = " "
        jsonString['project_types'] = " "
        jsonString['department'] = " "
        jsonString['time'] = " "
        jsonString['member'] = " "
        jsonString['country'] = " "

    results = classify(sentence)
    # That Means if Classification is Done then Find the Matching Tag.
    if results:
        # Long Loop to get the Result.
        while results:
            for i in intents['intents']:
                # Tag Finding
                if (i['tag'] == results[0][0]and not  (get_result == 0 and  i['tag']=="Result")):
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        #if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']
                        #print('context', context[userID])
                    if 'context_filter' in i:
                        match[userID] = i['context_filter']
                    # check if this intent is contextual and applies to this user's conversation
                    if (not 'context_filter' in i  or \
                        (userID in context and 'context_filter' in i and match[userID] == context[userID])):
                        #if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        if('context_filter' in i and i['context_filter'] == context[userID]):
                            context[userID] = "" 
                            match[userID] = ""
                        
                        tmp_response = random.choice(i['responses'])
                        fileName = "my-data.json"    
                        jsonString['response'] = tmp_response
                        if(i['type']== 0):
                            if(i['tag'] == "Duration_Set"):
                                output=sentence.split()
                                global time
                                get_result = 1
                                time = output[1]
                                jsonString['time'] = time
                            if(i['tag'] == "Country_Set"):
                                output=sentence.split()
                                global country
                                get_result = 1
                                country = output[1]
                                jsonString['country'] = country
                            if(i['tag'] == "Taiwan"):
                                output=sentence.split()
                                get_result = 1
                                country = output[1]
                                jsonString['country'] = country
                            if(i['tag'] == "India"):
                                output=sentence.split()
                                get_result = 1
                                country = output[1]
                                jsonString['country'] = country
                            if(i['tag'] == "Department_Set"):
                                output=sentence.split()
                                global department
                                tmp = " "
                                output.pop(0)
                                department = tmp.join(output)
                                get_result = 1
                                jsonString['department'] = department
                            if(i['tag'] == "Member_Set"):
                                output=sentence.split()
                                global member
                                get_result = 1
                                member = output[1]
                                jsonString['member'] = member
                            if(i['tag'] == "Project_Type"):
                                flag=2
                                jsonString['flag'] = "2"
                            if(i['tag']=="Result"):
                                flag=1
                                jsonString['flag'] = "1"

                        if(i['type']== 1):
                            global type_switch
                            type_switch = 1
                            for j in intents['intents']:
                                if(i['tag']== j['tag'] and i['type'] == 1 and j['type'] == 1):
                                    global proj_type
                                    proj_type = i['tag']
                        if(i['type'] == 2):
                            type_switch = 0
                            for j in intents['intents']:
                                if(i['tag']== j['tag'] and i['type'] == 2 and j['type'] == 2):
                                    get_result = 1
                                    jsonString['project_types'] += " "
                                    jsonString['project_types'] += proj_type
                        if(i['type'] == 3):
                            type_switch = 1
                            for j in intents['intents']:
                                if(i['tag'] == j['tag'] and i['type'] == 3 and j['type'] == 3):
                                    department = i['tag']
                        if(i['type'] == 4):
                            type_switch = 0
                            for j in intents['intents']:
                                if(i['tag'] == j['tag'] and i['type'] == 4 and j['type'] == 4):
                                    jsonString['department'] = department
                        
                        print(flag)
                        file = open(fileName, "a")
                        json.dump(jsonString, file)
                        file.write('\n')
                        file.close()
                        return jsonString
            results.pop(0)
            
#ERROR_THRESHOLD = 0.25

def send_msg(msg):
    input_data = msg
    answer = response(input_data, userID)
    return answer




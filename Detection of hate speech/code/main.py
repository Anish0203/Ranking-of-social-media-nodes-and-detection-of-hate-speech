import pandas as pd
import string
import numpy as np
from sklearn import svm
import spacy
import fasttext
import en_core_web_md
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


def remove_pun(txt):                                   # function for removing punctuation
    text_no_pun="".join([c for c in txt if c not in string.punctuation])
    return text_no_pun
##Training data
with open("../data/train.tsv") as f:
    lines=f.readlines()
id=[]
text=[]
hateful=[]
for line in lines:                        #The following steps are done to read the file properly
    s=""
    c=0
    for char in line:
        if char=='\t' and c==0:
            id.append(s)
            s=""
            c=1
            continue
        if char=='\t' and c==1:
            text.append(s)
            s=""
            c=0
            continue
        if char=='\n':
            hateful.append(s)
            s=""
            break
        s=s+char
id.pop(0)
text.pop(0)
hateful.pop(0)
data_train=pd.DataFrame({'id': id, 'text': text, 'hateful': hateful})
data_train['text_no_pun']=data_train['text'].apply(lambda x: remove_pun(x))
data_train['text_lower']=data_train['text_no_pun'].apply(lambda x: str(x).lower())  #converting to lower
data_train=data_train.drop(columns=["text","text_no_pun"])
##Testing data
with open("../data/test.tsv") as f:
    lines=f.readlines()
id=[]
text=[]
for line in lines:                         #similarly done for the test file
    s=""
    for char in line:
        if char=='\t':
            id.append(s)
            s=""
            continue
        if char=='\n':
            text.append(s)
            s=""
            break
        s=s+char
id.pop(0)
text.pop(0)
data_test=pd.DataFrame({'id': id, 'text': text})
data_test['text_no_pun']=data_test['text'].apply(lambda x: remove_pun(x))
data_test['text_lower']=data_test['text_no_pun'].apply(lambda x: str(x).lower())
data_test=data_test.drop(columns=["text","text_no_pun"])
df3=data_train.copy()
corpus=[]                                  #corpus of training data
for i in range(df3.shape[0]):
    corpus.append(df3.iloc[i][2])
test_corpus=[]                             #corpus of testing data
for i in range(data_test.shape[0]):
    test_corpus.append(data_test.iloc[i][1])
df10=df3.copy()


def RForest():                            # Random Forest
    vectorizer = TfidfVectorizer(min_df=5,max_df=0.8)
    X=vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    dense = X.todense()
    denselist = dense.tolist()
    X_train=pd.DataFrame(denselist, columns=feature_names)
    y_train=df3["hateful"]
    model1=RandomForestClassifier()
    model1.fit(X_train,y_train)
    test_X=vectorizer.transform(test_corpus)
    test_dense = test_X.todense()
    test_denselist = test_dense.tolist()
    X_test=pd.DataFrame(test_denselist, columns=feature_names)
    y_pred=model1.predict(X_test)
    test_id=data_test["id"]
    pred = pd.DataFrame({'id': test_id, 'hateful': y_pred})
    pred.to_csv('../predictions/RF.csv', index=False)

def SpacySVM():                 #SVM
    nlp=en_core_web_md.load()
    document=nlp.pipe(corpus)
    tweets_vector = np.array([tweet.vector for tweet in document])
    df7=df3.copy()
    X_train = tweets_vector
    y_train = df7["hateful"]
    model_svm=svm.SVC(kernel='rbf')
    model_svm.fit(X_train,y_train)
    test_doc=nlp.pipe(test_corpus)
    X_test=np.array([tweet.vector for tweet in test_doc])
    y_pred=model_svm.predict(X_test)
    test_id=data_test["id"]
    pred = pd.DataFrame({'id': test_id, 'hateful': y_pred})
    pred.to_csv('../predictions/SVM.csv', index=False)

def fast():                    #Fasttest
    X=df10["text_lower"]
    y=df10["hateful"]
    X_train=X.copy()
    y_train=y.copy()
    # Write the train file.                 Done for specified input for the model
    with open("./trainfast.txt", "w") as train_file_handler:
        for X_train_entry, y_train_entry in zip(X_train, y_train):
            line_to_write = "__label__" + str(y_train_entry) + "\t" + str(X_train_entry) + "\n"
            try:
                train_file_handler.write(line_to_write)
            except:
                print(line_to_write)
                break
    model_f=fasttext.train_supervised(input="./trainfast.txt")
    y_pred=[]
    for i in range(data_test.shape[0]):  #Done to check the presence of any \n in sentence
        s=data_test.iloc[i][1]
        sub=""
        for char in s:
            if(char=='\n'):
                break
            else:
                sub=sub+char
        pred=model_f.predict(sub)[0]
        y_pred.append(pred[0][9])       #To get only the label value
    test_id=data_test["id"]
    pred = pd.DataFrame({'id': test_id, 'hateful': y_pred})
    pred.to_csv('../predictions/FT.csv', index=False)


RForest()
SpacySVM()
fast()
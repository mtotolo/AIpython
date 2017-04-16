import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier

train_path = "./aclImdb/train/" # use terminal to ls files under this directory
test_path = "./imdb_te.csv" # test data for grade evaluation

os.chdir("d:/Users/TotoloM/Desktop/AI/project5/")

def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    files = [f for f in os.listdir(inpath + "neg/") if os.path.isfile(
            inpath + "neg/" + f)]
    data=[]
    for f in files:
        with open (inpath + "neg/" + f, "r", encoding="utf8") as myfile:
            data.append(myfile.read())
    df_neg = pd.DataFrame({"text":data, "polarity":0})
    files = [f for f in os.listdir(inpath + "pos/") if os.path.isfile(
            inpath + "pos/" + f)]
    data=[]
    for f in files:
        with open (inpath + "pos/" + f, "r", encoding="utf8") as myfile:
            data.append(myfile.read())
    df_pos = pd.DataFrame({"text":data, "polarity":1})
    df=pd.concat([df_neg,df_pos])
    df=df[["text","polarity"]]
    df.to_csv(name,encoding="utf8")
    
    
  
if __name__ == "__main__":
    df = pd.read_csv("./imdb_tr.csv",names=["text","polarity"],encoding="utf8",
                     header=0,index_col=0)
    df_v = pd.read_csv("./imdb_va.csv",names=["text","polarity"],encoding="utf8",
                     header=0,index_col=0)
    with open ("./stopwords.en.txt","r") as f:
        stopwords=f.read().split("\n")
    count_vect = CountVectorizer(stop_words=stopwords+["br","br br","br br br"], 
                                analyzer="word",
                                ngram_range=(1,1), 
                                min_df=20)
    train_token = count_vect.fit_transform(df["text"])
    tfidftransformer = TfidfTransformer()
    train_token_tfidf = tfidftransformer.fit_transform(train_token)
    
    SGDcl = SGDClassifier(loss="hinge",penalty="l1")
    model=SGDcl.fit(train_token,df["polarity"])
    modelTfidf=SGDcl.fit(train_token_tfidf,df["polarity"])
    
    val_token = count_vect.transform(df_v["text"])
#    print(model.score(train_token,df["polarity"]))
#    print(model.score(train_token_tfidf,df["polarity"]))    
#    print(model.score(val_token,df_v["polarity"]))
#    print(modelTfidf.score(tfidftransformer.transform(val_token),df_v["polarity"]))
    with open("./unigram.output.txt","w") as f:
        f.write("\n".join(map(str,(list(model.predict(val_token))))))
    with open("./unigramtfidf.output.txt","w") as f:
        f.write("\n".join(map(str,(list(modelTfidf.predict(tfidftransformer.transform(val_token)))))))
        
    count_vect = CountVectorizer(stop_words=stopwords+["br","br br","br br br"], 
                                analyzer="word",
                                ngram_range=(1,2), 
                                min_df=20)
    train_token = count_vect.fit_transform(df["text"])
    tfidftransformer = TfidfTransformer()
    train_token_tfidf = tfidftransformer.fit_transform(train_token)
    
    SGDcl = SGDClassifier(loss="hinge",penalty="l1")
    model=SGDcl.fit(train_token,df["polarity"])
    modelTfidf=SGDcl.fit(train_token_tfidf,df["polarity"])
    
    val_token = count_vect.transform(df_v["text"])
    with open("./bigram.output.txt","w") as f:
        f.write("\n".join(map(str,(list(model.predict(val_token))))))
    with open("./bigramtfidf.output.txt","w") as f:
        f.write("\n".join(map(str,(list(modelTfidf.predict(tfidftransformer.transform(val_token)))))))
#    print(model.score(train_token,df["polarity"]))
#    print(model.score(train_token_tfidf,df["polarity"]))    
#    print(model.score(val_token,df_v["polarity"]))
#    print(modelTfidf.score(tfidftransformer.transform(val_token),df_v["polarity"]))
 
    
    
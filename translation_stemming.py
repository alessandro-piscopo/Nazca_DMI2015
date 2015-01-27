from nltk.corpus import stopwords
import nltk, string
import pandas as pd
import goslate
import re
from collections import Counter
import csv


#load the data
#the code that translate and normalise japanese tweets works also on spanish and can be applied to that by changng the variables' names
nazca_tweets_ja = pd.read_csv('tweets_jap.csv', header=0)
#nazca_tweets_es = pd.read_csv('tweets_es.csv', header=0)
nazca_tweets_eng = pd.read_csv('tweets_eng.csv', header=0)

#load goslate API
gs = goslate.Goslate()


contents_ja = nazca_tweets_ja['content'] #contents_es = nazca_tweets_es['content']
contents_eng = nazca_tweets_eng['content']


#translate tweets' content
translated_tweets_ja = []
for content in contents_ja:
    translated = gs.translate(content, 'en')
    translated_tweets_ja.append(translated)


#encoding to prevent errors when writing the csv files
translated_encoded_ja = []
for i in translated_tweets_ja:
    enc = i.encode('utf-8')
    translated_encoded_ja.append(enc)

#for english
content_encoded = []
for i in contents_eng:
    enc = str(i)
    content_encoded.append(enc)



nazca_tweets_ja['translated_tweets'] = translated_encoded_ja
 
#apply stemming
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]   

#the two following functions are not used      
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.translate(remove_punctuation_map)))
 
def normalize_eng(text):
    return stem_tokens(nltk.word_tokenize(text))


#the stopwords list is applied after translation, for the lack of a correspondent Japanese list  
stops = set(stopwords.words('english'))
  
def apply_stopwords(text_list):
    cleaned_content = []
    for text in text_list:
        new_text = []
        for w in text.split():
            if w not in stops:
                new_text.append(w)
                new_string = " ".join(new_text)
        cleaned_content.append(new_string)
    return cleaned_content

#apply stopwords list 
stopped_text_enc = apply_stopwords(translated_encoded_ja)
stopped_text = apply_stopwords(translated_tweets_ja)

nazca_tweets_ja['stopped_tweets'] = stopped_text_enc

stopped_text_eng1 = apply_stopwords(contents_eng)
stopped_text_eng2 = apply_stopwords(content_encoded)

#normalise texts
stopped_tweets_ja = nazca_tweets_ja['stopwords_tweets']

#text in lower case
lowered_text = []
for i in stopped_text_enc:
    encoded_text = i.lower().decode('utf-8')
    lowered_text.append(encoded_text)

#stem text 
normalised_ja = []
for tweet in lowered_text:
    stemmed_tweets = normalize(tweet)
    normalised_ja.append(stemmed_tweets)


#tokenise does not work with the english text, we apply another method 
exclude = set(string.punctuation)    
new_text = []
for i in stopped_text_eng2:
    s = ''.join(ch for ch in i if ch not in exclude)
    encoded_s = s.lower().decode('utf-8')
    new_text.append(encoded_s)

 
#stemming 
nlist2 = [] 
for element in new_text:
    nlist2.append(re.split(r' ', element))


normalised_eng = []
for i in nlist2:
    stemmed_tweets = stem_tokens(i)
    normalised_eng.append(stemmed_tweets)




        
#add columns to dataframes
nazca_tweets_eng['normalised_tweets'] = normalised_eng
nazca_tweets_eng['stopwords_tweets'] = stopped_text_eng1
nazca_tweets_ja['normalised_tweets'] = normalised_ja




#write files
nazca_tweets_eng.to_csv('nazca_tweets_en.csv')
nazca_tweets_ja.to_csv('nazca_tweets_ja.csv')

#word frequencies
#texts have to be encoded, otherwise it is not possible to write the results on csv

new_normalised_eng = []
for i in normalised_eng:
    new_tweet = []
    for j in i:
        dec_string = j.encode('utf-8')
        new_tweet.append(dec_string)
    new_normalised_eng.append(new_tweet)
    
eng_freq = Counter(word for sublist in new_normalised_eng for word in sublist)

#japanese
new_normalised_ja = []
for i in normalised_ja:
    new_tweet = []
    for j in i:
        dec_string = j.encode('utf-8')
        new_tweet.append(dec_string)
    new_normalised_ja.append(new_tweet)
ja_freq = Counter(word for sublist in new_normalised_ja for word in sublist)

#write frequencies on files
writer = csv.writer(open('eng_freq.csv', 'wb'))
for key, value in eng_freq.items():
   writer.writerow([key, value])
   
writer = csv.writer(open('ja_freq.csv', 'wb'))
for key, value in ja_freq.items():
   writer.writerow([key, value])
   

        

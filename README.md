# DMI2015
The scripts in this folder were written in occasion of the 2015 Digital Methods Initiative Winter School

### translation_stemming.py
The 'translation_stemming.py' script uses the Goslate API to automatically translate the tweets content in our dataset, by using Google Translate. A stopword list is applied to the translated text, in order to eliminate the most common words. Afterwards, the text are stemmed, using the nltk Python package.
It would have been desirable to apply the stopwords list directly to the original text, but in the package used (nltk) a list for Japanese was not available.

The script also provide the word occurrencies. The data related to these frequencies are dirty, due to the presence of several URLs in the dataset, each of one occurring only once.

### news_image_scraping.py
This script downloads automatically the images associated to the URLs in the 'images_url' column of the news dataset of the dataset related to the Nazca incident in December 2014.

### datasets
### datasets are not available anymore, as they are not open
This folder contains:
- the datasets with the tweets related to the Nazca incident from the dataset provided by Greenpeace, which were retweeted at least twice and were either in English, Spanish or Japanese (tweets_eng.csv, tweets_es.csv, tweets_ja.csv).
- the news dataset, referred by the news_image_scraping.py.

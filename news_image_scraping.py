import urllib
import pandas as pd
import csv as csv

#load the dataset
nazca_news = pd.read_csv('nazca_news_1401.csv', header=0)


#create arrays
images_links = nazca_news['images.url']
dates = nazca_news['published']
images_place = nazca_news['url']
images_engagement = nazca_news['engagement']
images_dated = zip(images_links, dates, images_place, images_engagement)



#download images
image_dated_partial = images_dated
picture_name_date = []
errors = []
counter = 0
for x, i, j, k in image_dated_partial:
    if x:
        if type(x) is not str or x == 0:
            continue
            
        counter += 1
        filename = str(counter) + ".jpg"
        urllib.urlretrieve(x, filename)            
        picture_name_date.append((filename, i, j, k))

    else :
        picture_name_date.append('none', i, j, k)



#save picture_name_date list
with open('nazca_pictures.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['img_name','date', 'url', 'engagement'])
    for row in picture_name_date:
        csv_out.writerow(row)    



    
            
    

                
        

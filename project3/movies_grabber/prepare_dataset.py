import pandas as pd
import omdb
from time import sleep
import re

API_KEY = '4d93e7c3' 
omdb.set_default('apikey', API_KEY)
omdb.set_default('timeout', 2)

def create_new_features(feature, number_of_new_features,  dataset):

    mylist = dataset[feature].split(',')
    dictionary = {}

    for i in range(1,number_of_new_features+1):

        if (number_of_new_features!=1):
            key = feature+str(i)
        else:
            key = feature

        if (i<=len(mylist)):
            mylist[i-1] = re.sub(r'\([^)]*\)', '', mylist[i-1])
            dictionary[key] = mylist[i-1].strip()
        else:
            dictionary[key] = 'N/A'

    return (dictionary)

def prepare_dataset(dataset):

    new_dataset = []

    for movie in dataset:
        
        movie_with_new_features = {}
        
        movie['actor'] = movie['actors']
        del movie['actors']

        # create some new features
        movie_with_new_features.update(create_new_features('actor', 2, movie))
        movie_with_new_features.update(create_new_features('writer', 1, movie))
        movie_with_new_features.update(create_new_features('director', 1, movie))
        movie_with_new_features.update(create_new_features('genre', 1, movie))
        movie_with_new_features.update(create_new_features('language', 1, movie))
        movie_with_new_features.update(create_new_features('country', 1, movie))
        
        # create target variable based on imdb rating
        if (float(movie['imdb_rating']) > 5.0):
            movie_with_new_features['Success_of_Movie'] = 'Success'
        else:
            movie_with_new_features['Success_of_Movie'] = 'Failure'

        #copy some features

        if (movie['released'] != 'N/A'):
            movie_with_new_features['released'] = movie['released'].split()[2]
        else:
            movie_with_new_features['released'] = movie['released']

        if (movie['runtime'] != 'N/A'):
            movie_with_new_features['runtime'] = movie['runtime'].split()[0]
        else:
            movie_with_new_features['runtime'] = movie['runtime']
        
        movie_with_new_features['id'] = movie['imdb_id']

        new_dataset.append(movie_with_new_features)

    return(new_dataset)

if __name__ == "__main__":

    df_2006_2016 = pd.read_csv("id_2006_2016.csv", usecols=["tconst"])
    df_2017 = pd.read_csv("id_2017.csv", usecols=["tconst"])

    movies_list = []

    num_of_movies = int(input("Give number of 2006-2016 movies: "))

    for i in range(0, num_of_movies):
        print("Movie: {}".format(i))
        # get the movie
        movie_id = df_2006_2016['tconst'].iloc[i]
    
        try:
            movie = omdb.imdbid(movie_id)

            if ('N/A' not in movie['imdb_rating']):
                movies_list.append(dict(movie))
        except:
            pass

    print("Completed!")

    num_of_movies = int(input("Give number of 2017 movies: "))

    for i in range(0, num_of_movies):
        print("Movie: {}".format(i))
        # get the movie
        movie_id = df_2017['tconst'].iloc[i]
        try:
            movie = omdb.imdbid(movie_id)

            if ('N/A' not in movie['imdb_rating']):
                movies_list.append(dict(movie))
        except:
            pass
   
    dataset = prepare_dataset(movies_list)
    df = pd.DataFrame(dataset)
    df.to_csv("movies.csv")

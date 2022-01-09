from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from unidecode import unidecode
import pandas as pd
import numpy as np
import re
from surprise import Dataset, Reader, KNNWithMeans

# Content based recommendation

# Read the data
bgg = pd.read_csv('bgg.csv')

# Process the data
# change the name to all English letters
bgg['name'] = bgg['name'].apply(unidecode)
# Add a column of whether the game is a cooperative game
bgg['cooperative'] = bgg['mechanics'].apply(lambda x: 'Cooperative' in x)


def text_processing(text):
    '''
    Function that takes in a text string, removes all the punctuations and converts it to lower case.
    '''
    text_new = " ".join(re.findall("[A-Za-z]+", text.lower()))
    return text_new


bgg['feature'] = bgg['gameType'].apply(text_processing) + ' ' + bgg['mechanics'].apply(
    text_processing)  # +" " +bgg['category'].apply(text_processing)


# Build the recommendation model
# Vectorize the text using tfidf
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(bgg['feature'])
# Compute the cosine similarity matrix
sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# mapping the game name with the indices
indices = pd.Series(bgg.index, index=bgg['name'].str.lower())


# # model-based recommendation


# # read the data, and add a column of userid
# ratings = pd.read_csv('ratings2.csv')
# userid = pd.Categorical(ratings["username"])
# ratings['userid'] = userid.codes

# # Extract users who have given more than 50 ratings
# m = ratings['userid'].value_counts() > 50
# ratings = ratings[ratings['userid'].isin(m[m].index)]

# # Prepare the data
# reader = Reader(rating_scale=(1, 10))

# games = Dataset.load_from_df(ratings[['userid', 'gameid', 'rating']], reader)

# trainingSet = games.build_full_trainset()

# # Build the model
# sim_options = {
#     "name": "cosine",
#     "user_based": False,  # Compute  similarities between items
# }

# model = KNNWithMeans(sim_options=sim_options)

# model.fit(trainingSet)
# game_sim = model.sim


def recommend_indices(games, sim=sim):
    '''
    Function that takes in a game name and output the indices from most recommended to least recommended
    '''
    if len(games) == 0:
        return bgg.index
    else:
        games = games.split(',')
        n = len(games)

        sim_scores = np.zeros(1000)
        game_idx = []
        for game in games:
            game = game.strip().lower()
            # Get the index of the given game
            idx = indices[game]
            sim_scores += sim[idx]
            game_idx.append(idx)

        scores = list(enumerate(sim_scores))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        # Get the index of the 10 most similar games
        game_indices = [i[0] for i in scores]
        recommend_indices = [i for i in game_indices if i not in game_idx]

        # Return the recommended indices in order
        return recommend_indices


def filtered_indices(rows, type, players, playtime, age, cooperative, rank, complexity):
    global bgg
    bgg_r = bgg.loc[rows, :]

    # filter by game type
    if type != 'All':
        bgg_r_1 = bgg_r[bgg_r['gameType'].apply(lambda x: type in x)]
    else:
        bgg_r_1 = bgg_r

    # filter by number of players
    if players != 0:
        bgg_r_2 = bgg_r_1.loc[(bgg_r_1['minPlayers'] <= players) & (
            bgg_r_1['maxPlayers'] >= players)]
    else:
        bgg_r_2 = bgg_r_1

    # filter by play time
    if playtime != 0:
        bgg_r_3 = bgg_r_2.loc[(bgg_r_2['minTime'] <= playtime) & (
            bgg_r_2['maxTime'] >= playtime)]
    else:
        bgg_r_3 = bgg_r_2

    # filter by age
    if age != 0:
        bgg_r_4 = bgg_r_3[bgg_r_3['age'] >= age]
    else:
        bgg_r_4 = bgg_r_3

    # filter by cooperative or not
    if cooperative == 1:
        bgg_r_5 = bgg_r_4[bgg_r_4['cooperative'] == True]
    elif cooperative == 2:
        bgg_r_5 = bgg_r_4[bgg_r_4['cooperative'] == False]
    else:
        bgg_r_5 = bgg_r_4

    # filter by rank
    bgg_r_6 = bgg_r_5[bgg_r_5['rank'] <= rank]

    # filter by complexity
    bgg_r_7 = bgg_r_6.loc[(bgg_r_6['complexity'] >= complexity[0]) & (
        bgg_r_6['complexity'] <= complexity[1])]

    return bgg_r_7.index


def get_labels(rows):
    labels = []
    for i in rows:
        labels.append(
            f"#{bgg['rank'][i]}: {bgg['name'][i]}")
    return labels


def get_images(rows):
    images = []
    for i in rows:
        images.append(bgg['thumbnail'][i])
    return images


def get_urls(rows):
    urls = []
    for i in rows:
        urls.append(bgg['url'][i])
    return urls

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
# For web scraping
from bs4 import BeautifulSoup as bs
import requests
import json

# Scrape data from BGG

# Create an empty dictionary to store the data
bgg = dict(id=[], url=[],
           name=[],  rank=[],
           longDescrip=[], shortDescrip=[],
           yearPublished=[],
           minPlayers=[], maxPlayers=[], bestPlayers=[],
           playTime=[], minTime=[], maxTime=[],
           age=[],
           thumbnail=[],
           votes=[], bggRating=[], avgRating=[],
           numWeights=[], complexity=[],
           playerPoll=[],
           publisher=[],
           gameType=[],
           mechanics=[],
           category=[]
           )


# Scrape the top 1000 games from boardgamegeeek.com
pages = range(1, 11)

for page in pages:

    print(page)
    url = f"https://boardgamegeek.com/browse/boardgame/page/{page}"

    # Load the url
    req = requests.get(url)
    sp = bs(req.content, 'html.parser')
    # find the table
    table = sp.find('table', class_='collection_table')
    rows = table.find_all('tr')
    # loop through each row
    for row in rows[1:]:

        # Get the game URL
        href = row.find('a', class_="primary")['href']
        try:
            bgg['shortDescrip'].append(row.find('p').text.strip())
        except:
            bgg['shortDescrip'].append('NA')

        bgg['url'].append(f'https://boardgamegeek.com/{href}')

        # Get the game id
        id = href.split('/')[2]
        bgg['id'].append(id)

        # Go to the API, and scrape the maxtime, mintime and age
        u = f"https://www.boardgamegeek.com/xmlapi/boardgame/{id}&stats=1"
        request = requests.get(u)
        soup = bs(request.content, 'html.parser')

        bgg['name'].append(soup.find('name', primary='true').text)
        bgg['rank'].append(int(soup.find("ranks").find('rank')['value']))
        bgg['yearPublished'].append(int(soup.yearpublished.text))
        bgg['bestPlayers'].append(np.argmax(
            [r.result['numvotes'] for r in soup.find("poll").find_all("results")]))
        bgg['minPlayers'].append(int(soup.minplayers.text))
        bgg['maxPlayers'].append(int(soup.maxplayers.text))
        bgg['playTime'].append(int(soup.playingtime.text))
        bgg['minTime'].append(int(soup.minplaytime.text))
        bgg['maxTime'].append(int(soup.maxplaytime.text))
        bgg['age'].append(int(soup.age.text))
        bgg['thumbnail'].append(soup.thumbnail.text)
        bgg['publisher'].append(soup.boardgamepublisher.text)
        bgg['votes'].append(int(soup.ratings.usersrated.text))
        bgg['bggRating'].append(float(soup.ratings.bayesaverage.text))
        bgg['avgRating'].append(float(soup.ratings.average.text))
        bgg['numWeights'].append(int(soup.ratings.numweights.text))
        bgg['complexity'].append(float(soup.ratings.averageweight.text))
        bgg['gameType'].append(
            [type.text for type in soup.find_all('boardgamesubdomain')])
        bgg['category'].append(
            [c.text for c in soup.find_all('boardgamecategory')])
        bgg['mechanics'].append(
            [m.text for m in soup.find_all('boardgamemechanic')])
        bgg['playerPoll'].append(
            [m.text for m in soup.find_all('boardgamemechanic')])
        bgg['longDescrip'].append(soup.description.text.split('<')[0])

# Turn the dictionary to a data frame.
bgg = pd.DataFrame(bgg)

# Save the scraped data
bgg.to_csv('bgg.csv', index=False)


# Scrape 1000 comments of each game for the top 1000 games from BGG
bgg = pd.read_csv('bgg.csv')

ratings = dict(username=[], rating=[], gameid=[])
pages = range(1, 31)
i = 1

for id in bgg['id'][:1000]:
    print(i)
    i += 1
    for page in pages:
        try:
            url = f"https://www.boardgamegeek.com/xmlapi/boardgame/{id}&stats=1&comments=1&page={page}"
            request = requests.get(url)
            soup = bs(request.content, 'html.parser')
            comments = soup.find_all('comment')

            for comment in comments:
                ratings['gameid'].append(id)
                ratings['username'].append(comment['username'])
                ratings['rating'].append(comment['rating'])

        except:
            print('no more pages')
            continue

ratings = pd.DataFrame(ratings)
ratings = ratings[ratings["rating"] != 'N/A']
ratings.to_csv('ratings2.csv', index=False)

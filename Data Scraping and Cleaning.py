
# coding: utf-8

# # Data Scraping and Cleaning
# 
# Using the SOFIFA website URLs of each of the players, the webpage contents of each of the players were fetched. The 'Beautiful Soup' package was used to scrape the required fifa player attributes from the contents of the webpages by creating objects from the webpages. The objects contained the HTML scripts of the webpages and the player attributes were scraped using the find() and find_all() functions provided by Beautiful Soup. Using these functions, the classes containing the required player attributes were found and subsequently the data was extracted.
# 
# The extracted data had punctuations and also some of the words and the player attributes were connected together and hence the data had to be cleaned. Once the data was cleaned, it was organized into a pandas dataframe and the dataframe was written into a '.csv' file.

# In[1]:


from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time


# ### Storing the Player URLs of each of the Players

# In[2]:


url_main='https://sofifa.com'
player_urls = {}
for n in range(0,15000,60):
    page = requests.get(url_main + '/players?offset=' + str(n))
    soup = bs(page.content, 'lxml')
    page_contents = soup.find('table', {'class': 'table table-hover persist-area'}).find('tbody').find_all('a')
    for i in page_contents:
        if i['href'][0:8] == '/player/':  player_urls[i.text] = i['href']


# ### Extracting the Player Attributes using the Player URLs

# In[3]:


start_time = time.time()

player_attr = {}
st, mid, df, gk = 'Striker', 'Midfielder', 'Defender', 'GoalKeeper'
player_category_map = {'LW':st, 'ST':st, 'RW':st, 'LF':st, 'CF':st, 'RF':st,
                      'CAM':mid, 'LM':mid, 'CM':mid, 'RM':mid, 'CDM':mid,
                      'LWB':df, 'LB':df, 'CB':df, 'RB':df, 'RWB':df,
                      'GK': gk}
content_aux_list = ['meta', 'column col-4 text-center']

attr_list = ['Crossing', 'Finishing', 'Heading Accuracy', 'Short Passing', 'Volleys', 'Dribbling', 'Curve', 'FK Accuracy',
             'Long Passing', 'Ball Control', 'Acceleration', 'Sprint Speed', 'Agility', 'Reactions', 'Balance', 'Shot Power',
             'Jumping', 'Stamina', 'Strength', 'Long Shots', 'Aggression', 'Interceptions', 'Positioning', 'Vision',
             'Penalties', 'Composure', 'Marking', 'Standing Tackle', 'Sliding Tackle', 'GK Diving', 'GK Handling',
             'GK Kicking', 'GK Positioning', 'GK Reflexes']
aux_attr_list = ['Player Category', 'Age', 'Height', 'Weight', 'Overall Rating', 'Value', 'Wage'] 
attr_len = len(attr_list)
aux_attr_len = len(aux_attr_list)

for player_name, url in player_urls.items():
    player_url = url_main + url
    page = requests.get(player_url)
    soup = bs(page.content, 'lxml')
    content = soup.find_all('ul', {'class': 'pl'})
    
    # storing all the words of each of the webpage as a list
    lines = []
    for c in content:
        line = c.text.strip().split()
        new_line = []
        for word in line:
            if word[0].isdigit(): 
                new_line.append(word)
                continue
            new_word = ''
            number = ''
            for letter in word:
                if letter.isdigit() or letter == '+' or letter == '-':   number += letter
                else:                                                    new_word += letter
            if len(new_word) != 0:    new_line.append(new_word)
            if len(number) != 0:      new_line.append(number)
        lines.append(new_line)

    # fetching the attribute ratings by matching the words with the list of attributes given by 'attr_list'
    attr_ratings = []
    attr_count = 0
    for line in lines:
        for i,word in enumerate(line):
            if word[0].isdigit():
                new_word = ''
                for next_word in line[i+1:]:
                    if next_word[0].isdigit(): 
                        break
                    else:
                        if len(new_word) == 0:    new_word += next_word
                        else :                    new_word += ' ' + next_word
                if new_word == attr_list[attr_count]:
                    attr_ratings.append(word)
                    if attr_count < attr_len-1:   attr_count += 1
    for i, rating in enumerate(attr_ratings):
        if len(rating.split('+')) != 1:   attr_ratings[i] = rating.split('+')[0]
        if len(rating.split('-')) != 1:   attr_ratings[i] = rating.split('-')[0]
    if attr_count != attr_len-1:
        print(player_name, '- datapoint not included')   # due to missed attributes, if any
        continue
    
    # fetching the auxiliary attribute data by matching the words with the 'aux_attr_list'
    aux_attr_data = []
    for item in content_aux_list:
        content_aux = soup.find_all('div', {'class': item})
        for c in content_aux:
            line = c.text.strip().split()
            for i,word in enumerate(line):
                word_prev = line[i-1]
                if word[0].isdigit() and word_prev[-3:] == aux_attr_list[1]:
                    if len(word_prev[:-3]) < 2:   aux_attr_data.append(player_category_map[line[i-2]])
                    else:                         aux_attr_data.append(player_category_map[word_prev[:-3]])
                    aux_attr_data.append(word)
                    height, weight = line[-2], line[-1][:-3]
                    aux_attr_data.append(height)
                    aux_attr_data.append(weight)
                if word_prev + ' ' + word == aux_attr_list[4] or word == aux_attr_list[5] or word == aux_attr_list[6]:
                    word_next = line[i+1]
                    aux_attr_data.append(word_next)
    if len(aux_attr_data) != aux_attr_len:
        print(player_name, '- datapoint not included')   # due to missed auxiliary attributes, if any
        continue
    
    # storing all the required player attributes as a dictionary
    player_attr[player_name] = aux_attr_data + attr_ratings
    
print('Time elapsed: %.2f minutes.' %((time.time()-start_time)/60))


# ### Creating, Trimming and Saving the Player Attributes Dataframe

# In[5]:


# creating the dataframe
player_attr_dataframe = pd.DataFrame(columns = ['Player Name'] + aux_attr_list + attr_list)
for name, ratings in player_attr.items():
    player_data = [name]
    for rating in ratings:   player_data.append(rating)
    player_attr_dataframe = player_attr_dataframe.append(pd.Series(player_data,
                                                 index = ['Player Name'] + aux_attr_list + attr_list), ignore_index=True)

# trimming the dataframe
players_per_category = {st:0, mid:0, df:0, gk:0}
desired_players_per_category = {st:2000, mid:4000, df:3000, gk:1000}
for row in player_attr_dataframe.iterrows():
    category = row[1][1]
    if players_per_category[category] != desired_players_per_category[category]:
        players_per_category[category] += 1
    else:
        player_attr_dataframe = player_attr_dataframe.drop(row[0])
player_attr_dataframe = player_attr_dataframe.reset_index(drop=True)
print('Number of players in each category:',players_per_category)

# saving the dataframe
player_attr_dataframe.to_csv('player_attributes.csv')


# ### Ensuring that all the required data is fetched

# In[7]:


if player_attr_dataframe.shape[1] != (player_attr_dataframe.count() == player_attr_dataframe.shape[0]).sum():
    print('Missed some data')
else:
    print('All data fetched')


# ### Reading and Displaying the Player Attributes Dataframe

# In[8]:


player_attr_dataframe = pd.read_csv('player_attributes.csv', index_col=[0])
player_attr_dataframe


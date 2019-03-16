
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import pandas as pd
import requests


# In[2]:


# variables used for extracting the player attributes

st, mid, df, gk = 'Striker', 'Midfielder', 'Defender', 'GoalKeeper'
player_category_map = {'LW':st, 'ST':st, 'RW':st, 'LF':st, 'CF':st, 'RF':st,
                      'CAM':mid, 'LM':mid, 'CM':mid, 'RM':mid, 'CDM':mid,
                      'LWB':df, 'LB':df, 'CB':df, 'RB':df, 'RWB':df,
                      'GK': gk}
content_aux_list = ['meta', 'column col-4 text-center']

attr_list = ['Crossing', 'Finishing', 'Heading Accuracy', 'Short Passing', 'Volleys', 'Dribbling','Curve',
             'FK Accuracy', 'Long Passing', 'Ball Control', 'Acceleration', 'Sprint Speed', 'Agility', 
             'Reactions', 'Balance', 'Shot Power', 'Jumping', 'Stamina', 'Strength', 'Long Shots', 
             'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking',
             'Standing Tackle', 'Sliding Tackle', 'GK Diving', 'GK Handling', 'GK Kicking',
             'GK Positioning', 'GK Reflexes']
aux_attr_list = ['Player Category', 'Age', 'Height', 'Weight', 'Overall Rating', 'Value', 'Wage']

attr_len = len(attr_list)
aux_attr_len = len(aux_attr_list)


# In[3]:


def words_of_page(player_url):
    ''' 
    Returns all the words of each of the webpage as a list given the page url
    
    Arguments:
    player_url (str) : The webpage url of the player
    
    Returns:
    lines (list) : The list of words contained in the webpage
    '''
    
    assert isinstance(player_url,  str), 'Player url is not a string'
    
    page = requests.get(player_url)
    soup = bs(page.content, 'lxml')
    content = soup.find_all('ul', {'class': 'pl'})

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
    
    return lines


# In[4]:


def extract_player_attributes(player_name, player_url):
    '''
    Extracts and returns the attibute ratings of a player given the player name and the player url
    
    Arguments:
    player_name (str) : The name of the player
    player_url  (str) : The website url of the player
    
    Returns:
    player_attributes (dict) : The dictionary containing the player attribute ratings
    '''
    
    assert isinstance(player_name, str), 'Player name is not a string'
    assert isinstance(player_url,  str), 'Player url  is not a string'

    player_attributes = {}
    
    # get all the words in the player's webpage to extract the attribute ratings 
    lines = words_of_page(player_url)
    
    # fetching the attribute ratings by matching the words with list of attributes given by 'attr_list'
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
        print(player_name, '- player not included')   # due to missed attributes, if any
        return {}

    # fetching the auxiliary attribute data by matching the words with the 'aux_attr_list'
    aux_attr_data = []
    for item in content_aux_list:
        page = requests.get(player_url)
        soup = bs(page.content, 'lxml')
        content_aux = soup.find_all('div', {'class': item})
        for c in content_aux:
            line = c.text.strip().split()
            for i,word in enumerate(line):
                word_prev = line[i-1]
                if word[0].isdigit() and word_prev[-3:] == aux_attr_list[1]:
                    if len(word_prev[:-3]) < 2:   
                        aux_attr_data.append(player_category_map[line[i-2]])
                    else:
                        aux_attr_data.append(player_category_map[word_prev[:-3]])
                    aux_attr_data.append(word)
                    height, weight = line[-2], line[-1][:-3]
                    aux_attr_data.append(height)
                    aux_attr_data.append(weight)
                if word_prev + ' ' + word == aux_attr_list[4] or word == aux_attr_list[5] or word == aux_attr_list[6]:
                    word_next = line[i+1]
                    aux_attr_data.append(word_next)
    if len(aux_attr_data) != aux_attr_len:
        print(player_name, '- player not included')   # due to missed auxiliary attributes, if any
        return {}

    # storing all the required player attributes as a dictionary
    player_attributes[player_name] = aux_attr_data + attr_ratings

    return player_attributes


# In[5]:


def create_trim_save_dataframe(attributes_of_all_the_players):
    '''
    Creates the player attributes dataframe from the given player attributes dictionary, trims it and saves it as '.csv' file
    
    Arguments:
    attributes_of_all_the_players (dict) : Attributes of all the players
    '''
    
    assert isinstance(attributes_of_all_the_players, dict), "Attributes of all the players is not a dictionary"
    
    # creating the dataframe
    player_attr_dataframe = pd.DataFrame(columns = ['Player Name'] + aux_attr_list + attr_list)
    for name, ratings in attributes_of_all_the_players.items():
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
    print('Number of players in each category:\n', players_per_category)

    # saving the dataframe
    player_attr_dataframe.to_csv('player_attributes.csv')


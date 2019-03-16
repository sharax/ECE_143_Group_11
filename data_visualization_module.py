
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import subplots
from math import pi

from data_loader_module import load_data


# In[2]:


# loading the player attributes dataframe
player_attributes = load_data


# In[3]:


# generation of the categorical attributes radar plot

def categorical_attributes_radar_plot(category, attributes, percentage, no_of_players, title_part):
    '''
    Generates the radar plots given the list of player attributes and the number of players

    Arguments:
    category (str)       : player category 'Striker','Midfielder','Defender','GoalKeeper'
    attributes (list)    : list of attributes for the plot
    percentage (list)    : list of percentage of players to be analyzed
    no_of_players (list) : list of number of players to be analyzed
    title_part (str)     : part of the title to be used in the plot
    '''
    assert isinstance(category, str)
    assert isinstance(attributes, list)
    assert isinstance(percentage, list)
    assert isinstance(no_of_players, list)
    assert isinstance(title_part, str)

    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111, polar=True)   # set polar axis    
    plot_colors = ['red', 'darkorange', 'green', 'blue']

    for i,number in enumerate(no_of_players):
        
        player_attributes.loc['mean']       = player_attributes.head(number).mean()
        player_attributes.loc['Striker']    = player_attributes[player_attributes['Player Category']=='Striker'].head(number).mean()
        player_attributes.loc['Midfielder'] = player_attributes[player_attributes['Player Category']=='Midfielder'].head(number).mean()
        player_attributes.loc['Defender']   = player_attributes[player_attributes['Player Category']=='Defender'].head(number).mean()
        player_attributes.loc['GoalKeeper'] = player_attributes[player_attributes['Player Category']=='GoalKeeper'].head(number).mean()

        plot_color = plot_colors[i]
        if i!=3:   plot_label = "Top " + str(percentage[i]) + "% of " + category + "s (Mean)"
        else:      plot_label = 'All the ' + category + 's (Mean)'

        stats = player_attributes.loc[category, attributes].values        # get values to be plotted
        angles = np.linspace(0,2*np.pi,len(attributes),endpoint = False)  # angles used for the radar plot
        stats = np.concatenate((stats,[stats[0]]))
        angles = np.concatenate((angles,[angles[0]]))
    
        ax.set_ylim(50-1,100)   # set the limits of yaxis
        ax.plot(angles, stats, plot_color,linewidth = 1.5, label = plot_label)
        ax.fill(angles, stats, plot_color, alpha = 0.05)   # fill the area with transparent color
        ax.set_thetagrids(angles*180/np.pi, attributes)
        
    plt.xticks(angles, attributes, color='black', size=15)
    ax.tick_params(axis='x', pad=50)
    plt.yticks(color="grey", size=10)

    plot_title =  title_part + ' Attributes'+  ' of '+ category +'s'
    ax.set_title(plot_title, pad=60, size=20)
    ax.grid(True)
    plt.legend(bbox_to_anchor=(0,0), fontsize=10)
    fig.savefig('radar/%s' %plot_title, bbox_inches='tight')    # save the figure
        


# In[4]:


# generation of the comprehensive attributes radar plot

def comprehensive_attributes_radar_plot(comparison_attr_dict, comparison_attr_list, comparison_attr_map, number_top):
    '''
    Generates the radar plots given the player attributes list and the top number of players

    Arguments:
    comparison_attr_dict (dict)    : dictionary of the attributes and the corresponding ratings for the plot
    comparison_attr_list (list)    : list of attributes for the plot that are in the dataframe
    comparison_attr_map (dict)     : mapping dictionary to map the attributes used in plots to the attributes in dataframe
    number_top (int)               : top number of players to be analyzed
    '''
    assert isinstance(comparison_attr_dict, dict)
    assert isinstance(comparison_attr_list, list)
    assert isinstance(comparison_attr_map, dict)
    assert isinstance(number_top, int)

    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111,polar =True)
    plot_colors_dict = {'Striker':'red', 'Midfielder':'green', 'Defender':'blue'}
    SMD_player_category = ['Striker','Midfielder','Defender']
    
    for category in SMD_player_category:

        data = player_attributes[player_attributes['Player Category'] == category].head(number_top).mean()[comparison_attr_list]
        for attribute in comparison_attr_dict.keys():
            if attribute in comparison_attr_map.keys():
                rating = [data[attr] for attr in comparison_attr_map[attribute]]
                rating = sum(rating)/len(rating)
            else:
                rating = data[attribute]
            comparison_attr_dict[attribute] = rating 

        angles = np.linspace(0,2*np.pi,len(comparison_attr_dict.keys()),endpoint = False)
        stats = np.array(list(comparison_attr_dict.values()))
        stats = np.concatenate((stats,[stats[0]]))
        angles = np.concatenate((angles,[angles[0]]))

        ax.set_ylim(0,100)
        plot_label = 'Top ' + str(number_top) + ' ' + category + 's'
        plot_color = plot_colors_dict[category]
        labels = list(comparison_attr_dict.keys())

        ax.plot(angles, stats, plot_color, linewidth = 1.8, label = plot_label)
        ax.fill(angles, stats, plot_color, alpha = 0.05)
        ax.set_thetagrids(angles*180/np.pi, labels)

    plt.xticks(angles, labels, color='black', size=15)
    ax.tick_params(axis='x', pad=50)
    plt.yticks(color="grey", size=10)

    plot_title = 'Attributes Comparison of Strikers, Midfielder and Defenders'
    ax.set_title(plot_title, pad=60, size=20)
    ax.grid(True)
    plt.legend(bbox_to_anchor=(0,0), fontsize=10)
    fig.savefig('radar/%s' %plot_title, bbox_inches='tight')



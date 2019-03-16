
# coding: utf-8

# # Data Loader
# 
# Module for loading the .csv file that contains the player attributes into a pandas dataframe

# In[1]:


def load_data():
    '''
    Loads the  player_attributes.csv file  into a pandas dataframe and returns the dataframe
    
    Returns:
    player_attr_dataframe (pd.DataFrame) : The player attributes dataframe
    '''
    import pandas as pd
    
    player_attr_dataframe = pd.read_csv('player_attributes.csv', index_col=[0])
    return player_attr_dataframe
    


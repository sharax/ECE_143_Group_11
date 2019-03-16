#!/usr/bin/env python
# coding: utf-8

# In[40]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import subplots
from math import pi
from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.patches as patches
from scipy import interpolate 
import seaborn as sns
from data_loader_module import load_data


# In[41]:


# loading the player attributes dataframe
player_attributes = load_data()


# In[42]:


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
        


# In[43]:


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


# In[44]:


#add attributes to the dataframe for further ploting
def add_attributes(player_attributes):
    '''
    pl:DataFrame
    add attributes to player_attributes：(Attacking,Skill.....)
    '''
    pl=player_attributes
    assert isinstance(pl,pd.DataFrame)
    pl['Attacking']=pl.loc[:,['Crossing','Finishing','Heading Accuracy','Short Passing','Volleys']].mean(1)
    pl['Skill']=pl.loc[:,['Dribbling', 'Curve', 'FK Accuracy', 'Long Passing', 'Ball Control']].mean(1)
    pl['Movement']=pl.loc[:,['Acceleration', 'Sprint Speed', 'Agility', 'Reactions', 'Balance']].mean(1)
    pl['Power']=pl.loc[:,['Shot Power', 'Jumping', 'Stamina', 'Strength', 'Long Shots']].mean(1)
    pl['Defending']=pl.loc[:,['Marking', 'Standing Tackle', 'Sliding Tackle']].mean(1)
    pl['Goalkeeping']=pl.loc[:,['GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes']].mean(1)
    pl['Attacking+Skill']=pl.loc[:,['Attacking','Skill']].mean(1)
    pl['Mentality']=pl.loc[:,['Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure']].mean(1)
    pl['Midfielding']=pl.loc[:,['Short Passing', 'Dribbling', 'Ball Control', 'Long Passing', 'Crossing']].mean(1)
    ph=pl['Height'].tolist()
    ph=[i.strip('""').split('\'') for i in ph]
    ph=np.array([(int(i[0])*12+int(i[1]))*2.54 for i in ph])
    pl['Hight (cm)']=ph
    pw=pl['Weight'].values*0.4535924
    BMI=pw/ph**2*1e4
    pl['BMI']=BMI
    pv=pl['Value'].tolist()
    pvk=np.array([(i[-1]=='M')*1000+(i[-1]=='K') for i in pv])
    pvn=np.array([float(i[1:].strip('M').strip('K'))for i in pv])
    pl['Value(M)']=pvn*pvk/1000
    plw=pl['Wage'].tolist()
    plwk=[float(i[1:].strip('K')) for i in plw]
    pl['Wage(K)']=plwk
    pl['Overall Skill']=pl['Skill'].values.astype(np.int)
    return pl


# In[45]:


player_attributes=add_attributes(player_attributes)


# In[46]:


#group the players by their categorys
def group_player(player_attributes):
    player_grouped=player_attributes.groupby('Player Category')
    strike_player=player_grouped.get_group('Striker')
    goalkeep_player=player_grouped.get_group('GoalKeeper')
    midfield_player=player_grouped.get_group('Midfielder')
    defend_player=player_grouped.get_group('Defender')
    return strike_player,midfield_player,defend_player,goalkeep_player   


# In[47]:


strike_player,midfield_player,defend_player,goalkeep_player=group_player(player_attributes)


# In[48]:


def value_vs_rating(number_of_players):
    '''
    plot scatter plot of value vs rating
    number_of_players(int):number of counting players
    '''
    n=number_of_players
    assert isinstance(n,int)
    sns.set_style("darkgrid")
    pvh=player_attributes.sort_values('Overall Rating',ascending=False).head(n)
    pvhg=pvh.groupby('Overall Rating').mean()
    pvhg['Overall Rating']=pvhg.index
    plt.figure(figsize=(12,6))
    sns.relplot(x='Overall Rating',y='Value(M)',hue='Player Category',aspect=1.7,legend="full",data=pvh,sizes=(20,20))
    sns.regplot(x='Overall Rating',y='Value(M)',data=pvhg,color='k',label='Mean')
    plt.legend()
    plt.title('Value vs Ratings (Top'+str(n)+' Players)',fontsize='x-large') 
    plt.savefig('./graph/Value vs top'+str(n)+' Rating2.jpg')


# In[49]:


def draw_pie(player_attributes):
    '''
    plot pie graph of players' catagrory
    '''
    plp=player_attributes.groupby('Player Category')
    sizes=plp.count()['Hight (cm)']
    explode=[0.05,0.05,0.05,0.05]
    labels=['Defender','GoalKeeper','Midfielder','Striker']
    colors=['lightgreen','gold','lightskyblue','lightcoral']
    pie=plt.pie(sizes,explode=explode, shadow=True,labels=labels,colors=colors,autopct='%1.1f%%',startangle=50)
    plt.axis('equal')
    plt.title('Distribution of Category of players')
    plt.legend()
    plt.savefig("./graph/Distribution of Category of players.jpg")


# In[50]:


def single_attribute_distribution(attribute,unit=''):
    '''
    draw distribution of  single attribute
    attribute(str):the attribute
    unit(str)
    '''
    item=attribute
    assert isinstance(item,str)
    assert isinstance(unit,str)
    x=player_attributes[item]
    bins = np.linspace(x.min(),x.max(),10)
    x1 = np.linspace(x.min(), x.max(), 100)
    normal = norm.pdf(x1, x.mean(), x.std())*x.count()*(bins[1]-bins[0])
    kde = mlab.GaussianKDE(x)
    plt.hist([defend_player[item],midfield_player[item],strike_player[item],goalkeep_player[item]],             bins = bins,rwidth=0.8,edgecolor = 'k',stacked= True,label=['Defender','Midfielder','Striker','GoalKeeper'])
    plt.plot(x1,kde(x1)*x.count()*(bins[1]-bins[0]),linewidth = 3,label='Kernel density')
    plt.plot(x1,normal,label='Normal distribution',linewidth = 3)
    plt.grid(True)
    plt.xlabel(item+unit,fontsize='x-large')
    plt.ylabel('Number of players',fontsize='x-large')
    plt.legend(loc= 'best')
    if item== 'Hight (cm)':
        item='Height'
    plt.title('Distribution of '+item,fontsize='x-large')
    plt.savefig('./graph/'+'Distribution of '+item+'.jpg')


# In[56]:


def draw_wage_of_top(top_number,max_of_x):
    '''
    draw the wage distribution of top players
    top_number:number of players:int
    max_of_x: limit of axis x
    '''
    h=top_number
    m=max_of_x
    assert isinstance(h,int)
    assert isinstance(m,int)
    item='Wage(K)'
    dph=defend_player.head(h)
    sph=strike_player.head(h)
    mph=midfield_player.head(h)
    gph=goalkeep_player.head(h)
    dpi=dph[item]
    spi=sph[item]
    mpi=mph[item]
    gpi=gph[item]
    x=pd.concat([dph,sph,mph,gph])[item]
    bins = np.linspace(x.min(),x.max(),10)
    db=bins[1]-bins[0]
    x1 = np.linspace(x.min(), x.max(), 100)
    normals = norm.pdf(x1, spi.mean(), spi.std())*h*db
    normalm = norm.pdf(x1, mpi.mean(), mpi.std())*h*db
    normald = norm.pdf(x1, dpi.mean(), dpi.std())*h*db
    normalg = norm.pdf(x1, gpi.mean(), gpi.std())*h*db
    kde = mlab.GaussianKDE(x)
    plt.hist([sph[item],mph[item],dph[item],mph[item]], bins = bins,rwidth=0.8,                edgecolor = 'k',stacked= True,                label=['Striker','Midfielder','Defender','GoalKeeper']              ,alpha=0.8)
    plt.plot(x1,normals,label='Striker',linewidth = 3,color='b')
    plt.plot(x1,normalm,label='Midfielder',linewidth = 3,color='yellow')
    plt.plot(x1,normald,label='Defender',linewidth = 3,color='lime')
    plt.plot(x1,normalg,label='GoalKeeper',linewidth = 3,color='red')
    plt.grid(True)
    plt.xlabel(item,fontsize='x-large')
    plt.ylabel('Number of players',fontsize='x-large')
    plt.legend(loc= 'best')
    plt.title('Distribution of Wage'+' of top'+str(h)+' players',fontsize='x-large')
    plt.xlim([0,m])


# In[54]:


def list_of_wage_of_top(list_of_number):
    '''
    plot a list of wage of players
    list_of number(list):list of number of top players
    '''
    l=list_of_number
    le=len(l)
    assert le>1
    plt.figure(figsize=(6*le, 5))
    for i in range(le):
        plt.subplot(1,le,i+1)
        draw_wage_of_top(l[i],450)
    plt.savefig('./graph/Wage.jpg')


# In[30]:


def plot_height_weight_BMI(attribute,players):
    '''
    plot the an attribute vs height, weight and BMI
    players: specific players:DataFrame
    item:attribute:str
    '''
    item=attribute
    ply=players
    x=[ply.groupby('Hight (cm)').mean(),ply.groupby('Weight').mean(),ply.groupby('BMI').mean()]
    assert isinstance(item,str)
    assert isinstance(ply,pd.DataFrame)
    fig,axs=subplots(1,3,figsize=(20, 5))
    for i in range(3):
        x1=x[i].index.values
        y1=x[i][item].values
        xv=np.linspace(min(x1),max(x1),100)
        fl=interpolate.interp1d(x1, y1)
        xname=x[i].index.name
        dx=ply[xname]
        #normal = norm.pdf(xv, dx.mean(), dx.std())
        normal=mlab.GaussianKDE(dx)(xv)
        normal=normal+max(normal)/2
        ax=axs[i]
        d=xv[1]-xv[0]    
        for j in range(99):
            ax.add_patch(patches.Rectangle((xv[j],0),d,fl(xv[j]),color='b',linewidth=0,alpha=normal[j]/max(normal)))  
        ax.set_xlabel(xname+' (lb)'*(xname=='Weight'),fontsize='x-large')    
        ax.set_ylabel(item,fontsize='x-large')
        if xname== 'Hight (cm)':
            xname='Height'
        ax.set_title(item +' vs '+xname,fontsize='x-large')    
        ax.grid(True)
        ax.set_ylim([0,100])
        ax.set_xlim([min(xv),max(xv)])
    fig.savefig('./graph/'+item+'.jpg')


# In[61]:


def pWH(attributes,players,players_group_name,save_name):
    '''
    plot the attributes vs height, weight and BMI
    players: players of specific group:DataFrame
    attributes:list of attributes:list
    players_group_name: group name of players:str
    save_name: name of saved graph:str
    '''
    items=attributes
    ply=players
    pln=players_group_name
    itemn=save_name
    assert isinstance(items,list)
    assert isinstance(ply,pd.DataFrame)
    assert isinstance(pln,str)
    assert isinstance(itemn,str)
    x=[ply.groupby('Hight (cm)').mean(),ply.groupby('Weight').mean()]
    l=len(items)
    fig,axs=subplots(l,2,figsize=(12, 6*l))
    for j in range(l):
        item=items[j]
        for i in range(2):
            x1=x[i].index.values
            y1=x[i][item].values
            xv=np.linspace(min(x1),max(x1),500)
            fl=interpolate.interp1d(x1, y1)
            xname=x[i].index.name
            dx=ply[xname]
            normal=mlab.GaussianKDE(dx)(xv)
            normal=normal+max(normal)/2
            if l>1:
                ax=axs[j,i]
            else:
                ax=axs[i]
            d=xv[1]-xv[0]    
            for k in range(499):
                ax.add_patch(patches.Rectangle((xv[k],0),d,fl(xv[k]),color='b',linewidth=0,alpha=normal[k]/max(normal)))  
            ax.set_xlabel(xname+' (lb)'*(xname=='Weight'),fontsize='x-large')    
            ax.set_ylabel(item,fontsize='x-large')
            if xname== 'Hight (cm)':
                xname='Height'
            ax.set_title(item +' vs '+xname+' for '+pln,fontsize='x-large')    
            ax.grid(True)
            ax.set_ylim([0,100])
            ax.set_xlim([min(xv),max(xv)])
    fig.savefig('./graph/'+itemn+' of '+pln+'.jpg')


# In[ ]:

alldata = player_attributes
alldata['wage'] = alldata['Wage']
alldata['wage'] = pd.to_numeric(alldata['wage'].str[1:-1])

def wage(no_of_players):
    assert isinstance(no_of_players,list)
    for i in no_of_players:
        assert isinstance(i,int)
    fig = plt.figure()
    fig, axs = plt.subplots(1,3,figsize=(15,5),sharex = True,sharey = True)

    for i in range(0,3):
        number = no_of_players[i]
        am = alldata.mean()
        s = alldata[alldata['Player Category']=='Striker']['wage'].head(number).mean()
        m = alldata[alldata['Player Category']=='Midfielder']['wage'].head(number).mean()
        d = alldata[alldata['Player Category']=='Defender']['wage'].head(number).mean()
        g = alldata[alldata['Player Category']=='GoalKeeper']['wage'].head(number).mean()
        
        data = {'Striker':s,'Midfielder': m,'Defender':d,'GoalKeeper':g}
        names = list(data.keys())
        values = list(data.values())
        #plt.titile(str(number))
        axs[i].bar(names, values, color=['dodgerblue','darkorange','limegreen','r'],edgecolor = 'k',alpha = 0.8)
        axs[i].set_xlabel('Kinds of players',fontsize = 14)
        axs[i].set_ylabel('Wages (K)', fontsize = 14)
        axs[i].set_title('Average Wage of '+str(number)+' top players',fontsize = 15)
    fig.savefig('./graph/Distribution of Wages of players.PNG')
        





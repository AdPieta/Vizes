# -*- coding: utf-8 -*-
"""
# Getting single scatterplot with xG for and against

@author: @AdPieta
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
from PIL import Image

# Features
team_name = 'Real Madrid'
league_name = 'Spanish La Liga'

# Loading data from FBRef
xg_stats = pd.read_csv('RealMadrid.csv', sep = ',', encoding = 'cp1250')

# Getting relevant columns
xg_stats = xg_stats[['Venue', 'GF', 'GA', 'Opponent', 'xG', 'xGA']]

# Get xG for all games
xg_for_all = xg_stats['xG']
xg_against_all = xg_stats['xGA']

# Get xG for Won Games
xg_for_won = xg_stats[xg_stats['GF'] > xg_stats['GA']]['xG']
xg_against_won = xg_stats[xg_stats['GF'] > xg_stats['GA']]['xGA']

# Get utils
lim = math.ceil(max(xg_for_all.max(), xg_against_all.max()))
color = "#D32929"

# Get logo and its size
image = Image.open('RealLogo.png')

# Creating plot
fig = plt.figure(figsize = (8, 8))
ax = plt.subplot(111)

# Colors of the background
fig.set_facecolor('white')
ax.set_facecolor('white')
# Getting scatterplot of all xG results
ax.scatter(
    xg_for_all,
    xg_against_all,
    alpha = 0.3,
    facecolor = 'blue',
    edgecolor = 'black',
    zorder = 2,
    s = 50,
    lw = 1.5)

# Getting scatterplot of won Man Utd Mathces
ax.scatter(
    xg_for_won,
    xg_against_won,
    alpha = 1,
    s = 50,
    facecolor = color,
    edgecolor = 'black',
    zorder = 3,
    lw = 1.5,
    label = 'Won Games')


# Geting lineplot of f(x) = x
plt.plot(
    [0, lim],
    [0, lim],
    linestyle = '--',
    color = 'brown',
    linewidth = 1.5,
    zorder = 1)

# Add grid
ax.grid(linestyle = '--')

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Force ticks to be integers
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

# Change tick size
ax.tick_params(axis = "both", labelsize = 12)

# Get axes limits
ax.set_xlim(0, lim)
ax.set_ylim(0, lim)

# Get axes titles
ax.set_xlabel("xG for", size = 13, fontfamily = 'monospace')
ax.set_ylabel(f"xG against", size = 13, fontfamily = 'monospace')

# Get title and subtitle
fig.text(0.2, 0.95, f"{team_name} xG for and against", fontfamily = 'monospace', fontsize = 16, fontweight = 'bold')
fig.text(0.2, 0.92, f"{league_name} 2021/22 season", fontfamily = 'monospace', fontsize = 12)

# Get logo
ax2 = fig.add_axes([0.1, 0.9, 0.08, 0.08])
ax2.axis('off')
ax2.imshow(image)

# Get credits
fig.text(0.55, 0.03, '@AdPieta | Data @StatsBomb via @FbRef', alpha = 0.4,  family = 'Comic Sans', fontfamily = 'cursive')

# Create legend
fig.legend(loc = 'upper right',
           frameon = False,
           bbox_to_anchor = [0.9, 0.93])
plt.show()
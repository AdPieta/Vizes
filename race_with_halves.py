# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 22:31:03 2022

@author: adamm
"""

# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
from utils_.JsonOpener import WyscoutJsonOpener
from utils_.JsonProcesser import processWyScout
from highlight_text import ax_text, fig_text


# Open JSON File
open_json = WyscoutJsonOpener('Data/Events.json')

# Convert JSON File into event dataframe
event_df = processWyScout(open_json)

# Get team names
team_1 = event_df['teamName'].unique()[0]
team_2 = event_df['teamName'].unique()[1]

# Get colors
team_1_color = 'blue'
team_2_color = 'red'

# Get shots
shots_df = event_df[event_df['xg'] >= 0]

first_half_shots = shots_df[shots_df['matchPeriod'] == '1H']
second_half_shots = shots_df[shots_df['matchPeriod'] == '2H']

# Get goals
first_half_goals = event_df[(event_df['isGoal'] == True) & (event_df['matchPeriod'] == '1H')]
second_half_goals = event_df[(event_df['isGoal'] == True) & (event_df['matchPeriod'] == '2H')]


# Get goal scorers
team_1_scorers_1h = first_half_goals[(first_half_goals['teamName'] == team_1) & (first_half_goals['matchPeriod'] == '1H')]['player'].tolist()
team_1_scorers_2h = second_half_goals[(second_half_goals['teamName'] == team_1) & (second_half_goals['matchPeriod'] == '2H')]['player'].tolist()
team_2_scorers_1h = first_half_goals[(first_half_goals['teamName'] == team_2) & (first_half_goals['matchPeriod'] == '1H')]['player'].tolist()
team_2_scorers_2h = second_half_goals[(second_half_goals['teamName'] == team_2) & (second_half_goals['matchPeriod'] == '2H')]['player'].tolist()

# Get goals xG
team_1_goals_xg_1h = first_half_goals[(first_half_goals['teamName'] == team_1) & (first_half_goals['matchPeriod'] == '1H')]['xg'].tolist()
team_1_goals_xg_2h = second_half_goals[(second_half_goals['teamName'] == team_1) & (second_half_goals['matchPeriod'] == '2H')]['xg'].tolist()
team_2_goals_xg_1h = first_half_goals[(first_half_goals['teamName'] == team_2) & (first_half_goals['matchPeriod'] == '1H')]['xg'].tolist()
team_2_goals_xg_2h = second_half_goals[(second_half_goals['teamName'] == team_2) & (second_half_goals['matchPeriod'] == '2H')]['xg'].tolist()


# Get Expected goals and minutes for the first half
team_1_xg_1h = [0]
team_2_xg_1h = [0]
team_1_minutes_1h = [0]
team_2_minutes_1h = [0]
team_1_goals_mins_1h = []
team_2_goals_mins_1h = []

for i, row in first_half_shots.iterrows():
    if row['teamName'] == team_1:
        team_1_xg_1h.append(row['xg'])
        team_1_minutes_1h.append(row['minute'])
        if row['isGoal'] == True:
            team_1_goals_mins_1h.append(row['minute'])
    else:
        team_2_xg_1h.append(row['xg'])
        team_2_minutes_1h.append(row['minute'])
        if row['isGoal'] == True:
            team_2_goals_mins_1h.append(row['minute'])

team_1_xg_1h.append(0)
team_2_xg_1h.append(0)

team_1_minutes_1h.append(max(event_df[event_df['matchPeriod'] == '1H']['minute']))
team_2_minutes_1h.append(max(event_df[event_df['matchPeriod'] == '1H']['minute']))

# Get cumulative xG for teams
team_1_cumulative_1h = list(np.cumsum(team_1_xg_1h))
team_1_cumulative_1h = [round(team_1_cumulative_1h[i], 2) for i in range(len(team_1_cumulative_1h))]

team_2_cumulative_1h = list(np.cumsum(team_2_xg_1h))
team_2_cumulative_1h = [round(team_2_cumulative_1h[i], 2) for i in range(len(team_2_cumulative_1h))]



# Get Expected goals and minutes for the second half
team_1_xg_2h = [team_1_cumulative_1h[-1]]
team_2_xg_2h = [team_2_cumulative_1h[-1]]
team_1_minutes_2h = [45]
team_2_minutes_2h = [45]
team_1_goals_mins_2h = []
team_2_goals_mins_2h = []

for i, row in second_half_shots.iterrows():
    if row['teamName'] == team_1:
        team_1_xg_2h.append(row['xg'])
        team_1_minutes_2h.append(row['minute'])
        if row['isGoal'] == True:
            team_1_goals_mins_2h.append(row['minute'])
    else:
        team_2_xg_2h.append(row['xg'])
        team_2_minutes_2h.append(row['minute'])
        if row['isGoal'] == True:
            team_2_goals_mins_2h.append(row['minute'])

team_1_xg_2h.append(0)
team_2_xg_2h.append(0)

team_1_minutes_2h.append(max(event_df[event_df['matchPeriod'] == '2H']['minute']))
team_2_minutes_2h.append(max(event_df[event_df['matchPeriod'] == '2H']['minute']))

# Get cumulative xG for teams
team_1_cumulative_2h = list(np.cumsum(team_1_xg_2h))
team_1_cumulative_2h = [round(team_1_cumulative_2h[i], 2) for i in range(len(team_1_cumulative_2h))]

team_2_cumulative_2h = list(np.cumsum(team_2_xg_2h))
team_2_cumulative_2h = [round(team_2_cumulative_2h[i], 2) for i in range(len(team_2_cumulative_2h))]



# Get cumulative xG when goal was scored for team 1
# Supportive index list to find minutes when goals were scored
# First Team
team_1_shots_indeces_1h = first_half_shots[first_half_shots['teamName'] == team_1]['isGoal'].reset_index()
team_1_goals_indeces_1h = team_1_shots_indeces_1h[team_1_shots_indeces_1h['isGoal'] == True].index.tolist()
team_1_goals_indeces_1h = [x+1 for x in team_1_goals_indeces_1h]


team_1_cumulative_goals_1h = []
for i in team_1_goals_indeces_1h:
    team_1_cumulative_goals_1h.append(team_1_cumulative_1h[i])


team_1_shots_indeces_2h = second_half_shots[second_half_shots['teamName'] == team_1]['isGoal'].reset_index()
team_1_goals_indeces_2h = team_1_shots_indeces_2h[team_1_shots_indeces_2h['isGoal'] == True].index.tolist()
team_1_goals_indeces_2h = [x+1 for x in team_1_goals_indeces_2h]


team_1_cumulative_goals_2h = []
for i in team_1_goals_indeces_2h:
    team_1_cumulative_goals_2h.append(team_1_cumulative_2h[i])



# Second Team
team_2_shots_indeces_1h = first_half_shots[first_half_shots['teamName'] == team_2]['isGoal'].reset_index()
team_2_goals_indeces_1h = team_2_shots_indeces_1h[team_2_shots_indeces_1h['isGoal'] == True].index.tolist()
team_2_goals_indeces_1h = [x+1 for x in team_2_goals_indeces_1h]

team_2_cumulative_goals_1h = []
for i in team_2_goals_indeces_1h:
    team_2_cumulative_goals_1h.append(team_2_cumulative_1h[i])


team_2_shots_indeces_2h = second_half_shots[second_half_shots['teamName'] == team_2]['isGoal'].reset_index()
team_2_goals_indeces_2h = team_2_shots_indeces_2h[team_2_shots_indeces_2h['isGoal'] == True].index.tolist()
team_2_goals_indeces_2h = [x+1 for x in team_2_goals_indeces_2h]

team_2_cumulative_goals_2h = []
for i in team_2_goals_indeces_2h:
    team_2_cumulative_goals_2h.append(team_2_cumulative_2h[i])




# Start plotting
fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, sharey = True, figsize = (12, 8))

# Plot xg lines for 1st half
ax1.step(team_1_minutes_1h, team_1_cumulative_1h, where = 'post', color = team_1_color, label = team_1)
ax1.step(team_2_minutes_1h, team_2_cumulative_1h, where = 'post', color = team_2_color, label = team_2)

# Plot xg lines for 2nd half
ax2.step(team_1_minutes_2h, team_1_cumulative_2h, where = 'post', color = team_1_color, label = team_1)
ax2.step(team_2_minutes_2h, team_2_cumulative_2h, where = 'post', color = team_2_color, label = team_2)

# Change x axis into every 15 minutes and y axis lim
ax1.set_xlim(0, max(45, max(max(team_1_minutes_1h), max(team_2_minutes_1h))))
ax1.set_xticks([0,15,30,45])

ax2.set_xlim(45, max(45, max(max(team_1_minutes_2h), max(team_2_minutes_2h))))
ax2.set_xticks([45,60,75,90])

# Set labels
fig.supxlabel("minute", y = 0.01, size = 13, fontfamily = 'monospace')
fig.supylabel("cumulative xG", x = 0.01, size = 13, fontfamily = 'monospace')

# Remove top and right spines
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)

# Add grid
ax1.grid(linestyle = '--')
ax2.grid(linestyle = '--')


# Get goals on the plot
# Team 1
for i in range(len(team_1_goals_mins_1h)):
    cumulative_xg = team_1_cumulative_goals_1h[i]
    goal_xg = round(team_1_goals_xg_1h[i], 2)
    goal_minute = team_1_goals_mins_1h[i]
    goal_scorer = team_1_scorers_1h[i]
    ax1.text(goal_minute - 4, cumulative_xg + 0.08, f"{goal_minute}' {goal_scorer}", color = team_1_color)
    ax1.scatter(goal_minute, cumulative_xg, s = 25, color = team_1_color, marker = 'o')
    
for i in range(len(team_1_goals_mins_2h)):
    cumulative_xg = team_1_cumulative_goals_2h[i]
    goal_xg = round(team_1_goals_xg_2h[i], 2)
    goal_minute = team_1_goals_mins_2h[i]
    goal_scorer = team_1_scorers_2h[i]
    ax2.text(goal_minute - 4, cumulative_xg + 0.08, f"{goal_minute}' {goal_scorer}", color = team_1_color)
    ax2.scatter(goal_minute, cumulative_xg, s = 25, color = team_1_color, marker = 'o')    
    
# Team 2
for i in range(len(team_2_goals_mins_1h)):
    cumulative_xg = team_2_cumulative_goals_1h[i]
    goal_xg = round(team_2_goals_xg_1h[i], 2)
    goal_minute = team_2_goals_mins_1h[i]
    goal_scorer = team_2_scorers_1h[i]
    ax1.text(goal_minute - 4, cumulative_xg + 0.08, f"{goal_minute}' {goal_scorer}", color = team_2_color)
    ax1.scatter(goal_minute, cumulative_xg, s = 25, color = team_2_color, marker = 'o') 

for i in range(len(team_2_goals_mins_2h)):
    cumulative_xg = team_2_cumulative_goals_2h[i]
    goal_xg = round(team_2_goals_xg_2h[i], 2)
    goal_minute = team_2_goals_mins_2h[i]
    goal_scorer = team_2_scorers_2h[i]
    ax2.text(goal_minute - 4, cumulative_xg + 0.08, f"{goal_minute}' {goal_scorer}", color = team_2_color)
    ax2.scatter(goal_minute, cumulative_xg, s = 25, color = team_2_color, marker = 'o') 


    
# Get xG maximum values
ax2.text(team_1_minutes_2h[-1] + 1, team_1_cumulative_2h[-1], str(team_1_cumulative_2h[-1]), color = team_1_color, fontsize = 14, fontweight = 'bold')
ax2.text(team_2_minutes_2h[-1] + 1, team_2_cumulative_2h[-1], str(team_2_cumulative_2h[-1]), color = team_2_color, fontsize = 14, fontweight = 'bold')

# Get title and subtitle
fig.suptitle("xG race chart", fontfamily = 'monospace', fontsize = 20, fontweight = 'bold')
fig_text(0.37, 0.94, f"{team_1} - <{team_2}>", highlight_textprops = [{"color":team_2_color}], fontfamily = 'monospace', fontsize = 18, color = team_1_color)
#fig.text(0.15, 0.9, f"{team_1}", fontfamily = 'monospace', fontsize = 15, fontweight = 'bold', color = team_1_color)
#fig.text(0.77, 0.9, f"{team_2}", fontfamily = 'monospace', fontsize = 15, fontweight = 'bold', color = team_2_color)

# Get credits
fig.text(0.73, 0.02, '@AdPieta | Data @WyScout', alpha = 0.4, fontfamily = 'monospace')
fig.tight_layout()

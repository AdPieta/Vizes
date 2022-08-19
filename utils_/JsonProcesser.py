# -*- coding: utf-8 -*-
"""
Processing Wyscout Json File 

@author: @AdPieta
"""
import pandas as pd

def processWyScout(raw_json):

    """
    THIS FUNCTION DOES NOT INCLUDE EVERY COLUMN THAT WYSCOUT PROVIDES
    I USE ONLY COLUMNS THAT SEEMED TO BE NECESSARY TO ME IN MY EXPIERIENCE OF WORKING WITH THE DATA
    """    

    ### CLEANING DATAFRAME
    # Selecting first columns that contain game info
    first_columns = raw_json[['id', 'matchId', 'matchPeriod', 'minute', 'second', 'matchTimestamp', 'videoTimestamp']]
   
    # Type of event
    type_df = pd.DataFrame(list(raw_json['type']))
    
    # Starting location
    location_df = pd.DataFrame(raw_json['location']).reset_index()
    location_df = location_df.dropna().reset_index(drop = True)
    coordinates = pd.DataFrame(list(location_df['location']))
    location_df = pd.concat([location_df, coordinates], axis = 1).drop('location', axis = 1).set_index('index')
    
    # Team info
    team_df = pd.DataFrame(list(raw_json['team']))
    team_df = team_df.rename(columns = {'id':'teamId', 'name':'teamName'}).drop('formation', axis = 1)
    
    # Player info
    player_df = pd.DataFrame(list(raw_json['player']))
    player_df = player_df.rename(columns = {'id':'playerId', 'name':'player'}).drop('position', axis = 1)
    
    # Pass info
    pass_df = pd.DataFrame(raw_json['pass']).reset_index()
    pass_df = pass_df.dropna().reset_index(drop = True)
    pass_details = pd.DataFrame(list(pass_df['pass']))
    recipient_details = pd.DataFrame(list(pass_details['recipient'])).rename(columns = {'id':'recipientId', 'name':'recipientName'}).drop('position', axis = 1)
    end_location = pd.DataFrame(list(pass_details['endLocation'])).rename(columns = {'x':'endX', 'y':'endY'})
    pass_details = pd.concat([pass_details, recipient_details, end_location], axis = 1).drop(['recipient', 'endLocation'], axis = 1)
    pass_df = pd.concat([pass_df, pass_details], axis = 1).drop('pass', axis = 1).set_index('index')
    
    # Shot info
    shot_df = pd.DataFrame(raw_json['shot']).reset_index()
    shot_df = shot_df.dropna().reset_index(drop = True)
    shot_details = pd.DataFrame(list(shot_df['shot'])).drop(['goalkeeper', 'goalkeeperActionId'], axis = 1)
    shot_df = pd.concat([shot_df, shot_details], axis = 1).drop('shot', axis = 1).set_index('index')
    
    # Ground Duel Info
    ground_df = pd.DataFrame(raw_json['groundDuel']).reset_index()
    ground_df = ground_df.dropna().reset_index(drop = True)
    ground_details = pd.DataFrame(list(ground_df['groundDuel'])).drop(['opponent', 'relatedDuelId', 'side'], axis = 1)
    ground_df = pd.concat([ground_df, ground_details], axis = 1).drop('groundDuel', axis = 1).set_index('index')
    
    # Aerial Duel Info
    aerial_df = pd.DataFrame(raw_json['aerialDuel']).reset_index()
    aerial_df = aerial_df.dropna().reset_index(drop = True)
    aerial_details = pd.DataFrame(list(aerial_df['aerialDuel'])).drop(['opponent', 'height', 'relatedDuelId'], axis = 1)
    aerial_df = pd.concat([aerial_df, aerial_details], axis = 1).drop('aerialDuel', axis = 1).set_index('index')
    
    # Infraction Info
    #infraction_df = pd.DataFrame(raw_json['infraction']).reset_index()
    #infraction_df = infraction_df.dropna().reset_index(drop = True)
    #infraction_details = pd.DataFrame(list(infraction_df['infraction']))
    #opponent_details = pd.DataFrame(list(infraction_details['opponent'])).rename(columns = {'id':'opponentId', 'name':'opponent'}).drop('position', axis = 1)
    
    # Carry info
    carry_df = pd.DataFrame(raw_json['carry']).reset_index()
    carry_df = carry_df.dropna().reset_index(drop = True)
    carry_details = pd.DataFrame(list(carry_df['carry']))
    carry_end_location = pd.DataFrame(list(carry_details['endLocation'])).rename(columns = {'x':'endX', 'y':'endY'})
    carry_details = pd.concat([carry_details, carry_end_location], axis = 1).drop('endLocation', axis = 1)
    carry_df = pd.concat([carry_df, carry_details], axis = 1).drop('carry', axis = 1).set_index('index')
    
    # Possession info
    possession_df = pd.DataFrame(raw_json['possession']).reset_index()
    possession_df = possession_df.dropna().reset_index(drop = True)
    possession_details = pd.DataFrame(list(possession_df['possession']))
    possessing_team_details = pd.DataFrame(list(possession_details['team'])).rename(columns = {'team':'possessingTeam'}).drop(['id', 'formation'], axis = 1)
    possession_attack = possession_details.dropna()
    possession_attack_details = pd.DataFrame(list(possession_attack['attack']))[['withShot', 'xg']].rename(columns = {'xg':'possessionXg'})
    possession_attack_details.index = possession_attack.index
    possession_details = pd.concat([possession_details, possessing_team_details, possession_attack_details], axis = 1).rename(columns = {'id':'possessionId'}).drop(['team', 'startLocation', 'endLocation', 'attack'], axis = 1)
    possession_df = pd.concat([possession_df, possession_details], axis = 1).drop('possession', axis = 1).set_index('index')
    
    
    # Join everything
    event_df = pd.concat([first_columns, type_df, location_df, team_df, player_df, pass_df, shot_df, ground_df, aerial_df, possession_df], axis = 1)
    event_df = event_df.merge(carry_df, how = 'left', on = ['endX', 'endY'])
    return event_df
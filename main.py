#written by omur ozgunlu-2019
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras.utils import  to_categorical
from sklearn.preprocessing import normalize

import requests
import json
import re
import time

def retrieve_league_data(league, year):
    '''retrieves data from understat'''
    response = requests.get('https://understat.com/league/'+league+'/'+year)

    dates_data = re.search(
        "datesData\s+=\s+JSON.parse\('([^']+)", response.text)
    decoded_string_dates_data = bytes(
        dates_data.groups()[0], 'utf-8').decode('unicode_escape')
    dates_data_list = json.loads(decoded_string_dates_data)

    print("dates data creted"+league+" "+year)

    teams_data = re.search(
        "teamsData\s+=\s+JSON.parse\('([^']+)", response.text)
    decoded_string_teams_data = bytes(
        teams_data.groups()[0], 'utf-8').decode('unicode_escape')
    teams_data_list = json.loads(decoded_string_teams_data)

    print("teams data creted"+league+" "+year)

    players_data = re.search(
        "playersData\s+=\s+JSON.parse\('([^']+)", response.text)
    decoded_string_players_data = bytes(
        players_data.groups()[0], 'utf-8').decode('unicode_escape')
    players_data_list = json.loads(
        decoded_string_players_data)
    print("teams data creted"+league+" "+year)
    time.sleep(1)
    return dates_data_list, teams_data_list, players_data_list

def get_unique_team_names(team_data):
    ''' returns unique names of the season team names'''
    empty_list = []
    for anahtar in team_data.keys():
        for key in team_data[anahtar]:
            empty_list.append(team_data[anahtar][key]['title'])
    empty_set = set(empty_list)
    empty_list = list(empty_set)
    return empty_list

def get_unique_key_team_names(team_data, dict):
    '''expects a empty dict to fill up with id-team pairs'''
    for key in team_data.keys():
        for anahtar in team_data[key].keys():
            dict[anahtar] = team_data[key][anahtar]['title']


def convert_to_seq_team_names(team_dict,epl,bundesliga,laliga,ligue1,seriea):
    i=0
    for val in epl.values():
        team_dict[val]=i
        i+=1
    for val in bundesliga.values():
        team_dict[val]=i
        i+=1
    for val in laliga.values():
        team_dict[val]=i
        i+=1
    for val in ligue1.values():
        team_dict[val]=i
        i+=1
    for val in seriea.values():
        team_dict[val]=i
        i+=1

def class_get_match_dict(dates_data, teams_data, year_length, season_dict, team_dict, year_dict, lig, result_dictionary):
    '''returns league stats in array of dictionary'''
    # dates_data_len = len(dates_data)  # len=380
    # index = dates_data_len-1  # 379
    sezon_sayisi = len(year_length)  # sezon_sayisi=6
    #match_week = int(index/10)+1
    #divider = match_week-1
    #print("match week: " + str(match_week))

    for key in dates_data.keys():
        key_int = int(key)

        dates_data_key_len = len(dates_data[key])  # 380
        index = dates_data_key_len-1  # 379
        #match_week = int(index/10)+1
        #divider = match_week-1
        #print("match week: " + str(match_week))

        for i in range(0, len(dates_data[key])):
            match_week = int(i/10)+1
            divider = match_week-1
            print("match week: " + str(match_week))
            if dates_data[key][i]['isResult'] == True:

                home_team_title = dates_data[key][i]['h']['title']
                home_team_id = dates_data[key][i]['h']['id']
                away_team_title = dates_data[key][i]['a']['title']
                away_team_id = dates_data[key][i]['a']['id']
                home_team_score = dates_data[key][i]['goals']['h']
                away_team_score = dates_data[key][i]['goals']['a']

                home_team_goal_total = 0
                away_team_goal_total = 0
                home_team_goal_average = 0
                away_team_goal_average = 0

                home_team_against_total = 0
                home_team_against_avg = 0
                away_team_against_total = 0
                away_team_agains_avg = 0

                home_team_xg_total = 0
                home_team_xg_avg = 0
                away_team_xg_total = 0
                away_team_xg_avg = 0

                home_team_xga_total = 0
                home_team_xga_avg = 0
                away_team_xga_total = 0
                away_team_xga_avg = 0

                home_team_ppda_att_total = 0
                home_team_ppda_def_total = 0
                home_team_ppda_avg = 0
                home_team_oppda_att_total = 0
                home_team_oppda_def_total = 0
                home_team_oppda_avg = 0

                away_team_ppda_att_total = 0
                away_team_ppda_def_total = 0
                away_team_ppda_avg = 0
                away_team_oppda_att_total = 0
                away_team_oppda_def_total = 0
                away_team_oppda_avg = 0

                home_team_dc_total = 0
                home_team_dc_avg = 0
                away_team_dc_total = 0
                away_team_dc_avg = 0

                home_team_odc_total = 0
                home_team_odc_avg = 0
                away_team_odc_total = 0
                away_team_odc_avg = 0

                home_count_index = 0
                away_count_index = 0

                temp_home_count_index = 0
                temp_away_count_index = 0

                home_index = 0
                away_index = 0

                home_team_result = 0
                away_team_result = 0

                if int(home_team_score) > int(away_team_score):
                    home_team_result = 'w'
                    away_team_result = 'l'
                elif int(home_team_score) < int(away_team_score):
                    home_team_result = 'l'
                    away_team_result = 'w'
                if int(home_team_score) == int(away_team_score):
                    home_team_result = 'd'
                    away_team_result = 'd'

                for x in range(0, divider):

                    if teams_data[key][home_team_id]['history'][x]['h_a'] == 'h':
                        home_count_index += 1
                        home_team_goal_total += teams_data[key][home_team_id]['history'][x]['scored']
                        home_team_against_total += teams_data[key][home_team_id]['history'][x]['missed']

                        home_team_xg_total += teams_data[key][home_team_id]['history'][x]['xG']
                        home_team_xga_total += teams_data[key][home_team_id]['history'][x]['xGA']

                        home_team_ppda_att_total += teams_data[key][home_team_id]['history'][x]['ppda']['att']
                        home_team_ppda_def_total += teams_data[key][home_team_id]['history'][x]['ppda']['def']
                        home_team_oppda_att_total += teams_data[key][home_team_id]['history'][x]['ppda_allowed']['att']
                        home_team_oppda_def_total += teams_data[key][home_team_id]['history'][x]['ppda_allowed']['def']

                        home_team_dc_total += teams_data[key][home_team_id]['history'][x]['deep']
                        home_team_odc_total += teams_data[key][home_team_id]['history'][x]['deep_allowed']

                    if teams_data[key][away_team_id]['history'][x]['h_a'] == 'a':
                        away_count_index += 1
                        away_team_goal_total += teams_data[key][away_team_id]['history'][x]['scored']
                        away_team_against_total += teams_data[key][away_team_id]['history'][x]['missed']

                        away_team_xg_total += teams_data[key][away_team_id]['history'][x]['xG']
                        away_team_xga_total += teams_data[key][away_team_id]['history'][x]['xGA']

                        away_team_ppda_att_total += teams_data[key][away_team_id]['history'][x]['ppda']['att']
                        away_team_ppda_def_total += teams_data[key][away_team_id]['history'][x]['ppda']['def']
                        away_team_oppda_att_total += teams_data[key][away_team_id]['history'][x]['ppda_allowed']['att']
                        away_team_oppda_def_total += teams_data[key][away_team_id]['history'][x]['ppda_allowed']['def']

                        away_team_dc_total += teams_data[key][away_team_id]['history'][x]['deep']
                        away_team_odc_total += teams_data[key][away_team_id]['history'][x]['deep_allowed']
                if home_count_index == 0:
                    temp_home_count_index = 0

                    for y in range(divider, divider+4):
                        if teams_data[key][home_team_id]['history'][y]['h_a'] == 'h':
                            temp_home_count_index += 1
                            home_team_goal_total += teams_data[key][home_team_id]['history'][y]['scored']
                            home_team_against_total += teams_data[key][home_team_id]['history'][y]['missed']

                            home_team_xg_total += teams_data[key][home_team_id]['history'][y]['xG']
                            home_team_xga_total += teams_data[key][home_team_id]['history'][y]['xGA']

                            home_team_ppda_att_total += teams_data[key][home_team_id]['history'][y]['ppda']['att']
                            home_team_ppda_def_total += teams_data[key][home_team_id]['history'][y]['ppda']['def']
                            home_team_oppda_att_total += teams_data[key][home_team_id]['history'][y]['ppda_allowed']['att']
                            home_team_oppda_def_total += teams_data[key][home_team_id]['history'][y]['ppda_allowed']['def']

                            home_team_dc_total += teams_data[key][home_team_id]['history'][y]['deep']
                            home_team_odc_total += teams_data[key][home_team_id]['history'][y]['deep_allowed']

                if away_count_index == 0:
                    temp_away_count_index = 0

                    for z in range(divider, divider+4):
                        if teams_data[key][away_team_id]['history'][z]['h_a'] == 'a':
                            temp_away_count_index += 1
                            away_team_goal_total += teams_data[key][away_team_id]['history'][z]['scored']
                            away_team_against_total += teams_data[key][away_team_id]['history'][z]['missed']

                            away_team_xg_total += teams_data[key][away_team_id]['history'][z]['xG']
                            away_team_xga_total += teams_data[key][away_team_id]['history'][z]['xGA']

                            away_team_ppda_att_total += teams_data[key][away_team_id]['history'][z]['ppda']['att']
                            away_team_ppda_def_total += teams_data[key][away_team_id]['history'][z]['ppda']['def']
                            away_team_oppda_att_total += teams_data[key][away_team_id]['history'][z]['ppda_allowed']['att']
                            away_team_oppda_def_total += teams_data[key][away_team_id]['history'][z]['ppda_allowed']['def']

                            away_team_dc_total += teams_data[key][away_team_id]['history'][z]['deep']
                            away_team_odc_total += teams_data[key][away_team_id]['history'][z]['deep_allowed']
                if home_count_index > 0:
                    home_index = home_count_index
                elif home_count_index == 0:
                    home_index = temp_home_count_index
                if away_count_index > 0:
                    away_index = away_count_index
                elif away_count_index == 0:
                    away_index = temp_away_count_index
                print("Home count: "+home_team_title)
                print("away count: "+away_team_title)
                print("key :"+key)

                home_team_goal_average = home_team_goal_total/home_index
                away_team_goal_average = away_team_goal_total/away_index

                home_team_against_avg = home_team_against_total/home_index
                away_team_agains_avg = away_team_against_total/away_index

                home_team_xg_avg = home_team_xg_total/home_index
                home_team_xga_avg = home_team_xga_total/home_index

                away_team_xg_avg = away_team_xg_total/away_index
                away_team_xga_avg = away_team_xga_total/away_index

                home_team_ppda_avg = home_team_ppda_att_total/home_team_ppda_def_total
                home_team_oppda_avg = home_team_oppda_att_total/home_team_oppda_def_total

                away_team_ppda_avg = away_team_ppda_att_total/away_team_ppda_def_total
                away_team_oppda_avg = away_team_oppda_att_total/away_team_oppda_def_total

                home_team_dc_avg = home_team_dc_total/home_index
                home_team_odc_avg = home_team_odc_total/home_index

                away_team_dc_avg = away_team_dc_total/away_index
                away_team_odc_avg = away_team_odc_total/away_index

                season_dict.append({'home_team': team_dict[home_team_title], 'away_team': team_dict[away_team_title], 'home_score': float(result_dictionary[home_team_result]), 'away_score': float(result_dictionary[away_team_result]), 'home_goal_avg': home_team_goal_average, 'home_goal_against': home_team_against_avg, 'away_goal_avg': away_team_goal_average, 'away_goal_against': away_team_agains_avg, 'home_xG': home_team_xg_avg, 'home_xGA': home_team_xga_avg,
                                    'home_PPDA': home_team_ppda_avg, 'home_OPPDA': home_team_oppda_avg, 'home_DC': home_team_dc_avg, 'home_ODC': home_team_odc_avg, 'away_xG': away_team_xg_avg, 'away_xGA': away_team_xga_avg, 'away_PPDA': away_team_ppda_avg, 'away_OPPDA': away_team_oppda_avg, 'away_DC': away_team_dc_avg, 'away_ODC': away_team_odc_avg, 'season': year_dict[key], 'league': league_dict[lig]})


epl_2019_dates_data, epl_2019_teams_data, epl_2019_players_data = retrieve_league_data(
    'EPL', '2019')
epl_2018_dates_data, epl_2018_teams_data, epl_2018_players_data = retrieve_league_data(
    'EPL', '2018')
epl_2017_dates_data, epl_2017_teams_data, epl_2017_players_data = retrieve_league_data(
    'EPL', '2017')
epl_2016_dates_data, epl_2016_teams_data, epl_2016_players_data = retrieve_league_data(
    'EPL', '2016')
epl_2015_dates_data, epl_2015_teams_data, epl_2015_players_data = retrieve_league_data(
    'EPL', '2015')
epl_2014_dates_data, epl_2014_teams_data, epl_2014_players_data = retrieve_league_data(
    'EPL', '2014')

# LA LIGA
laliga_2019_dates_data, laliga_2019_teams_data, laliga_2019_players_data = retrieve_league_data(
    'La_liga', '2019')
laliga_2018_dates_data, laliga_2018_teams_data, laliga_2018_players_data = retrieve_league_data(
    'La_liga', '2018')
laliga_2017_dates_data, laliga_2017_teams_data, laliga_2017_players_data = retrieve_league_data(
    'La_liga', '2017')
laliga_2016_dates_data, laliga_2016_teams_data, laliga_2016_players_data = retrieve_league_data(
    'La_liga', '2016')
laliga_2015_dates_data, laliga_2015_teams_data, laliga_2015_players_data = retrieve_league_data(
    'La_liga', '2015')
laliga_2014_dates_data, laliga_2014_teams_data, laliga_2014_players_data = retrieve_league_data(
    'La_liga', '2014')

# BUNDESLIGA
bundes_2019_dates_data, bundes_2019_teams_data, bundes_2019_players_data = retrieve_league_data(
    'Bundesliga', '2019')
bundes_2018_dates_data, bundes_2018_teams_data, bundes_2018_players_data = retrieve_league_data(
    'Bundesliga', '2018')
bundes_2017_dates_data, bundes_2017_teams_data, bundes_2017_players_data = retrieve_league_data(
    'Bundesliga', '2017')
bundes_2016_dates_data, bundes_2016_teams_data, bundes_2016_players_data = retrieve_league_data(
    'Bundesliga', '2016')
bundes_2015_dates_data, bundes_2015_teams_data, bundes_2015_players_data = retrieve_league_data(
    'Bundesliga', '2015')
bundes_2014_dates_data, bundes_2014_teams_data, bundes_2014_players_data = retrieve_league_data(
    'Bundesliga', '2014')

# SERIA
seria_2019_dates_data, seria_2019_teams_data, seria_2019_players_data = retrieve_league_data(
    'Serie_A', '2019')
seria_2018_dates_data, seria_2018_teams_data, seria_2018_players_data = retrieve_league_data(
    'Serie_A', '2018')
seria_2017_dates_data, seria_2017_teams_data, seria_2017_players_data = retrieve_league_data(
    'Serie_A', '2017')
seria_2016_dates_data, seria_2016_teams_data, seria_2016_players_data = retrieve_league_data(
    'Serie_A', '2016')
seria_2015_dates_data, seria_2015_teams_data, seria_2015_players_data = retrieve_league_data(
    'Serie_A', '2015')
seria_2014_dates_data, seria_2014_teams_data, seria_2014_players_data = retrieve_league_data(
    'Serie_A', '2014')

# LIGUE1
ligue1_2019_dates_data, ligue1_2019_teams_data, ligue1_2019_players_data = retrieve_league_data(
    'Ligue_1', '2019')
ligue1_2018_dates_data, ligue1_2018_teams_data, ligue1_2018_players_data = retrieve_league_data(
    'Ligue_1', '2018')
ligue1_2017_dates_data, ligue1_2017_teams_data, ligue1_2017_players_data = retrieve_league_data(
    'Ligue_1', '2017')
ligue1_2016_dates_data, ligue1_2016_teams_data, ligue1_2016_players_data = retrieve_league_data(
    'Ligue_1', '2016')
ligue1_2015_dates_data, ligue1_2015_teams_data, ligue1_2015_players_data = retrieve_league_data(
    'Ligue_1', '2015')
ligue1_2014_dates_data, ligue1_2014_teams_data, ligue1_2014_players_data = retrieve_league_data(
    'Ligue_1', '2014')

EPL_TEAMS_DATA = {'2019': epl_2019_teams_data, '2018': epl_2018_teams_data, '2017': epl_2017_teams_data,
                  '2016': epl_2016_teams_data, '2015': epl_2015_teams_data, '2014': epl_2014_teams_data}
LALIGA_TEAMS_DATA = {'2019': laliga_2019_teams_data, '2018': laliga_2018_teams_data, '2017': laliga_2017_teams_data,
                     '2016': laliga_2016_teams_data, '2015': laliga_2015_teams_data, '2014': laliga_2014_teams_data}
BUNDES_TEAMS_DATA = {'2019': bundes_2019_teams_data, '2018': bundes_2018_teams_data, '2017': bundes_2017_teams_data,
                     '2016': bundes_2016_teams_data, '2015': bundes_2015_teams_data, '2014': bundes_2014_teams_data}
SERIEA_TEAMS_DATA = {'2019': seria_2019_teams_data, '2018': seria_2018_teams_data, '2017': seria_2017_teams_data,
                     '2016': seria_2016_teams_data, '2015': seria_2015_teams_data, '2014': seria_2014_teams_data}
LIGUE1_TEAMS_DATA = {'2019': ligue1_2019_teams_data, '2018': ligue1_2018_teams_data, '2017': ligue1_2017_teams_data,
                     '2016': ligue1_2016_teams_data, '2015': ligue1_2015_teams_data, '2014': ligue1_2014_teams_data}

EPL_PLAYERS_DATA = {'2019': epl_2019_players_data, '2018': epl_2018_players_data, '2017': epl_2017_players_data,
                    '2016': epl_2016_players_data, '2015': epl_2015_players_data, '2014': epl_2014_players_data}
LALIGA_PLAYERS_DATA = {'2019': laliga_2019_players_data, '2018': laliga_2018_players_data, '2017': laliga_2017_players_data,
                       '2016': laliga_2016_players_data, '2015': laliga_2015_players_data, '2014': laliga_2014_players_data}
BUNDES_PLAYERS_DATA = {'2019': bundes_2019_players_data, '2018': bundes_2018_players_data, '2017': bundes_2017_players_data,
                       '2016': bundes_2016_players_data, '2015': bundes_2015_players_data, '2014': bundes_2014_players_data}
SERIEA_PLAYERS_DATA = {'2019': seria_2019_players_data, '2018': seria_2018_players_data, '2017': seria_2017_players_data,
                       '2016': seria_2016_players_data, '2015': seria_2015_players_data, '2014': seria_2014_players_data}
LIGUE1_PLAYERS_DATA = {'2019': ligue1_2019_players_data, '2018': ligue1_2018_players_data, '2017': ligue1_2017_players_data,
                       '2016': ligue1_2016_players_data, '2015': ligue1_2015_players_data, '2014': ligue1_2014_players_data}

EPL_DATES_DATA = {'2019': epl_2019_dates_data, '2018': epl_2018_dates_data, '2017': epl_2017_dates_data,
                  '2016': epl_2016_dates_data, '2015': epl_2015_dates_data, '2014': epl_2014_dates_data}
LALIGA_DATES_DATA = {'2019': laliga_2019_dates_data, '2018': laliga_2018_dates_data, '2017': laliga_2017_dates_data,
                     '2016': laliga_2016_dates_data, '2015': laliga_2015_dates_data, '2014': laliga_2014_dates_data}
BUNDES_DATES_DATA = {'2019': bundes_2019_dates_data, '2018': bundes_2018_dates_data, '2017': bundes_2017_dates_data,
                     '2016': bundes_2016_dates_data, '2015': bundes_2015_dates_data, '2014': bundes_2014_dates_data}
SERIEA_DATES_DATA = {'2019': seria_2019_dates_data, '2018': seria_2018_dates_data, '2017': seria_2017_dates_data,
                     '2016': seria_2016_dates_data, '2015': seria_2015_dates_data, '2014': seria_2014_dates_data}
LIGUE1_DATES_DATA = {'2019': ligue1_2019_dates_data, '2018': ligue1_2018_dates_data, '2017': ligue1_2017_dates_data,
                     '2016': ligue1_2016_dates_data, '2015': ligue1_2015_dates_data, '2014': ligue1_2014_dates_data}


LEAGUES = ['EPL', 'La_liga', 'Bundesliga', 'Serie_A', 'Ligue_1']
YEARS = ['2019', '2018', '2017', '2016', '2015', '2014']

epl_dict_team = {}
bundesliga_dict_team={}
laliga_dict_team={}
seriea_dict_team={}
ligue1_dict_team={}

get_unique_key_team_names(EPL_TEAMS_DATA, epl_dict_team)
get_unique_key_team_names(BUNDES_TEAMS_DATA, bundesliga_dict_team)
get_unique_key_team_names(LALIGA_TEAMS_DATA, laliga_dict_team)
get_unique_key_team_names(LIGUE1_TEAMS_DATA, ligue1_dict_team)
get_unique_key_team_names(SERIEA_TEAMS_DATA, seriea_dict_team)

team_dict_2={}
convert_to_seq_team_names(team_dict_2,epl_dict_team,bundesliga_dict_team,laliga_dict_team,ligue1_dict_team,seriea_dict_team)
result_dict = {'w': 1, 'd': 0.5, 'l': 0}

years_dict={'2019':5,'2018':4,'2017':3,'2016':2,'2015':1,'2014':0}
YEARS = ['2019', '2018', '2017', '2016', '2015', '2014']
league_dict={'EPL':0,'BUNDESLIGA':1,'LALIGA':2,'SERIEA':3,'LIGUE1':4}
sezon_dict=[]

class_get_match_dict(EPL_DATES_DATA,EPL_TEAMS_DATA,YEARS,sezon_dict,team_dict_2,years_dict,'EPL',result_dict)
class_get_match_dict(BUNDES_DATES_DATA,BUNDES_TEAMS_DATA,YEARS,sezon_dict,team_dict_2,years_dict,'BUNDESLIGA',result_dict)
class_get_match_dict(LALIGA_DATES_DATA,LALIGA_TEAMS_DATA,YEARS,sezon_dict,team_dict_2,years_dict,'LALIGA',result_dict)
class_get_match_dict(SERIEA_DATES_DATA,SERIEA_TEAMS_DATA,YEARS,sezon_dict,team_dict_2,years_dict,'SERIEA',result_dict)
class_get_match_dict(LIGUE1_DATES_DATA,LIGUE1_TEAMS_DATA,YEARS,sezon_dict,team_dict_2,years_dict,'LIGUE1',result_dict)

data_frame=pd.DataFrame(sezon_dict)
maclar=data_frame.drop(["home_score","away_score"],axis=1)
home_teams=maclar["home_team"].copy()
away_teams=maclar["away_team"].copy()
seasons=maclar["season"].copy()
leagues=maclar["league"].copy()

sonuclar=data_frame[["home_score","away_score"]].copy()

sonuclar_np=sonuclar.to_numpy()
maclar_dropped=maclar.drop(["home_team","away_team","season","league"],axis=1)
maclar_np=maclar.to_numpy()
maclar_np_norm=normalize(maclar_np,axis=0,norm='max')

maclar=maclar_np_norm[30:]
maclar.shape
sonuclar_maclar=sonuclar[30:]
tahminler=maclar_np_norm[:30]
tahminler.shape

modelx5 = keras.models.Sequential([
    keras.layers.Input(shape=[20]),
    keras.layers.Dense(400, activation="relu"),
    keras.layers.Dense(200, activation="relu"),
    keras.layers.Dense(100,activation="relu"),
    keras.layers.Dense(50, activation="softmax"),
    keras.layers.Dense(2)
])
modelx5.compile(loss="mse", optimizer=keras.optimizers.RMSprop(0.001),metrics=["accuracy"])

modelx5.fit(maclar,sonuclar_maclar,batch_size=80,epochs=300)

np.set_printoptions(suppress=True)

modelx5.predict(tahminler)


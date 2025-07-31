import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import joblib
import os

# ------------------------------------------------------------------------------------------------------------------------------------------
# Load datasets
filepath = os.path.abspath('data/processed/deliveries_all.joblib')
deliveries_all = joblib.load(filepath)

filepath = os.path.abspath('data/processed/matches.joblib')
matches = joblib.load(filepath)

filepath = os.path.abspath('data/processed/deliveries.joblib')
deliveries = joblib.load(filepath)

# ------------------------------------------------------------------------------------------------------------------------------------------

matches = (
    matches
    .assign(
        winner = lambda df_: df_['winner'].fillna('No Result')
    )
    .replace({'Elimination Final': 'Eliminator'})
)

# ------------------------------------------------------------------------------------------------------------------------------------------

df_all1 = (
    matches
    .merge(deliveries, left_on = 'id', right_on = 'match_id', how = 'inner') 
)

# ------------------------------------------------------------------------------------------------------------------------------------------
## Batsman Team(s) for Seasons
def player_teams(player_name):
    if player_name not in non_striker_batter['batter'].values:
        df = (
            df_all1
            .groupby(by = ['batter', 'batting_team', 'season'], as_index = False)
            .agg(count = ('batting_team', 'nunique'))
            .query(f"batter == '{player_name}'")
            .groupby(by = 'batting_team', as_index = False)
            .agg(seasons = ('season', lambda x: ", ".join(x.unique())), count = ('season', lambda x: len((x.unique()))))
            .rename(columns = {'batting_team': 'Team', 'seasons': 'Season', 'count': 'Count'})
        )
    else:
        df = (
            df_all1[df_all1['non_striker'].isin(non_striker_batter['batter'])][['non_striker', 'season', 'batting_team']]
            .groupby(by = ['batting_team'], as_index = False)
            .agg(seasons = ('season', lambda x: ", ".join(x.unique())), count = ('season', lambda x: len((x.unique()))))
            .rename(columns = {'batting_team': 'Team', 'seasons': 'Season', 'count': 'Count'})
        )
    df.index = range(1, len(df)+1)
    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
## Batsman Overall Stats
runs_df = (
    deliveries
    .groupby(by = ['batter'], as_index = False)
    .agg(
        Runs = ('batsman_runs', 'sum'),
        Balls = ('batsman_runs', 'count'),
        Sixes = ('batsman_runs', lambda x: (x == 6).sum()),
        Fours = ('batsman_runs', lambda x: (x == 4).sum()),
        Threes = ('batsman_runs', lambda x: (x == 3).sum()),
        Twos = ('batsman_runs', lambda x: (x == 2).sum()),
        Ones = ('batsman_runs', lambda x: (x == 1).sum()),
        Dots = ('batsman_runs', lambda x: (x == 0).sum())
    )
)

dismissals_df = (
    deliveries
    .groupby(by = ['player_dismissed'], as_index = False)
    .agg(dismissals = ('is_wicket', 'sum'))
)

innings_df = (
    deliveries
    .groupby(by = ['batter'], as_index = False)
    .agg(innings = ('match_id', 'nunique'))
)

batsman_striker_list = set(list(deliveries['batter'].unique()))
batsman_non_striker_list = set(list(deliveries['non_striker'].unique()))
non_striker_batter = list(batsman_non_striker_list - batsman_striker_list)
non_striker_batter = pd.DataFrame(non_striker_batter, columns = ['batter'])

batsman_overall_df = (
    runs_df
    .merge(non_striker_batter, on  = ['batter'], how = 'outer')
    .merge(dismissals_df, left_on = ['batter'], right_on = ['player_dismissed'], how = 'outer')
    .merge(innings_df, on = ['batter'], how = 'outer')
    .sort_values(by = 'Runs', ascending = False, ignore_index = True)
    .assign(
        Runs = lambda df_: df_['Runs'].fillna(0).astype('int'),
        Balls = lambda df_: df_['Balls'].fillna(0).astype('int'),
        Sixes = lambda df_: df_['Sixes'].fillna(0).astype('int'),
        Fours = lambda df_: df_['Fours'].fillna(0).astype('int'),
        Threes = lambda df_: df_['Threes'].fillna(0).astype('int'),
        Twos = lambda df_: df_['Twos'].fillna(0).astype('int'),
        Ones = lambda df_: df_['Ones'].fillna(0).astype('int'),
        dismissals = lambda df_: df_['dismissals'].fillna(0).astype('int'),
        innings = lambda df_: df_['innings'].fillna(1).astype('int'),
        not_outs = lambda df_: df_['innings'] - df_['dismissals'],
        strike_rate = lambda df_: round((df_['Runs']/df_['Balls'])*100, 2),
        batting_average = lambda df_: round(df_['Runs']/df_['dismissals'],2),
        boundary_proportion_of_total = lambda df_: round(((df_['Sixes']*6 + df_['Fours']*4)/df_['Runs'])*100, 2),
        dot_ball_percent = lambda df_: round((df_['Dots']/df_['Balls'])*100,2),
        Dots = lambda df_: df_['Dots'].fillna(0).astype('int')
    )
    .rename(columns = {'batter': 'Batsman', 'dismissals': 'Dismissals', 'innings': 'Innings',
                       'not_outs': 'Not Outs', 'strike_rate': 'Strike Rate', 'batting_average': 'Batting Average', 
                       'boundary_proportion_of_total': 'Boundary Dominance', 'dot_ball_percent': 'Dot Ball Reliance'})
    .drop(columns = 'player_dismissed')
    [['Batsman', 'Innings', 'Runs', 'Balls', 'Sixes', 'Fours', 'Threes', 'Twos', 'Ones', 'Dots',	
      'Dismissals', 'Not Outs', 'Strike Rate',	'Batting Average', 'Boundary Dominance', 'Dot Ball Reliance']]
)

# ------------------------------------------------------------------------------------------------------------------------------------------
## Match-wise Runs
def match_runs(player_name):
    return (
        df_all1.query(f"batter == '{player_name}'")
        .groupby(by = ['batter', 'id', 'season', 'inning', 'batting_team', 'bowling_team'], as_index = False)
        .agg(
            Runs = ('batsman_runs', 'sum'),
            Balls = ('batsman_runs', 'count'),
            Sixes = ('batsman_runs', lambda x: (x == 6).sum()),
            Fours = ('batsman_runs', lambda x: (x == 4).sum()),
            Threes = ('batsman_runs', lambda x: (x == 3).sum()),
            Twos = ('batsman_runs', lambda x: (x == 2).sum()),
            Ones = ('batsman_runs', lambda x: (x == 1).sum()),
            Dots = ('batsman_runs', lambda x: (x == 0).sum())
        )
        .assign(
            Century = lambda df_: (df_['Runs'] >= 100).astype('int'),
            Half_Century = lambda df_: ((df_['Runs'] >= 50) & (df_['Runs'] < 100)).astype('int')
        )
        .rename(columns = {'batter': 'Batsman', 'id': 'Match ID', 'inning': 'Inning',
                           'batting_team': 'Team', 'bowling_team': 'Bowling Team', 'season': 'Season'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Player Inning Group
def player_inning_group(player_name):
    return (
        match_runs(player_name)
        .groupby(by = ['Batsman', 'Inning'], as_index = False)
        .agg(
            Matches = ('Match ID', 'count'), Runs = ('Runs', 'sum'),
            Balls = ('Balls', 'sum'), Centuries = ('Century', 'sum'),
            Half_Century = ('Half_Century', 'sum'), Sixes = ('Sixes', 'sum'),
            Fours = ('Fours', 'sum'),Threes = ('Threes', 'sum'),
            Twos = ('Twos', 'sum'), Ones = ('Ones', 'sum'), Dots = ('Dots', 'sum'),  
        )
        .assign(
            Strike_Rate = lambda df_: round((df_['Runs']/df_['Balls'])*100,2),
            Boundary_Percent = lambda df_: round(((df_['Sixes']*6 + df_['Fours']*4)/df_['Runs'])*100,2),
            Dot_Percent = lambda df_: round((df_['Dots']/df_['Balls'])*100,2)
        )
        .rename(columns = {'Half_Century': 'Half Centuries', 'Strike_Rate': 'Strike Rate',
                           'Boundary_Percent': 'Boundary Dominance', 'Dot_Percent': 'Dot Ball Reliance'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Season-wise Stats
runs_df1 = (
    df_all1
    .groupby(by = ['season','batter'], as_index = False)
    .agg(
        Runs = ('batsman_runs', 'sum'),
        Balls = ('batsman_runs', 'count'),
        Sixes = ('batsman_runs', lambda x: (x == 6).sum()),
        Fours = ('batsman_runs', lambda x: (x == 4).sum()),
        Threes = ('batsman_runs', lambda x: (x == 3).sum()),
        Twos = ('batsman_runs', lambda x: (x == 2).sum()),
        Ones = ('batsman_runs', lambda x: (x == 1).sum()),
        Dots = ('batsman_runs', lambda x: (x == 0).sum())
    )
)

dismissals_df1 = (
    df_all1
    .groupby(by = ['season', 'player_dismissed'], as_index = False)
    .agg(dismissals = ('is_wicket', 'sum'))
)

innings_df1 = (
    df_all1
    .groupby(by = ['season', 'batter'], as_index = False)
    .agg(innings = ('match_id', 'nunique'))
)

batsman_striker_list = set(list(df_all1['batter'].unique()))
batsman_non_striker_list = set(list(df_all1['non_striker'].unique()))
non_striker_batter = list(batsman_non_striker_list - batsman_striker_list)
non_striker_batter = pd.DataFrame(non_striker_batter, columns = ['batter'])
non_striker_batter_df = df_all1[df_all1['non_striker'].isin(non_striker_batter['batter'])][['non_striker', 'season']]
non_striker_batter_df = non_striker_batter_df.rename(columns = {'non_striker': 'batter'})

batsman_overall_df1 = (
    runs_df1
    .merge(non_striker_batter_df, on  = ['season','batter'], how = 'outer')
    .merge(dismissals_df1, left_on = ['season','batter'], right_on = ['season','player_dismissed'], how = 'outer')
    .merge(innings_df1, on = ['season','batter'], how = 'outer')
    .sort_values(by = 'season', ignore_index = True)
    .assign(
        Runs = lambda df_: df_['Runs'].fillna(0).astype('int'),
        Balls = lambda df_: df_['Balls'].fillna(0).astype('int'),
        Sixes = lambda df_: df_['Sixes'].fillna(0).astype('int'),
        Fours = lambda df_: df_['Fours'].fillna(0).astype('int'),
        Threes = lambda df_: df_['Threes'].fillna(0).astype('int'),
        Twos = lambda df_: df_['Twos'].fillna(0).astype('int'),
        Ones = lambda df_: df_['Ones'].fillna(0).astype('int'),
        dismissals = lambda df_: df_['dismissals'].fillna(0).astype('int'),
        innings = lambda df_: df_['innings'].fillna(1).astype('int'),
        not_outs = lambda df_: df_['innings'] - df_['dismissals'],
        strike_rate = lambda df_: round((df_['Runs']/df_['Balls'])*100, 2),
        batting_average = lambda df_: round(df_['Runs']/df_['dismissals'],2),
        boundary_proportion_of_total = lambda df_: round(((df_['Sixes']*6 + df_['Fours']*4)/df_['Runs'])*100, 2),
        dot_ball_percent = lambda df_: round((df_['Dots']/df_['Balls'])*100,2),
        Dots = lambda df_: df_['Dots'].fillna(0).astype('int')
    )
    .rename(columns = {'season': 'Season', 'batter': 'Batsman', 'dismissals': 'Dismissals', 'innings': 'Innings',
                       'not_outs': 'Not Outs', 'strike_rate': 'Strike Rate', 'batting_average': 'Batting Average', 
                       'boundary_proportion_of_total': 'Boundary Dominance', 'dot_ball_percent': 'Dot Ball Reliance'})
    .drop(columns = 'player_dismissed')
    [['Season', 'Batsman', 'Innings', 'Runs', 'Balls', 'Sixes', 'Fours', 'Threes', 'Twos', 'Ones', 'Dots',	
      'Dismissals', 'Not Outs', 'Strike Rate',	'Batting Average', 'Boundary Dominance', 'Dot Ball Reliance']]
)

# ------------------------------------------------------------------------------------------------------------------------------------------
## Dismisaal Kind
def player_dismissal_type(player_name, season = 'All'):
    if season == 'All':
        df_filtered = (
            df_all1
            .query(f"player_dismissed == '{player_name}'")
            .groupby(by = ['dismissal_kind'], as_index = False)
            .agg(Count = ('dismissal_kind', 'count'))
            .sort_values(by = 'Count', ascending = False, ignore_index = True)
            .rename(columns = {'dismissal_kind': 'Dismissal Kind'})
            )
    else:
        df_filtered = (
            df_all1.query(f"player_dismissed == '{player_name}' & season == '{season}'")
            .groupby(by = ['season','dismissal_kind'], as_index = False)
            .agg(Count = ('dismissal_kind', 'count'))
            .sort_values(by = 'Count', ascending = False, ignore_index = True)
            .rename(columns = {'dismissal_kind': 'Dismissal Kind'})
            )
    return df_filtered 

# ------------------------------------------------------------------------------------------------------------------------------------------
## Dismissal Kind by Bowler
def player_dismissal_bowler(player_name, season = 'All'):
    if season == 'All':
        df_filtered = (
            df_all1
            .query(f"player_dismissed == '{player_name}' & dismissal_kind != 'run out'")
            .groupby(by = ['bowler', 'dismissal_kind'], as_index = False)
            .agg(Count = ('dismissal_kind', 'count'))
            .sort_values(by = 'Count', ascending = False, ignore_index = True)
            .rename(columns = {'bowler': 'Bowler', 'dismissal_kind': 'Dismissal Kind'})
            )
    else:
        df_filtered = (
            df_all1.query(f"player_dismissed == '{player_name}' & season == '{season}' & dismissal_kind != 'run out'")
            .groupby(by = ['season','bowler', 'dismissal_kind'], as_index = False)
            .agg(Count = ('dismissal_kind', 'count'))
            .sort_values(by = 'Count', ascending = False, ignore_index = True)
            .rename(columns = {'season': 'Season', 'bowler': 'Bowler','dismissal_kind': 'Dismissal Kind'})
            )
    return df_filtered 

# ------------------------------------------------------------------------------------------------------------------------------------------
## Performance against Rival Bowlers
def top_rival_bowler(player_name):
    return (
        player_dismissal_bowler(player_name = player_name, season = 'All')
        .groupby(by = ['Bowler'], as_index = False)
        .agg(Dismissals = ('Count', 'sum'))
        .sort_values(by = ['Dismissals'], ascending = False, ignore_index = True)  
    )

def run_type(player_name, type):
    top_rival_bowlers_list = top_rival_bowler(player_name)['Bowler'].head(10).values
    return (
        df_all1
        .query(f"batter == '{player_name}' & bowler in @top_rival_bowlers_list & batsman_runs == {type}")
        .groupby(by = ['bowler'], as_index = False)
        .agg(**{f"{type}'s": ('batsman_runs', 'count')})
        .rename(columns = {'bowler': 'Bowler'})
    )

def performance_rival_bowler(player_name):
    top_rival_bowlers_list = top_rival_bowler(player_name)['Bowler'].head(10).values

    df = (
        df_all1.query(f"batter == '{player_name}' & bowler in @top_rival_bowlers_list")
        .groupby(by = ['bowler'], as_index = False)
        .agg(
            Balls = ('ball', 'count'),
            Runs = ('batsman_runs', 'sum')
        )
        .rename(columns = {'bowler': 'Bowler'})
        .merge(top_rival_bowler(player_name), on = 'Bowler')
        .merge(run_type(player_name, 6), on = 'Bowler', how = 'outer')
        .merge(run_type(player_name, 4), on ='Bowler', how = 'outer')
        .merge(run_type(player_name, 3), on ='Bowler', how = 'outer')
        .merge(run_type(player_name, 2), on ='Bowler', how = 'outer')
        .merge(run_type(player_name, 1), on ='Bowler', how = 'outer')
        .merge(run_type(player_name, 0), on ='Bowler', how = 'outer')
        .fillna(0)
        .assign(
            strike_rate = lambda df_: round((df_['Runs']/df_['Balls'])*100,2),
            batting_average = lambda df_: round(df_['Runs']/df_['Dismissals'],2),
            dot_percent = lambda df_: round((df_["0's"]/df_['Balls']*100),2)
        )
        .rename(columns = {"0's": 'Dots', 'strike_rate': 'Strike Rate', 
                           'batting_average': 'Batting Average', 'dot_percent': 'Dot %'})
        .sort_values(by = 'Dismissals', ascending = False, ignore_index = True)
    )
    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
## Century
def player_century(player_name):
    return (
        df_all1.query(f"batter == '{player_name}'")
        .groupby(by = ['id', 'season', 'bowling_team', 'batter'], as_index = False)
        .agg(Runs = ('batsman_runs', 'sum'))
        .query("Runs >= 100")
        .rename(columns = {'id':'Match ID', 'season': 'Season', 'bowling_team':'Bowling Team', 'batter': 'Batsman'})
    )

def player_half_century(player_name):
    return (
        df_all1.query(f"batter == '{player_name}'")
        .groupby(by = ['id', 'season', 'bowling_team', 'batter'], as_index = False)
        .agg(Runs = ('batsman_runs', 'sum'))
        .query("Runs >= 50 & Runs < 100")
        .rename(columns = {'id':'Match ID', 'season': 'Season', 'bowling_team':'Bowling Team', 'batter': 'Batsman'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Batsman Overall stats
def batsman_stats_all(player_name):
    return (
        df_all1.query(f"batter == '{player_name}'")
        .groupby(by = ['batter', 'inning','season', 'batting_team', 'bowling_team'], as_index = False)
        .agg(
            Runs = ('batsman_runs', 'sum'),
            Balls = ('batsman_runs', 'count'),
            Sixes = ('batsman_runs', lambda x: (x == 6).sum()),
            Fours = ('batsman_runs', lambda x: (x == 4).sum()),
            Threes = ('batsman_runs', lambda x: (x == 3).sum()),
            Twos = ('batsman_runs', lambda x: (x == 2).sum()),
            Ones = ('batsman_runs', lambda x: (x == 1).sum()),
            Dots = ('batsman_runs', lambda x: (x == 0).sum())
        )
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Batsman Innings Stats
def batsman_stats_inning(player_name):
    return (
        batsman_stats_all(player_name)
        .groupby(by = ['batter','inning', 'season'], as_index = False)
        .agg(
            Runs = ('Runs', 'sum'),
            Balls = ('Balls', 'sum'),
            Sixes = ('Sixes', 'sum'),
            Fours = ('Fours', 'sum'),
            Threes = ('Threes', 'sum'),
            Twos = ('Twos', 'sum'),
            Ones = ('Ones', 'sum'),
            Dots = ('Dots', 'sum')
        )
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Player top scores
def player_top_scores(player_name):
    return (
        match_runs(player_name)
        .sort_values(by = 'Runs', ascending = False, ignore_index = True)
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Century win Cause
def century_win_cause(player_name, century = True):
    if century == True:
        df = match_runs(player_name).query("Runs >= 100")
    else:
        df = match_runs(player_name).query("Runs >= 50 & Runs < 100")
    return (
        df
        .merge(matches[['id', 'winner']], left_on = 'Match ID', right_on = 'id')
        .assign(Won = lambda df_: (df_['Team'] == df_['winner']).astype('int'))
        .rename(columns = {'winner': 'Winner'})
        .drop('id', axis = 1)
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Performance of Batsman against Teams
def batsman_against_team(player_name, rival_team):
    return (
        match_runs(player_name)
        .query(f"`Bowling Team` == '{rival_team}'")
        .groupby(by = 'Bowling Team', as_index = False)
        .agg(
            Innings = ('Match ID', 'nunique'),
            Runs = ('Runs', 'sum'),
            Balls = ('Balls', 'sum'),
            Centuries = ('Century', 'sum'),
            Half_Centuries = ('Half_Century', 'sum'),
            Sixes = ('Sixes', 'sum'),
            Fours = ('Fours', 'sum'),
            Threes = ('Threes', 'sum'),
            Twos = ('Twos', 'sum'),
            Ones = ('Ones', 'sum'),
            Dots = ('Dots', 'sum'),
        )
        .merge(
            (
            df_all1.query(f"batter == '{player_name}' & bowling_team == '{rival_team}' & player_dismissed == '{player_name}'")
            .groupby(by = 'bowling_team', as_index = False)
            .agg(count = ('player_dismissed', 'count'))
            .rename(columns = {'bowling_team': 'Bowling Team', 'count': 'Dismissals'})
            ), on = 'Bowling Team', how = 'outer'
        )
        .assign(
            Strike_Rate = lambda df_: round((df_['Runs']/df_['Balls'])*100,4),
            Boundary_Percent = lambda df_: round(((df_['Sixes']*6 + df_['Fours']*4)/df_['Runs'])*100,4),
            Dot_Ball_Percent = lambda df_: round((df_['Dots']/df_['Balls'])*100,4),
            Not_Outs = lambda df_: df_['Innings'] - df_['Dismissals'],
            Batting_Average = lambda df_: round((df_['Runs']/df_['Dismissals']),4)
        )
        .rename(columns = {'Half_Centuries':'Half Centuries', 'Strike_Rate':'Strike Rate',
                           'Boundary_Percent':'Boundary Dominance', 'Dot_Ball_Percent': 'Dot Ball Reliance', 
                           'Not_Outs': 'Not Outs', 'Batting_Average': 'Batting Average'})
        [['Bowling Team', 'Innings', 'Runs', 'Balls', 'Centuries', 'Half Centuries', 'Sixes', 'Fours', 'Threes', 
              'Twos', 'Ones', 'Dots', 'Dismissals', 'Not Outs', 'Strike Rate', 'Batting Average', 'Boundary Dominance', 
              'Dot Ball Reliance']]
        
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Bowler Team(s) & Season(s)
def bowler_teams(bowler_name):
    df = (
        df_all1
        .groupby(by = ['bowler', 'bowling_team'], as_index = False)
        .agg(
            Season = ('season', lambda x: ", ".join(x.unique())),
            Count = ('season', 'nunique')
        )
        .query(f"bowler == '{bowler_name}'")
        .rename(columns = {'bowler': 'Bowler', 'bowling_team': 'Team'})
        .drop(columns = ['Bowler'])
    )
    df.index = range(1, len(df)+1)
    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
## Bowler Stats Overall
bowler_dismissal_type = ['bowled', 'lbw', 'stumped', 'caught and bowled', 'caught', 'hit wicket']
individual_wickets = (
    df_all1.query("is_wicket == 1 & dismissal_kind in @bowler_dismissal_type")
    .groupby(by = ['bowler', 'season', 'id', 'inning', 'bowling_team','batting_team'], as_index = False)
    .agg(
        matches = ('id', 'nunique'),
        wickets = ('is_wicket', 'sum')
    )
)

economy_rate = (
    df_all1
    .groupby(by = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], as_index = False)
    .agg(
        balls = ('total_runs', 'count'),
        runs_conceded = ('total_runs', 'sum')
    )
    .assign(
        overs = lambda df_: round(df_['balls']/6, 2),
        economy_rate = lambda df_: round(df_['runs_conceded']/df_['overs'],2)
    )
    .sort_values(by = 'economy_rate', ascending = True, ignore_index = True)
)

dot_balls = (
    df_all1.query("total_runs == 0")
    .groupby(by = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], as_index = False)
    .agg(
        dot_balls = ('total_runs', 'count')
    )
    .sort_values(by = 'dot_balls', ascending = False, ignore_index = True)
)

def runs_type_conceded(run_type, str_run_type):
    return (
        df_all1.query(f"batsman_runs == {run_type}")
        .groupby(by = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], as_index=False)
        .agg(**{f'count_{str_run_type}_conceded': ('batsman_runs', 'count')}) 
    )

sixes_conceded_df = runs_type_conceded(run_type = 6, str_run_type = 'six')
fours_conceded_df = runs_type_conceded(run_type = 4, str_run_type = 'four')
threes_conceded_df = runs_type_conceded(run_type = 3, str_run_type = 'three')
twos_conceded_df = runs_type_conceded(run_type = 2, str_run_type = 'two')
ones_conceded_df = runs_type_conceded(run_type = 1, str_run_type = 'one')

bowler_extra_runs = (
    df_all1.query("extra_runs > 0")
    .groupby(by = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], as_index = False)
    .agg(
        count_extra_runs = ('extra_runs', 'sum')
    )
)

bowler_stats_overall = (
    individual_wickets
    .merge(economy_rate, on = ['bowler', 'season', 'inning', 'id', 'bowling_team', 'batting_team'], how = 'outer')
    .merge(dot_balls, on = ['bowler', 'season', 'inning', 'id', 'bowling_team', 'batting_team'], how = 'outer')
    .merge(sixes_conceded_df, on = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], how = 'outer')
    .merge(fours_conceded_df, on = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], how = 'outer')
    .merge(threes_conceded_df, on = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], how = 'outer')
    .merge(twos_conceded_df, on = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], how = 'outer')
    .merge(ones_conceded_df, on = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], how = 'outer')
    .merge(bowler_extra_runs, on = ['bowler', 'season', 'id', 'inning', 'bowling_team', 'batting_team'], how = 'outer')
    .assign(
        matches = lambda df_: df_['matches'].fillna(0).astype('int'),
        wickets = lambda df_: df_['wickets'].fillna(0).astype('int'),
        dot_balls = lambda df_: df_['dot_balls'].fillna(0).astype('int'),
        count_six_conceded = lambda df_: df_['count_six_conceded'].fillna(0).astype('int'),
        count_four_conceded = lambda df_: df_['count_four_conceded'].fillna(0).astype('int'),
        count_three_conceded = lambda df_: df_['count_three_conceded'].fillna(0).astype('int'),
        count_two_conceded = lambda df_: df_['count_two_conceded'].fillna(0).astype('int'),
        count_one_conceded = lambda df_: df_['count_one_conceded'].fillna(0).astype('int'),
        count_extra_runs = lambda df_: df_['count_extra_runs'].fillna(0).astype('int')
    )
    .assign(
        bowling_average = lambda df_: round(df_['runs_conceded']/df_['wickets'], 2),
        strike_rate = lambda df_: round(df_['balls']/df_['wickets'],2),
        boundary_rate = lambda df_: round((df_['count_six_conceded'] + df_['count_four_conceded'])/df_['balls'],2),
        dot_ball_percent = lambda df_: round((df_['dot_balls']/df_['balls'])*100, 4)
    )
)

# ------------------------------------------------------------------------------------------------------------------------------------------
## Bowler Inning-wise Stats
def bowler_stats_innings(bowler_name):
    return (
        bowler_stats_overall
        .groupby(by = ['bowler', 'inning'], as_index = False)
        .agg(
            matches = ('id', 'nunique'),
            wickets = ('wickets', 'sum'),
            balls = ('balls', 'sum'),
            runs_conceded = ('runs_conceded', 'sum'),
            dot_balls = ('dot_balls', 'sum'),
            count_six_conceded = ('count_six_conceded', 'sum'),
            count_four_conceded = ('count_four_conceded', 'sum'),
            count_three_conceded = ('count_three_conceded', 'sum'),
            count_two_conceded = ('count_two_conceded', 'sum'),
            count_one_conceded = ('count_one_conceded', 'sum'),
            count_extra_runs = ('count_extra_runs', 'sum')
        )
        .assign(
            overs = lambda df_: df_['balls']/6,
            bowling_average = lambda df_: round(df_['runs_conceded']/df_['wickets'], 4),
            strike_rate = lambda df_: round(df_['balls']/df_['wickets'], 4),
            boundary_rate = lambda df_: round((df_['count_six_conceded'] + df_['count_four_conceded'])*100/df_['balls'], 4),
            economy_rate = lambda df_: df_['runs_conceded']/df_['overs'],
            dot_ball_percent = lambda df_: round((df_['dot_balls']/df_['balls'])*100, 4)
        )
        .rename(columns = {'bowler': 'Bowler', 'inning': 'Inning', 'matches': 'Matches', 'wickets': 'Wickets',
                           'balls': 'Balls', 'overs': 'Overs', 'runs_conceded': 'Runs Conceded',
                           'economy_rate': 'Economy Rate', 'bowling_average': 'Bowling Average',
                           'strike_rate': 'Strike Rate', 'boundary_rate': 'Boundary %', 'dot_balls': 'Dot Balls', 
                           'dot_ball_percent': 'Dot Ball %', 'count_six_conceded': '6s Conceded', 
                           'count_four_conceded': '4s Conceded', 'count_three_conceded': '3s Conceded', 
                           'count_two_conceded': '2s Conceded', 'count_one_conceded': '1s Conceded', 
                           'count_extra_runs': 'Extra Runs'})
        .loc[:, ['Bowler', 'Inning', 'Matches', 'Wickets', 'Balls', 'Overs', 'Runs Conceded', 'Dot Balls',
                 'Economy Rate', 'Bowling Average', 'Strike Rate', 'Boundary %', 'Dot Ball %', '6s Conceded', 
                 '4s Conceded', '3s Conceded', '2s Conceded', '1s Conceded', 'Extra Runs']]
        .query(f"Bowler == '{bowler_name}'")
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Season wise Perfromance of Bowlers
def bowler_stats_seasons(bowler_name):
    return (
        bowler_stats_overall
        .groupby(by = ['bowler', 'season'], as_index = False)
        .agg(
            matches = ('id', 'nunique'),
            wickets = ('wickets', 'sum'),
            balls = ('balls', 'sum'),
            runs_conceded = ('runs_conceded', 'sum'),
            dot_balls = ('dot_balls', 'sum'),
            count_six_conceded = ('count_six_conceded', 'sum'),
            count_four_conceded = ('count_four_conceded', 'sum'),
            count_three_conceded = ('count_three_conceded', 'sum'),
            count_two_conceded = ('count_two_conceded', 'sum'),
            count_one_conceded = ('count_one_conceded', 'sum'),
            count_extra_runs = ('count_extra_runs', 'sum')
        )
        .assign(
            overs = lambda df_: round(df_['balls']/6, 4),
            bowling_average = lambda df_: round(df_['runs_conceded']/df_['wickets'], 4),
            strike_rate = lambda df_: round(df_['balls']/df_['wickets'], 4),
            boundary_rate = lambda df_: round((df_['count_six_conceded'] + df_['count_four_conceded'])*100/df_['balls'], 4),
            economy_rate = lambda df_: round(df_['runs_conceded']/df_['overs'], 4),
            dot_ball_percent = lambda df_: round((df_['dot_balls']/df_['balls'])*100, 4)
        )
        .rename(columns = {'bowler': 'Bowler', 'season': 'Season', 'matches': 'Matches', 'wickets': 'Wickets',
                           'balls': 'Balls', 'overs': 'Overs', 'runs_conceded': 'Runs Conceded',
                           'economy_rate': 'Economy Rate', 'bowling_average': 'Bowling Average',
                           'strike_rate': 'Strike Rate', 'boundary_rate': 'Boundary Rate', 'dot_balls': 'Dot Balls', 
                           'dot_ball_percent': 'Dot Ball %', 'count_six_conceded': '6s Conceded', 
                           'count_four_conceded': '4s Conceded', 'count_three_conceded': '3s Conceded', 
                           'count_two_conceded': '2s Conceded', 'count_one_conceded': '1s Conceded', 
                           'count_extra_runs': 'Extra Runs'})
        .loc[:, ['Bowler', 'Season', 'Matches', 'Wickets', 'Balls', 'Overs', 'Runs Conceded', 'Dot Balls',
                 'Economy Rate', 'Bowling Average', 'Strike Rate', 'Boundary Rate', 'Dot Ball %', '6s Conceded', 
                 '4s Conceded', '3s Conceded', '2s Conceded', '1s Conceded', 'Extra Runs']]
        .query(f"Bowler == '{bowler_name}'")
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Season-wise Inning Wise Performance of Bowlers
def bowler_stats_seasons_inning(bowler_name):
    return (
        bowler_stats_overall
        .groupby(by = ['bowler', 'season', 'inning'], as_index = False)
        .agg(
            matches = ('id', 'nunique'),
            wickets = ('wickets', 'sum'),
            balls = ('balls', 'sum'),
            runs_conceded = ('runs_conceded', 'sum'),
            dot_balls = ('dot_balls', 'sum'),
            count_six_conceded = ('count_six_conceded', 'sum'),
            count_four_conceded = ('count_four_conceded', 'sum'),
            count_three_conceded = ('count_three_conceded', 'sum'),
            count_two_conceded = ('count_two_conceded', 'sum'),
            count_one_conceded = ('count_one_conceded', 'sum'),
            count_extra_runs = ('count_extra_runs', 'sum')
        )
        .assign(
            overs = lambda df_: round(df_['balls']/6, 4),
            bowling_average = lambda df_: round(df_['runs_conceded']/df_['wickets'], 4),
            strike_rate = lambda df_: round(df_['balls']/df_['wickets'], 4),
            boundary_rate = lambda df_: round((df_['count_six_conceded'] + df_['count_four_conceded'])*100/df_['balls'], 4),
            economy_rate = lambda df_: round(df_['runs_conceded']/df_['overs'], 4),
            dot_ball_percent = lambda df_: round((df_['dot_balls']/df_['balls'])*100, 4)
        )
        .rename(columns = {'bowler': 'Bowler', 'season': 'Season', 'inning': 'Inning', 'matches': 'Matches', 'wickets': 'Wickets',
                           'balls': 'Balls', 'overs': 'Overs', 'runs_conceded': 'Runs Conceded',
                           'economy_rate': 'Economy Rate', 'bowling_average': 'Bowling Average',
                           'strike_rate': 'Strike Rate', 'boundary_rate': 'Boundary Rate', 'dot_balls': 'Dot Balls', 
                           'dot_ball_percent': 'Dot Ball %', 'count_six_conceded': '6s Conceded', 
                           'count_four_conceded': '4s Conceded', 'count_three_conceded': '3s Conceded', 
                           'count_two_conceded': '2s Conceded', 'count_one_conceded': '1s Conceded', 
                           'count_extra_runs': 'Extra Runs'})
        .loc[:, ['Bowler', 'Season', 'Inning', 'Matches', 'Wickets', 'Balls', 'Overs', 'Runs Conceded', 'Dot Balls',
                 'Economy Rate', 'Bowling Average', 'Strike Rate', 'Boundary Rate', 'Dot Ball %', '6s Conceded', 
                 '4s Conceded', '3s Conceded', '2s Conceded', '1s Conceded', 'Extra Runs']]
        .query(f"Bowler == '{bowler_name}'")
    )

def bowler_stats_teams(bowler_name):
    return (
        bowler_stats_overall
        .groupby(by = ['bowler', 'batting_team'], as_index = False)
        .agg(
            matches = ('id', 'nunique'),
            wickets = ('wickets', 'sum'),
            balls = ('balls', 'sum'),
            runs_conceded = ('runs_conceded', 'sum'),
            dot_balls = ('dot_balls', 'sum'),
            count_six_conceded = ('count_six_conceded', 'sum'),
            count_four_conceded = ('count_four_conceded', 'sum'),
            count_three_conceded = ('count_three_conceded', 'sum'),
            count_two_conceded = ('count_two_conceded', 'sum'),
            count_one_conceded = ('count_one_conceded', 'sum'),
            count_extra_runs = ('count_extra_runs', 'sum')
        )
        .assign(
            overs = lambda df_: round(df_['balls']/6,4),
            bowling_average = lambda df_: round(df_['runs_conceded']/df_['wickets'], 4),
            strike_rate = lambda df_: round(df_['balls']/df_['wickets'], 4),
            boundary_rate = lambda df_: round((df_['count_six_conceded'] + df_['count_four_conceded'])*100/df_['balls'], 4),
            economy_rate = lambda df_: round(df_['runs_conceded']/df_['overs'],4),
            dot_ball_percent = lambda df_: round((df_['dot_balls']/df_['balls'])*100, 4)
        )
        .rename(columns = {'bowler': 'Bowler', 'batting_team': 'Rival Team', 'matches': 'Matches', 'wickets': 'Wickets',
                           'balls': 'Balls', 'overs': 'Overs', 'runs_conceded': 'Runs Conceded',
                           'economy_rate': 'Economy Rate', 'bowling_average': 'Bowling Average',
                           'strike_rate': 'Strike Rate', 'boundary_rate': 'Boundary %', 'dot_balls': 'Dot Balls', 
                           'dot_ball_percent': 'Dot Ball %', 'count_six_conceded': '6s Conceded', 
                           'count_four_conceded': '4s Conceded', 'count_three_conceded': '3s Conceded', 
                           'count_two_conceded': '2s Conceded', 'count_one_conceded': '1s Conceded', 
                           'count_extra_runs': 'Extra Runs'})
        .loc[:, ['Bowler', 'Rival Team', 'Matches', 'Wickets', 'Balls', 'Overs', 'Runs Conceded', 'Dot Balls',
                 'Economy Rate', 'Bowling Average', 'Strike Rate', 'Boundary %', 'Dot Ball %', '6s Conceded', 
                 '4s Conceded', '3s Conceded', '2s Conceded', '1s Conceded', 'Extra Runs']]
        .query(f"Bowler == '{bowler_name}'")
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
## Bowler Performance against Teams - Seasonwise
def bowler_stats_teams_season(bowler_name, team):
    return (
        bowler_stats_overall
        .groupby(by = ['bowler', 'batting_team', 'season'], as_index = False)
        .agg(
            matches = ('id', 'nunique'),
            wickets = ('wickets', 'sum'),
            balls = ('balls', 'sum'),
            runs_conceded = ('runs_conceded', 'sum'),
            dot_balls = ('dot_balls', 'sum'),
            count_six_conceded = ('count_six_conceded', 'sum'),
            count_four_conceded = ('count_four_conceded', 'sum'),
            count_three_conceded = ('count_three_conceded', 'sum'),
            count_two_conceded = ('count_two_conceded', 'sum'),
            count_one_conceded = ('count_one_conceded', 'sum'),
            count_extra_runs = ('count_extra_runs', 'sum')
        )
        .assign(
            overs = lambda df_: df_['balls']/6,
            bowling_average = lambda df_: round(df_['runs_conceded']/df_['wickets'], 4),
            strike_rate = lambda df_: round(df_['balls']/df_['wickets'], 4),
            boundary_rate = lambda df_: round((df_['count_six_conceded'] + df_['count_four_conceded'])*100/df_['balls'], 4),
            economy_rate = lambda df_: df_['runs_conceded']/df_['overs'],
            dot_ball_percent = lambda df_: round((df_['dot_balls']/df_['balls'])*100, 4)
        )
        .rename(columns = {'bowler': 'Bowler', 'season': 'Season', 'batting_team': 'Rival Team', 'matches': 'Matches', 'wickets': 'Wickets',
                           'balls': 'Balls', 'overs': 'Overs', 'runs_conceded': 'Runs Conceded',
                           'economy_rate': 'Economy Rate', 'bowling_average': 'Bowling Average',
                           'strike_rate': 'Strike Rate', 'boundary_rate': 'Boundary Rate', 'dot_balls': 'Dot Balls', 
                           'dot_ball_percent': 'Dot Ball %', 'count_six_conceded': '6s Conceded', 
                           'count_four_conceded': '4s Conceded', 'count_three_conceded': '3s Conceded', 
                           'count_two_conceded': '2s Conceded', 'count_one_conceded': '1s Conceded', 
                           'count_extra_runs': 'Extra Runs'})
        .loc[:, ['Bowler', 'Rival Team', 'Season', 'Matches', 'Wickets', 'Balls', 'Overs', 'Runs Conceded', 'Dot Balls',
                 'Economy Rate', 'Bowling Average', 'Strike Rate', 'Boundary Rate', 'Dot Ball %', '6s Conceded', 
                 '4s Conceded', '3s Conceded', '2s Conceded', '1s Conceded', 'Extra Runs']]
        .query(f"Bowler == '{bowler_name}' & `Rival Team` == '{team}'")
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
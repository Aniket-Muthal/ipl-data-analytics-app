import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import joblib
from scripts import player_analysis
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

df_all = matches.merge(deliveries, left_on = 'id', right_on = 'match_id')

# ------------------------------------------------------------------------------------------------------------------------------------------
## 1. Key-Highlights
### 1.1. Team, Seasons and Matches Played
matches_played_teams = (
    matches
    .groupby(by = ['team1'], as_index = False)
    .agg(
        matches = ('id', 'nunique')
    )
    .merge(
        matches
        .groupby(by = 'team2', as_index = False)
        .agg(
            matches = ('id', 'nunique')
        ),
        left_on = 'team1', right_on = 'team2'
    )
    .assign(
        matches_x = lambda df_: df_['matches_x'].fillna(0),
        matches_y = lambda df_: df_['matches_y'].fillna(0),
        matches = lambda df_: df_['matches_x'] + df_['matches_y']
    )
    .drop(columns = ['team2', 'matches_x', 'matches_y'])
    .rename(columns = {'team1': 'Team', 'matches': 'Matches'})
    .sort_values(by = 'Matches', ascending = False, ignore_index = True)
)
matches_played_teams.index = range(1, len(matches_played_teams)+1)

matches_teams_seasons = (
    matches
    .groupby(by = ['team1', 'season'], as_index = False)
    .agg(
        matches = ('id', 'nunique')
    )
    .merge(
        matches
        .groupby(by = ['team2', 'season'], as_index = False)
        .agg(
            matches = ('id', 'count')
        ),
        left_on = ['team1', 'season'], right_on = ['team2', 'season'], how = 'outer'
    )
    .assign(
        matches_x = lambda df_: df_['matches_x'].fillna(0),
        matches_y = lambda df_: df_['matches_y'].fillna(0),
        matches = lambda df_: (df_['matches_x'] + df_['matches_y']).astype('int')
    )
    .drop(['team2', 'matches_x', 'matches_y'], axis = 1)
    .rename(columns = {'team1': 'Team', 'season': 'Season', 'matches': 'Matches'})
)

teams_season_count = matches_teams_seasons['Team'].value_counts().reset_index(name = 'Total Seasons')

teams_seasons = (
    matches_teams_seasons
    .groupby('Team', as_index=False)
    .agg(years=('Season', lambda x: ', '.join(map(str, sorted(set(x))))))
)

teams_df1 = teams_season_count.merge(teams_seasons, on='Team')

teams_df = (
    teams_df1
    .merge(matches_played_teams, on = 'Team')
    .rename(columns = {'years': 'Seasons'})
    .sort_values(by = 'Matches', ascending = False, ignore_index = True)
)
teams_df.index = range(1, len(teams_df)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
### 1.2. Metrics I
def extract_team(team_name):
    return df_all.query(f"team1 == '{team_name}' or team2 == '{team_name}'")

#### 1.2.1. General Highlights
def team_highlights_general(team_name, seasons = 'All'):
    df_team = extract_team(team_name)

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    total_matches = df_filtered['id'].nunique()
    superovers = df_filtered[df_filtered['super_over'] == 'Y']['id'].nunique()
    cities = df_filtered['city'].nunique()
    venues = df_filtered['venue'].nunique()

    return total_matches, superovers, cities, venues

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.2.2. Batsman Highlights
def team_highlights_batsman(team_name, seasons='All'):
    df_team = extract_team(team_name)

    if seasons == 'All':
        df_filtered = df_team.query(f"batting_team == '{team_name}'")
    elif isinstance(seasons, list):
        df_filtered = df_team.query(f"batting_team == '{team_name}' and season in @seasons")
    else:
        df_filtered = df_team.query(f"batting_team == '{team_name}' and season == '{seasons}'")

    batsman_runs = df_filtered['batsman_runs'].sum()
    extra_runs = df_filtered['extra_runs'].sum()

    p1 = df_filtered['batter'].unique()
    p2 = df_filtered['non_striker'].unique()
    batsman_count = len(set(list(p1) + list(p2)))

    sixes = df_filtered.query("batsman_runs == 6")['batsman_runs'].count()
    fours = df_filtered.query("batsman_runs == 4")['batsman_runs'].count()

    centuries = (
        df_filtered.groupby(['id', 'batter'])
        .agg(runs=('batsman_runs', 'sum'))
        .query("runs >= 100")
        .runs.count()
    )

    half_centuries = (
        df_filtered.groupby(['id', 'batter'])
        .agg(runs=('batsman_runs', 'sum'))
        .query("50 <= runs < 100")
        .runs.count()
    )

    return batsman_runs, extra_runs, sixes, fours, centuries, half_centuries, batsman_count

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.2.3. Bowler Highlights
def team_highlights_bowler(team_name, seasons='All'):
    df_team = extract_team(team_name)

    if seasons == 'All':
        df_filtered = df_team.query(f"bowling_team == '{team_name}'")
    elif isinstance(seasons, list):
        df_filtered = df_team.query("bowling_team == @team_name and season in @seasons")
    else:
        df_filtered = df_team.query(f"bowling_team == '{team_name}' and season == '{seasons}'")

    bowler_count = df_filtered['bowler'].nunique()
    balls = df_filtered.shape[0]
    wickets = df_filtered.query("is_wicket == 1").shape[0]

    bowler_dismissal_type = ['caught', 'caught and bowled', 'bowled', 'lbw', 'stumped']
    
    four_wickets = (
        df_filtered.query("is_wicket == 1 and dismissal_kind in @bowler_dismissal_type")
        .groupby(['id', 'bowler'])
        .agg(wickets=('is_wicket', 'sum'))
        .query("wickets == 4")
        .shape[0]
    )

    five_plus_wickets = (
        df_filtered.query("is_wicket == 1 and dismissal_kind in @bowler_dismissal_type")
        .groupby(['id', 'bowler'])
        .agg(wickets=('is_wicket', 'sum'))
        .query("wickets >= 5")
        .shape[0]
    )

    return bowler_count, balls, wickets, four_wickets, five_plus_wickets

# ------------------------------------------------------------------------------------------------------------------------------------------
### 1.3. Metrics II
#### 1.3.1. Most Player of the Match Awards
def pom(team_name, seasons = 'All'):
    df_team = extract_team(team_name)

    if seasons == 'All':
        df_filtered = df_team.query(f"winner == '{team_name}'")
    elif isinstance(seasons, list):
        df_filtered = df_team.query("winner == @team_name and season in @seasons")
    else:
        df_filtered = df_team.query(f"winner == '{team_name}' and season == '{seasons}'")
    
    return (
        df_filtered
        .groupby(by = ['player_of_match'], as_index = False)
        .agg(Count = ('id', 'nunique'))
        .sort_values(by = 'Count', ascending = False, ignore_index = True)
        .rename(columns = {'player_of_match': 'Player of Match'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.3.2. Leading Run Scorer
def leading_run_scorer(team_name, seasons='All'):
    df_team = extract_team(team_name)

    if seasons == 'All':
        df_filtered = df_team.query(f"batting_team == '{team_name}'")
    elif isinstance(seasons, list):
        df_filtered = df_team.query("batting_team == @team_name and season in @seasons")
    else:
        df_filtered = df_team.query(f"batting_team == '{team_name}' and season == '{seasons}'")

    return (
        df_filtered
        .groupby(by = 'batter', as_index = False)
        .agg(Runs = ('batsman_runs', 'sum'))
        .sort_values(by = 'Runs', ascending = False, ignore_index = True)
        .rename(columns = {'batter': 'Batsman'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.3.3. Leading Wicket Taker
bowler_dismissal_type = ['caught', 'caught and bowled', 'bowled', 'lbw', 'stumped', 'hit wicket']

def leading_wicket_taker(team_name, seasons='All'):
    df_team = extract_team(team_name).query(f"(bowling_team == '{team_name}' & is_wicket == 1) & (dismissal_kind in @bowler_dismissal_type)")

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return (
        df_filtered
        .groupby(by = 'bowler', as_index = False)
        .agg(Wickets = ('is_wicket', 'sum'))
        .sort_values(by = 'Wickets', ascending = False, ignore_index = True)
        .rename(columns = {'bowler': 'Bowler'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.3.4. Highest Team Score
def individual_team_score(team_name, seasons='All'):
    df_team = extract_team(team_name)

    if seasons == 'All':
        df_filtered = df_team.query(f"batting_team == '{team_name}'")
    elif isinstance(seasons, list):
        df_filtered = df_team.query("batting_team == @team_name and season in @seasons")
    else:
        df_filtered = df_team.query(f"batting_team == '{team_name}' and season == '{seasons}'")

    return (
        df_filtered
        .groupby(by = ['id','season'], as_index = False)
        .agg(Runs = ('total_runs', 'sum'))
        .sort_values(by = 'Runs', ascending = False, ignore_index = True)
        .rename(columns = {'id': 'Match', 'season': 'Season'})
        .drop(columns = 'Match')
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.3.5. Highest Individual Score
def individual_score(team_name, seasons='All'):
    df_team = extract_team(team_name)

    if seasons == 'All':
        df_filtered = df_team.query(f"batting_team == '{team_name}'")
    elif isinstance(seasons, list):
        df_filtered = df_team.query("batting_team == @team_name and season in @seasons")
    else:
        df_filtered = df_team.query(f"batting_team == '{team_name}' and season == '{seasons}'")

    return (
        df_filtered
        .groupby(by = ['id', 'batter'], as_index = False)
        .agg(Runs = ('batsman_runs', 'sum'))
        .sort_values(by = 'Runs', ascending = False, ignore_index = True)
        .rename(columns = {'batter': 'Batsman'})
        .drop(columns = ['id'])
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.3.6. Best Bowling Figure
bowler_dismissal_type = ['caught', 'caught and bowled', 'bowled', 'lbw', 'stumped', 'hit wicket']

def best_bowling_figure(team_name, seasons = 'All'):
    df_team1 = extract_team(team_name).query(f"(bowling_team == '{team_name}' & is_wicket == 1) & (dismissal_kind in @bowler_dismissal_type)")
    df_team2 = extract_team(team_name).query(f"(bowling_team == '{team_name}' & is_wicket == 0)")
    
    if seasons == 'All':
        df_filtered1 = df_team1
        df_filtered2 = df_team2
    elif isinstance(seasons, list):
        df_filtered1 = df_team1.query("season in @seasons")
        df_filtered2 = df_team2.query("season in @seasons")
    else:
        df_filtered1 = df_team1.query(f"season == '{seasons}'")
        df_filtered2 = df_team2.query(f"season == '{seasons}'")

    return (
        df_filtered1
        .groupby(by = ['id', 'bowler'], as_index = False)
        .agg(Wickets = ('is_wicket', 'sum'))
        .merge(
            (
                df_filtered2
                .groupby(by = ['id', 'bowler'], as_index = False)
                .agg(Runs = ('total_runs', 'sum'))
            ),
            on = ['id', 'bowler']
        )
        .sort_values(by = ['Wickets', 'Runs'], ascending = [False, True], ignore_index = True)
        .rename(columns = {'id': 'Match ID', 'bowler': 'Bowler'})    
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.3.7. Most Boundaries (Sixes and Fours)
def boundaries(team_name, boundary = None, seasons = 'All'):
    df_team = extract_team(team_name)

    if seasons == 'All':
        df_filtered = df_team.query(f"batting_team == '{team_name}'")
    elif isinstance(seasons, list):
        df_filtered = df_team.query("batting_team == @team_name and season in @seasons")
    else:
        df_filtered = df_team.query(f"batting_team == '{team_name}' and season == '{seasons}'")

    if (boundary == 4) | (boundary == 6):
        return(
            df_filtered
            .query(f"batsman_runs == {boundary}")
            .groupby(by = ['batter'], as_index = False)
            .agg(Count = ('batsman_runs', 'count'))
            .sort_values(by = 'Count', ascending = False, ignore_index = True)
            .rename(columns = {'batter': 'Batsman'})
        )
    else:
        return(
            df_filtered
            .query(f"batsman_runs == 4 or batsman_runs == 6")
            .groupby(by = ['batter'], as_index = False)
            .agg(Count = ('batsman_runs', 'count'))
            .sort_values(by = 'Count', ascending = False, ignore_index = True)
            .rename(columns = {'batter': 'Batsman'})
        )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.3.8. Most Catches
fielding = ['caught', 'caught and bowled']
def catches(team_name, seasons = 'All'):
    df_team1 = extract_team(team_name).query(f"(bowling_team == '{team_name}' & is_wicket == 1) & (dismissal_kind == 'caught')")
    df_team2 = extract_team(team_name).query(f"(bowling_team == '{team_name}' & is_wicket == 1) & (dismissal_kind == 'caught and bowled')")
    
    if seasons == 'All':
        df_filtered1 = df_team1
        df_filtered2 = df_team2
    elif isinstance(seasons, list):
        df_filtered1 = df_team1.query("season in @seasons")
        df_filtered2 = df_team2.query("season in @seasons")
    else:
        df_filtered1 = df_team1.query(f"season == '{seasons}'")
        df_filtered2 = df_team2.query(f"season == '{seasons}'")

    return(
        df_filtered1['fielder'].value_counts().reset_index()
        .merge(
            (df_filtered2['bowler'].value_counts().reset_index()),
             left_on = 'fielder', right_on = 'bowler', how = 'outer'
        )
        .assign(
            count_y = lambda df_: df_['count_y'].fillna(0),
            count_x = lambda df_: df_['count_x'].fillna(0),
            count = lambda df_: (df_['count_x'] + df_['count_y']).astype('int'),
            fielder = lambda df_: df_['fielder'].fillna(df_['bowler']),
            bowler = lambda df_: df_['bowler'].fillna(df_['fielder'])
        )
        .drop(columns = ['count_x', 'count_y', 'bowler'])
        .sort_values(by = 'count', ascending = False, ignore_index = True)
        .rename(columns = {'fielder': 'Fielder', 'count': 'Count'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.3.9. Most Stumpings
def stumpings(team_name, seasons = 'All'):
    df_team = extract_team(team_name).query(f"(bowling_team == '{team_name}' & is_wicket == 1) & (dismissal_kind == 'stumped')")

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return(
        df_filtered['fielder']
        .value_counts()
        .reset_index()
        .rename(columns = {'fielder': 'Fielder', 'count': 'Count'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 1.3.10. Most Run Outs
def runouts(team_name, seasons = 'All'):
    df_team = extract_team(team_name).query(f"(bowling_team == '{team_name}' & is_wicket == 1) & (dismissal_kind == 'run out')")

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return(
        df_filtered['fielder']
        .value_counts()
        .reset_index()
        .rename(columns = {'fielder': 'Fielder', 'count': 'Count'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
## 2. Visualizations
### 2.1. General
### 2.1.1. Season-wise Match Count 
def season_match_count(team):
    return (
        matches
        .query(f"team1 == '{team}' or team2 == '{team}'")
        .groupby(by = 'season', as_index = False)
        .agg(Count = ('id', 'nunique'))
        .rename(columns = {'season': 'Season'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.1.2. Win-Loss % (Season Cumulative)
def team_stats(team_name):
    df = matches.query(f"team1 == '{team_name}' or team2 == '{team_name}'")
    num_matches = df.shape[0]
    matches_won = df[df['winner'] == team_name].shape[0]
    win_percent = round(matches_won*100/num_matches, 2)
    
    return df, num_matches, matches_won, win_percent

# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.1.3. Match-Type Success Rate
def team_swap(row, team_name):
    if row['team2'] == team_name:
        row['team2'] = row['team1']
    return row

def team_record(team_name):
    return (
        matches
        .query(f"team1 == '{team_name}' or team2 == '{team_name}'")
        .groupby(by = ['team1', 'team2', 'match_type', 'winner'], as_index = False)
        .agg(count = ('id', 'nunique'))
        .apply(lambda row: team_swap(row, team_name), axis=1)
        .assign(team1 = team_name)
    )

def team_matchtype(team_name):
    return (
        team_record(team_name)
        .groupby(by = ['match_type'], as_index = False)
        .agg(num_matches = ('count', 'sum'))
        .rename(columns = {'match_type': 'Match Type', 'num_matches': 'Total Matches'})
        .merge(
            team_record(team_name)
            .groupby(by = ['match_type', 'winner'], as_index = False)
            .agg(matches_won = ('count', 'sum'))
            .query(f"winner == '{team_name}'")
            .rename(columns = {'match_type': 'Match Type', 'matches_won': 'MatchesWon'})
            .drop(columns = 'winner'),
            on = 'Match Type', how = 'outer'
        )
        .fillna(0)
        .assign(win_percent = lambda df_: round((df_['MatchesWon']/df_['Total Matches'])*100,2),
                MatchesWon = lambda df_: df_['MatchesWon'].astype('int'))
        .rename(columns = {'win_percent': 'Win %', 'MatchesWon': 'Matches Won'})
    )
team_matchtype('Rising Pune Supergiants')

# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.1.4. Toss Impact
def team(team_name, seasons = 'All'):
    if seasons == 'All':
        return matches.query(f"team1 == '{team_name}' or team2 == '{team_name}'")
    elif isinstance(seasons, list):
        return matches.query("(team1 == @team_name or team2 == @team_name) and season in @seasons")
    else: 
        return matches.query(f"(team1 == '{team_name}' or team2 == '{team_name}') and season == '{seasons}'")

def toss_distribution(team_name, seasons = 'All'):
    toss_won = team(team_name, seasons = seasons).query(f"toss_winner == '{team_name}'").shape[0]
    toss_lost = team(team_name, seasons = seasons).query(f"toss_winner != '{team_name}'").shape[0]
    return toss_won, toss_lost

def toss_winning_cause(team_name, seasons = 'All'):
    toss_won_match_won = team(team_name, seasons = seasons).query(f"toss_winner == '{team_name}' and winner == '{team_name}'").shape[0]
    toss_lost_match_won = team(team_name, seasons = seasons).query(f"toss_winner != '{team_name}' and winner == '{team_name}'").shape[0]
    return toss_won_match_won, toss_lost_match_won

# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.1.5. Home & Away Win %
def home_away_wins(team_name, seasons = 'all'):
    if team_name == 'Chennai Super Kings':
        home_city = 'Chennai'
    if team_name == 'Delhi Capitals':
        home_city = 'Delhi'
    if team_name == 'Gujarat Titans':
        home_city = 'Ahmedabad'
    if team_name == 'Kings XI Punjab':
        home_city = 'Chandigarh'
    if team_name == 'Kolkata Knight Riders':
        home_city = 'Kolkata'
    if team_name == 'Lucknow Super Giants':
        home_city = 'Lucknow'
    if team_name == 'Mumbai Indians':
        home_city = 'Mumbai'
    if team_name == 'Rajasthan Royals':
        home_city = 'Jaipur'
    if team_name == 'Rising Pune Supergiants':
        home_city = 'Pune'
    if team_name == 'Royal Challengers Bengaluru':
        home_city = 'Bengaluru'
    if team_name == 'Sunrisers Hyderabad':
        home_city = 'Hyderabad'
    if team_name == 'Kochi Tuskers Kerala':
        home_city = 'Kochi'
    df =  (
        team(team_name, seasons = seasons)
        .assign(Game = lambda df_: df_['city'].apply(lambda city: 'Home' if  city == home_city else 'Away'))
        .groupby(by = 'Game', as_index = False)
        .agg(matches_played = ('id', 'nunique'))
        .merge(
            team(team_name, seasons = seasons)
            .assign(Game = lambda df_: df_['city'].apply(lambda city: 'Home' if  city == home_city else 'Away'))
            .query(f"winner == '{team_name}'")
            .groupby(by = 'Game', as_index = False)
            .agg(matches_won = ('id', 'nunique')), on = 'Game', how = 'outer'
        )
        .fillna(0)
        .assign(
            matches_lost = lambda df_: df_['matches_played'] - df_['matches_won'],
            win_percent = lambda df_: round((df_['matches_won']/df_['matches_played'])*100,2)
        )
        .rename(columns = {'matches_played': 'Total Matches', 'matches_won': 'Matches Won', 
                           'matches_lost': 'Matches Lost', 'win_percent': 'Win %'})
    )
    df.index = range(1, len(df)+1)

    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.1.6. Level Hierarchy
map_data = {'League': 'League', 'Qualifier 1': 'Playoff',
            'Qualifier 2': 'Qualifier 2', 'Eliminator': 'Playoff',
            '3rd Place Play-Off': 'Playoff', 'Semi Final': 'Playoff',
            'Final': 'Final'}

def next_level_status(row, team_name):
    progression_map = {
        "Qualifier 1": "Final",
        "Qualifier 2": "Final",
        "Eliminator": "Qualifier 2",
        "Semi Final": "Final",
        "Final": "Champion"
    }

    if row["winner"] == team_name:
        return progression_map.get(row["match_type"], "Eliminated")
    elif (row['match_type'] == 'Qualifier 1') & (row["winner"] != team_name):
        return "Qualifier 2"
    elif (row['match_type'] == 'Final') & (row["winner"] != team_name):
        return 'Runner Up'
    else:
        return "Eliminated"

def seasonwise_matchtype(team_name, match_level):
    return (
        matches
        .assign(match_category = lambda df_: df_['match_type'].map(map_data))
        .query(f"team1 == '{team_name}' or team2 == '{team_name}'")
        .groupby(by = ['season', 'match_category', 'match_type', 'winner'], as_index = False)
        .agg(count = ('id', 'nunique'))
        .query(f"match_category == '{match_level}'")
        .reset_index(drop = True)
        .drop(columns = 'count')
        .assign(next_level = lambda df_: df_.apply(lambda row: next_level_status(row, team_name), axis=1))
        .rename(columns = {'season': 'Season', 'match_category': 'Match Category',
                           'match_type': 'Match Type', 'winner': 'Winner', 'next_level': 'Next Level'})
    )

def level_hierarchy(team_name):
    df =  (
        seasonwise_matchtype(team_name, 'Playoff')
        .merge(
            seasonwise_matchtype(team_name, 'Qualifier 2'),
            on='Season', how='outer'
        )
        .merge(
            seasonwise_matchtype(team_name, 'Final'),
            on='Season', how='outer'
        )
        .drop(columns = ['Match Category_y', 'Match Type_y', 'Match Category'])
        .fillna('-')
        .rename(columns = {'Match Category_x': 'Level I', 'Match Type_x': 'Type I', 
                           'Winner_x': 'Playoff - Winner', 'Next Level_x': 'Level II', 
                           'Winner_y': 'Qualifier2 - Winner', 'Next Level_y': 'Level III', 
                           'Next Level': 'Result'})
        .assign(Result = lambda df_: df_['Result'].replace('-', 'Eliminated'))
    )
    df.index = range(1, len(df)+1)
    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.2. Players
#### 2.2.1. List of Teams Batsman
def team_batsman_list(team):
    return (
    deliveries
    .query(f"batting_team == '{team}'")
    .batter.unique()
)

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.2.2. Teams Bowler List
def team_bowler_list(team):
    return (
    deliveries
    .query(f"bowling_team == '{team}'")
    .bowler.unique()
)

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.2.3. Batsman Performance
def team_batsman_performance(team):
    return (
        deliveries
        .query(f"batting_team == '{team}'")
        .groupby(by = 'batter', as_index = False)
        .agg(
            Matches = ('match_id', 'nunique'),
            Runs = ('batsman_runs', 'sum'),
            Balls = ('batsman_runs', 'count')
        )
        .merge(
            deliveries
            .query(f"batting_team == '{team}'")
            .groupby(by = 'player_dismissed', as_index = False)
            .agg(
                Dismissals = ('is_wicket', 'sum')
            ), left_on = 'batter', right_on = 'player_dismissed', how = 'outer'
        )
        .drop(columns = ['player_dismissed'])
        .fillna(0)
        .assign(
            Strike_Rate = lambda df_: round((df_['Runs']/df_['Balls'])*100,4),
            Matches = lambda df_: df_['Matches'].astype('int'),
            Runs = lambda df_: df_['Runs'].astype('int'),
            Balls = lambda df_: df_['Balls'].astype('int'),
            Dismissals = lambda df_: df_['Dismissals'].astype('int'),
            NotOuts = lambda df_: df_['Matches'] - df_['Dismissals'],
            BattingAverage = lambda df_: round(df_['Runs']/df_['Dismissals'], 4)
        )
        .sort_values(by = 'Runs', ascending = False, ignore_index = True)
        .rename(columns = {'batter': 'Batsman', 'Strike_Rate': 'Strike Rate',
                           'NotOuts': 'Not Outs', 'BattingAverage': 'Batting Average'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.2.3. Bowler Performance
def team_bowler_performance(team):
    return (
        player_analysis.bowler_stats_overall
        .query(f"bowling_team == '{team}'")
        .groupby(by = 'bowler', as_index = False)
        .agg(
            matches = ('id', 'nunique'),
            wickets = ('wickets', 'sum'),
            balls = ('balls', 'sum'),
            runs_conceded = ('runs_conceded', 'sum'),
            count_six_conceded = ('count_six_conceded', 'sum'),
            count_four_conceded = ('count_four_conceded', 'sum'),
            count_three_conceded = ('count_three_conceded', 'sum'),
            count_two_conceded = ('count_two_conceded', 'sum'),
            count_one_conceded = ('count_one_conceded', 'sum'),
            count_extra_runs = ('count_extra_runs', 'sum'),
            dot_balls = ('dot_balls', 'sum')
        )
        .sort_values(by = 'wickets', ascending = False, ignore_index = True)
        .assign(
            overs = lambda df_: round(df_['balls']/6, 4),
            bowling_average = lambda df_: round(df_['runs_conceded']/df_['wickets'], 2),
            strike_rate = lambda df_: round(df_['balls']/df_['wickets'],2),
            boundary_rate = lambda df_: round((df_['count_six_conceded'] + df_['count_four_conceded'])*100/df_['balls'],2),
            dot_ball_percent = lambda df_: round((df_['dot_balls']/df_['balls'])*100, 4),
            economy_rate = lambda df_: round(df_['runs_conceded']/df_['overs'], 4),
        )
        .rename(columns = {'matches': 'Matches', 'wickets': 'Wickets', 'balls': 'Balls', 'runs_conceded': 'Runs Conceded', 
                           'count_six_conceded': '6s Conceded', 'count_four_conceded': '4s Conceded', 
                           'count_three_conceded': '3s Conceded', 'count_two_conceded': '2s Conceded', 
                           'count_one_conceded': '1s Conceded', 'count_extra_runs': 'Extra Runs',
                           'dot_balls':'Dot Balls', 'bowling_average': 'Bowling Average', 'strike_rate': 'Strike Rate',
                           'economy_rate': 'Economy Rate', 'boundary_rate': 'Boundary %', 'dot_ball_percent': 'Dot Ball %',
                           'bowler': 'Bowler', 'overs': 'Overs'})
    )

bowler_dismissal_type = ['caught', 'caught and bowled', 'bowled', 'lbw', 'stumped', 'hit wicket']

def leading_wicket_taker(team_name, seasons='All'):
    df_team = extract_team(team_name).query(f"(bowling_team == '{team_name}' & is_wicket == 1) & (dismissal_kind in @bowler_dismissal_type)")

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return (
        df_filtered
        .groupby(by = 'bowler', as_index = False)
        .agg(Wickets = ('is_wicket', 'sum'))
        .sort_values(by = 'Wickets', ascending = False, ignore_index = True)
        .rename(columns = {'bowler': 'Bowler'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.3. Rival Teams
#### 2.3.1. Matches by Rivals & Win %
def team_swap(row, team_name):
    if row['team2'] == team_name:
        row['team2'] = row['team1']
    return row

def team_record(team_name, seasons = 'All'):
        if seasons == 'All':
            df = matches.query(f"team1 == '{team_name}' or team2 == '{team_name}'")
        elif isinstance(seasons, list):
            df = matches.query("(team1 == @team_name or team2 == @team_name) and season in @seasons")
        else:
            df = matches.query(f"(team1 == '{team_name}' or team2 == '{team_name}') and season == '{seasons}'")
    
        return (
            df
            .query(f"team1 == '{team_name}' or team2 == '{team_name}'")
            .groupby(by = ['team1', 'team2', 'match_type', 'winner'], as_index = False)
            .agg(count = ('id', 'nunique'))
            .apply(lambda row: team_swap(row, team_name), axis=1)
            .assign(team1 = team_name)
        )

def team_rival_matches(team_name, seasons = 'All'):
    df = (
        team_record(team_name, seasons = seasons)
        .groupby(by = ['team1', 'team2'], as_index = False)
        .agg(num_matches = ('count', 'sum'))
        .sort_values(by = 'team2', ignore_index = True)
        .merge(
            (team_record(team_name, seasons = seasons)
             .groupby(by = ['team1', 'team2', 'winner'], as_index = False)
             .agg(matches_won = ('count', 'sum'))
             .sort_values(by = 'team2')
             .query(f"winner == '{team_name}'")),
            on = ['team1', 'team2'], how = 'outer'
        )
        .fillna(0)
        .assign(
            matches_won = lambda df_: df_['matches_won'].fillna(0).astype('int'),
            win_percent = lambda df_: round((df_['matches_won']/df_['num_matches'])*100,2)
            )
        .drop(columns = ['winner'])
        .sort_values(by = 'win_percent', ascending = False, ignore_index = True)
        .rename(columns = {'team1': 'Team', 'team2': 'Rival', 'num_matches': 'Total Matches',
                           'matches_won': 'Matches Won', 'win_percent': 'Win %'})
    )
    df.index = range(1, len(df)+1)
    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.3.2. Matches by Match Type for Rivals & Win %
def team_rival_matchtype(team_name, rival, seasons = 'All'):
    df = (
        team_record(team_name, seasons = seasons)
        .groupby(by = ['team1', 'team2', 'match_type'], as_index = False)
        .agg(matches_played = ('count', 'sum'))
        .merge(
            team_record(team_name, seasons = seasons)
            .query(f"winner == '{team_name}'")
            .groupby(by = ['team1', 'team2', 'match_type'], as_index = False)
            .agg(matches_won = ('count', 'sum')),
            on = ['team1', 'team2', 'match_type'], how = 'outer'
        )
        .assign(
            matches_won = lambda df_: df_['matches_won'].fillna(0).astype('int'),
            win_percent = lambda df_: round((df_['matches_won']/df_['matches_played'])*100,2)
            )
        .query(f"team2 == '{rival}'")
        .fillna(0)
        .rename(columns = {'team1': 'Team', 'team2': 'Rival', 'match_type': ' Match Type',
                           'matches_played': 'Matches Played', 'matches_won': 'Matches Won', 'win_percent': 'Win %'})
    )
    df.index = range(1, len(df)+1)
    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.3.3. Performance against Rivals - Summary
def team_rival_performance(team_name, rival, seasons = 'all'):
    df = (
        team(team_name, seasons = seasons)
        .query(f"team1 == '{rival}' or team2 == '{rival}'")
        .groupby(by = ['season', 'match_type', 'toss_winner', 'toss_decision',
                       'target_runs', 'winner', 'result_margin', 'result'], as_index = False)
        .agg(Matches = ('id', 'nunique'))
        .assign(
            target_runs = lambda df_: df_['target_runs'].astype('int'),
            result_margin = lambda df_: df_['result_margin'].astype('int')
        )
        .rename(columns = {'season': 'Season', 'match_type': 'Match Type', 'toss_winner': 'Toss',
                           'toss_decision': 'Toss Decision', 'target_runs': 'Target Runs', 'winner': 'Winner', 
                           'result_margin': 'Result Margin', 'result': 'Result'})
    )
    df.index = range(1, len(df)+1)
    return df
# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
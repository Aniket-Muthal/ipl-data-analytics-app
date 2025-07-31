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
## 1. Key-Highlights
### 1.1. Total Matches
def season_total_matches(seasons = 'All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    total_matches = df_filtered['id'].nunique()

    return total_matches

# ------------------------------------------------------------------------------------------------------------------------------------------
### 1.2. Total Matches by Match Type
def season_match_type(seasons = 'All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return (
        df_filtered
        .groupby(by = ['match_type'], as_index = False)
        .agg(Matches = ('id', 'nunique'))
        .sort_values(by = 'Matches', ascending = False, ignore_index = True)
        .rename(columns = {'match_type': 'Match Type'})  
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
### 1.3. Participating Teams
def season_teams(seasons = 'All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    teams = list(set(list(df_filtered['team1'].unique()) + list(df_filtered['team2'].unique())))
    teams_df = pd.DataFrame(teams, columns = ['Team'])
    teams_df = teams_df.sort_values(by = 'Team')
    teams_df.index = range(1, len(teams_df)+1)
    return teams_df

# ------------------------------------------------------------------------------------------------------------------------------------------
## 1.4.1. Metrics I - SunBurst Chart
def season_highlights_general(seasons = 'All'):
    if seasons == 'All':  
        df_filtered = df_all1
    elif isinstance(seasons, list):
        df_filtered = df_all1.query("season == @seasons")
    else:
        df_filtered = df_all1.query(f"season == '{seasons}'")

    total_matches1 =  df_filtered['id'].nunique()
    cities1 = df_filtered['city'].nunique()
    venues1 = df_filtered['venue'].nunique()

    return total_matches1, cities1, venues1

def season_highlights_batsman(seasons='All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

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

def season_highlights_bowler(seasons='All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

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
## 1.4.2. Metrics II - Metrics Display

### 1.4.2.1. Player of Match
def pom(seasons = 'All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")
    
    return (
        df_filtered
        .groupby(by = 'player_of_match', as_index = False)
        .agg(Count = ('id', 'nunique'))
        .sort_values(by = 'Count', ascending = False, ignore_index = True)
        .rename(columns = {'player_of_match': 'Player of Match'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
### 1.4.2.2. Leading Run Scorer
def leading_run_scorer(seasons='All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return (
        df_filtered
        .groupby(by = 'batter', as_index = False)
        .agg(Runs = ('batsman_runs', 'sum'))
        .sort_values(by = 'Runs', ascending = False, ignore_index = True)
        .rename(columns = {'batter': 'Batsman'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
### 1.4.2.3. Leading Wicket Taker
bowler_dismissal_type = ['caught', 'caught and bowled', 'bowled', 'lbw', 'stumped', 'hit wicket']

def leading_wicket_taker(seasons='All'):
    df_team = df_all1.query(f"dismissal_kind in @bowler_dismissal_type")

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
### 1.4.2.4. Highest Team Score
def individual_team_score(seasons='All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return (
        df_filtered
        .groupby(by = ['id','batting_team','season'], as_index = False)
        .agg(Runs = ('total_runs', 'sum'))
        .sort_values(by = 'Runs', ascending = False, ignore_index = True)
        .rename(columns = {'id': 'Match', 'batting_team': 'Batting Team', 'season': 'Season'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
### 1.4.2.5. Individual Highest Score
def individual_score(seasons='All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return (
        df_filtered
        .groupby(by = ['id', 'batter'], as_index = False)
        .agg(Runs = ('batsman_runs', 'sum'))
        .sort_values(by = 'Runs', ascending = False, ignore_index = True)
        .rename(columns = {'batter': 'Batsman'})
        .drop(columns = ['id'])
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
### 1.4.2.6. Best Bowling Figures
bowler_dismissal_type = ['caught', 'caught and bowled', 'bowled', 'lbw', 'stumped', 'hit wicket']

def best_bowling_figure(seasons = 'All'):
    df_team1 = df_all1.query(f"dismissal_kind in @bowler_dismissal_type")
    df_team2 = df_all1.query("is_wicket == 0")
    
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
        .groupby(by = ['id', 'season', 'bowler'], as_index = False)
        .agg(Wickets = ('is_wicket', 'sum'))
        .merge(
            (
                df_filtered2
                .groupby(by = ['id', 'season', 'bowler'], as_index = False)
                .agg(Runs = ('total_runs', 'sum'))
            ),
            on = ['id', 'season', 'bowler']
        )
        .sort_values(by = ['Wickets', 'Runs'], ascending = [False, True], ignore_index = True)
        .rename(columns = {'id': 'Match ID', 'bowler': 'Bowler', 'season': 'Season'})    
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
### 1.4.2.7. Most Boundaries, Sixes & Fours
def boundaries(boundary = None, seasons = 'All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

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
### 1.4.2.8. Most Catches
fielding = ['caught', 'caught and bowled']
def catches(seasons = 'All'):
    df_team1 = df_all1.query("dismissal_kind == 'caught'")
    df_team2 = df_all1.query("dismissal_kind == 'caught and bowled'")
    
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
### 1.4.2.9. Most Stumpings
def stumpings(seasons = 'All'):
    df_team = df_all1.query("dismissal_kind == 'stumped'")

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
### 1.4.2.10. Most Run Outs
def runouts(seasons = 'All'):
    df_team = df_all1.query("dismissal_kind == 'run out'")

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

### 2.1. General Analysis
#### 2.1.1. Inning-wise Average Score
def season_avg_score(seasons = 'All', inning = None):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return(
        df_filtered
        .query("result != 'no result'")
        .groupby(by = ['season', 'id', 'inning'], as_index = False)
        .agg(score = ('total_runs', 'sum'))
        .query(f"inning == {inning}")
        .groupby(by = 'season', as_index = False)
        .agg(avg_runs = ('score', 'mean'))
        .rename(columns = {'season': 'Season', 'avg_runs': 'Average Score'})   
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.1.2. Inning-wise Distribution of Score
def season_avg_score_boxplot(seasons = 'All', inning = None):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return(
        df_filtered
        .query("result != 'no result'")
        .groupby(by = ['season', 'id', 'inning'], as_index = False)
        .agg(score = ('total_runs', 'sum'))
        .query(f"inning == {inning}")
        .groupby(by = ['season', 'id'], as_index = False)
        .agg(avg_runs = ('score', 'mean'))
        .assign(avg_runs = lambda df_: df_['avg_runs'].astype('int'))
        .rename(columns = {'season': 'Season', 'id': 'Match ID', 'avg_runs': 'Score'})  
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.2. Toss Analysis
#### 2.2.1. Distribution of Toss Decision
def toss_decision(seasons = 'All'):
    df_team = (
        matches.query("result != 'No Result'")
        .groupby(by = ['season', 'toss_decision'], as_index = False)
        .agg(Count = ('toss_decision', 'count'))
    )

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return(
        df_filtered
        .rename(columns = {'season': 'Season', 'toss_decision': 'Toss Decision', 'count': 'Count'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.2.2. Impact of Toss Decision on Outcome
def toss_decision_impact(seasons = 'All'):
    df_team = matches.query("winner != 'No Result'")

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    df_toss_decision_impact = (
        df_filtered
        .assign(toss_match=lambda df_: (df_['toss_winner'] == df_['winner']).astype('int'))
        .groupby(by=['season', 'toss_decision'], as_index=False)
        .agg(toss_won_match_won=('toss_match', 'sum'))
        .merge(
            df_filtered
            .assign(toss_match=lambda df_: (df_['toss_winner'] != df_['winner']).astype('int'))
            .groupby(by=['season', 'toss_decision'], as_index=False)
            .agg(toss_won_match_lost=('toss_match', 'sum')),
            on=['season', 'toss_decision']
        )
        .merge(
            df_filtered[['season', 'toss_decision']].value_counts().reset_index().sort_values(by=['season', 'toss_decision']),
            on=['season', 'toss_decision']
        )
    )

    return df_toss_decision_impact

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.2.3. Venue-based Toss Impact on Outcome
def venue_toss_impact(seasons = 'All'):
    df_team = matches.query("winner != 'No Result'")
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    df = (
        df_filtered
        .assign(toss_match_won = lambda x: (x['toss_winner'] == x['winner']).astype('int'))
        .groupby(by = ['city'], as_index = False)
        .agg(toss_match_won = ('toss_match_won', 'sum'))
        .merge(
            df_filtered
            .groupby(by = ['city'], as_index = False)
            .agg(total_matches = ('id', 'nunique')), on = ['city']
        )
        .assign(win_percent = lambda x: round((x['toss_match_won']/x['total_matches'])*100,2))
        .rename(columns = {'city': 'City', 'toss_match_won': 'Won Toss & Match', 
                           'total_matches': 'Total Matches', 'win_percent': 'Win %'})
    )
    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.2.4. Venue-based Toss Decision Impact
def venue_toss_decision_impact(seasons = 'All'):
    df_team = matches.query("winner != 'No Result'")
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    df = (
        df_filtered
        .assign(toss_match_won = lambda x: (x['toss_winner'] == x['winner']).astype('int'))
        .groupby(by = ['city', 'toss_decision'], as_index = False)
        .agg(toss_match_won = ('toss_match_won', 'sum'))
        .merge(
            df_filtered
            .groupby(by = ['city', 'toss_decision'], as_index = False)
            .agg(total_matches = ('id', 'nunique')), on = ['city','toss_decision']
        )
        .assign(win_percent = lambda x: round((x['toss_match_won']/x['total_matches'])*100,2))
        .rename(columns = {'city': 'City', 'toss_decision': 'Toss Decision', 'toss_match_won': 'Won Toss & Match', 
                           'total_matches': 'Total Matches', 'win_percent': 'Win %'})
    )
    df.index = range(1, len(df)+1)

    return df
# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.3. Top Stats
#### 2.3.1. Team
def top_team_scores(seasons = 'All'):
    df_team = df_all1
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    df = (
        df_filtered
        .groupby(by = ['season', 'id', 'batting_team'], as_index = False)
        .agg(Score = ('total_runs', 'sum'))
        .sort_values(by = 'Score', ascending = False, ignore_index = True)
        .rename(columns = {'season': 'Season', 'id': ' Match ID', 'batting_team': 'Team'})
    )

    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
##### 2.3.1.2. 200+ Scores
def top_team_200_plus_scores(seasons = 'All'):
    df_team = df_all1
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    df = (
        df_filtered
        .groupby(by = ['season', 'id', 'batting_team'], as_index = False)
        .agg(Score = ('total_runs', 'sum'))
        .sort_values(by = 'Score', ascending = False, ignore_index = True)
        .rename(columns = {'season': 'Season', 'id': ' Match ID', 'batting_team': 'Team'})
        .query("Score >= 200")
        .groupby(by = ['Season', 'Team'], as_index = False)
        .agg(Count = ('Team', 'count'))
        .sort_values(by = 'Count', ascending = False, ignore_index = True)
    )

    return df

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.3.1.3. Top Teams with Most Centuries
def top_team_centuries(seasons = 'All'):
    df_team = df_all1
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")
    return (
        df_filtered
        .groupby(by = ['season', 'id', 'batting_team', 'batter'], as_index = False)
        .agg(score = ('batsman_runs', 'sum'))
        .query("score >= 100")
        .groupby(by = ['season', 'batting_team'], as_index = False)
        .agg(Count = ('batting_team', 'count'))
        .rename(columns = {'season': 'Season', 'batting_team': 'Team'})
        .sort_values(by = ['Season'], ignore_index = True)
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.3.1.4. Top Teams with Most Half Centuries
def top_team_half_centuries(seasons = 'All'):
    df_team = df_all1
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")
    return (
        df_filtered
        .groupby(by = ['season', 'id', 'batting_team', 'batter'], as_index = False)
        .agg(score = ('batsman_runs', 'sum'))
        .query("score >= 50 & score < 100")
        .groupby(by = ['season', 'batting_team'], as_index = False)
        .agg(Count = ('batting_team', 'count'))
        .rename(columns = {'season': 'Season', 'batting_team': 'Team'})
        .sort_values(by = ['Season'], ignore_index = True)
    )
# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.3.2. Batsman
#### 2.3.2.1. Leading Scorer
def top_leading_run_scorer(seasons = 'All'):
    df_team = df_all1
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return(
        df_filtered
        .groupby(by = ['batter'], as_index = False)
        .agg(Runs = ('batsman_runs', 'sum'))
        .sort_values(by = ['Runs'], ascending = False, ignore_index = True)
        .rename(columns = {'batter': 'Batsman'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.3.2.2. Highest Individual Score
def top_individual_score(seasons = 'All'):
    df_team = df_all1
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    return(
        df_filtered
        .groupby(by = ['id', 'batter'], as_index = False)
        .agg(Runs = ('batsman_runs', 'sum'))
        .sort_values(by = 'Runs', ascending = False, ignore_index = True)
        .rename(columns = {'batter': 'Batsman'})
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.3.2.3. Top Centuries Count
def top_batsman_centuries(seasons = 'All'):
    df_team = df_all1
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")
    return (
        df_filtered
        .groupby(by = ['season', 'id', 'batting_team', 'batter'], as_index = False)
        .agg(score = ('batsman_runs', 'sum'))
        .query("score >= 100")
        .groupby(by = ['season', 'batter'], as_index = False)
        .agg(Count = ('batter', 'count'))
        .rename(columns = {'season': 'Season', 'batter': 'Batsman'})
        .sort_values(by = ['Season'], ignore_index = True)
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.3.2.4. Top Half Centuries Count
def top_batsman_half_centuries(seasons = 'All'):
    df_team = df_all1
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")
    return (
        df_filtered
        .groupby(by = ['season', 'id', 'batting_team', 'batter'], as_index = False)
        .agg(score = ('batsman_runs', 'sum'))
        .query("score >= 50 & score < 100")
        .groupby(by = ['batter'], as_index = False)
        .agg(Count = ('batter', 'count'))
        .rename(columns = {'batter': 'Batsman'})
        .sort_values(by = ['Count'], ascending = False, ignore_index = True)
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
#### 2.3.2.5. Top Most Boundaries
def top_batsman_sixes(seasons = 'All'):
    df_team = df_all1
    
    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")
    return (
        df_filtered
        .query("batsman_runs == 6 or batsman_runs == 4")
        .groupby(by = ['season', 'batting_team', 'batter'], as_index = False)
        .agg(Boundaries = ('batsman_runs', 'count'))
        .rename(columns = {'season': 'Season', 'batter': 'Batsman',
                           'batting_team': 'Team'})
        .sort_values(by = ['Season'], ignore_index = True)
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
### 2.3.3. Bowler
#### 2.3.3.1. Leading Wicket Taker
def season_highlights_bowler_new(seasons='All'):
    df_team = df_all1

    if seasons == 'All':
        df_filtered = df_team
    elif isinstance(seasons, list):
        df_filtered = df_team.query("season in @seasons")
    else:
        df_filtered = df_team.query(f"season == '{seasons}'")

    bowler_count = df_filtered['bowler'].nunique()
    balls = df_filtered.shape[0]
    wickets = df_filtered.query("is_wicket == 1").shape[0]

    bowler_dismissal_type = ['caught', 'caught and bowled', 'bowled', 'lbw', 'stumped']
    
    four_wickets = (
        df_filtered.query("is_wicket == 1 and dismissal_kind in @bowler_dismissal_type")
        .groupby(['id', 'bowler'], as_index = False)
        .agg(wickets=('is_wicket', 'sum'))
        .query("wickets == 4")
        .rename(columns = {'id': 'Match ID', 'bowler': 'Bowler', 'wickets': 'Wickets'})
    )

    five_plus_wickets = (
        df_filtered.query("is_wicket == 1 and dismissal_kind in @bowler_dismissal_type")
        .groupby(['id', 'bowler'], as_index = False)
        .agg(wickets=('is_wicket', 'sum'))
        .query("wickets >= 5")
        .rename(columns = {'id': 'Match ID', 'bowler': 'Bowler', 'wickets': 'Wickets'})
    )

    return four_wickets, five_plus_wickets
# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
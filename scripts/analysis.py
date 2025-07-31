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
# 1. Total IPL Seasons
total_seasons = matches['season'].nunique()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 2. Season, Months and Duration of IPL
matches['date'] = pd.to_datetime(matches['date'])

matches = matches.assign(
    month=lambda df_: df_['date'].dt.month,
    monthname=lambda df_: df_['date'].dt.month_name()
)

duration_df = (
    matches
    .assign(
        monthname = lambda df_: df_['date'].dt.month_name()
    )
    .groupby(by = ['season'], as_index = False)
    .agg(
        Months = ('monthname', lambda x: ', '.join(x.unique())),
        Duration = ('monthname', 'nunique')
    )
    .rename(columns = {'season': 'Season'})
)
duration_df.index = range(1, len(duration_df)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 3. Total IPL Matches
total_matches = matches['id'].nunique()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 4. Total IPL Matches by Type
match_by_type = (
    matches
    .groupby(by = 'match_type', as_index = False)
    .agg(
        match_count = ('id', 'count')
    )
    .sort_values(by = 'match_count', ascending = False, ignore_index = True)
    .rename(columns = {'match_count': 'Match Count', 'match_type': 'Match Type'})
)
match_by_type.index = range(1, len(match_by_type)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 5. Total Teams Participated So Far
total_teams = pd.DataFrame(matches['team1'].unique(), columns = ['Team'])
total_teams = total_teams.sort_values(by = 'Team')
total_teams.index = range(1, len(total_teams)+1)

count_teams = matches['team1'].nunique()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 6. Total Super-Overs
total_superovers = matches[matches['super_over'] == 'Y'].shape[0]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 7. Total Venues (Stadiums)
total_venues = matches['venue'].nunique()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 8. Total Venues (Cities)
total_cities = matches['city'].nunique()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 9. Total Batsmans Who Batted in IPL
total_batsman1 = list(deliveries['batter'].unique())
total_batsman2 = list(deliveries['non_striker'].unique())

total_batsman_list = sorted(list(set(total_batsman1 + total_batsman2)))
total_batsman = len(total_batsman_list)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 10. Total Runs in IPL
total_runs = deliveries['total_runs'].sum()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 11. Total Batsman Runs in IPL
total_batsman_runs = deliveries['batsman_runs'].sum()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 12. Total Extra Runs in IPL
total_extra_runs = deliveries['extra_runs'].sum()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 13. Total Sixes
total_sixes = deliveries[deliveries['batsman_runs'] == 6].shape[0]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 14. Total Fours
total_fours = deliveries[deliveries['batsman_runs'] == 4].shape[0]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 15. Highest Individual Score
individual_match_scores = (
    deliveries
    .groupby(by = ['match_id', 'batter'], as_index = False)
    .agg(
        runs = ('batsman_runs', 'sum')
    )
    .sort_values(by = 'runs', ascending = False, ignore_index = True)
    .drop(columns = ['match_id'])
)
individual_match_scores.index = range(1, len(individual_match_scores)+1)
scorer_match = individual_match_scores[['batter', 'runs']].head(1).values[0,0]
runs_match = individual_match_scores[['batter', 'runs']].head(1).values[0,1]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 16. Total Centuries in IPL
centuries_df = (
    individual_match_scores
    .loc[individual_match_scores['runs'] >= 100]
    .reset_index(drop = True)
)
centuries_df.index = range(1, len(centuries_df)+1)
total_centuries = centuries_df.shape[0]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 17. Total Half Centuries
half_centuries_df = (
    individual_match_scores
    .loc[(individual_match_scores['runs'] >= 50) & (individual_match_scores['runs'] < 100)]
    .reset_index(drop = True)
)
half_centuries_df.index = range(1, len(half_centuries_df)+1)
total_half_centuries = half_centuries_df.shape[0]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 18. Total Bowlers Who Bowled in IPL
total_bowlers_list = sorted(deliveries['bowler'].unique())
total_bowlers = len(total_bowlers_list)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 19. Total Overs Bowled in IPL
total_balls = deliveries.shape[0]
total_overs = total_balls//6

# ------------------------------------------------------------------------------------------------------------------------------------------
# 20. Total Wickets in IPL
total_wickets = deliveries['is_wicket'].sum()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 21. Highest Team Score
team_scores = (
    deliveries
    .groupby(by = ['match_id', 'batting_team'], as_index = False)
    .agg(
        team_score = ('total_runs', 'sum')
    )
    .sort_values(by = 'team_score', ascending = False, ignore_index = True)
    .drop(columns = 'match_id')
    .rename(columns = {'batting_team': 'Batting Team', 'total_runs': 'Total Runs', 'team_score': 'Team Score'})
)
team_scores.index = range(1, len(team_scores)+1)
highest_team_score = team_scores['Team Score'].head(1).values[0]
highest_score_teamname = team_scores['Batting Team'].head(1).values[0]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 22. Leading Run Scorer
individual_scores = (
    deliveries
    .groupby(by = 'batter', as_index = False)
    .agg(
        runs = ('batsman_runs', 'sum')
    )
    .sort_values(by = 'runs', ascending = False, ignore_index = True)
    .rename(columns = {'batter': 'Batsman', 'runs': 'Runs'})
)
individual_scores.index = range(1, len(individual_scores)+1)
scorer = individual_scores[['Batsman', 'Runs']].head(1).values[0,0]
runs = individual_scores[['Batsman', 'Runs']].head(1).values[0,1]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 23. Leading Wicket-Taker
bowler_dismissal_type = ['bowled', 'lbw', 'stumped', 'caught and bowled', 'caught', 'hit wicket']

individual_wickets = (
    deliveries
    .loc[(deliveries['is_wicket'] == 1) & (deliveries['dismissal_kind'].isin(bowler_dismissal_type))]
    ['bowler']
    .value_counts()
    .reset_index(name = 'wickets')
)
individual_wickets.index = range(1, len(individual_wickets)+1)
bowler = individual_wickets.head(1).values[0,0]
wickets = individual_wickets.head(1).values[0,1]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 24. Leading Wicket-Taker in a Match
bowler_dismissal_type = ['bowled', 'lbw', 'stumped', 'caught and bowled', 'caught', 'hit wicket']

individual_match_wickets = (
    deliveries
    .loc[(deliveries['is_wicket'] == 1) & (deliveries['dismissal_kind'].isin(bowler_dismissal_type))]
    .groupby(by = ['match_id', 'bowler'], as_index = False)
    .agg(
        wickets = ('match_id', 'count')
    )
    .sort_values(by = 'wickets', ascending = False, ignore_index = True)
    .drop(columns = ['match_id'])
)
individual_match_wickets.index = range(1, len(individual_match_wickets)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 25. Bowler Stats
bowler_dismissal_type = ['bowled', 'lbw', 'stumped', 'caught and bowled', 'caught', 'hit wicket']

individual_wickets = (
    deliveries
    .loc[(deliveries['is_wicket'] == 1) & (deliveries['dismissal_kind'].isin(bowler_dismissal_type))]
    ['bowler']
    .value_counts()
    .reset_index(name = 'wickets')
)
individual_wickets.index = range(1, len(individual_wickets)+1)
individual_wickets

economy_rate = (
    deliveries
    .groupby(by = 'bowler', as_index = False)
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
economy_rate.index = range(1, len(economy_rate)+1)

bowler_stats1 = (
    pd.merge(left = economy_rate,
             right = individual_wickets,
             on = 'bowler',
             how = 'left')
).fillna(0)

bowler_stats1['wickets'] = bowler_stats1['wickets'].astype('int')

bowler_matches = (
    deliveries
    .groupby(by = 'bowler', as_index = False)
    .agg(
        matches = ('match_id', 'nunique')
    )
    .sort_values(by = 'matches', ascending = False, ignore_index = True)
)

dot_balls = (
    deliveries[deliveries['total_runs'] == 0]
    .groupby(by = 'bowler', as_index = False)
    .agg(
        dot_balls = ('total_runs', 'count')
    )
    .sort_values(by = 'dot_balls', ascending = False, ignore_index = True)
)

bowler_stats2 = pd.merge(left = bowler_stats1, right = bowler_matches, on = 'bowler', how = 'inner')
bowler_stats3 = pd.merge(left = bowler_stats2, right = dot_balls, on = 'bowler', how = 'left').fillna(0)
bowler_stats3['dot_balls'] = bowler_stats3['dot_balls'].astype('int')
bowler_stats3.sort_values(by = 'wickets', ascending = False, ignore_index = True)

def runs_type_conceded(run_type, str_run_type):
    return (
        deliveries
        .loc[deliveries['batsman_runs'] == run_type]
        .groupby('bowler', as_index=False)
        .agg(**{f'count_{str_run_type}_conceded': ('batsman_runs', 'count')}) 
    )

sixes_conceded_df = runs_type_conceded(run_type = 6, str_run_type = 'six')
fours_conceded_df = runs_type_conceded(run_type = 4, str_run_type = 'four')
threes_conceded_df = runs_type_conceded(run_type = 3, str_run_type = 'three')
twos_conceded_df = runs_type_conceded(run_type = 2, str_run_type = 'two')
ones_conceded_df = runs_type_conceded(run_type = 1, str_run_type = 'one')

bowler_extra_runs = (
    deliveries
    .loc[deliveries['extra_runs'] > 0]
    .groupby(by = ['bowler'], as_index = False)
    .agg(
        count_extra_runs = ('extra_runs', 'sum')
    )
)

bowler_stats = (
    bowler_stats3
    .merge(sixes_conceded_df, on = 'bowler', how = 'left')
    .merge(fours_conceded_df, on = 'bowler', how = 'left')
    .merge(threes_conceded_df, on = 'bowler', how = 'left')
    .merge(twos_conceded_df, on = 'bowler', how = 'left')
    .merge(ones_conceded_df, on = 'bowler', how = 'left')
    .merge(bowler_extra_runs, on = 'bowler', how = 'left')
)
bowler_stats = bowler_stats.fillna(0)
bowler_stats[['count_six_conceded', 'count_four_conceded',
              'count_three_conceded', 'count_two_conceded',
              'count_one_conceded', 'count_extra_runs']] = (
    bowler_stats[['count_six_conceded', 'count_four_conceded', 'count_three_conceded',
                  'count_two_conceded', 'count_one_conceded', 'count_extra_runs']].astype('int')
)

bowler_stats['dot_balls_percent'] = round((bowler_stats['dot_balls']/bowler_stats['balls'])*100,2)
bowler_stats.index = range(1, len(bowler_stats)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 26. Count of 4+ Wickets
bowler_dismissal_type = ['bowled', 'lbw', 'stumped', 'caught and bowled', 'caught', 'hit wicket']
four_wickets = (
    deliveries
    .query("is_wicket == 1 & dismissal_kind in @bowler_dismissal_type")
    .groupby(by =['match_id', 'bowler'], as_index = False)
    .agg(Wickets = ('is_wicket', 'sum'))
    .query('Wickets == 4')
    .sort_values(by = 'Wickets', ascending = False, ignore_index = True)
    .shape[0]
)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 27. Count of 5+ Wickets
five_plus_wickets = (
    deliveries
    .query("is_wicket == 1 & dismissal_kind in @bowler_dismissal_type")
    .groupby(by =['match_id', 'bowler'], as_index = False)
    .agg(Wickets = ('is_wicket', 'sum'))
    .query('Wickets >= 5')
    .sort_values(by = 'Wickets', ascending = False, ignore_index = True)
    .shape[0]
)

bowler_dismissal_type = ['bowled', 'lbw', 'stumped', 'caught and bowled', 'caught', 'hit wicket']
best_bowling_figure = (
    deliveries
    .query("is_wicket == 1 & dismissal_kind in @bowler_dismissal_type")
    .groupby(by = ['match_id', 'bowler'], as_index = False)
    .agg(wickets = ('is_wicket', 'sum'))
    .merge(
        (
        deliveries
        .query("is_wicket == 0")
        .groupby(by = ['match_id', 'bowler'])
        .agg(runs_conceded = ('total_runs', 'sum'))
        ),
        on = ['match_id', 'bowler']
    )
    .sort_values(by = ['wickets', 'runs_conceded'], ascending = [False, True])
    .rename(columns = {'bowler': 'Bowler', 'wickets': 'Wickets', 'runs_conceded': 'Runs Conceded'})
)
best_fig_wickets = best_bowling_figure.head(1)['Wickets'].values[0]
best_fig_runs= best_bowling_figure.head(1)['Runs Conceded'].values[0]
best_fig_bowler = best_bowling_figure.head(1)['Bowler'].values[0]

player_of_match  = matches['player_of_match'].value_counts().reset_index().head(1)['player_of_match'][0]
pom_count  = matches['player_of_match'].value_counts().reset_index().head(1)['count'][0]

boundary_count = (
    deliveries
    .query("batsman_runs == 6 or batsman_runs == 4")
    .groupby(by = ['batter'], as_index = False)
    .agg(boundaries = ('batsman_runs', 'count'))
    .sort_values(by = 'boundaries', ascending = False, ignore_index = True)
    .head(1)    
)
boundary_batsman = boundary_count['batter'].values[0]
boundary_numbers = boundary_count['boundaries'].values[0]

sixes_count = (
    deliveries
    .query("batsman_runs == 6")
    .groupby(by = ['batter'], as_index = False)
    .agg(sixes = ('batsman_runs', 'count'))
    .sort_values(by = 'sixes', ascending = False, ignore_index = True)
    .head(1)    
)
sixes_batsman = sixes_count['batter'].values[0]
sixes_numbers = sixes_count['sixes'].values[0]

fours_count = (
    deliveries
    .query("batsman_runs == 4")
    .groupby(by = ['batter'], as_index = False)
    .agg(fours = ('batsman_runs', 'count'))
    .sort_values(by = 'fours', ascending = False, ignore_index = True)
    .head(1)    
)
fours_batsman = fours_count['batter'].values[0]
fours_numbers = fours_count['fours'].values[0]

dismissal_type = ['caught', 'caught and bowled']
most_catches_df = (
    deliveries
    .query("dismissal_kind == 'caught'")['fielder'].value_counts().reset_index()
    .merge(
        deliveries.query("dismissal_kind == 'caught and bowled'")['bowler'].value_counts().reset_index(),
        left_on = 'fielder', right_on = 'bowler', how = 'outer'
    )
    .assign(
        count_x = lambda df_: df_['count_x'].fillna(0),
        count_y = lambda df_: df_['count_y'].fillna(0),
        count = lambda df_: (df_['count_x'] + df_['count_y']).astype('int'),
        fielder = lambda df_: df_['fielder'].fillna(df_['bowler']),
        bowler = lambda df_: df_['bowler'].fillna(df_['fielder'])
    )
    .drop(columns = ['count_x', 'count_y', 'bowler'])
    .sort_values(by = 'count', ascending = False)
    .rename(columns = {'fielder': 'Fielder', 'count': 'Catches'})
)
most_catches_fielder = most_catches_df['Fielder'].head(1).values[0]
most_catches = most_catches_df['Catches'].head(1).values[0]

most_stumpings_df = (
    deliveries
    .query("dismissal_kind == 'stumped'")
    ['fielder'].value_counts().reset_index()
    .rename(columns = {'fielder': 'Fielder', 'count': 'Stumpings'})
)

most_stump_fielder = most_stumpings_df['Fielder'].head(1).values[0]
most_stumpings = most_stumpings_df['Stumpings'].head(1).values[0]

most_runouts_df = (
    deliveries
    .query("dismissal_kind == 'run out'")
    ['fielder'].value_counts().reset_index()
    .rename(columns = {'fielder': 'Fielder', 'count': 'Run Outs'})
)
most_runouts_fielder = most_runouts_df['Fielder'].values[0]
most_runouts = most_runouts_df['Run Outs'].values[0]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 28. Team-wise IPL Titles
finals_df = matches[matches['match_type'] == 'Final']
team_wins = finals_df.groupby("winner")["season"].apply(lambda x: ", ".join(map(str, x))).reset_index()
team_wins.columns = ["Team", "Winning Seasons"]
team_wins["Trophies"] = team_wins["Winning Seasons"].apply(lambda x: len(x.split(", ")))
team_wins = team_wins.sort_values(by = 'Trophies', ascending = False, ignore_index = True)
team_wins.index = range(1, len(team_wins)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 29. Venue-Wise Total Matches
venue_matches = (
    matches['city']
    .value_counts()
    .reset_index(name = 'Total Matches')
    .rename(columns = {'city': 'City'})
    )
venue_matches.index = range(1, len(venue_matches)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 30. Match Type vs Venue
def venue_match_type(match_type):
    venue_match_type = (
        matches[['city', 'match_type']]
        .value_counts()
        .reset_index(name = 'Total Matches')
        .rename(columns = {'city': 'City', 'match_type': 'Match Type'})
    )
    return venue_match_type[venue_match_type['Match Type'] == match_type]
            
# ------------------------------------------------------------------------------------------------------------------------------------------
# 31. City_wise Count of Stadiums
city_stadium_count = (
    matches
    .groupby(by = 'city', as_index = False)
    .agg(
        stadium=('venue', lambda x: '| '.join(sorted(set(x)))),
        count_stadium = ('venue', 'nunique')
    )
    .sort_values(by = 'count_stadium', ascending = False, ignore_index = True)
    .rename(columns = {'city': 'City', 'stadium': 'Stadium', 'count_stadium': 'Total Number of Stadiums'})
)
city_stadium_count.index = range(1, len(city_stadium_count)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 32. Impact of Toss on Outcome
matches["toss_won_and_won_match"] = matches["toss_winner"] == matches["winner"]
label_map = {True: "Won Toss & Match", False: "Lost After Winning Toss"}
matches['toss_won_and_won_match'] = matches['toss_won_and_won_match'].map(label_map)
toss_impact = matches["toss_won_and_won_match"].value_counts().reset_index()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 33. Distribution of Toss
toss_decision = matches['toss_decision'].value_counts().reset_index()
Field = toss_decision.iloc[:1].values[0,1]
Bat = toss_decision.iloc[1:].values[0,1]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 34. Impact of Toss Decision on Outcome
toss_impact_df = (
                    matches
                    .groupby(by = ['toss_decision', 'result'])
                    .agg(
                        Count = ('id', 'count')
                    )
                    .reset_index()
                )

conditions = [
       ((toss_impact_df["toss_decision"] == "bat") & (toss_impact_df["result"] == "runs")) |
       ((toss_impact_df["toss_decision"] == "field") & (toss_impact_df["result"] == "wickets")),
       
       ((toss_impact_df["toss_decision"] == "bat") & (toss_impact_df["result"] == "wickets")) |
       ((toss_impact_df["toss_decision"] == "field") & (toss_impact_df["result"] == "runs")),
                    
       (toss_impact_df["result"] == "no result"),
       (toss_impact_df["result"] == "tie")
]

outcomes = ["Won", "Lost", "No Result", "Tie"]
toss_impact_df["Outcome"] = np.select(conditions, outcomes, default="unknown")

# ------------------------------------------------------------------------------------------------------------------------------------------
# 35. Impact of Toss Decision on Outcome - Field & Bat
data = {
       'Outcome': ['Lost', 'No Result', 'Tie', 'Won'],
       'Bat': [207, 1, 6, 177],
       'Field': [321, 4, 8, 371]
}

df = pd.DataFrame(data)
df_bat = df[['Outcome', 'Bat']].rename(columns={'Bat': 'Count'})
df_field = df[['Outcome', 'Field']].rename(columns={'Field': 'Count'})

# ------------------------------------------------------------------------------------------------------------------------------------------
# 36. Count of Matches Won Given Toss Won Across Cities
matches["toss_won_and_won_match"] = matches["toss_winner"] == matches["winner"]
match_won_toss_won_across_city = (
    matches
    .groupby('city')
    .agg(count=('toss_won_and_won_match', 'sum'))
    .reset_index()
    .sort_values(by='count', ascending=False)
)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 37. Impact of Toss on Match Wins Across Citis - Success Rate
venue_toss_wins = (
       matches
       .groupby(by = 'city')
       .agg(won_toss_and_match = ('toss_won_and_won_match', 'sum'))
       .sort_values(by = 'won_toss_and_match', ascending = False)
)

venue_matches_df = (
       matches
       .groupby(by = 'city')
       .agg(total_matches = ('id', 'count'))
       .sort_values(by = 'total_matches', ascending = False)
)

venue_toss_outcome = pd.merge(left = venue_matches_df, right = venue_toss_wins, how = 'inner', on = 'city')
venue_toss_outcome['success_rate'] = round((venue_toss_outcome['won_toss_and_match']/venue_toss_outcome['total_matches'])*100,2)
venue_toss_outcome = venue_toss_outcome.sort_values(by = 'success_rate', ascending = False)
venue_toss_outcome = venue_toss_outcome.reset_index()
venue_toss_outcome = venue_toss_outcome.rename(columns = {'city': 'City', 'total_matches': 'Total Matches',
                                                           'won_toss_and_match': 'Won Toss & Match', 'success_rate': 'Success Rate'})
venue_toss_outcome.index = range(1, len(venue_toss_outcome)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 38. Venue Based Toss Decision and Sucess Rate
venue_toss_decision = (
       matches
       .groupby(by = ['city', 'toss_decision'], as_index = False)
       .agg(
              matches_won = ('toss_won_and_won_match', 'sum'),
              total = ('toss_decision', 'count')
        )
        .assign(
               win_percent = lambda df_: (df_['matches_won']/df_['total'])*100
        )
        .rename(columns = {'city': 'City', 'toss_decision': 'Toss Decision',  "matches_won": 'Matches Won', 'total': 'Total', 'win_percent': 'Win (%)'})
)
venue_toss_decision.index = range(1, len(venue_toss_decision)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 39. Top N Team Scores
def top_n_team_scores(n_value):
 return team_scores.head(n_value)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 40. 200+ Team Scores
team_200_plus_scores = (
    team_scores
    .query("`Team Score` >= 200")
    .groupby(by = 'Batting Team')
    .size()
    .reset_index(name = 'Count of 200+ Scores')
)

df_team_names = pd.DataFrame(matches['team1'].unique(), columns = ['Batting Team'])

team_200_plus_scores = (
    df_team_names
    .merge(team_200_plus_scores, on = 'Batting Team', how = 'left')
    .fillna(0)
    .assign(**
        {'Count of 200+ Scores': lambda df_: df_['Count of 200+ Scores'].astype('int')}
    )
    .sort_values(by = 'Count of 200+ Scores', ascending = False, ignore_index = True)
)
team_200_plus_scores.index = range(1, len(team_200_plus_scores)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 41. Team-Wise 200+ Scores
def team_200_score(team_name):
    return (
        team_scores
        .query(f"(`Team Score` >= 200) & (`Batting Team` == '{team_name}')")
        [['Batting Team', 'Team Score']]
        .sort_values(by = ['Batting Team', 'Team Score'], ascending = [True, False], ignore_index = True)
    )

# ------------------------------------------------------------------------------------------------------------------------------------------
# 42. 200+ Scores - First Innings vs Second Innings
def innings(inning):
    return (
        deliveries[['match_id', 'inning', 'batting_team']]
        .merge(
            matches[['id', 'toss_winner', 'toss_decision', 'winner', 'target_runs']],
            left_on = 'match_id',
            right_on = 'id', 
            how = 'inner'
        )
        .drop(columns = ['id'])
        .drop_duplicates(keep = 'first')
        .query(f"inning == {inning}")
        .assign(
            toss_won = lambda df_: (df_['batting_team'] == df_['toss_winner']).astype('int'),
            match_won = lambda df_: (df_['batting_team'] == df_['winner']).astype('int')
        )
    )

first_inning = (
    innings(1)
    .assign(runs_scored = lambda df_: df_['target_runs'] - 1)
    .query("runs_scored >= 200")
    .groupby(by = ['batting_team', 'toss_won', 'match_won'], as_index = False)
    .agg(
        **{'count' : ('runs_scored', 'count')}
    )
    .rename(columns = {'batting_team': 'Batting Team', 'count': 'Count of 200+ Scores',
                       'toss_won': 'Toss Won', 'match_won': 'Match Won'})
)

second_inning_score = (
    deliveries[['match_id', 'inning', 'batting_team', 'total_runs']]
    .query("inning == 2")
    .groupby(by = ['match_id', 'batting_team'], as_index = False)
    .agg(
        runs_scored = ('total_runs', 'sum')
    )    
)

second_inning = (
    innings(2)
    .merge(
        second_inning_score,
        on = ['match_id', 'batting_team']
    )
    .query("runs_scored >= 200")
    .groupby(by = ['batting_team', 'toss_won', 'match_won'], as_index = False)
    .agg(
        **{'count' : ('runs_scored', 'count')}
    )
    .rename(columns = {'batting_team': 'Batting Team', 'count': 'Count of 200+ Scores',
                       'toss_won': 'Toss Won', 'match_won': 'Match Won'})
)

bat_first_200 = (
    first_inning
    .groupby(by = 'Batting Team')['Count of 200+ Scores']
    .sum()
    .reset_index()
)
bat_first_200.index = range(1, len(bat_first_200)+1)

field_first_200 = (
    second_inning
    .groupby(by = 'Batting Team')['Count of 200+ Scores']
    .sum()
    .reset_index()
)
field_first_200.index = range(1, len(field_first_200)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 43. Team-Wise 200+ Scores
team_scores_200 = (
    bat_first_200
    .merge(field_first_200, on = 'Batting Team')
    .rename(
        columns = {'Count of 200+ Scores_x': 'Count of 200+ Scores: Bat First',
                   'Count of 200+ Scores_y': 'Count of 200+ Scores: Field First'
                  }
           )
)
team_scores_200.index = range(1, len(team_scores_200)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 44. Win Percent for 200+ Scores
setting_target_200plus = (
    first_inning
    .groupby(by = ['Batting Team', 'Match Won'], as_index = False)
    .agg(
        **{
            'Winning Cause' : ('Count of 200+ Scores', 'sum'),
        }
    )
    .query("`Match Won` == 1")
    .merge(bat_first_200, on = 'Batting Team')
    .assign(
        Win_Percent =  lambda df_: round((df_['Winning Cause'] / df_['Count of 200+ Scores'])*100,2)
    )
    .drop(columns = ['Match Won'])
    .rename(columns = {'Win_Percent': 'Win Percent'})
    .sort_values(by = 'Win Percent', ascending = False, ignore_index = True)
)
setting_target_200plus.index = range(1, len(setting_target_200plus)+1)

chasing_target_200plus = (
    second_inning
    .groupby(by = ['Batting Team', 'Match Won'], as_index = False)
    .agg(
        **{
            'Winning Cause' : ('Count of 200+ Scores', 'sum'),
        }
    )
    .query("`Match Won` == 1")
    .merge(field_first_200, on = 'Batting Team')
    .assign(
        Win_Percent =  lambda df_: round((df_['Winning Cause'] / df_['Count of 200+ Scores'])*100,2)
    )
    .drop(columns = ['Match Won'])
    .rename(columns = {'Win_Percent': 'Win Percent'})
    .sort_values(by = 'Win Percent', ascending = False, ignore_index = True)
)
chasing_target_200plus.index = range(1, len(chasing_target_200plus)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# Batsman Stats - Overall
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
        Ducks = ('batsman_runs', lambda x: (x == 0).sum())
    )
)

batsman_striker_list = set(list(deliveries['batter'].unique()))
batsman_non_striker_list = set(list(deliveries['non_striker'].unique()))
non_striker_batter = list(batsman_non_striker_list - batsman_striker_list)
non_striker_batter = pd.DataFrame(non_striker_batter, columns = ['batter'])

dismissals_df = (
    deliveries
    .groupby(by = 'player_dismissed', as_index = False)
    .agg(
        dismissals = ('is_wicket', 'sum')
    )
)

innings_df = (
    deliveries
    .groupby(by = 'batter', as_index = False)
    .agg(
        innings = ('match_id', 'nunique')
    )
)

batsman_overall_df = (
    runs_df
    .merge(non_striker_batter, on  = 'batter', how = 'outer')
    .merge(dismissals_df, left_on = 'batter', right_on = 'player_dismissed', how = 'outer')
    .merge(innings_df, on = 'batter', how = 'outer')
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
    )
    .rename(columns = {'batter': 'Batsman', 'dismissals': 'Dismissals', 'innings': 'Innings',
                       'not_outs': 'Not Outs', 'strike_rate': 'Strike Rate', 'batting_average': 'Batting Average'})
    .drop(columns = 'player_dismissed')
)

batsman_overall_df = batsman_overall_df[['Batsman', 'Innings', 'Runs', 'Balls', 'Sixes', 'Fours', 'Threes', 'Twos', 'Ones', 'Ducks',
                                         'Not Outs', 'Dismissals', 'Strike Rate', 'Batting Average']]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 45. Top N Overall Batsman Scores
leading_scorers = batsman_overall_df.sort_values(by = 'Runs', ascending = False, ignore_index = True)
leading_scorers.index = range(1, len(leading_scorers)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 46. To N Individual Scores in a Match

# ------------------------------------------------------------------------------------------------------------------------------------------
# 47. Top N Overall Strike Rate (Minimum 10 Innings)
strike_rate_overall = (
    batsman_overall_df[['Batsman', 'Innings', 'Runs', 'Balls', 'Strike Rate']]
    .query("Innings >= 10")
    .sort_values(by = 'Strike Rate', ascending = False, ignore_index = True)
)
strike_rate_overall.index = range(1, len(strike_rate_overall)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 48. Top N Overall Batting Average (Minimum 10 Innings)
batting_average_overall = (
    batsman_overall_df[['Batsman', 'Innings', 'Runs', 'Dismissals', 'Batting Average']]
    .query("Innings >= 10")
    .sort_values(by = 'Batting Average', ascending = False, ignore_index = True)
)
batting_average_overall.index = range(1, len(batting_average_overall)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 49. Overall - Strike Rate vs Batting Average
sr_average = strike_rate_overall.merge(batting_average_overall, on = ['Batsman', 'Innings', 'Runs'])

def categorize(sr, avg):
    if sr > 130 and avg > 40:
        return ('green', 'Highly Consistent')
    elif 110 <= sr <= 140 and 30 <= avg <= 40:
        return ('orange', 'Consistent & Aggressive') 
    elif 140 <= sr <= 170 and 30 <= avg <= 40:
        return ('red', 'Reliable Power Hitters')
    elif 100 <= sr <= 130 and 20 <= avg <= 30:
        return ('magenta', 'Anchors') 
    elif 130 <= sr <= 170 and 20 <= avg <= 30:
        return ('blue', 'Power Hitters')  
    elif 30 <= sr <= 120 and 0 <= avg <= 20:
        return ('gray', 'Lower-Order Contributor') 
    return ('lightgray', 'Lower-Order Hitters')  

sr_average[['Color', 'Category']] = sr_average.apply(lambda row: categorize(row['Strike Rate'], row['Batting Average']), axis=1, result_type="expand")

categories = sr_average['Category'].unique()

# ------------------------------------------------------------------------------------------------------------------------------------------
# 50. Most Centuries
centuries_count = (
    centuries_df
    .batter
    .value_counts()
    .reset_index()
    .rename(columns = {'batter': 'Batsman', 'count': 'Centuries'})
)
centuries_count.index = range(1, len(centuries_count)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 51. Most Half-Centuries
half_centuries_count = (
    half_centuries_df
    .batter
    .value_counts()
    .reset_index()
    .rename(columns = {'batter': 'Batsman', 'count': 'Half-Centuries'})
)
half_centuries_count.index = range(1, len(half_centuries_count)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 52. Most Boundaries
overall_boundaries = (
    batsman_overall_df
    .assign(
        Boundaries = lambda df_: df_['Sixes'] + df_['Fours']
    )
    .sort_values(by = 'Boundaries', ascending = False)
    [['Batsman', 'Runs', 'Balls', 'Sixes', 'Fours', 'Boundaries']]
)
overall_boundaries.index = range(1, len(overall_boundaries)+1)

overall_sixes = (
    overall_boundaries
    .sort_values(by = 'Sixes', ascending = False, ignore_index = True)
)
overall_sixes.index = range(1, len(overall_sixes)+1)

overall_fours = (
    overall_boundaries
    .sort_values(by = 'Fours', ascending = False, ignore_index = True)
)
overall_fours.index = range(1, len(overall_fours)+1)

df_melted = overall_boundaries.melt(id_vars=['Batsman'], value_vars=['Fours', 'Sixes'],
                                    var_name="Boundary Type", value_name="Count")

agg_df = df_melted.groupby(["Batsman"]).sum().reset_index()
agg_df["Total Boundaries"] = agg_df["Count"]
agg_df = agg_df.sort_values(by="Total Boundaries", ascending=False)

# ------------------------------------------------------------------------------------------------------------------------------------------
## Bowler Analysis
bowler_stats = (
    bowler_stats
    .assign(
        bowling_average = lambda df_: round(df_['runs_conceded']/df_['wickets'], 2),
        strike_rate = lambda df_: round(df_['balls']/df_['wickets'],2),
        wicket_per_match = lambda df_: round(df_['wickets']/df_['matches'],2),
        boundary_rate = lambda df_: round((df_['count_six_conceded'] + df_['count_four_conceded'])/df_['balls'],2)
    )
    .rename(columns = {'bowler': 'Bowler', 'balls': 'Balls', 'runs_conceded': 'Runs Conceded', 'overs': 'Overs', 
                       'economy_rate': 'Economy Rate', 'wickets': 'Wickets', 'matches': 'Matches', 'dot_balls': 'Dot Balls', 
                       'count_six_conceded': 'Sixes Conceded', 'count_four_conceded': 'Fours Conceded',
                       'count_three_conceded': 'Threes Conceded', 'count_two_conceded': 'Twos Conceded', 
                       'count_one_conceded': 'Ones Conceded', 'count_extra_runs': 'Extras Conceded',
                       'dot_balls_percent': 'Dot Ball %', 'bowling_average': 'Bowling Average', 'strike_rate': 'Strike Rate',
                       'wicket_per_match': 'Wicket per Match', 'boundary_rate': 'Boundary Rate'})
)
bowler_stats = bowler_stats[['Bowler', 'Matches', 'Balls', 'Overs', 'Runs Conceded', 'Wickets', 'Dot Balls', 'Sixes Conceded', 'Fours Conceded', 
              'Threes Conceded', 'Twos Conceded', 'Ones Conceded', 'Extras Conceded', 'Dot Ball %', 'Boundary Rate',
              'Wicket per Match', 'Bowling Average', 'Strike Rate', 'Economy Rate']]

# ------------------------------------------------------------------------------------------------------------------------------------------
# 53. Top N Overall Individual Wickets
individual_wickets_df = (
    bowler_stats[['Bowler', 'Wickets']]
    .sort_values(by = 'Wickets', ascending = False, ignore_index = True)
)
individual_wickets_df.index = range(1, len(individual_wickets_df)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 54. Top N Individual Wickets in a Match
individual_match_wickets = (
    individual_match_wickets
    .rename(columns = {'bowler': 'Bowler', 'wickets': 'Wickets'})
)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 55. Top N Overall Economy Rates
overall_economy_rates = (
    bowler_stats[bowler_stats['Overs'] >= 10]
    .sort_values(by = 'Economy Rate', ignore_index = True)
)
overall_economy_rates.index = range(1, len(overall_economy_rates)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 56. Top N Overall Strike Rates
overall_strike_rates = (
    bowler_stats[bowler_stats['Overs'] >= 10]
    .sort_values(by = 'Strike Rate', ignore_index = True)
)
overall_strike_rates.index = range(1, len(overall_strike_rates)+1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 57. Strike Rate Vs Economy Rate
df_bowlers = bowler_stats[bowler_stats['Overs'] >= 10]
def categorize_bowler_sr_er(row):
    if row["Strike Rate"] < 20 and row["Economy Rate"] < 8:
        return "Match Winning Wicket-Takers"
    elif row["Strike Rate"] < 20 and row["Economy Rate"] < 12:
        return "Aggressive Wicket Takers"
    elif 20 <= row["Strike Rate"] <= 35 and row["Economy Rate"] <= 8:
        return "Restrictive Specialists"
    elif 20 <= row["Strike Rate"] <= 35 and row["Economy Rate"] > 8:
        return "Expensive but Balanced Performer"
    elif row["Strike Rate"] > 35 and row["Economy Rate"] > 8:
        return "Expensive & Inefficient"
    else:
        return "Others"

df_bowlers["Category_SR_ER"] = df_bowlers.apply(categorize_bowler_sr_er, axis=1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# 58. Dot Ball % Vs Dot Balls
def categorize_bowler(row):
    if row["Dot Balls"] >= 1200 and row["Dot Ball %"] >= 35:
        return "Elite Defenders"
    elif row["Dot Balls"] >= 1200 and row["Dot Ball %"] >= 30:
        return "Volume Restrictors"
    elif row["Dot Balls"] >= 800 and row["Dot Ball %"] >= 35:
        return "Efficient Controllers"
    elif row["Dot Balls"] >= 800 and row["Dot Ball %"] >= 30:
        return "Balanced Containment"
    elif row["Dot Balls"] < 800 and row["Dot Ball %"] < 30:
        return "Expensive Attackers"
    else:
        return "Impactful Short-Sprint Bowlers"

df_bowlers["Category"] = df_bowlers.apply(categorize_bowler, axis=1)

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
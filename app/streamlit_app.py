import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from scripts import analysis
from scripts import team_analysis
from scripts import season_analysis
from scripts import player_analysis

st.set_page_config(layout="wide") 

# Main Title
st.markdown("<h1 style='text-align: center;'>IPL - 'Indian Premier League'</h1>", unsafe_allow_html=True)

# Sidebar selection
selection1 = st.sidebar.selectbox(
    "IPL Analysis (2008-2024)",
    ["Home", "Brief Description", "Overall Insights", "Season-wise Insights", "Team-wise Insights", "Player-wise Insights"]
)

if selection1 == 'Home':
    st.markdown("<h1 style='text-align: center;'> Welcome to IPL Insights! 🏏</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style=\"font-size:24px; text-align: justify;\"> Dive into the world of IPL data like never before! This app brings you overall statistics, season-wise statistics, team-wise statistics, and in-depth player performance analysis, all in one interactive dashboard. Whether you're a passionate cricket fan or a data enthusiast, explore trends, uncover insights, and make informed decisions with ease.🚀🔥</p>",
        unsafe_allow_html=True
    )
    st.markdown(
    "<p style=\"font-size:24px;\">Let the numbers do the talking and stay ahead of the game!</p>",
    unsafe_allow_html=True
    )

elif selection1 == 'Brief Description':
    st.markdown(
        '<h1 style="font-size:32px; text-align: center;">🏏 <b>Indian Premier League (IPL) — Cricket’s Biggest Festival!</b></h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="font-size:24px; text-align: justify;">Since its electrifying debut in <b>2008</b>, the IPL has redefined T20 cricket with high-intensity matches, '
        'legendary rivalries, and unforgettable performances. Featuring the best global talent, each season brings fresh excitement, '
        'record-breaking auctions, and jaw-dropping moments. IPL is where <b>cricket meets entertainment, passion, and drama!</b> 🚀🔥</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="font-size:24px; text-align: justify;">This interactive dashboard offers a comprehensive view of team performances across IPL seasons, with a focus on franchise continuity. Regardless of player churn, team rebranding, or structural changes, each franchise is treated as a unified entity to enable meaningful trend analysis.</p>',
        unsafe_allow_html=True
    )
    st.markdown(
    '''
    <p style="font-size:24px; text-align: justify;">
    For consistency in franchise-level analysis, <strong>defunct or renamed teams are merged under their latest franchise identities</strong>. 
    Examples include:
    <ul style="padding-left: 20px;">
        <li style="font-size:20px;"><strong>Deccan Chargers → Sunrisers Hyderabad</strong></li>
        <li style="font-size:20px;"><strong>Delhi Daredevils → Delhi Capitals</strong></li>
        <li style="font-size:20px;"><strong>Gujarat Lions → Gujarat Titans</strong></li>
        <li style="font-size:20px;"><strong>Pune Warriors & Rising Pune Supergiants → One Pune Franchise (represented as Rising Pune Supergiants)</strong></li>
    </ul>
    </p>
    ''',
    unsafe_allow_html=True
    )
    
    st.markdown("##### Only the most recent team identity is considered for analysis to ensure franchise continuity across seasons.")

    st.subheader("🏆 IPL Playoffs Format")
    st.markdown("#### • Seasons - 2008, 2009 & 2010")
    st.markdown('<p style="font-size:22px; text-align: justify;">Top 4 teams advanced to two semi-finals, followed by a final</p>', unsafe_allow_html=True)

    st.markdown("#### • Seasons - 2011 & onwards")

    st.markdown(
        '''
        <div style="font-size:20px; text-align: justify;">
        1. <strong>Qualifier 1</strong><br>
        - Played between the <strong>top two teams</strong> from the league stage<br>
        - <strong>Winner</strong> advances directly to the <strong>Final</strong><br>
        - <strong>Loser</strong> gets another chance in Qualifier 2<br><br>

        <div style="font-size:20px; text-align: justify;">
        2. <strong>Eliminator</strong><br>
        - Contested between teams ranked <strong>3rd and 4th</strong><br>
        - <strong>Loser is eliminated</strong>, <strong>winner moves</strong> to Qualifier 2<br><br>

        <div style="font-size:20px; text-align: justify;">
        3. <strong>Qualifier 2</strong><br>
        - Played between the <strong>loser of Qualifier 1</strong> and the <strong>winner of the Eliminator</strong><br>
        - <strong>Winner</strong> goes to the <strong>Final</strong><br><br>

        <div style="font-size:20px; text-align: justify;">
        4. <strong>Final</strong><br>
        - The <strong>winners of Qualifier 1 and Qualifier 2</strong> clash for the championship title
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.info("This format rewards consistency and gives the top two teams a safety net, keeping the playoffs competitive and exciting.")

elif selection1 == 'Overall Insights':
        selection2 = st.sidebar.radio("Overall Statistics Summary", ["Key-Highlights", "Visualizations"])

        if selection2 == "Key-Highlights":
            st.markdown("<h3 style='text-align: center;'>IPL Season 2008-2024 Data</h3>", unsafe_allow_html=True)
            # st.header('IPL Season 2008-2024 Data')
            st.markdown(f'<h1 style="color:Red;">🏆 Total Seasons: {analysis.total_seasons}</h1>', unsafe_allow_html=True)
            st.table(analysis.duration_df)

            st.markdown(f"### 🔥 **<span style='color:red;'>{analysis.total_matches} matches</span> played since IPL's inception!** 🔥", unsafe_allow_html=True)

            log_value = np.log1p(analysis.match_by_type['Match Count'])
            fig1 = px.bar(analysis.match_by_type, y='Match Type', x=log_value, text='Match Count', 
                        title="IPL Matches by Type", labels={'match_count': 'Number of Matches', 'match_type': 'Match Type'},
                        color='Match Type', orientation = 'h')
            fig1.update_layout(xaxis = {'title': 'Match Count', 'showticklabels':False})
            st.plotly_chart(fig1, key="chart1")

            st.table(analysis.match_by_type)

            st.markdown(f'<h1 style="font-size:32px; color:Red;">🏆 Total Teams Participated So Far: {analysis.count_teams}</h1>', unsafe_allow_html=True)

            st.table(analysis.total_teams)

            data2 = {
            "SubChild": ["Batsman Runs", "Extra Runs", "Fours", "Sixes", "Batsman", "Half-Centuries", "Centuries", "Balls", "Wickets", "4 Wickets", "5+ Wickets", "Bowler", "Super-Overs", "Venue-Cities", "Venue-Stadiums"],

            "Child": ["Runs", "Runs", "Boundaries", "Boundaries", "Batsman Count", "Century Club", "Century Club", "Balls", "Wickets", "Magic Spell", "Magic Spell", "Bowler Count", "Super-Overs", "Venue-Cities", "Venue-Stadiums"],

            "Parent": ["Batting(Overall)", "Batting(Overall)", "Batting(Overall)", "Batting(Overall)", "Batting(Overall)", "Batting(Overall)", "Batting(Overall)", "Bowling(Overall)", "Bowling(Overall)", "Bowling(Overall)", "Bowling(Overall)", "Bowling(Overall)", "General", "General", "General"],
            
            "Values": [analysis.total_batsman_runs, analysis.total_extra_runs, analysis.total_fours, 
                    analysis.total_sixes, analysis.total_batsman, analysis.total_half_centuries, analysis.total_centuries, analysis.total_balls, analysis.total_wickets, analysis.four_wickets, analysis.five_plus_wickets, analysis.total_bowlers, analysis.total_superovers, analysis.total_cities, analysis.total_venues]
            }

            df2 = pd.DataFrame(data2)
            df2["Log Values"] = np.log1p(df2["Values"])
            df2["SubChild"] = df2["SubChild"] + ": " + df2["Values"].astype(str)

            fig2 = px.sunburst(df2, path=["Parent", "Child", "SubChild"], values="Log Values", custom_data=["Values"], hover_data="Values", 
                            title="IPL Overall Metrics Breakdown")
            fig2.update_traces(hovertemplate="Value: %{customdata[0]}")
            fig2.update_layout(width=700, height=700, font=dict(size=18))

            st.plotly_chart(fig2, key='chart2', use_container_width=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<h2 style="font-size:24px;">🏅 Most Player of the Match </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.player_of_match} ({analysis.pom_count})"), label_visibility = 'hidden')
            with col2:
                st.markdown(f'<h2 style="font-size:24px;">🏏 Leading Run Scorer </h2>', unsafe_allow_html=True)
                st.metric(label="123", value=(f"{analysis.scorer} ({analysis.runs})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">🎯 Leading Wicket Taker </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.bowler} ({analysis.wickets})"), label_visibility = 'hidden')


            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<h2 style="font-size:24px;">🏆 Highest Team Score </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{int(analysis.highest_team_score)} ({analysis.highest_score_teamname})"), label_visibility = 'hidden')
            with col2:
                st.markdown('<h2 style="font-size:24px;">💥 Highest Individual Score </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.runs_match} ({analysis.scorer_match})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">⚡ Best Bowling Figure </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.best_fig_wickets} - {analysis.best_fig_runs} ({analysis.best_fig_bowler})"), label_visibility = 'hidden')

            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<h2 style="font-size:24px;">🚀 Most Boundaries </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.boundary_numbers} ({analysis.boundary_batsman})"), label_visibility = 'hidden')
            with col2:
                st.markdown('<h2 style="font-size:24px;">6️⃣ Most Sixes </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.sixes_numbers} ({analysis.sixes_batsman})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">4️⃣ Most Fours </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.fours_numbers} ({analysis.fours_batsman})"), label_visibility = 'hidden')

            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<h2 style="font-size:24px;"> 🤲 Most Catches </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.most_catches} ({analysis.most_catches_fielder})"), label_visibility = 'hidden')
            with col2:
                st.markdown('<h2 style="font-size:24px;">🧤 Most Stumpings </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.most_stumpings} ({analysis.most_stump_fielder})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">🔄 Most Run Outs </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{analysis.most_runouts} ({analysis.most_runouts_fielder})"), label_visibility = 'hidden')

            st.write('-------------------------------------')
        
        if selection2 == "Visualizations":
            selection3 = st.sidebar.radio('Visualizations', ('General Analysis', 'Toss Analysis', "Top 'N' Stats"))
            # st.subheader('IPL Season 2008-2024 Data')
            st.markdown("<h3 style='text-align: center;'>IPL Season 2008-2024 Data</h3>", unsafe_allow_html=True)

            if selection3 == "General Analysis":
                
                st.markdown("### • IPL Titles")
                fig3 = px.pie(analysis.team_wins, names="Team", values="Trophies", hover_data={"Winning Seasons": True}, hole = 0.5)
                st.plotly_chart(fig3, key="chart3")
                if st.checkbox('View Table: IPL Titles'):
                    st.table(analysis.team_wins)
            
                st.markdown("### • Venue-wise Total Matches")
                fig4 = px.bar(analysis.venue_matches, x = 'City', y= 'Total Matches', text_auto=True, color = 'City', title = 'Count of Matches by City')
                fig4.update_layout(xaxis = {'title': 'City'}, yaxis = {'title': 'Count of Matches'})
                st.plotly_chart(fig4, key = 'chart4')
                if st.checkbox('View Table: Venue-wise Matches'):
                    st.table(analysis.venue_matches)
            
                selection4 = st.selectbox('Match Type vs Venue', ('League', 'Final', 'Semi Final', 'Qualifier 1', 'Qualifier 2', 'Eliminator'))

                if selection4 == 'League':
                    result = analysis.venue_match_type('League')
                    st.write("Displaying results for 'League' matches")
                if selection4 == 'Final':
                    result = analysis.venue_match_type('Final')
                    st.write("Displaying results for 'Final' matches")
                if selection4 == 'Semi Final':
                    result = analysis.venue_match_type('Semi Final')
                    st.write("Displaying results for 'Semi Final' matches")
                if selection4 == 'Qualifier 1':
                    result = analysis.venue_match_type('Qualifier 1')
                    st.write("Displaying results for 'Qualifier 1' matches")
                if selection4 == 'Qualifier 2':
                    result = analysis.venue_match_type('Qualifier 2')
                    st.write("Displaying results for 'Qualifier 2' matches")
                if selection4 == 'Eliminator':
                    result = analysis.venue_match_type('Eliminator')
                    st.write("Displaying results for 'Eliminator' matches")

                result.index = range(1, len(result)+1)
                fig5 = px.bar(result, x = 'City', y = 'Total Matches', color = 'City', text_auto=True, title = 'Count of Matches by City for Match Types')
                st.plotly_chart(fig5, key = 'chart5')

                if st.checkbox("View Table: Venue-wise Match type"):
                    st.table(result)

                st.markdown('### • City-wise Count of Stadiums')

                fig6 = px.bar(analysis.city_stadium_count, x = 'City', y = 'Total Number of Stadiums', text_auto=True, hover_data = 'Stadium', title = 'Stadiums by City', color = 'City')
                st.plotly_chart(fig6, key = 'chart6')

                if st.checkbox("View Table: Stadium List"):
                    st.table(analysis.city_stadium_count)

            
            if selection3 == 'Toss Analysis':
                selection5 = st.sidebar.radio('Toss Analysis', ('Impact of Toss', 'Impact of Toss Decision', 'Venue Based Toss Impact'))

                if selection5 == 'Impact of Toss':
                    st.markdown("### • Impact of Toss on Outcome")

                    fig7 = px.pie(analysis.toss_impact, names="toss_won_and_won_match", values="count", title = 'Impact of Toss on Match Victory')
                    st.plotly_chart(fig7, key="chart7")

                if selection5 == 'Impact of Toss Decision':
                    st.markdown("### • Impact of Toss Decision on Outcome")

                    fig8 = px.bar(analysis.toss_decision, x = 'toss_decision', y = 'count', text_auto=True, labels = {'toss_decision': 'Toss Decision', 'count': 'Count'}, color = 'toss_decision', title = 'Distribution of Toss Decision')
                    fig8.update_xaxes(
                        tickvals=["bat", "field"],
                        ticktext=["Opted to Bat", "Chose to Field"]
                    )
                    fig8.update_traces(marker=dict(line=dict(width=1, color='black')))

                    st.plotly_chart(fig8, key = 'chart8')

                    st.write(f"After winning a toss, teams have decided to Field first for {analysis.Field} matches and Bat first for {analysis.Bat} matches!")

                    fig9 = px.bar(analysis.toss_impact_df, x = 'Outcome', y = 'Count', color = 'toss_decision', barmode = 'group', text_auto = True, labels = {'toss_decision': 'Toss Decision'}, title = "Impact of Toss Decision on Match Outcomes", color_discrete_map={'bat': 'skyblue', 'field': 'pink'})
                    fig9.update_traces(marker=dict(line=dict(width=1, color='black')))
                    # fig9.update_xaxes(categoryorder='category ascending')
                    st.plotly_chart(fig9, key = 'chart9')

                    # Pie Chart for Bat Decision
                    fig_bat = px.pie(analysis.df_bat, names='Outcome', values='Count', title="Match Outcomes When Choosing to Bat")
                    fig_bat.update_traces(textinfo="percent+label")

                    # Pie Chart for Field Decision
                    fig_field = px.pie(analysis.df_field, names='Outcome', values='Count', title="Match Outcomes When Choosing to Field")
                    fig_field.update_traces(textinfo="percent+label")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(fig_bat)
                    with col2:
                        st.plotly_chart(fig_field)
                
                if selection5 == 'Venue Based Toss Impact':
                    st.markdown("### • Venue Based Toss Impact")

                    fig10 = px.bar(analysis.match_won_toss_won_across_city, x = 'city', y = 'count', title = "Count of Matches Won Given Toss Won Across Cities", text_auto = True, color = 'city', labels = {'city': 'City', 'count': 'Count'})
                    st.plotly_chart(fig10, key = 'chart10')

                    fig11 = px.bar(analysis.venue_toss_outcome,
                        x='City', y='Success Rate', 
                        title="Impact of Toss on Match Wins Across Cities",
                        text_auto=True, color = 'Success Rate', color_continuous_scale= 'viridis'
                    )
                    st.plotly_chart(fig11, key="chart11")

                    if st.checkbox("View Table: Venue Based Toss Success Rate"):
                        st.table(analysis.venue_toss_outcome)
                    
                    fig12 = px.density_heatmap(analysis.venue_toss_decision, x='City', y='Toss Decision', z='Win (%)',
                         title="Venue-Based Toss Decision & Success", color_continuous_scale='Viridis')

                    st.plotly_chart(fig12, key="chart12")

                    if st.checkbox('View Table: Venue Based Toss Decision Success Rate'):
                        st.table(analysis.venue_toss_decision)
            
            if selection3 == "Top 'N' Stats":
                selection6 = st.sidebar.radio('Top Stats', ('Team', 'Batsman', 'Bowler'))
            
                if selection6 == 'Team':
                    n_value1 = st.slider("Select top N", min_value=1, max_value=100, value = 5)
                    st.markdown(f"### • Top {n_value1} - Team Scores")

                    fig13 = px.bar(analysis.top_n_team_scores(n_value1), x = 'Batting Team', y = 'Team Score', color = 'Team Score', text_auto = True)
                    fig13.update_traces(marker=dict(line=dict(width=1, color='black')))
                    st.plotly_chart(fig13, key = 'chart13')

                    if st.checkbox("View Table: Top Team Scores"):
                        st.table(analysis.top_n_team_scores(n_value1))
                    
                    st.markdown(f"### • Teams with 200+ Scores")
                    
                    fig14 = px.bar(analysis.team_200_plus_scores, x = 'Batting Team', y = 'Count of 200+ Scores', text_auto = True, color = 'Count of 200+ Scores', color_continuous_scale = 'viridis')
                    st.plotly_chart(fig14, key = 'chart14')
                    
                    st.markdown(f"### • Inning-Wise 200+ Scores for Teams")

                    trace1 = go.Bar(x = analysis.team_scores_200['Batting Team'], y = analysis.team_scores_200['Count of 200+ Scores: Bat First'], name = 'Bat First', text = analysis.team_scores_200['Count of 200+ Scores: Bat First'])
                    trace2 = go.Bar(x = analysis.team_scores_200['Batting Team'], y = analysis.team_scores_200['Count of 200+ Scores: Field First'], name = 'Field First', text = analysis.team_scores_200['Count of 200+ Scores: Field First'])
                    
                    data = [trace1, trace2]
                    layout = go.Layout(title = 'Inning-Wise 200+ Scores for Teams',
                                       xaxis = {'title': 'Team'}, 
                                       yaxis = {'title': 'Count of 200+ Scores'})
            
                    fig15 = go.Figure(data = data, layout = layout)

                    st.plotly_chart(fig15, key = 'chart15')

                    st.markdown(f"### • Team-Wise 200+ Scores")

                    team_name = st.selectbox("Select Team", (analysis.total_teams['Team']))

                    df_scores = analysis.team_200_score(team_name)
                    df_scores1 = df_scores.assign(cumulative_total = lambda df_: df_['Team Score'].cumsum())
                    df_scores1 = df_scores1.rename(columns = {'cumulative_total': 'Cumulative Total'})
                    df_scores1.index = range(1, len(df_scores1)+1)

                    if df_scores.empty:
                        st.warning(f"No 200+ scores found for {team_name}.")

                    fig16 = px.bar(df_scores, x = 'Team Score', y = 'Batting Team', barmode = 'stack', text_auto = True, title = f"{team_name}:   Scored 200+ runs '{df_scores1.shape[0]}' times", color = 'Team Score', color_continuous_scale = 'plasma')
                    st.plotly_chart(fig16, key = 'chart16')

                    if st.checkbox(f"View Table: 200+ Scores for {team_name}"):
                        st.table(df_scores1)

                    st.markdown(f"### • Win Percentage for 200+ Scores")

                    trace11 = go.Bar(x = analysis.setting_target_200plus['Batting Team'], y = analysis.setting_target_200plus['Win Percent'], name = 'Bat First', text = analysis.setting_target_200plus['Win Percent'], hovertext = analysis.setting_target_200plus['Winning Cause'])
                    trace22 = go.Bar(x = analysis.chasing_target_200plus['Batting Team'], y = analysis.chasing_target_200plus['Win Percent'], name = 'Field First', text = analysis.chasing_target_200plus['Win Percent'])
                    
                    data2 = [trace11, trace22]
                    layout2 = go.Layout(title = 'Win Percent while scoring 200+ runs',
                                       xaxis = {'title': 'Team'}, 
                                       yaxis = {'title': 'Win Percent'})
            
                    fig17 = go.Figure(data = data2, layout = layout2)

                    st.plotly_chart(fig17, key = 'chart17')

                    if st.checkbox("View Table: Winning Cause for 200+ Scores"):
                        radio_selection = st.radio('Select One', ('Setting Target', 'Chasing Target'))
                        if radio_selection == 'Setting Target':
                            st.table(analysis.setting_target_200plus)
                        elif radio_selection == 'Chasing Target':
                            st.table(analysis.chasing_target_200plus)
                        else:
                            None
                    
                if selection6 == 'Batsman':
                    st.header("Batsman Analysis")
                    n_value2 = st.slider("Select value of N", min_value=1, max_value=100, value = 5)
                    st.markdown(f"### • Top {n_value2} - Overall Individual Scores")

                    fig18 = px.bar(analysis.leading_scorers.head(n_value2), x = 'Batsman', y = 'Runs', title="Top Individual Scores", color='Runs', text_auto = True, color_continuous_scale = 'sunset')
                    st.plotly_chart(fig18, key = 'chart18')
                    
                    if st.checkbox("View Table: Leading Run Scorers"):
                        st.table(analysis.leading_scorers.head(n_value2))
                    
                    n_value3 = st.slider("Set N", min_value=1, max_value=100, value = 5)
                    st.markdown(f"### • Top {n_value3} - Individual Scores in a Match")

                    fig19 = px.bar(analysis.individual_match_scores.head(n_value3), x = 'batter', y = 'runs', title="Top Individual Scores", color='runs', text_auto = True)
                    st.plotly_chart(fig19, key = 'chart19')
                    
                    if st.checkbox("View Table: Leading Run Scorers in a Match"):
                        st.table(analysis.individual_match_scores.head(n_value3))

                    n_value4 = st.slider("Choose N", min_value=1, max_value=100, value = 5)
                    st.markdown(f"### • Top {n_value4} - Overall Strike Rate (Minimum 10 Innings)")

                    fig20 = px.line(analysis.strike_rate_overall.head(n_value4), x = 'Batsman', y = 'Strike Rate', title = 'Top Overall Strike Rate of a Player', markers = True, hover_data = ['Innings', 'Runs', 'Balls'])
                    fig20.update_traces(
                        marker = {'size': 10, 'color': 'red'},
                        text=analysis.strike_rate_overall["Strike Rate"], textposition="top center"
                    )
                    st.plotly_chart(fig20, key = 'chart20')

                    if st.checkbox("View Table: Strike Rate"):
                        st.table(analysis.strike_rate_overall.head(n_value4))

                    n_value5 = st.slider("Choose value of N", min_value=1, max_value=100, value = 5)
                    st.markdown(f"### • Top {n_value5} - Overall Batting Average (Minimum 10 Innings)")

                    fig21 = px.line(analysis.batting_average_overall.head(n_value5), x = 'Batsman', y = 'Batting Average', title = 'Top Overall Batting Average of a Player', markers = True, hover_data = ['Innings', 'Runs', 'Dismissals'])
                    fig21.update_traces(
                        marker = {'size': 10, 'color': 'Magenta'},
                        text=analysis.batting_average_overall["Batting Average"], textposition="top center"
                    )
                    st.plotly_chart(fig21, key = 'chart21')

                    if st.checkbox("View Table: Batting Average"):
                        st.table(analysis.batting_average_overall.head(n_value5))

                    st.markdown(f"### • Strike Rate Vs Batting Average (Minimum 10 Innings)")
                    
                    fig22 = go.Figure()

                    for category in analysis.categories:
                        df_filtered = analysis.sr_average[analysis.sr_average['Category'] == category]
                        fig22.add_trace(go.Scatter(
                            x=df_filtered['Batting Average'],
                            y=df_filtered['Strike Rate'],
                            mode='markers',
                            marker=dict(size=15, color=df_filtered['Color'].iloc[0] if not df_filtered.empty else 'lightgray', opacity=0.7),
                            name=category,
                            hovertext=df_filtered['Batsman']
                        ))

                    fig22.update_layout(
                        title='Categorized Strike Rate vs Batting Average',
                        xaxis=dict(title='Batting Average'),
                        yaxis=dict(title='Strike Rate'),
                        height=700,
                        width=1000,
                        legend_title="Batting Categories"
                    )
                    
                    st.plotly_chart(fig22, key = 'chart22')

                    n_value6 = st.slider("Set N value", min_value = 1, max_value = 100, value = 5)
                    st.markdown(f"### • Top {n_value6} - Count of Centuries by a Player")

                    fig23 = px.bar(analysis.centuries_count.head(n_value6), x = 'Batsman', y = 'Centuries', text_auto = True, title = 'Count of Centuries', color = 'Batsman')
                    st.plotly_chart(fig23, key = 'chart23')

                    n_value7 = st.slider("Set value for N", min_value = 1, max_value = 100, value = 5)
                    st.markdown(f"### • Top {n_value7} - Count of Half-Centuries by a Player")

                    fig24 = px.bar(analysis.half_centuries_count.head(n_value7), x = 'Batsman', y = 'Half-Centuries', text_auto = True, title = 'Count of Half-Centuries', color = 'Batsman')
                    st.plotly_chart(fig24, key = 'chart24')

                    num_players = st.slider("Select Number of Top Players", min_value=1, max_value=100, value = 5)
                    st.markdown(f"### • Top {num_players} - Count of Boundaries by a Player")

                    top_players = analysis.agg_df.head(num_players)["Batsman"].tolist()
                    filtered_df = analysis.df_melted[analysis.df_melted["Batsman"].isin(top_players)]

                    fig25 = px.density_heatmap(filtered_df, x="Batsman", y="Boundary Type", z="Count",
                                            color_continuous_scale="Viridis")
                    st.plotly_chart(fig25, key = 'chart25')

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.checkbox(f"Top {num_players} Sixes:"):
                            st.table(analysis.overall_sixes.head(num_players))
                    
                    with col2:
                        if st.checkbox(f"Top {num_players} Fours:"):
                            st.table(analysis.overall_fours.head(num_players))
                
                if selection6 == 'Bowler':
                    st.header("Bowler Analysis")

                    n_value8 = st.slider("Select Number of Top Bowlers", min_value=1, max_value=100, value = 5)
                    st.markdown(f"### • Top {n_value8} - Overall Wickets by a Bowler") 

                    fig26 = px.bar(analysis.individual_wickets_df.head(n_value8), x = 'Bowler', y = 'Wickets', text_auto = True, title = 'Overall Wickets by a Bowler', color = 'Bowler')
                    st.plotly_chart(fig26, key = 'chart26')

                    n_value9 = st.slider("Select Number of Top Bowlers in a Match", min_value=1, max_value=100, value = 50)
                    st.markdown(f"### • Top {n_value9} - Wickets by a Bowler in a Match") 
                    
                    fig27 = px.bar(analysis.individual_match_wickets.head(n_value9), x = 'Bowler', y = 'Wickets', text_auto = True, title = 'Wickets by a Bowler in a Match', color = 'Bowler')
                    st.plotly_chart(fig27, key = 'chart27')

                    n_value10 = st.slider("Select Count of Top Bowlers - Economy Rate", min_value=1, max_value=100, value = 50)
                    st.markdown(f"### • Top {n_value10} - Overall Economy Rates (Minimum 10 Overs)") 

                    fig28 = px.line(analysis.overall_economy_rates.head(n_value10), x = 'Bowler', y = 'Economy Rate', markers = True, hover_data = ['Matches', 'Overs', 'Runs Conceded', 'Wickets'])
                    fig28.update_traces(marker = {'size': 8, 'color': 'Magenta'})
                    st.plotly_chart(fig28, key = 'chart28')

                    n_value11 = st.slider("Select Count of Top Bowlers - Bowling Average", min_value=1, max_value=100, value = 50)
                    st.markdown(f"### • Top {n_value11} - Overall Strike Rates (Minimum 10 Overs)") 

                    fig29 = px.line(analysis.overall_strike_rates.head(n_value11), x = 'Bowler', y = 'Strike Rate', markers = True, hover_data = ['Matches', 'Overs', 'Balls', 'Wickets'])
                    fig29.update_traces(marker = {'size': 8, 'color': 'Red'})
                    st.plotly_chart(fig29, key = 'chart29')

                    st.markdown(f"### • Economy Rate Vs Strike Rate (Minimum 10 Overs)")
                    color_map = {
                        "Match Winning Wicket-Takers": "red",
                        "Restrictive Specialists": "blue",
                        "Aggressive Wicket Takers": "green",
                        "Expensive & Inefficient": "orange",
                        "Expensive but Balanced Performer": "purple"
                    }

                    fig30 = px.scatter(analysis.df_bowlers, x="Strike Rate", y="Economy Rate", color="Category_SR_ER",
                                    hover_data = ["Bowler", "Matches", "Overs", "Runs Conceded", "Wickets"], size_max=15, title="Economy Rate vs Strike Rate - Categorized",
                                    color_discrete_map=color_map)
                    fig30.update_traces(marker = {'size': 12, 'opacity': 0.7})
                    fig30.update_layout(height = 600)
                    st.plotly_chart(fig30, key = 'chart30')

                    st.markdown(f"### • Dot Balls Percentage Vs Dot Balls (Minimum 10 Overs)")
                    fig31 = px.scatter(analysis.df_bowlers, x="Dot Balls", y="Dot Ball %", color="Category",
                                    hover_data = ["Bowler", "Matches", "Overs", "Wickets"], size_max=15,
                                    title="Dot Balls vs Dot Ball Percentage - Categorized",
                                    color_discrete_map={
                                        "Elite Defenders": "green",
                                        "Volume Restrictors": "blue",
                                        "Efficient Controllers": "yellow",
                                        "Balanced Containment": "orange",
                                        "Expensive Attackers": "red",
                                        "Impactful Short-Sprint Bowlers": "purple"
                                    })
                    fig31.update_traces(marker = {'size': 12, 'opacity': 0.7})
                    fig31.update_layout(height = 600)
                    st.plotly_chart(fig31, key = 'chart31')

elif selection1 == 'Team-wise Insights':
    selection7 = st.sidebar.radio("Team-wise Statistics Summary", ["Key-Highlights", "Visualizations"])

    if selection7 == 'Key-Highlights':
        st.markdown("<h3 style='text-align: center;'>IPL Season 2008-2024 Data</h3>", unsafe_allow_html=True)

        st.markdown("<h3> • Team & Seasons </h3>", unsafe_allow_html=True)
        if st.checkbox("View Table: Team-wise Seasons & Matches"):
            st.dataframe(team_analysis.teams_df, use_container_width=True)

            # st.table(team_analysis.teams_df)

        st.markdown("<h3> • Metrics </h3>", unsafe_allow_html=True)

        options = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

        col_left, col_right = st.columns(2)
        with col_left:
            selected_team = st.selectbox("Select Team", options = analysis.total_teams)
            st.write(f"You've selected: {selected_team}")
            if not selected_team:
                st.warning("⚠️ Please select at least one option!")

        with col_right:
            selected_season = st.multiselect("Select Season", options = options, default = 'All')

            if 'All' in selected_season:
                selected_season = 'All'
            else:
                selected_season = [team for team in selected_season if team != 'All']
            
            if selected_season == 'All':
                st.write("You've have selected 'All'")
            else:
                st.write(f"You've selected: {sorted(selected_season)}")

            if not selected_season:
                st.warning("⚠️ Please select at least one option!")
        
        st.markdown(f"<h3> Team: {selected_team} </h3>", unsafe_allow_html=True)
        st.markdown(f"<h3> Season(s): {selected_season} </h3>", unsafe_allow_html=True)

        # Fetch team highlights while handling missing data gracefully
        batsman_stats = team_analysis.team_highlights_batsman(selected_team, selected_season)
        bowler_stats = team_analysis.team_highlights_bowler(selected_team, selected_season)
        general_stats = team_analysis.team_highlights_general(selected_team, selected_season)

        # If any function returns None due to missing data, display a message instead of crashing
        # Check if all values in stats are zero
        if all(value == 0 for value in batsman_stats) and all(value == 0 for value in bowler_stats) and all(value == 0 for value in general_stats):
            st.error(f"⚠️ No meaningful data available for {selected_team} in season(s): {selected_season}. All values are zero.")
        else:
            # Prepare data for visualization
            data3 = {
                "SubChild": ["Batsman Runs", "Extra Runs", "Fours", "Sixes", "Batsman", "Half-Centuries", "Centuries", "Balls", 
                            "Wickets", "4 Wickets", "5+ Wickets", "Bowler", "Super-Overs", "Venue-Cities", "Venue-Stadiums", "Total Matches"],
                
                "Child": ["Runs", "Runs", "Boundaries", "Boundaries", "Batsman Count", "Century Club", "Century Club", "Balls", 
                        "Wickets", "Magic Spell", "Magic Spell", "Bowler Count", "Super-Overs", "Venue-Cities", "Venue-Stadiums", "Total Matches"],
                
                "Parent": ["Batting", "Batting", "Batting", "Batting", "Batting", "Batting", "Batting", "Bowling", "Bowling", 
                        "Bowling", "Bowling", "Bowling", "General", "General", "General", "General"],
                
                "Values": [batsman_stats[0], batsman_stats[1], batsman_stats[3], batsman_stats[2], batsman_stats[6], 
                        batsman_stats[5], batsman_stats[4], bowler_stats[1], bowler_stats[2], bowler_stats[3], 
                        bowler_stats[4], bowler_stats[0], general_stats[1], general_stats[2], general_stats[3], general_stats[0]]
            }

            df3 = pd.DataFrame(data3)
            df3["Log Values"] = np.log1p(df3["Values"])
            df3["SubChild"] = df3["SubChild"] + ": " + df3["Values"].astype(str)

            fig32 = px.sunburst(df3, path=["Parent", "Child", "SubChild"], values="Log Values", custom_data=["Values"], hover_data="Values")
            fig32.update_traces(hovertemplate="Value: %{customdata[0]}")
            fig32.update_layout(width=700, height=700, font=dict(size=18))

            st.plotly_chart(fig32, key='chart32', use_container_width=True)
            
            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<h2 style="font-size:24px;">🏅 Most Player of the Match </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{team_analysis.pom(selected_team, selected_season).head(1)['Player of Match'][0]} ({team_analysis.pom(selected_team, selected_season).head(1)['Count'][0]})"), label_visibility = 'hidden')             
            with col2:
                st.markdown('<h2 style="font-size:24px;">🏏 Leading Run Scorer </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{team_analysis.leading_run_scorer(selected_team, selected_season).head(1)['Batsman'][0]} ({team_analysis.leading_run_scorer(selected_team, selected_season).head(1)['Runs'][0]})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">🎯 Leading Wicket Taker </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{team_analysis.leading_wicket_taker(selected_team, selected_season).head(1)['Bowler'][0]} ({team_analysis.leading_wicket_taker(selected_team, selected_season).head(1)['Wickets'][0]})"), label_visibility = 'hidden')

            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<h2 style="font-size:24px;">🏆 Highest Team Score </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{team_analysis.individual_team_score(selected_team, selected_season).head(1)['Runs'][0]} (Season- {team_analysis.individual_team_score(selected_team, selected_season).head(1)['Season'][0]})"), label_visibility = 'hidden')
            with col2:
                st.markdown('<h2 style="font-size:24px;">💥 Highest Individual Score </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{team_analysis.individual_score(selected_team, selected_season).head(1)['Runs'][0]} ({team_analysis.individual_score(selected_team, selected_season).head(1)['Batsman'][0]})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">⚡ Best Bowling Figure </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{team_analysis.best_bowling_figure(selected_team, selected_season).head(1)['Wickets'][0]} - {team_analysis.best_bowling_figure(selected_team, selected_season).head(1)['Runs'][0]} ({team_analysis.best_bowling_figure(selected_team, selected_season).head(1)['Bowler'][0]})"), label_visibility = 'hidden')

            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<h2 style="font-size:24px;">🚀 Most Boundaries </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{team_analysis.boundaries(team_name=selected_team, boundary = None, seasons = selected_season).head(1)['Count'][0]} ({team_analysis.boundaries(team_name=selected_team, boundary = None, seasons = selected_season).head(1)['Batsman'][0]})"), label_visibility = 'hidden')
            with col2:
                st.markdown('<h2 style="font-size:24px;">6️⃣ Most Sixes </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{team_analysis.boundaries(team_name=selected_team, boundary = 6, seasons = selected_season).head(1)['Count'][0]} ({team_analysis.boundaries(team_name=selected_team, boundary = 6, seasons = selected_season).head(1)['Batsman'][0]})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">4️⃣ Most Fours </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{team_analysis.boundaries(team_name=selected_team, boundary = 4, seasons = selected_season).head(1)['Count'][0]} ({team_analysis.boundaries(team_name=selected_team, boundary = 4, seasons = selected_season).head(1)['Batsman'][0]})"), label_visibility = 'hidden')

            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<h2 style="font-size:24px;"> 🤲 Most Catches </h2>', unsafe_allow_html=True)
                catches_df = team_analysis.catches(team_name=selected_team, seasons=selected_season)
                if not catches_df.empty:
                    value = f"{catches_df.head(1)['Count'][0]} ({catches_df.head(1)['Fielder'][0]})"
                else:
                    value = "0 (N/A)"
                st.metric(label="12", value=value, label_visibility='hidden')
            with col2:
                st.markdown('<h2 style="font-size:24px;">🧤 Most Stumpings </h2>', unsafe_allow_html=True)
                stumpings_df = team_analysis.stumpings(team_name=selected_team, seasons=selected_season)
                if not stumpings_df.empty:
                    value = f"{stumpings_df.head(1)['Count'][0]} ({stumpings_df.head(1)['Fielder'][0]})"
                else:
                    value = "0 (N/A)"
                st.metric(label="12", value=value, label_visibility='hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">🔄 Most Run Outs </h2>', unsafe_allow_html=True)
                runouts_df = team_analysis.runouts(team_name=selected_team, seasons=selected_season)
                if not runouts_df.empty:
                    value = f"{runouts_df.head(1)['Count'][0]} ({runouts_df.head(1)['Fielder'][0]})"
                else:
                    value = "0 (N/A)"
                st.metric(label="12", value=value, label_visibility='hidden')

            st.write('-------------------------------------')
        
    if selection7 == 'Visualizations':
        st.markdown("<h3 style='text-align: center;'>IPL Season 2008-2024 Data</h3>", unsafe_allow_html=True)
        insight_team = st.selectbox("Select Team", options = analysis.total_teams)
        insight_type = st.radio("Select Option", ['General', 'Players', 'Rival Teams'], horizontal = True)

        if insight_type == 'General':
            st.markdown(f"### {insight_team} - {insight_type} Stats")

            st.markdown(f"#### • Season-wise Count of Matches")
            fig89 = px.bar(team_analysis.season_match_count(insight_team), x = 'Season', y = 'Count', color = 'Season', text_auto = True)
            st.plotly_chart(fig89, key="chart89")

            st.markdown(f"#### • Win-Loss %")
            team, num_matches, matches_won, win_percent = team_analysis.team_stats(insight_team)
            total_matches = [matches_won, num_matches - matches_won]
            labels = ['Matches Won', 'Matches Lost']

            fig90 = px.pie(values=total_matches, names=labels, hole=0.3)
            st.plotly_chart(fig90, key = 'chart90')

            st.markdown(f"#### • Success Rate by Match-Type")
            st.table(team_analysis.team_matchtype(insight_team))

            st.markdown(f"#### • Toss Distribution & Impact on Outcome (For Selected Seasons)")
            insight_options = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
            insight_season = st.multiselect("Select Season(s)", options = insight_options, default = 'All')

            if 'All' in insight_season:
                insight_season = 'All'
            else:
                insight_season = [i for i in insight_season if i != 'All']
            
            if insight_season == 'All':
                st.write("You've have selected 'All'")
            else:
                st.write(f"You've selected: {sorted(insight_season)}")

            if not insight_season:
                st.warning("⚠️ Please select at least one option!")
            col1, col2 = st.columns(2)
            with col1:
                toss_won, toss_lost = team_analysis.toss_distribution(insight_team, insight_season)
                fig91 = px.pie(values = [toss_won, toss_lost], names = ['Toss Won', 'Toss Lost'], title = 'Toss Distribution', hole=0.3)
                st.plotly_chart(fig91, key = 'chart91')
            with col2:
                toss_won_match_won, toss_lost_match_won = team_analysis.toss_winning_cause(insight_team, insight_season)
                fig92 = px.pie(values = [toss_won_match_won, toss_lost_match_won],
                            names = ['Toss Won Match Won', 'Toss Lost Match Won'],
                            title = 'Toss Distribution for a Winning Cause', hole=0.3)
                st.plotly_chart(fig92, key = 'chart92')
            
            st.markdown(f"#### • Home - Away Success Rate (For Selected Seasons)")
            st.table(team_analysis.home_away_wins(insight_team, insight_season))

            st.markdown(f"#### • Playoffs and Progression - {insight_team}")
            st.write(f"Total Playoffs: {team_analysis.level_hierarchy(insight_team).shape[0]}")
            st.table(team_analysis.level_hierarchy(insight_team))
        
        if insight_type == 'Players':
            st.markdown(f"### {insight_team} - {insight_type} Stats")
            st.markdown(f"#### • Batsman List")
            if st.checkbox("View Batsman List:"):
                df = team_analysis.team_batsman_list(insight_team)
                st.table(df)
            st.markdown(f"#### • Bowler List")
            if st.checkbox("View Bowler List"):
                df = team_analysis.team_bowler_list(insight_team)
                st.table(df)
            
            st.markdown(f"#### • Batsman Performance")
            df = team_analysis.team_batsman_performance(insight_team)
            df = df.query("Matches >= 5")
            fig93 = px.scatter(df, x = 'Batting Average', y = 'Strike Rate', color = 'Batsman', hover_data = ['Runs', 'Balls', 'Not Outs'])
            fig93.update_traces(marker = {'size': 18, 'opacity': 0.7})
            st.plotly_chart(fig93, key = 'chart93')

            st.markdown(f"#### • Bowler Performance")
            df = team_analysis.team_bowler_performance(insight_team)
            df = df.query("Matches >= 5")
            fig94 = px.scatter(df, x = 'Economy Rate', y = 'Bowling Average', color = 'Bowler', hover_data = ['Matches', 'Wickets', 'Balls', 'Runs Conceded'])
            fig94.update_traces(marker = {'size': 18, 'opacity': 0.7})
            st.plotly_chart(fig94, key = 'chart94')

            st.markdown(f"#### • Leading Run Scorers")

            options9 = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
            insight_season2 = st.multiselect("Select Season(s)", options = options9, default = 'All')

            if 'All' in insight_season2:
                insight_season2 = 'All'
            else:
                insight_season2 = [i for i in insight_season2 if i != 'All']
            
            if insight_season2 == 'All':
                st.write("You've have selected 'All'")
            else:
                st.write(f"You've selected: {sorted(insight_season2)}")

            if not insight_season2:
                st.warning("⚠️ Please select at least one option!")

            slider_value = st.slider("Choose value", min_value = 0, max_value = len(team_analysis.team_batsman_list(insight_team)))
            df = team_analysis.leading_run_scorer(insight_team, insight_season2)
            fig95 = px.bar(df.head(slider_value), x = 'Batsman', y = 'Runs', text_auto = True, color = 'Runs')
            st.plotly_chart(fig95, key="chart95")

            st.markdown(f"#### • Leading Wicket Takers")
            slider_value2 = st.slider("Choose value using slider", min_value = 0, max_value = len(team_analysis.team_bowler_list(insight_team)))
            df2 = team_analysis.leading_wicket_taker(insight_team, insight_season2)
            fig96 = px.bar(df2.head(slider_value2), x = 'Bowler', y = 'Wickets', text_auto = True, color = 'Wickets')
            st.plotly_chart(fig96, key="chart96")

        if insight_type == 'Rival Teams':
            st.markdown(f"### {insight_team} - {insight_type} Stats")
            st.markdown(f"#### • Performance against Rival Teams - Success Rate")
            options10 = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
            insight_season2 = st.multiselect("Select Season(s)", options = options10, default = 'All')

            if 'All' in insight_season2:
                insight_season2 = 'All'
            else:
                insight_season2 = [i for i in insight_season2 if i != 'All']
            
            if insight_season2 == 'All':
                st.write("You've have selected 'All'")
            else:
                st.write(f"You've selected: {sorted(insight_season2)}")

            if not insight_season2:
                st.warning("⚠️ Please select at least one option!")

            st.table(team_analysis.team_rival_matches(insight_team, insight_season2))

            st.markdown(f"#### • Performance against Rival Teams by Match Type - Success Rate")
            selected_rival_team = st.selectbox("Select Rival Team", options = analysis.total_teams)
            st.table(team_analysis.team_rival_matchtype(insight_team, selected_rival_team, insight_season2))
            st.markdown(f"#### • Performance against Rival Teams - Summary")
            st.table(team_analysis.team_rival_performance(insight_team, selected_rival_team, insight_season2))

elif selection1 == 'Season-wise Insights':
    selection8 = st.sidebar.radio("Season-wise Statistics Summary", ["Key-Highlights", "Visualizations"])

    if selection8 == 'Key-Highlights':

        options2 = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

        selected_season1 = st.multiselect("Select Season(s)", options = options2, default = 'All')

        if 'All' in selected_season1:
            selected_season1 = 'All'
        else:
            selected_season1 = [team for team in selected_season1 if team != 'All']
            
        if selected_season1 == 'All':
            st.write("You've have selected 'All'")
        else:
            st.write(f"You've selected: {sorted(selected_season1)}")

        if not selected_season1:
            st.warning("⚠️ Please select at least one option!")
        
        st.markdown(f"<h3> Season(s) - {selected_season1} </h3>", unsafe_allow_html=True)

        st.markdown(f"### 🔥 **<span style='color:red;'>{season_analysis.season_total_matches(selected_season1)} matches</span> played for selected season(s)!** 🔥", unsafe_allow_html=True)

        log_value1 = np.log1p(season_analysis.season_match_type(selected_season1)['Matches'])
        fig34 = px.bar(season_analysis.season_match_type(selected_season1), y='Match Type', x=log_value1, text='Matches', 
                    title="IPL Matches by Type", labels={'season_match_type': 'Number of Matches'},
                    color='Match Type', orientation = 'h')
        fig34.update_layout(xaxis = {'title': 'Match Count', 'showticklabels': False})
        st.plotly_chart(fig34, key="chart34")

        st.markdown(f'<h1 style="font-size:32px; color:Red;">🏆 Participated Teams: {season_analysis.season_teams(selected_season1).nunique().values[0]}</h1>', unsafe_allow_html=True)

        st.table(season_analysis.season_teams(selected_season1))

        st.markdown("<h3> • Metrics </h3>", unsafe_allow_html=True)

        batsman_stats1 = season_analysis.season_highlights_batsman(selected_season1)
        bowler_stats1 = season_analysis.season_highlights_bowler(selected_season1)
        general_stats1 = season_analysis.season_highlights_general(selected_season1)

        if all(value == 0 for value in batsman_stats1) and all(value == 0 for value in bowler_stats1) and all(value == 0 for value in general_stats1):
            st.error(f"⚠️ No meaningful data available for {selected_season1} in season(s): {selected_season1}. All values are zero.")
        else:
            data4 = {
                "SubChild": ["Batsman Runs", "Extra Runs", "Fours", "Sixes", "Batsman", "Half-Centuries", "Centuries", "Balls", 
                            "Wickets", "4 Wickets", "5+ Wickets", "Bowler", "Venue-Cities", "Venue-Stadiums", "Total Matches"],
                
                "Child": ["Runs", "Runs", "Boundaries", "Boundaries", "Batsman Count", "Century Club", "Century Club", "Balls", 
                        "Wickets", "Magic Spell", "Magic Spell", "Bowler Count", "Venue-Cities", "Venue-Stadiums", "Total Matches"],
                
                "Parent": ["Batting", "Batting", "Batting", "Batting", "Batting", "Batting", "Batting", "Bowling", "Bowling", 
                        "Bowling", "Bowling", "Bowling", "General", "General", "General"],
                
                "Values": [batsman_stats1[0], batsman_stats1[1], batsman_stats1[3], batsman_stats1[2], batsman_stats1[6], 
                        batsman_stats1[5], batsman_stats1[4], bowler_stats1[1], bowler_stats1[2], bowler_stats1[3], 
                        bowler_stats1[4], bowler_stats1[0], general_stats1[1], general_stats1[2], general_stats1[0]]
            }

            df4 = pd.DataFrame(data4)
            df4["Log Values"] = np.log1p(df4["Values"])
            df4["SubChild"] = df4["SubChild"] + ": " + df4["Values"].astype(str)

            fig33 = px.sunburst(df4, path=["Parent", "Child", "SubChild"], values="Log Values", custom_data=["Values"], hover_data="Values")
            fig33.update_traces(hovertemplate="Value: %{customdata[0]}")
            fig33.update_layout(width=700, height=700, font=dict(size=18))
            st.plotly_chart(fig33, key='chart33', use_container_width=True)
            
            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)
            pom_count = season_analysis.pom(selected_season1)['Count'].max()
            pom_names = season_analysis.pom(selected_season1)['Player of Match'].values[0]
            with col1:
                st.markdown('<h2 style="font-size:24px;">🏅 Most Player of the Match </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{pom_names} ({pom_count})"), label_visibility = 'hidden')             
            with col2:
                st.markdown('<h2 style="font-size:24px;">🏏 Leading Run Scorer </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{season_analysis.leading_run_scorer(selected_season1).head(1)['Batsman'][0]} ({season_analysis.leading_run_scorer(selected_season1).head(1)['Runs'][0]})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">🎯 Leading Wicket Taker </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{season_analysis.leading_wicket_taker(selected_season1).head(1)['Bowler'][0]} ({season_analysis.leading_wicket_taker(selected_season1).head(1)['Wickets'][0]})"), label_visibility = 'hidden')

            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<h2 style="font-size:24px;">🏆 Highest Team Score </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{season_analysis.individual_team_score(selected_season1).head(1)['Runs'][0]} (Season- {season_analysis.individual_team_score(selected_season1).head(1)['Season'][0]})"), label_visibility = 'hidden')
            with col2:
                st.markdown('<h2 style="font-size:24px;">💥 Highest Individual Score </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{season_analysis.individual_score(selected_season1).head(1)['Runs'][0]} ({season_analysis.individual_score(selected_season1).head(1)['Batsman'][0]})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">⚡ Best Bowling Figure </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{season_analysis.best_bowling_figure(selected_season1).head(1)['Wickets'][0]} - {season_analysis.best_bowling_figure(selected_season1).head(1)['Runs'][0]} ({season_analysis.best_bowling_figure(selected_season1).head(1)['Bowler'][0]})"), label_visibility = 'hidden')

            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<h2 style="font-size:24px;">🚀 Most Boundaries </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{season_analysis.boundaries(boundary = None, seasons = selected_season1).head(1)['Count'][0]} ({season_analysis.boundaries(boundary = None, seasons = selected_season1).head(1)['Batsman'][0]})"), label_visibility = 'hidden')
            with col2:
                st.markdown('<h2 style="font-size:24px;">6️⃣ Most Sixes </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{season_analysis.boundaries(boundary = 6, seasons = selected_season1).head(1)['Count'][0]} ({season_analysis.boundaries(boundary = 6, seasons = selected_season1).head(1)['Batsman'][0]})"), label_visibility = 'hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">4️⃣ Most Fours </h2>', unsafe_allow_html=True)
                st.metric(label="12", value=(f"{season_analysis.boundaries(boundary = 4, seasons = selected_season1).head(1)['Count'][0]} ({season_analysis.boundaries(boundary = 4, seasons = selected_season1).head(1)['Batsman'][0]})"), label_visibility = 'hidden')

            st.write('-------------------------------------')

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<h2 style="font-size:24px;"> 🤲 Most Catches </h2>', unsafe_allow_html=True)
                catches_df = season_analysis.catches(seasons=selected_season1)
                if not catches_df.empty:
                    value = f"{catches_df.head(1)['Count'][0]} ({catches_df.head(1)['Fielder'][0]})"
                else:
                    value = "0 (N/A)"
                st.metric(label="12", value=value, label_visibility='hidden')
            with col2:
                st.markdown('<h2 style="font-size:24px;">🧤 Most Stumpings </h2>', unsafe_allow_html=True)
                stumpings_df = season_analysis.stumpings(seasons=selected_season1)
                if not stumpings_df.empty:
                    value = f"{stumpings_df.head(1)['Count'][0]} ({stumpings_df.head(1)['Fielder'][0]})"
                else:
                    value = "0 (N/A)"
                st.metric(label="12", value=value, label_visibility='hidden')
            with col3:
                st.markdown('<h2 style="font-size:24px;">🔄 Most Run Outs </h2>', unsafe_allow_html=True)
                runouts_df = season_analysis.runouts(seasons=selected_season1)
                if not runouts_df.empty:
                    value = f"{runouts_df.head(1)['Count'][0]} ({runouts_df.head(1)['Fielder'][0]})"
                else:
                    value = "0 (N/A)"
                st.metric(label="12", value=value, label_visibility='hidden')

            st.write('-------------------------------------')

    if selection8 == 'Visualizations':
        season_visualizations = st.sidebar.radio('Visualizations', ('General Analysis', 'Toss Analysis', "Top 'N' Stats"))

        if season_visualizations == 'General Analysis':
            options3 = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

            selected_season2 = st.multiselect("Select Season(s)", options = options3, default = 'All')

            if 'All' in selected_season2:
                selected_season2 = 'All'
            else:
                selected_season2 = [team for team in selected_season2 if team != 'All']
                
            if selected_season2 == 'All':
                st.write("You've have selected 'All'")
            else:
                st.write(f"You've selected: {sorted(selected_season2)}")

            if not selected_season2:
                st.warning("⚠️ Please select at least one option!")
        
            st.markdown(f"<h3> Season(s) - {selected_season2} </h3>", unsafe_allow_html=True)

            avg_score1 = season_analysis.season_avg_score(seasons = selected_season2, inning = 1)
            avg_score2 = season_analysis.season_avg_score(seasons = selected_season2, inning = 2)

            trace1 = go.Scatter(x = avg_score1['Season'], y = avg_score1['Average Score'], mode = 'lines+markers', name = '1st Innings')
            trace2 = go.Scatter(x = avg_score2['Season'], y = avg_score2['Average Score'], mode = 'lines+markers', name = '2nd Innings')
            layout = go.Layout(title = 'Average 1st Inning Vs 2nd Inning Scores Across Seasons', xaxis = {'title': 'Season'}, yaxis = {'title': 'Average Score'})
            fig35 = go.Figure(data = [trace1, trace2], layout = layout)
            st.plotly_chart(fig35, key = 'chart35')

            avg_score11 = season_analysis.season_avg_score_boxplot(seasons = selected_season2, inning = 1)
            avg_score22 = season_analysis.season_avg_score_boxplot(seasons = selected_season2, inning = 2)

            fig36 = px.box(avg_score11, x = 'Season', y = 'Score', color = 'Season', title = 'Distribution of 1st Inning Scores Across Season')
            fig36.update_layout(xaxis = {'title': 'Season'}, yaxis = {'title': 'Average Score'})
            st.plotly_chart(fig36, key = 'chart36')

            fig37 = px.box(avg_score22, x = 'Season', y = 'Score', color = 'Season', title = 'Distribution of 2nd Inning Scores Across Season')
            fig37.update_layout(xaxis = {'title': 'Season'}, yaxis = {'title': 'Score'})
            st.plotly_chart(fig37, key = 'chart37')

        elif season_visualizations == 'Toss Analysis':
            options4 = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

            selected_season3 = st.multiselect("Select Season(s) for Analysis", options = options4, default = 'All')

            if 'All' in selected_season3:
                selected_season3 = 'All'
            else:
                selected_season3 = [team for team in selected_season3 if team != 'All']
                
            if selected_season3 == 'All':
                st.write("You've have selected 'All'")
            else:
                st.write(f"You've selected: {sorted(selected_season3)}")

            if not selected_season3:
                st.warning("⚠️ Please select at least one option!")
        
            st.markdown(f"<h3> Season(s) - {selected_season3} </h3>", unsafe_allow_html=True)
            st.markdown("### • Distribution of Toss Decision")

            fig38 = px.bar(season_analysis.toss_decision(selected_season3), x = 'Season', y = 'Count', color = 'Toss Decision', barmode = 'group', color_discrete_map = {'bat': 'pink', 'field': 'skyblue'}, text_auto = True)
            st.plotly_chart(fig38, key = 'chart38')

            st.markdown("### • Impact of Toss Decision on Outcome")
            st.write("Note: Matches with 'No Result' outcome are excluded")
            df_filtered = season_analysis.toss_decision_impact(selected_season3)
            data = {
                "Child": ["Opted-Bat & Won", "Opted-Bat & Lost", "Opted-Field & Won", "Opted-Field & Lost"],
                "Parent": ["Bat", "Bat", "Field", "Field"],
                "Values": [df_filtered[df_filtered['toss_decision'] == 'bat']['toss_won_match_won'].sum(),
                        df_filtered[df_filtered['toss_decision'] == 'bat']['toss_won_match_lost'].sum(),
                        df_filtered[df_filtered['toss_decision'] == 'field']['toss_won_match_won'].sum(),
                        df_filtered[df_filtered['toss_decision'] == 'field']['toss_won_match_lost'].sum()]
            }

            df_sunburst = pd.DataFrame(data)
            df_sunburst["Log Values"] = np.log1p(df_sunburst["Values"])
            df_sunburst["Child"] = df_sunburst["Child"] + ": " + df_sunburst["Values"].astype(str)

            fig39 = px.sunburst(df_sunburst, path=["Parent", "Child"], values="Values", hover_data=["Values"])
            fig39.update_traces(hovertemplate="Value: %{customdata[0]}")
            st.plotly_chart(fig39, key = 'chart39')

            st.markdown("### • Venue Based Toss Impact")
            st.write("Note: Matches with 'No Result' outcome are excluded")

            venue_toss_impact = season_analysis.venue_toss_impact(selected_season3).sort_values(by = 'Win %', ascending = False, ignore_index = True)
            venue_toss_impact.index = range(1, len(venue_toss_impact)+1)
            fig40 = px.bar(venue_toss_impact, x = 'City', y = 'Win %', color = 'City', text_auto = True, hover_data = ['Total Matches', 'Won Toss & Match'], title = 'Impact of Toss on Match Wins across Venues')
            st.plotly_chart(fig40, key = 'chart40')

            if st.checkbox("View Table: Venue-Toss Impact"):
                st.table(venue_toss_impact)
            
            st.markdown("### • Venue Based Toss Decision Impact")
            fig41 = px.bar(season_analysis.venue_toss_decision_impact(selected_season3), x = 'City', y = 'Win %', color = 'Toss Decision', barmode = 'group', text_auto = True, hover_data = ['Total Matches', 'Won Toss & Match'], title = 'Venue Based Toss Decison & Success Rate')
            st.plotly_chart(fig41, key = 'chart41')

            if st.checkbox("View Table: Venue-Toss Decision Impact"):
                st.table(season_analysis.venue_toss_decision_impact(selected_season3))

        if season_visualizations == "Top 'N' Stats":
            season_top_stats= st.sidebar.radio('Top Stats', ('Team', 'Batsman', 'Bowler', 'Fielder'))

            if season_top_stats == 'Team':
                options5 = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
                selected_season4 = st.multiselect("Select Season(s) for Insights", options = options5, default = 'All')

                if 'All' in selected_season4:
                    selected_season4 = 'All'
                else:
                    selected_season4 = [team for team in selected_season4 if team != 'All']
                    
                if selected_season4 == 'All':
                    st.write("You've have selected 'All'")
                else:
                    st.write(f"You've selected: {sorted(selected_season4)}")

                if not selected_season4:
                    st.warning("⚠️ Please select at least one option!")
                
                n_value12 = st.slider("Slide to select count", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value12} - Team Scores for Seasons - {selected_season4}")
                fig42 = px.bar(season_analysis.top_team_scores(selected_season4).head(n_value12), x = 'Team', y = 'Score', color = 'Season',text_auto = True, hover_data = ['Season'])
                st.plotly_chart(fig42, key = 'chart42')

                n_value13 = st.slider("Use slider to select value", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value13} - 200+ Scores for Seasons - {selected_season4}")
                fig43 = px.bar(season_analysis.top_team_200_plus_scores(selected_season4).head(n_value13), x = 'Team', y = 'Count', color = 'Season',text_auto = True, hover_data = ['Season'])
                st.plotly_chart(fig43, key = 'chart43')

                st.markdown(f"### • Team - Century Count for Season(s)- {selected_season4}")
                fig44 = px.bar(season_analysis.top_team_centuries(selected_season4), x = 'Team', y = 'Count', color = 'Season',text_auto = True, hover_data = ['Season'])
                st.plotly_chart(fig44, key = 'chart44')

                st.markdown(f"### • Team - Half Century Count for Season(s)- {selected_season4}")
                fig45 = px.bar(season_analysis.top_team_half_centuries(selected_season4), x = 'Team', y = 'Count', color = 'Season',text_auto = True, hover_data = ['Season'])
                st.plotly_chart(fig45, key = 'chart45')

            if season_top_stats == 'Batsman':
                options6 = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
                selected_season5 = st.multiselect("Select Season(s) for Batsman Insights", options = options6, default = 'All')

                if 'All' in selected_season5:
                    selected_season5 = 'All'
                else:
                    selected_season5 = [team for team in selected_season5 if team != 'All']
                    
                if selected_season5 == 'All':
                    st.write("You've have selected 'All'")
                else:
                    st.write(f"You've selected: {sorted(selected_season5)}")

                if not selected_season5:
                    st.warning("⚠️ Please select at least one option!")

                n_value14 = st.slider("Slide and select", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value14} - Leading Scorer for Season(s) - {selected_season5}")
                fig46 = px.bar(season_analysis.top_leading_run_scorer(selected_season5).head(n_value14), x = 'Batsman', y = 'Runs', color = 'Runs',text_auto = True, hover_data = ['Batsman'], color_continuous_scale = 'sunset')
                st.plotly_chart(fig46, key = 'chart46')

                n_value15 = st.slider("Slide for selection", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value15} - Highest Individual Scores for Season(s) - {selected_season5}")
                fig47 = px.bar(season_analysis.top_individual_score(selected_season5).head(n_value15), x = 'Batsman', y = 'Runs', color = 'Runs',text_auto = True, hover_data = ['Batsman'], color_continuous_scale = 'viridis')
                st.plotly_chart(fig47, key = 'chart47')

                # n_value16 = st.slider("Select appropriate value", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top - Most Centuries for Season(s) - {selected_season5}")
                fig48 = px.bar(season_analysis.top_batsman_centuries(selected_season5), x = 'Batsman', y = 'Count', color = 'Season',text_auto = True, hover_data = ['Season'])
                st.plotly_chart(fig48, key = 'chart48')

                n_value16 = st.slider("Select value for count", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value16}- Most Half Centuries for Season(s) - {selected_season5}")
                fig49 = px.bar(season_analysis.top_batsman_half_centuries(selected_season5).head(n_value16), x = 'Batsman', y = 'Count', color = 'Batsman', text_auto = True, hover_data = ['Count'])
                st.plotly_chart(fig49, key = 'chart49')

                n_value17 = st.slider("Select appropriate value", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value17}- Most 6's for Season(s) - {selected_season5}")
                fig50 = px.bar(season_analysis.boundaries(seasons = selected_season5, boundary = 6).head(n_value17), x = 'Batsman', y = 'Count', color = 'Batsman',text_auto = True, hover_data = ['Batsman'])
                st.plotly_chart(fig50, key = 'chart50')

                n_value18 = st.slider("Slide for setting value", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value18}- Most 4's for Season(s) - {selected_season5}")
                fig51 = px.bar(season_analysis.boundaries(seasons = selected_season5, boundary = 4).head(n_value18), x = 'Batsman', y = 'Count', color = 'Batsman',text_auto = True, hover_data = ['Batsman'])
                st.plotly_chart(fig51, key = 'chart51')
            
            if season_top_stats == 'Bowler':
                options7 = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
                selected_season6 = st.multiselect("Select Season(s) for Bowler Insights", options = options7, default = 'All')

                if 'All' in selected_season6:
                    selected_season6 = 'All'
                else:
                    selected_season6 = [season for season in selected_season6 if season != 'All']
                    
                if selected_season6 == 'All':
                    st.write("You've have selected 'All'")
                else:
                    st.write(f"You've selected: {sorted(selected_season6)}")

                if not selected_season6:
                    st.warning("⚠️ Please select at least one option!")
                
                n_value19 = st.slider("Set value", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value19}- Leading Wicket Takers for Season(s) - {selected_season6}")
                fig52 = px.bar(season_analysis.leading_wicket_taker(seasons = selected_season6).head(n_value19), x = 'Bowler', y = 'Wickets', color = 'Bowler',text_auto = True, hover_data = ['Bowler'])
                st.plotly_chart(fig52, key = 'chart52')

                n_value20 = st.slider("Set value for count", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value20}- Best Bowling Figures for Season(s) - {selected_season6}")
                fig53 = px.bar(season_analysis.best_bowling_figure(seasons = selected_season6).head(n_value19), x = 'Bowler', y = 'Wickets', color = 'Bowler',text_auto = True, hover_data = ['Runs'])
                st.plotly_chart(fig53, key = 'chart53')

                n_value21 = st.slider("Select desired value", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value21}- Most 4 Wickets for Season(s) - {selected_season6}")
                four_wicket_df, five_wicket_df = season_analysis.season_highlights_bowler_new(seasons = selected_season6)
                fig54 = px.bar(four_wicket_df.head(n_value21), x = 'Bowler', y = 'Wickets', color = 'Bowler',text_auto = True, hover_data = ['Wickets'])
                st.plotly_chart(fig54, key = 'chart54')

                n_value22 = st.slider("Set desired value", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value22}- Most 5+ Wickets for Season(s) - {selected_season6}")
                four_wicket_df, five_wicket_df = season_analysis.season_highlights_bowler_new(seasons = selected_season6)
                fig55 = px.bar(five_wicket_df.head(n_value22), x = 'Bowler', y = 'Wickets', color = 'Bowler',text_auto = True, hover_data = ['Wickets'])
                st.plotly_chart(fig55, key = 'chart55')
            
            if season_top_stats == 'Fielder':
                options8 = ['All', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
                selected_season7 = st.multiselect("Select Season(s) for Fielders", options = options8, default = 'All')

                if 'All' in selected_season7:
                    selected_season7 = 'All'
                else:
                    selected_season7 = [season for season in selected_season7 if season != 'All']
                    
                if selected_season7 == 'All':
                    st.write("You've have selected 'All'")
                else:
                    st.write(f"You've selected: {sorted(selected_season7)}")

                if not selected_season7:
                    st.warning("⚠️ Please select at least one option!")
                
                n_value23 = st.slider("Choose desired value for Fielders", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value23}- Most Catches for Season(s) - {selected_season7}")
                fig56 = px.bar(season_analysis.catches(selected_season7).head(n_value23), x = 'Fielder', y = 'Count', color = 'Fielder',text_auto = True, hover_data = ['Count'])
                st.plotly_chart(fig56, key = 'chart56')

                n_value24 = st.slider("Select value by using slider", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value24}- Most Stumpings for Season(s) - {selected_season7}")
                fig57 = px.bar(season_analysis.stumpings(selected_season7).head(n_value24), x = 'Fielder', y = 'Count', color = 'Fielder',text_auto = True, hover_data = ['Count'])
                st.plotly_chart(fig57, key = 'chart57')

                n_value25 = st.slider("Set desired value using slider", min_value=1, max_value=100, value = 5)
                st.markdown(f"### • Top {n_value25}- Most Run Outs for Season(s) - {selected_season7}")
                fig58 = px.bar(season_analysis.runouts(selected_season7).head(n_value25), x = 'Fielder', y = 'Count', color = 'Fielder',text_auto = True, hover_data = ['Count'])
                st.plotly_chart(fig58, key = 'chart58')

elif selection1 == 'Player-wise Insights':
    selection9 = st.sidebar.radio("Player-wise Statistics Summary", ["Batsman", "Bowler"])

    if selection9 == 'Batsman':
        st.markdown(f"### Batsman List:")
        st.write(analysis.total_batsman_list)
        player_selection = st.selectbox("Select Player", analysis.total_batsman_list)

        stats_selection = st.radio("Select Option", ['Overall Performance', 'Season on Season', 'Performance against Teams', 'Bowler Face off'], horizontal = True)

        if stats_selection == 'Overall Performance':
            st.markdown(f"### {player_selection} - {stats_selection}")
            st.markdown(f"#### • Team(s) & Season(s) where '{player_selection}' bat!")
            st.table(player_analysis.player_teams(player_selection))

            st.markdown(f"#### • Overall Stats")
            player_df = player_analysis.batsman_overall_df[player_analysis.batsman_overall_df['Batsman'] == player_selection]
            player_df['Centuries'] = player_analysis.player_century(player_selection)['Runs'].count()
            player_df['Half Centuries'] = player_analysis.player_half_century(player_selection)['Runs'].count()
            player_df = player_df[['Batsman', 'Innings', 'Runs', 'Balls', 'Centuries', 'Half Centuries', 'Sixes', 'Fours', 'Threes', 'Twos', 'Ones', 'Dots', 'Dismissals', 'Not Outs', 'Strike Rate', 'Batting Average', 'Boundary Dominance', 'Dot Ball Reliance']]
            player_df.index = range(1, len(player_df)+1)
            st.table(player_df)

            st.markdown(f"#### • Inning-wise Stats")
            df = player_analysis.player_inning_group(player_selection)
            df.index = range(1, len(df)+1)
            st.table(df)

            st.markdown(f"#### • Runs Scored by Match")
            df = player_analysis.match_runs(player_selection)
            df['Match #'] = range(1, len(df) + 1) 
            fig59 = px.line(df, x = 'Match #', y = 'Runs', markers = True, hover_data = ['Balls', 'Batsman', 'Team', 'Season', 'Inning', 'Bowling Team', 'Sixes', 'Fours', 'Threes', 'Twos', 'Ones', 'Dots'])
            fig59.update_traces(marker = {'color': 'red'})
            fig59.update_layout(xaxis = {'title': 'Matches'})
            st.plotly_chart(fig59, key = 'chart59')

            col1, col2, col3 = st.columns(3)
            with col1:
                df = player_analysis.match_runs(player_selection)
                fig60 = px.histogram(df, x = 'Runs', color = 'Inning', text_auto = True, title = 'Distribution of Runs Scored by Innings')
                fig60.update_layout(bargap = 0.05, yaxis = {'title': 'Count'})
                st.plotly_chart(fig60, key = 'chart60')
            
            with col2:
                df = player_analysis.match_runs(player_selection)
                fig61 = px.histogram(df, x = 'Sixes', color = 'Inning', text_auto = True, title = 'Distribution of Sixes Hit by Innings')
                fig61.update_layout(bargap = 0.05, yaxis = {'title': 'Count'})
                st.plotly_chart(fig61, key = 'chart61')
            
            with col3:
                df = player_analysis.match_runs(player_selection)
                fig62 = px.histogram(df, x = 'Fours', color = 'Inning', text_auto = True, title = 'Distribution of Fours Hit by Innings')
                fig62.update_layout(bargap = 0.05, yaxis = {'title': 'Count'})
                st.plotly_chart(fig62, key = 'chart62')
            
            st.markdown(f"#### • Top 'N' Performances" )
            slider_top_scores = st.slider('Slide and select as desired', min_value = 0, max_value = player_df['Innings'].max())
            
            df = player_analysis.player_top_scores(player_selection).head(slider_top_scores)
            df.index = range(1, len(df)+1)
            fig63 = px.line(df, y = 'Runs', markers = True, hover_data = ['Batsman', 'Team', 'Bowling Team', 'Season', 'Inning', 'Sixes', 'Fours', 'Threes', 'Twos', 'Ones', 'Dots'])
            fig63.update_traces(marker = {'color': 'red'})
            fig63.update_layout(xaxis = {'title': 'Index'})
            st.plotly_chart(fig63, key = 'chart63')

            st.markdown(f"#### • Match-Winning Milestones" )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"##### 100+ Impact Ratio" )
                st.write(f"Century Count - {player_analysis.player_century(player_selection)['Runs'].count()}")
                if player_analysis.player_century(player_selection)['Runs'].count() > 0:
                    won_matches = player_analysis.century_win_cause(player_selection, century = True)['Won'].sum()
                    lost_matches = player_analysis.century_win_cause(player_selection, century = True).shape[0] - won_matches
                    fig64 = px.pie(values = [won_matches, lost_matches], names = ['Matches Won', 'Matches Lost'])
                    fig64.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{value} matches<br>Percentage: %{percent}')
                    st.plotly_chart(fig64, key = 'chart64')
                else:
                    st.error("No Centuries by this player")
            with col2:
                st.markdown(f"##### 50+ Impact Ratio" )
                st.write(f"Half Century Count - {player_analysis.player_half_century(player_selection)['Runs'].count()}")
                if player_analysis.player_half_century(player_selection)['Runs'].count() > 0:
                    won_matches = player_analysis.century_win_cause(player_selection, century = False)['Won'].sum()
                    lost_matches = player_analysis.century_win_cause(player_selection, century = False).shape[0] - won_matches
                    fig65 = px.pie(values = [won_matches, lost_matches], names = ['Matches Won', 'Matches Lost'])
                    fig65.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{value} matches<br>Percentage: %{percent}')
                    st.plotly_chart(fig65, key = 'chart65')
                else:
                    st.error("No Half-Centuries by this player")

        elif stats_selection == 'Season on Season':
            st.markdown(f"### {player_selection} - {stats_selection} Stats")
            player_df1 = player_analysis.batsman_overall_df1[player_analysis.batsman_overall_df1['Batsman'] == player_selection]
            player_df1['Centuries'] = player_analysis.player_century(player_selection)['Runs'].count()
            player_df1['Half Centuries'] = player_analysis.player_half_century(player_selection)['Runs'].count()
            player_df1.index = range(1, len(player_df1)+1)

            st.markdown(f"#### • Runs Scored by Season")
            fig66 = px.line(player_df1, x = 'Season', y = 'Runs', markers = True, hover_data = ['Innings', 'Balls', 'Strike Rate', 'Batting Average', 'Sixes', 'Fours', 'Threes', 'Twos', 'Ones', 'Dots', 'Dismissals', 'Not Outs', 'Boundary Dominance', 'Dot Ball Reliance'])
            fig66.update_traces(marker = {'size': 12, 'color': 'red'})
            st.plotly_chart(fig66, key = 'chart66')

            st.markdown(f"#### • Strike Rate Vs Batting Average by Season")
            fig67 = px.scatter(player_df1, x = 'Batting Average', y = 'Strike Rate', color = 'Season')
            fig67.update_traces(marker = {'size': 18, 'opacity': 0.7})
            st.plotly_chart(fig67, key = 'chart67')

            st.markdown(f"#### • Season-wise Runs Scored - Breakdown by Innings")
            df = (
                player_analysis.match_runs(player_selection)
                .groupby(by = ['Batsman', 'Season', 'Inning'], as_index = False)
                .agg(Runs = ('Runs', 'sum'))
            )
            df['Inning'] = df['Inning'].astype('category')

            fig68 = px.bar(df, x = 'Season', y = 'Runs', color = 'Inning', barmode = 'stack', text_auto = True)
            st.plotly_chart(fig68, key = 'chart68')

            st.markdown(f"#### • Boundary % Vs Dot Ball % by Season")
            fig69 = px.scatter(player_df1, x = 'Dot Ball Reliance', y = 'Boundary Dominance', color = 'Season')
            fig69.update_traces(marker = {'size': 18, 'opacity': 0.7})
            st.plotly_chart(fig69, key = 'chart69')

        elif stats_selection == 'Performance against Teams':
            st.markdown(f"### {player_selection} - {stats_selection}")
            st.markdown(f"#### • Runs Scored against Teams")
            df = (
                player_analysis.match_runs(player_selection)
                .groupby(by = ['Batsman', 'Bowling Team'], as_index = False)
                .agg(Runs = ('Runs', 'sum'), Innings = ('Match ID', 'nunique'))
            )
            fig70 = px.bar(df, x = 'Bowling Team', y = 'Runs', color = 'Bowling Team', text_auto = True, hover_data = ['Batsman', 'Innings'])
            st.plotly_chart(fig70, key = 'chart70')

            st.markdown(f"#### • Runs Scored against Teams by Innings")
            df = (
                player_analysis.match_runs(player_selection)
                .groupby(by = ['Batsman', 'Bowling Team', 'Inning'], as_index = False)
                .agg(Runs = ('Runs', 'sum'), Innings = ('Match ID', 'nunique'))
            )
            df['Inning'] = df['Inning'].astype('category')
            fig71 = px.bar(df, x = 'Bowling Team', y = 'Runs', color = 'Inning', text_auto = True, hover_data = ['Batsman', 'Innings'])
            st.plotly_chart(fig71, key = 'chart71')

            rival_team_selection1 = st.selectbox("Select team for visualizing player performance against the team", analysis.total_teams['Team'])

            st.markdown(f"#### • Performance Metrics of {player_selection} against {rival_team_selection1}")
            df = player_analysis.batsman_against_team(player_selection, rival_team_selection1)
            df.index = range(1, len(df)+1)
            if df.empty:
                st.warning("No match data available for this player against the selected team.")
            else:
                st.table(df)

                df = player_analysis.match_runs(player_selection).query(f"`Bowling Team` == '{rival_team_selection1}'")
                df['Match #'] = range(1, len(df) + 1) 
                st.markdown(f"#### • Match-wise Runs Scored against {rival_team_selection1}")
                fig72 = px.line(df, x = 'Match #', y = 'Runs', markers = True, hover_data = ['Balls', 'Batsman', 'Team', 'Season', 'Inning', 'Bowling Team', 'Sixes', 'Fours', 'Threes', 'Twos', 'Ones', 'Dots'])
                fig72.update_traces(marker = {'color': 'red'})
                fig72.update_layout(xaxis = {'title': 'Matches'})
                st.plotly_chart(fig72, key = 'chart72')

                col1, col2, col3 = st.columns(3)
                df = player_analysis.match_runs(player_selection).query(f"`Bowling Team` == '{rival_team_selection1}'")
                with col1:
                    fig73 = px.histogram(df, x = 'Runs', color = 'Inning', text_auto = True, title = 'Distribution of Runs Scored by Innings')
                    fig73.update_layout(bargap = 0.05, yaxis = {'title': 'Count'})
                    st.plotly_chart(fig73, key = 'chart73')
                
                with col2:
                    fig74 = px.histogram(df, x = 'Sixes', color = 'Inning', text_auto = True, title = 'Distribution of Sixes Hit by Innings')
                    fig74.update_layout(bargap = 0.05, yaxis = {'title': 'Count'})
                    st.plotly_chart(fig74, key = 'chart74')
                
                with col3:
                    fig75 = px.histogram(df, x = 'Fours', color = 'Inning', text_auto = True, title = 'Distribution of Fours Hit by Innings')
                    fig75.update_layout(bargap = 0.05, yaxis = {'title': 'Count'})
                    st.plotly_chart(fig75, key = 'chart75')

        elif stats_selection == 'Bowler Face off':
            st.markdown(f"### {player_selection} - {stats_selection}")
            st.markdown(f"#### • Dismissal Type")
            edition = st.selectbox("Select season of your choice", ['All'] + sorted(analysis.matches['season'].unique().tolist()))
            fig76 = px.bar(player_analysis.player_dismissal_type(player_selection, edition), x = 'Count', y = 'Dismissal Kind', orientation='h', title=f" {player_selection} Dismissal Types", color='Dismissal Kind', text_auto = True)
            st.plotly_chart(fig76, key = 'chart76')

            st.markdown(f"#### • Dismissal Type by Bowler")
            fig77 = px.bar(player_analysis.player_dismissal_bowler(player_selection, edition), x = 'Count', y = 'Dismissal Kind', orientation='h', title=f" {player_selection} Dismissal Types by Bowler", color='Dismissal Kind', hover_data = ['Bowler'], text_auto = True)
            st.plotly_chart(fig77, key = 'chart77')

            st.markdown(f"#### • Batsman Vs Bowler: Rivalry")
            st.write(f"Performance of '{player_selection}' against top (max 10) Bowlers who have dismissed him the most!")
            top_rival_bowlers_list = player_analysis.top_rival_bowler(player_selection)['Bowler'].head(10).values
            st.write(f"Rival Bowlers: {", ".join(top_rival_bowlers_list)}")
            rival_bowler = st.selectbox("Select Rival Bowler", top_rival_bowlers_list)

            st.markdown(f"#### • {player_selection} Vs {rival_bowler}")

            df = player_analysis.performance_rival_bowler(player_selection)
            df.index = range(1, len(df)+1)
            if not df.empty:
            # st.table(df)
                rival_bowler_df = df.query(f"Bowler == '{rival_bowler}'")
                balls = rival_bowler_df['Balls']
                runs = rival_bowler_df['Runs']
                dismissals = rival_bowler_df['Dismissals']
                sixes = rival_bowler_df["6's"]
                fours = rival_bowler_df["4's"]
                threes = rival_bowler_df["3's"]
                twos = rival_bowler_df["2's"]
                ones = rival_bowler_df["1's"]
                dots = rival_bowler_df["Dots"]
                sr = rival_bowler_df["Strike Rate"]
                avg = rival_bowler_df["Batting Average"]
                dot_percent = rival_bowler_df["Dot %"]

                st.write('-------------------------------------')
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown('<h2 style="font-size:24px;"> Runs Scored </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= runs , label_visibility = 'hidden')
                with col2:
                    st.markdown('<h2 style="font-size:24px;"> Balls Faced </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= balls, label_visibility = 'hidden')
                with col3:
                    st.markdown('<h2 style="font-size:24px;"> Dissmissal Count </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= dismissals, label_visibility = 'hidden')
                with col4:
                    st.markdown('<h2 style="font-size:24px;"> Six Hit Count </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= sixes , label_visibility = 'hidden')

                st.write('-------------------------------------')

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown('<h2 style="font-size:24px;"> Four Hit Count </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= fours , label_visibility = 'hidden')
                with col2:
                    st.markdown('<h2 style="font-size:24px;"> Threes Count </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= threes, label_visibility = 'hidden')
                with col3:
                    st.markdown('<h2 style="font-size:24px;"> Twos Count </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= twos, label_visibility = 'hidden')
                with col4:
                    st.markdown('<h2 style="font-size:24px;"> Ones Count </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= ones, label_visibility = 'hidden')

                st.write('-------------------------------------')

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown('<h2 style="font-size:24px;"> Dots Count </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= dots , label_visibility = 'hidden')
                with col2:
                    st.markdown('<h2 style="font-size:24px;"> Dot Ball % </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= dot_percent, label_visibility = 'hidden')
                with col3:
                    st.markdown('<h2 style="font-size:24px;"> Strike Rate </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= sr, label_visibility = 'hidden')
                with col4:
                    st.markdown('<h2 style="font-size:24px;"> Batting Average </h2>', unsafe_allow_html=True)
                    st.metric(label="12", value= avg, label_visibility = 'hidden')

                st.write('-------------------------------------')
                
                st.markdown(f"#### • Performance against Top (max 10) Rival Bowlers")
                st.markdown(f"##### Strike Rate Vs Batting Average")
                fig78 = px.scatter(player_analysis.performance_rival_bowler(player_selection), x = 'Batting Average', y = 'Strike Rate', hover_data = ['Dismissals', 'Balls', 'Runs', 'Dot %'], color = 'Bowler')
                fig78.update_traces(marker = {'size': 18, 'opacity': 0.7})
                st.plotly_chart(fig78, key = 'chart78')

            else:
                st.warning("No matching data!")


    if selection9 == 'Bowler':
        st.markdown(f"### Bowler List:")
        st.write(analysis.total_bowlers_list)

        bowler_selection = st.selectbox("Select Player", analysis.total_bowlers_list)
        stats_selection_bowler = st.radio("Select Option", ['Overall Performance', 'Season on Season', 'Performance against Teams'], horizontal = True)

        if stats_selection_bowler == 'Overall Performance':
            st.markdown(f"### {bowler_selection} - {stats_selection_bowler}")
            st.markdown(f"#### • Team(s) & Season(s) where '{bowler_selection}' bowl!")
            st.table(player_analysis.bowler_teams(bowler_selection))

            st.markdown(f"#### • Overall Stats")
            df = analysis.bowler_stats.query(f"Bowler == '{bowler_selection}'")
            df = df[['Bowler','Matches','Wickets','Balls','Overs','Runs Conceded','Dot Balls','Economy Rate','Bowling Average','Strike Rate','Wicket per Match','Boundary Rate','Dot Ball %','Sixes Conceded','Fours Conceded','Threes Conceded','Twos Conceded','Ones Conceded','Extras Conceded']]
            df['Boundary Rate'] = round(df['Boundary Rate']*100, 4)
            df = df.rename(columns = {'Sixes Conceded': '6s Conceded', 'Fours Conceded': '4s Conceded', 'Threes Conceded': '3s Conceded', 'Twos Conceded': '2s Conceded', 'Ones Conceded': '1s Conceded', 'Extras Conceded': 'Extra Runs', 'Boundary Rate': 'Boundary %'})
            df.index = range(1, len(df)+1)
            st.table(df)

            st.markdown(f"#### • Inning-wise Stats")
            df = player_analysis.bowler_stats_innings(bowler_selection)
            df.index = range(1, len(df)+1)
            st.table(df)

            st.markdown(f"#### • Wickets by Match")
            df = player_analysis.bowler_stats_overall.query(f"bowler == '{bowler_selection}'")
            df['Match #'] = range(1, len(df) + 1) 
            fig79 = px.line(df, x = 'Match #', y = 'wickets', markers = True, hover_data = ['balls', 'bowler', 'bowling_team', 'season', 'inning', 'batting_team', 'runs_conceded', 'economy_rate','bowling_average', 'strike_rate', 'dot_ball_percent'])
            fig79.update_traces(marker = {'color': 'red'})
            fig79.update_layout(xaxis = {'title': 'Matches'}, yaxis = {'title': 'Wickets'})
            st.plotly_chart(fig79, key = 'chart59')

            df = player_analysis.bowler_stats_overall.query(f"bowler == '{bowler_selection}'")
            fig80 = px.histogram(df, x = 'wickets', color = 'inning', text_auto = True, title = 'Distribution of Wickets by Innings')
            fig80.update_layout(bargap = 0.05, yaxis = {'title': 'Count'})
            st.plotly_chart(fig80, key = 'chart80')

            st.markdown(f"#### • Top 'N' Performances" )
            df = player_analysis.bowler_stats_overall.query(f"bowler == '{bowler_selection}'")
            df = df.sort_values(by = ['wickets', 'runs_conceded'], ascending = [False, True], ignore_index = True)
            df.index = range(1, len(df)+1)
            max_value_wickets = (
                player_analysis.bowler_stats_overall
                .groupby(by = 'bowler', as_index = False)
                .agg(Wickets = ('wickets', 'sum'))
                .query(f"bowler == '{bowler_selection}'")
                ['Wickets'].max()
                )
            slider_top_wickets = st.slider('Slide and select value', min_value = 0, max_value = max_value_wickets)
            fig81 = px.line(df.head(slider_top_wickets), y = 'wickets', markers = True, hover_data = ['runs_conceded'])
            fig81.update_traces(marker = {'color': 'red'})
            fig81.update_layout(xaxis = {'title': 'Index'})
            st.plotly_chart(fig81, key = 'chart81')
        
        elif stats_selection_bowler == 'Season on Season':
            st.markdown(f"### {bowler_selection} - {stats_selection_bowler} Stats")
            st.markdown(f"#### • Wickets by Season")
            df = player_analysis.bowler_stats_seasons(bowler_selection)
            df.index = range(1, len(df)+1)
            fig82 = px.line(df, x = 'Season', y = 'Wickets', markers = True, hover_data = ['Balls', 'Overs', 'Runs Conceded', 'Economy Rate', 'Bowling Average', 'Strike Rate', 'Boundary Rate', 'Dot Ball %', 'Extra Runs', '6s Conceded', '4s Conceded'])
            fig82.update_traces(marker = {'size': 12, 'color': 'red'})
            st.plotly_chart(fig82, key = 'chart82')
            
            st.markdown(f"#### • Distribution of Wickets by Season & Innings")
            df = player_analysis.bowler_stats_seasons_inning(bowler_selection)
            df.index = range(1, len(df)+1)
            fig83 = px.line(df, x = 'Season', y = 'Wickets', color = 'Inning', color_discrete_sequence = ['red', 'skyblue'], markers = True, hover_data = ['Balls', 'Overs', 'Runs Conceded', 'Economy Rate', 'Bowling Average', 'Strike Rate', 'Boundary Rate', 'Dot Ball %', 'Extra Runs', '6s Conceded', '4s Conceded'])
            fig83.update_traces(marker = {'size': 8, 'color': 'blue'})
            st.plotly_chart(fig83, key = 'chart83')

            st.markdown(f"#### • Bowling Efficiency Matrix: Average Vs Economy with Strike Rate Emphasis")
            st.write("Note: Size of markers denote Strike Rate (Balls per Wicket)")
            df = player_analysis.bowler_stats_seasons(bowler_selection)
            fig84 = px.scatter(df, x = 'Economy Rate', y = 'Bowling Average', color = 'Season', size = 'Strike Rate')
            fig84.update_layout(xaxis = {'title': 'Economy Rate (Runs per Over)'}, yaxis = {'title': 'Bowling Average (Runs per Wicket)'})
            st.plotly_chart(fig84, key = 'chart84')

            st.markdown(f"#### • Bowling Containment Map: Dot Ball % Vs Boundary %")
            df = player_analysis.bowler_stats_seasons(bowler_selection)
            fig85 = px.scatter(df, x = 'Dot Ball %', y = 'Boundary Rate', color = 'Season', hover_data = ['Season', 'Wickets'])
            fig85.update_layout(yaxis = {'title': 'Boundary %'})
            fig85.update_traces(marker = {'size': 18, 'opacity': 0.7})
            st.plotly_chart(fig85, key = 'chart85')
        
        else:
            st.markdown(f"### {bowler_selection} - {stats_selection_bowler}")
            st.markdown(f"#### • Wickets taken against Teams")
            fig86 = px.bar(player_analysis.bowler_stats_teams(bowler_selection), x = 'Rival Team', y = 'Wickets', color='Rival Team', text_auto = True, hover_data = ['Matches', 'Overs', 'Runs Conceded', 'Economy Rate', 'Bowling Average', 'Strike Rate'])
            st.plotly_chart(fig86, key = 'chart86')

            rival_team_choice = st.selectbox("Select any Rival Team", analysis.total_teams['Team'])

            st.markdown(f"#### • Performance Metrics of '{bowler_selection}' against '{rival_team_choice}'")
            df = player_analysis.bowler_stats_teams(bowler_selection).query(f"`Rival Team` == '{rival_team_choice}'")
            df.index = range(1, len(df)+1)
            if df.empty:
                st.warning("No match data available for this player against the selected team.")
            else:
                st.table(df)

            st.markdown(f"#### • Performance Metrics of '{bowler_selection}' against '{rival_team_choice}' - Breakdown by Season")
            seasons = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
            season_choice = st.selectbox("Select any Season", options = seasons)
            df = player_analysis.bowler_stats_teams_season(bowler_selection, rival_team_choice).query(f"Season == '{season_choice}'")
            df.index = range(1, len(df)+1)
            if df.empty:
                st.warning("No match data available for this player against the selected team or season.")
            else:
                st.table(df)

            st.markdown(f"#### • Match-wise Wickets taken by '{bowler_selection}' against '{rival_team_choice}'")
            df = player_analysis.bowler_stats_overall.query(f"bowler == '{bowler_selection}' & batting_team == '{rival_team_choice}'")
            df.index = range(1, len(df)+1)
            fig87 = px.line(df, y = 'wickets', color = 'inning', color_discrete_sequence = ['red', 'skyblue'], markers = True, hover_data = 'season', labels = {'inning': 'Inning'})
            fig87.update_traces(marker = {'size': 8, 'color': 'blue'})
            fig87.update_layout(xaxis = {'title': 'Matches'}, yaxis =  {'title': 'Wickets'})
            st.plotly_chart(fig87, key = 'chart87') 

            st.markdown(f"#### • Distribution of Wickets taken by '{bowler_selection}' against '{rival_team_choice}'")
            df = player_analysis.bowler_stats_overall.query(f"bowler == '{bowler_selection}' & batting_team == '{rival_team_choice}'")
            df.index = range(1, len(df)+1)
            fig88 = px.histogram(df, x = 'wickets', color = 'inning', text_auto = True, title = 'Distribution of Wickets by Innings')
            fig88.update_layout(bargap = 0.05, yaxis = {'title': 'Count'})
            st.plotly_chart(fig88, key = 'chart88')



            



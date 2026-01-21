import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympics Analysis')
user_menu= st.sidebar.radio('Select an Option',
                            ('Medal Tally', 'Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'))
if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    year,country = helper.country_year_list(df)
    selected_year=st.sidebar.selectbox('Select Year', year)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Medal Tally')
    if selected_year=='Overall' and selected_country!='Overall':
        st.title('Overall Medal Tally for '+selected_country)
    if selected_year!='Overall' and selected_country=='Overall':
        st.title('Medal Tally for all countries during ' + str(selected_year))
    if selected_year!='Overall' and selected_country!='Overall':
        st.title('Medal Tally for '+ selected_country+' in ' + str(selected_year))

    st.table(medal_tally)

if user_menu=='Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes= df['Name'].unique().shape[0]
    nations= df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.subheader(editions)
    with col2:
        st.header('Hosts')
        st.subheader(cities)
    with col3:
        st.header('Sports')
        st.subheader(sports)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header('Events')
        st.subheader(events)
    with col5:
        st.header('Nations')
        st.subheader(nations)
    with col6:
        st.header('Athletes')
        st.subheader(athletes)
    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x='Year', y='Number of Countries')
    st.title('')
    st.title('Nations Over Time')
    st.plotly_chart(fig)
    events_over_time = helper.participating_events_over_time(df)
    fig1 = px.line(events_over_time, x='Year', y='Number of Events')
    st.title('')
    st.title('Events Over Time')
    st.plotly_chart(fig1)
    athletes_over_time = helper.participating_athletes_over_time(df)
    fig2 = px.line(athletes_over_time, x='Year', y='Number of Athletes')
    st.title('')
    st.title('Athletes Over Time')
    st.plotly_chart(fig2)
    st.title('')
    st.title('Events of each Sport over Time')
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count', ).fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

if user_menu=='Country-wise Analysis':
    country_list = df['region'].unique().astype(str).tolist()
    country_list.sort()
    country = st.sidebar.selectbox('Select a Country', country_list)
    st.title('Medal plot of ' + country)
    country_analysis=helper.country_analysis(df,country)
    fign = px.line(country_analysis, x='Year', y='Medal')
    st.plotly_chart(fign)
    st.title('')
    st.title('Sport-wise Performance of ' + country)
    country_heatmap=helper.country_sport(df,country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(country_heatmap, annot=True)
    st.pyplot(fig)
    st.title('')
    st.title('Top 15 athletes of ' + country)
    country_ath=helper.most_successful(df,country)
    st.table(country_ath)

if user_menu=='Athlete-wise Analysis':
    st.title('Age Distribution')
    ath_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = ath_df['Age'].dropna()
    x2 = ath_df[ath_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = ath_df[ath_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = ath_df[ath_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=600)
    st.plotly_chart(fig)

    sp = df['Sport'].value_counts().reset_index().truncate(after=41)
    famous_sports = sp['Sport'].tolist()
    x = []
    name = []
    for sport in famous_sports:
        temp_df = ath_df[ath_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=600)
    st.title('Sport-wise Age Distribution- Gold Medalist')
    st.plotly_chart(fig)

    x = []
    name = []
    for sport in famous_sports:
        temp_df = ath_df[ath_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=600)
    st.title('Sport-wise Age Distribution- Silver Medalist')
    st.plotly_chart(fig)

    st.title('Sport-wise Height vs Weight Scatter Plot')
    sport= st.selectbox('Select Sport', df['Sport'].unique().tolist())
    ath_df = df.drop_duplicates(subset=['Name', 'region'])
    ath_df['Medal'].fillna('No Medal', inplace=True)
    temp_df = ath_df[ath_df['Sport'] == sport]
    fig, ax= plt.subplots()
    ax= sns.scatterplot(x=temp_df['Weight'], y=ath_df['Height'], hue=temp_df["Medal"], style=temp_df['Sex'])
    st.pyplot(fig)

    st.title('Men and Women participation')
    men = ath_df[ath_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = ath_df[ath_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left').rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}).fillna(0)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)


import pandas as pd
import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    medal_tally.rename(columns={'region': 'Region'}, inplace=True)
    return medal_tally

def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return year,country

def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year').reset_index().drop(['index'], axis=1)
    nations_over_time.rename(columns={'count': 'Number of Countries'}, inplace=True)
    return nations_over_time

def participating_events_over_time(df):
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year').reset_index().drop(['index'], axis=1)
    events_over_time.rename(columns={'count': 'Number of Events'}, inplace=True)
    return events_over_time

def participating_athletes_over_time(df):
    athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('Year').reset_index().drop(['index'], axis=1)
    athletes_over_time.rename(columns={'count': 'Number of Athletes'}, inplace=True)
    return athletes_over_time

def country_analysis(df,country):
    z = df.drop_duplicates(['Year', 'Sport', 'Event', 'Medal', 'Team', 'NOC', 'Games', 'City'])
    temp_df = z.dropna(subset=['Medal'])
    new_df=temp_df[temp_df['region']==country]
    new_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return new_df

def country_sport(df,country):
    z=df.drop_duplicates(['Year', 'Sport','Event','Medal','Team','NOC','Games','City'])
    temp_df=z.dropna(subset=['Medal'])
    new_df=temp_df[temp_df['region']==country]
    new_df=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return new_df

def most_successful(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df[temp_df['region']==country]
    ath=temp_df['Name'].value_counts()
    ath=ath.reset_index().head(15).merge(df,on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates().reset_index().drop(['index'],axis=1).drop(['region'],axis=1)
    return ath

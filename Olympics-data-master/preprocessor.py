import pandas as pd
def preprocess(df, region_df):
    df = df[df['Season']=='Summer']
    df = pd.merge(df, region_df, left_on=['NOC'], right_on=['NOC'], how='left', suffixes=('', '_drop'))
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)
    return df
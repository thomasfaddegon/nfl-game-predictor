import pandas as pd
import os

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to next line

def load_and_clean_offense_defense_data (year):
    #check if the current working directory is backend, if not prepend it (for running from the root directory of the project)
    cwd = os.getcwd()
    prefix = '' if cwd.endswith('backend') else 'backend/'

    # Load the offense and defense data, rename the columns and drop unnecessary columns
    offense_passing_df = pd.read_csv(f'{prefix}data/{year}/offense_passing_{year}.csv', index_col=0)
    offense_passing_df.columns = ['Offense_Passing_' + col for col in offense_passing_df.columns]
    offense_passing_df = offense_passing_df.drop('Offense_Passing_SACK YDS', axis=1)

    offense_rushing_df = pd.read_csv(f'{prefix}data/{year}/offense_rushing_{year}.csv', index_col=0)
    offense_rushing_df.columns = ['Offense_Rushing_' + col for col in offense_rushing_df.columns]

    defense_passing_df = pd.read_csv(f'{prefix}data/{year}/defense_passing_{year}.csv', index_col=0)
    defense_passing_df.columns = ['Defense_Passing_' + col for col in defense_passing_df.columns]
    defense_passing_df = defense_passing_df.drop('Defense_Passing_Unnamed: 2', axis=1)

    defense_rushing_df = pd.read_csv(f'{prefix}data/{year}/defense_rushing_{year}.csv', index_col=0)
    defense_rushing_df.columns = ['Defense_Rushing_' + col for col in defense_rushing_df.columns]
    defense_rushing_df = defense_rushing_df.drop('Defense_Rushing_Unnamed: 2', axis=1)

    # Convert Time of Possession to seconds
    offense_rushing_df['Offense_Rushing_TOP'] = offense_rushing_df['Offense_Rushing_TOP'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))
    defense_rushing_df['Defense_Rushing_TOP'] = defense_rushing_df['Defense_Rushing_TOP'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))

    # Merge the rushing and passing data for offense and defense
    offense_combined_df = pd.merge(offense_passing_df, offense_rushing_df, left_on='Offense_Passing_TEAM', right_on='Offense_Rushing_TEAM')
    defense_combined_df = pd.merge(defense_passing_df, defense_rushing_df, left_on='Defense_Passing_TEAM', right_on='Defense_Rushing_TEAM')

    return offense_combined_df, defense_combined_df

def get_team_name(team_acronym):
    acronym_to_name = {
        "ARI": "Cardinals",
        "ATL": "Falcons",
        "BAL": "Ravens",
        "BUF": "Bills",
        "CAR": "Panthers",
        "CHI": "Bears",
        "CIN": "Bengals",
        "CLE": "Browns",
        "DAL": "Cowboys",
        "DEN": "Broncos",
        "DET": "Lions",
        "GB": "Packers",
        "HOU": "Texans",
        "IND": "Colts",
        "JAX": "Jaguars",
        "KC": "Chiefs",
        "LAC": "Chargers",
        "LV": "Raiders",
        "MIA": "Dolphins",
        "MIN": "Vikings",
        "NE": "Patriots",
        "NO": "Saints",
        "NYG": "Giants",
        "NYJ": "Jets",
        "OAK": "Raiders",
        "PHI": "Eagles",
        "PIT": "Steelers",
        "SD": "Chargers",
        "SEA": "Seahawks",
        "SF": "49ers",
        "STL": "Rams",
        "LA": "Rams",
        "TB": "Buccaneers",
        "TEN": "Titans",
        "WAS": "Commanders",
    }

    return acronym_to_name.get(team_acronym, "Unknown")


def get_team_acronym(team_name):
    team_acronyms = {
        "49ers": "SF",
        "Bears": "CHI",
        "Bengals": "CIN",
        "Bills": "BUF",
        "Broncos": "DEN",
        "Browns": "CLE",
        "Buccaneers": "TB",
        "Cardinals": "ARI",
        "Chargers": "LAC",
        "Chiefs": "KC",
        "Colts": "IND",
        "Cowboys": "DAL",
        "Dolphins": "MIA",
        "Eagles": "PHI",
        "Falcons": "ATL",
        "Giants": "NYG",
        "Jaguars": "JAX",
        "Jets": "NYJ",
        "Lions": "DET",
        "Packers": "GB",
        "Panthers": "CAR",
        "Patriots": "NE",
        "Raiders": "LV",
        "Rams": "LA",
        "Ravens": "BAL",
        "Saints": "NO",
        "Seahawks": "SEA",
        "Steelers": "PIT",
        "Texans": "HOU",
        "Titans": "TEN",
        "Vikings": "MIN"
    }

    return team_acronyms.get(team_name, "Unknown")

def remove_features_from_dataframe(df):

    features_to_remove = [
        'Offense_Passing_PTS/G', 'Offense_Rushing_PTS/G',
        'Offense_Rushing_TOTAL PTS', 'Offense_Passing_TOTAL PTS',
        'Defense_Rushing_TOTAL PTS, Defense_Passing_TOTAL PTS',
    ]

    return df.drop(columns=features_to_remove, errors='ignore')



# features_to_remove = ['Offense_Passing_PTS/G', 'Offense_Rushing_PTS/G', 'Offense_Rushing_TOTAL PTS', 'Offense_Passing_TOTAL PTS', 'Defense_Rushing_TOTAL PTS',
    #                         'Defense_Passing_SACK YDS', 'Offense_Passing_SACKS',
    #                         'Defense_Passing_TD', 'Defense_Rushing_TOP', 'Defense_Rushing_ATT',
    #                         'Offense_Passing_INT', 'Offense_Rushing_ATT', 'Offense_Rushing_YDS/ATT',
    #                         'Offense_Rushing_TOP', 'Offense_Rushing_YDS']
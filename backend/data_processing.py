import pandas as pd
from utils.constants import PROGRAM_DIRECTORY, PROGRAM_NAMES

df = pd.read_excel(
    PROGRAM_DIRECTORY / "resultat-ansokningsomgang-2024.xlsx",
    sheet_name="Tabell 3",
    skiprows=5,
)
df_list= []
for value in PROGRAM_NAMES.values():
    temp_df = pd.read_excel(
        PROGRAM_DIRECTORY / value,
        sheet_name="Tabell 3",
        skiprows=5,
        
    )
    df_list.append(temp_df)
df_merged = pd.concat(df_list, sort=False, ignore_index=True)

df_list1= []
for value in [2020, 2021, 2022]:
    temp_df1 = pd.read_excel(
        PROGRAM_DIRECTORY / PROGRAM_NAMES[value],
        sheet_name="Tabell 4",
    )[['Sökta platser totalt', 'Beviljade platser totalt']]
    temp_df1['År'] = value
    df_list1.append(temp_df1)
df_merged1 = pd.concat(df_list1, sort=False, ignore_index=True)

df_platser = df_merged.copy()
df_platser = df_platser[['Sökta platser totalt', 'Beviljade platser totalt', 'År']].dropna(subset='Sökta platser totalt')
df_platser = pd.concat([df_merged1, df_platser], sort=False, ignore_index=True)

df_sum = df_platser.copy()
df_sum = df_sum.groupby('År')[['Sökta platser totalt', 'Beviljade platser totalt']].sum().reset_index()

def filter_df_bar(df, educational_area="Data/IT", area="Kommun"):
    return (
        df.query("Utbildningsområde == @educational_area")[area]
        .value_counts()
        .reset_index()
        .rename({"count": "Ansökta utbildningar"}, axis=1)
    )

def filter_education(df, educational_area="Data/IT"):
    return (
        df.query("Utbildningsområde == @educational_area")
    )

def filter_decision(df):
    return(
        df["Beslut"]
        .value_counts()
        .reset_index()
        .rename({"count": "Ansökta utbildningar"}, axis=1)
    )

<<<<<<< HEAD
=======
def filter_year(df, min_year, max_year):
    return(
        df[(df['År'] <= max_year) & (df['År'] >= min_year)]
    )
>>>>>>> 56d65713d1c57da2068bbc91dbdc7e84d6b9125b

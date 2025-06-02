import pandas as pd
from utils.constants import PROGRAM_DIRECTORY, PROGRAM_NAMES, COURSE_DIRECTORY, COURSE_NAMES

#Skapar en dataframe med data från 2020-2024 för program
df_list= []
for value in PROGRAM_NAMES.values():
    temp_df = pd.read_excel(
        PROGRAM_DIRECTORY / value,
        sheet_name="Tabell 3",
        skiprows=5,
        
    )
    df_list.append(temp_df)
df_merged = pd.concat(df_list, sort=False, ignore_index=True)

#Skapar en temporär lista om platser från 2020-2021 för att kombineras senare
df_list1= []
for value in [2020, 2021, 2022]:
    temp_df1 = pd.read_excel(
        PROGRAM_DIRECTORY / PROGRAM_NAMES[value],
        sheet_name="Tabell 4",
    )[['Utbildningsområde', 'Sökta platser totalt', 'Beviljade platser totalt']]
    temp_df1['År'] = value
    df_list1.append(temp_df1)
df_merged1 = pd.concat(df_list1, sort=False, ignore_index=True)

#Använder datan från den temporära df_merged1 och datan från df_merged för att skapa en dataframe från 2020-2024 om programs platser
df_platser = df_merged.copy()
df_platser = df_platser[['Utbildningsområde', 'Sökta platser totalt', 'Beviljade platser totalt', 'År']].dropna(subset='Sökta platser totalt')
df_platser = pd.concat([df_merged1, df_platser], sort=False, ignore_index=True)

#Summerar antalet platser från df_platser per år inom ett utbildningsområde
df_sum = df_platser.copy()
educational_area = 'Data/IT'
df_sum = df_sum.query('Utbildningsområde == @educational_area')
df_sum = df_sum.groupby('År')[['Sökta platser totalt', 'Beviljade platser totalt']].sum().reset_index()

#Skapar en dataframe df_course med data om kurser
df_list5= []
for value in COURSE_NAMES["Resultat"].values():
    temp_df5 = pd.read_excel(
        COURSE_DIRECTORY / value,
        sheet_name="Lista ansökningar"   
    )
    df_list5.append(temp_df5)
df_course = pd.concat(df_list5, sort=False, ignore_index=True).drop(columns='Diarienummer')
df_course["Beslut"] = df_course['Beslut'].fillna('Beviljad')
df_course['Kommun'] = df_course['Kommun'].replace('Se "Lista flera kommuner"', 'Flera kommuner')

#Summerar antalet beviljade platser per år för kurser inom 'Data/IT'
df_course_sum = df_course[df_course['Utbildningsområde'] == 'Data/IT'].groupby('År')[['Antal beviljade platser 1', 'Antal beviljade platser 2']].sum().reset_index()
df_course_sum['Total_Beviljade_Platser'] = df_course_sum[['Antal beviljade platser 1', 'Antal beviljade platser 2']].sum(axis=1)

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

def filter_year(df, min_year, max_year):
    return(
        df[(df['År'] <= max_year) & (df['År'] >= min_year)]
    )
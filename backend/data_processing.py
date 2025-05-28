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

def filter_df_municipality(df, educational_area="Data/IT", area="Kommun"):
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
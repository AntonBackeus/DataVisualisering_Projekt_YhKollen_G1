from backend.data_processing import filter_df_municipality, filter_decision, filter_education
from frontend.charts import create_municipality_bar
from frontend.maps import swe_map

def filter_data(state):

    df_municipality = filter_df_municipality(
        state.df, educational_area=state.selected_educational_area
    )
    state.municipality_chart = create_municipality_bar(
        df_municipality.head(state.number_municipalities),
        ylabel="KOMMUN",
        xlabel="# ANSÖKTA UTBILDNINGAR",
    )

    state.municipalities_title = state.number_municipalities
    state.educational_area_title = state.selected_educational_area

def filter_mydata(state):

    state.gen_df = filter_education(
        state.df, educational_area=state.gen_educational_area
    )

    state.geducational_area_title = state.gen_educational_area

    state.beslut_df = filter_decision(
        state.gen_df
    )

    state.swe_fig = swe_map(state.gen_df)
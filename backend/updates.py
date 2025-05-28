from backend.data_processing import filter_df_municipality, filter_decision, filter_education
from backend.data_processing import df_merged, df
from frontend.charts import create_data_bar
from frontend.maps import swe_map

def filter_data(state):

    df_municipality = filter_df_municipality(
        state.df, educational_area=state.selected_educational_area
    )
    state.municipality_chart = create_data_bar(
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

def filter_swedata(state):

    df_municipality = filter_df_municipality(
        df_merged, educational_area=state.swe_educational_area, area=state.field_type
    )

    state.municipality_chart = create_data_bar(
        df_municipality, area=state.field_type, xlabel="# ANSÖKTA UTBILDNINGAR"
    )

    test_municipality = filter_df_municipality(
        df, educational_area=state.swe_educational_area, area=state.field_type
    )

    state.test_chart = create_data_bar(
        test_municipality, area=state.field_type, xlabel="# ANSÖKTA UTBILDNINGAR"
    )

    
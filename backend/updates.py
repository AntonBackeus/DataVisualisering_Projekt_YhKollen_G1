from backend.data_processing import filter_df_bar, filter_education
from backend.data_processing import df_merged, df
from frontend.charts import create_data_bar
from frontend.maps import swe_map


def filter_swedata(state):

    df_bar_chart = filter_df_bar(
        df_merged, educational_area=state.swe_educational_area, area=state.field_type
    )

    state.swe_bar_chart = create_data_bar(
        df_bar_chart.head(state.bar_amount), area=state.field_type, xlabel="# ANSÖKTA UTBILDNINGAR"
    )

    test_municipality = filter_df_bar(
        df, educational_area=state.swe_educational_area, area=state.field_type
    )

    state.test_chart = create_data_bar(
        test_municipality, area=state.field_type, xlabel="# ANSÖKTA UTBILDNINGAR"
    )

def filter_mundata(state):

    df_municipality = filter_df_bar(
        df_merged, educational_area=state.mun_educational_area, area="Kommun"
    )

    state.municipality_chart = create_data_bar(
        df_municipality.head(state.municipality_amount), area="Kommun", xlabel="# ANSÖKTA UTBILDNINGAR"
    )

    mun_map_df = filter_education(df_merged, educational_area=state.mun_educational_area)

    state.mun_fig = swe_map(mun_map_df)
    

def filter_busdata(state):

    df_business = filter_df_bar(
        df_merged, educational_area=state.bus_educational_area, area="Utbildningsanordnare administrativ enhet"
    )
    df_max = df_business[df_business["Ansökta utbildningar"] !=0]

    state.max_business = len(df_max)

    if state.business_amount > state.max_business:
        state.business_amount = state.max_business

    state.business_chart = create_data_bar(
        df_business.head(state.business_amount), area="Utbildningsanordnare administrativ enhet", xlabel="# ANSÖKTA UTBILDNINGAR"
    )
    
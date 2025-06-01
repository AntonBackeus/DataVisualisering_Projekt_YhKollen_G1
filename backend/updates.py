from backend.data_processing import filter_df_bar, filter_education, filter_year
from backend.data_processing import df_merged, df_sum
from frontend.charts import create_data_bar, create_line_dia
from frontend.maps import swe_map


def filter_swedata(state):

    df_bar_chart1 = filter_year(df_merged, state.swe_years[0], state.swe_years[1])
    df_bar_chart = filter_df_bar(
        df_bar_chart1, educational_area=state.swe_educational_area, area=state.field_type
    )

    state.swe_bar_chart = create_data_bar(
        df_bar_chart.head(state.bar_amount), area=state.field_type, xlabel="# ANSÖKTA UTBILDNINGAR"
    )
    df_line = filter_year(df_sum, state.swe_years[0], state.swe_years[1])
    if state.line_select == 'Sökta platser totalt':
        state.swe_line = create_line_dia(
            df_line,
            title='Antalet sökta platser över åren',
            x_title='År',
            y_title='Sökta studentplatser',
            filter_=state.line_select
            )    
    elif state.line_select == 'Beviljade platser totalt':
        state.swe_line = create_line_dia(
            df_line,
            title='Antalet beviljade platser över åren',
            x_title='År',
            y_title='Beviljade studentplatser',
            filter_=state.line_select
            )

def filter_mundata(state):
    df_municipality1 = filter_year(df_merged, state.mun_years[0], state.mun_years[1])
    df_municipality = filter_df_bar(
        df_municipality1, educational_area=state.mun_educational_area, area="Kommun"
    )

    state.municipality_chart = create_data_bar(
        df_municipality.head(state.municipality_amount), area="Kommun", xlabel="# ANSÖKTA UTBILDNINGAR"
    )

    mun_map_df = filter_education(df_merged, educational_area=state.mun_educational_area)

    state.mun_fig = swe_map(mun_map_df)
    

def filter_busdata(state):
    df_business1 = filter_year(df_merged, state.bus_years[0], state.bus_years[1])

    df_business = filter_df_bar(
        df_business1, educational_area=state.bus_educational_area, area="Utbildningsanordnare administrativ enhet"
    )


    df_max = df_business[df_business["Ansökta utbildningar"] !=0]

    state.max_business = len(df_max)

    if state.business_amount > state.max_business:
        state.business_amount = state.max_business

    state.business_chart = create_data_bar(
        df_business.head(state.business_amount), area="Utbildningsanordnare administrativ enhet", xlabel="# ANSÖKTA UTBILDNINGAR"
    )
    
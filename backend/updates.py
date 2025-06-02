from backend.data_processing import filter_df_bar, filter_education, filter_year
from backend.data_processing import df_merged, df_platser, df_course
from frontend.charts import create_data_bar, create_line_dia
from frontend.maps import swe_map


def filter_swedata(state):
    df_sum = df_platser.copy()

    df_course_sum = df_course[df_course['Utbildningsområde'] == state.swe_educational_area].groupby('År')[['Antal beviljade platser 1', 'Antal beviljade platser 2']].sum().reset_index()
    df_course_sum['Total_Beviljade_Platser'] = df_course_sum[['Antal beviljade platser 1', 'Antal beviljade platser 2']].sum(axis=1)
    df_course_sum = filter_year(df_course_sum, state.swe_years[0], state.swe_years[1])

    educational_area = state.swe_educational_area
    df_sum = df_sum.query('Utbildningsområde == @educational_area')
    df_sum = df_sum.groupby('År')[['Sökta platser totalt', 'Beviljade platser totalt']].sum().reset_index()
    df_time = filter_year(df_merged, state.swe_years[0], state.swe_years[1])
    df_bar_chart = filter_df_bar(
        df_time, educational_area=state.swe_educational_area, area=state.field_type
    )

    state.swe_bar_chart = create_data_bar(
        df_bar_chart.head(state.bar_amount), area=state.field_type, xlabel="# ANSÖKTA UTBILDNINGAR"
    )
    df_line = filter_year(df_sum, state.swe_years[0], state.swe_years[1])
    if state.line_select == 'Sökta platser totalt':
        state.swe_line = create_line_dia(
            df_line,
            title='Antalet sökta utbildningsplatser över åren',
            x_title='År',
            y_title='Sökta utbildningsplatser',
            filter_=state.line_select
            )    
    elif state.line_select == 'Beviljade platser totalt':
        state.swe_line = create_line_dia(
            df_line,
            title='Antalet beviljade utbildningsplatser över åren',
            x_title='År',
            y_title='Beviljade utbildningsplatser',
            filter_=state.line_select
            )
    
    state.swe_line_course = create_line_dia(
            df_course_sum,
            title='Antalet beviljade kursplatser över åren',
            x_title='År',
            y_title= 'Beviljade kursplatser',
            filter_= 'Total_Beviljade_Platser')

    swe_educational_area = state.swe_educational_area
        
    state.Data_value1 = int(df_time.query('Utbildningsområde == @swe_educational_area')['Sökta utbildningsomgångar'].sum())
    state.Data_value2 = int(df_time.query('Utbildningsområde == @swe_educational_area')['Beviljade utbildningsomgångar'].sum())
    state.Data_value3 = df_time.query("Beslut == 'Ej beviljad' and Utbildningsområde == @swe_educational_area").shape[0]
    state.Data_value4 = df_time.query("Beslut == 'Beviljad' and Utbildningsområde == @swe_educational_area").shape[0]
    tempData_value5 = df_time.query("`Studietakt %` == 100 and Utbildningsområde == @swe_educational_area").shape[0]
    state.Data_value6 = df_time.shape[0]
    state.Data_value5 = str(round((tempData_value5 / state.Data_value6) * 100, 2)) + "%"

def filter_mundata(state):
    df_sum = df_platser.copy()
    educational_area = state.mun_educational_area
    df_sum = df_sum.query('Utbildningsområde == @educational_area')
    df_sum = df_sum.groupby('År')[['Sökta platser totalt', 'Beviljade platser totalt']].sum().reset_index()
    df_time = filter_year(df_merged, state.mun_years[0], state.mun_years[1])
    df_municipality = filter_df_bar(
        df_time, educational_area=state.mun_educational_area, area="Kommun"
    )

    state.municipality_chart = create_data_bar(
        df_municipality.head(state.municipality_amount), area="Kommun", xlabel="# ANSÖKTA UTBILDNINGAR"
    )

    mun_map_df = filter_education(df_merged, educational_area=state.mun_educational_area)

    state.mun_fig = swe_map(mun_map_df)

    mun_kommun = state.mun_kommun
    mun_educational_area = state.mun_educational_area
    df_mun = df_time.query('Kommun == @mun_kommun and Utbildningsområde == @mun_educational_area')
    state.Mun_value1 = int(df_mun['Sökta utbildningsomgångar'].sum())
    state.Mun_value2 = int(df_mun['Beviljade utbildningsomgångar'].sum())
    state.Mun_value3 = df_mun.query("Beslut == 'Ej beviljad'").shape[0]
    state.Mun_value4 = df_mun.query("Beslut == 'Beviljad'").shape[0]
    tempMun_value5 = df_mun.query("`Studietakt %` == 100").shape[0]
    state.Mun_value6 = df_mun.shape[0]
    state.Mun_value5 = str(round((tempMun_value5 / state.Mun_value6) * 100, 2)) + "%"
    

def filter_busdata(state):
    df_sum = df_platser.copy()
    educational_area = state.bus_educational_area
    df_sum = df_sum.query('Utbildningsområde == @educational_area')
    df_sum = df_sum.groupby('År')[['Sökta platser totalt', 'Beviljade platser totalt']].sum().reset_index()
    df_time = filter_year(df_merged, state.bus_years[0], state.bus_years[1])

    df_business = filter_df_bar(
        df_time, educational_area=state.bus_educational_area, area="Utbildningsanordnare administrativ enhet"
    )

    df_max = df_business[df_business["Ansökta utbildningar"] !=0]

    state.max_business = len(df_max)

    if state.business_amount > state.max_business:
        state.business_amount = state.max_business

    state.business_chart = create_data_bar(
        df_business.head(state.business_amount), area="Utbildningsanordnare administrativ enhet", xlabel="# ANSÖKTA UTBILDNINGAR"
    )
    
    anordnare = state.bus_anordnare
    bus_educational_area = state.bus_educational_area
    df_bus = df_time.query('`Utbildningsanordnare administrativ enhet` == @anordnare')
    state.bus_value1 = int(df_bus.query('Utbildningsområde == @bus_educational_area')['Sökta utbildningsomgångar'].sum())
    state.bus_value2 = int(df_bus.query('Utbildningsområde == @bus_educational_area')['Beviljade utbildningsomgångar'].sum())
    state.bus_value3 = df_bus.query("Beslut == 'Ej beviljad' and Utbildningsområde == @bus_educational_area").shape[0]
    state.bus_value4 = df_bus.query("Beslut == 'Beviljad' and Utbildningsområde == @bus_educational_area").shape[0]
    tempbus_value5 = df_bus.query("`Studietakt %` == 100 and Utbildningsområde == @bus_educational_area").shape[0]
    state.bus_value6 = df_bus.query('Utbildningsområde == @bus_educational_area').shape[0]
    state.bus_value5 = str(round((tempbus_value5 / state.bus_value6) * 100, 2)) + "%"
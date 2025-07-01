from backend.data_processing import filter_df_bar, filter_education, filter_year
from backend.data_processing import df_merged, df_platser, df_course
from frontend.charts import create_data_bar, create_line_dia
from frontend.maps import swe_map
import plotly.express as px


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
        df_bar_chart.head(state.bar_amount), area=state.field_type, xlabel="Antal ansökta utbildningar", ylabel='Län'
    )

    swe_map_df = filter_education(df_time, educational_area=state.swe_educational_area)
    state.swe_fig = swe_map(swe_map_df)

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
    if state.Data_value6 == 0: state.Data_value5 = "0"
    else: state.Data_value5 = str(round((tempData_value5 / state.Data_value6) * 100, 2)) + "%"

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
        df_municipality.head(state.municipality_amount), area="Kommun", xlabel="Ansökta Utbildningar", ylabel="Kommun"
    )

    df_time_course = filter_year(df_course, state.mun_years[0], state.mun_years[1])
    df_bar_chart_course = filter_df_bar(df_time_course, educational_area=state.mun_educational_area, area='Kommun')
    state.mun_bar_chart_course = create_data_bar(
        df_bar_chart_course.head(state.municipality_amount), area='Kommun', xlabel="Ansökta Kurser", ylabel="Kommun"
    )

    mun_kommun = state.mun_kommun
    mun_educational_area = state.mun_educational_area
    df_mun = df_time.query('Kommun == @mun_kommun and Utbildningsområde == @mun_educational_area')
    state.Mun_value1 = int(df_mun['Sökta utbildningsomgångar'].sum())
    state.Mun_value2 = int(df_mun['Beviljade utbildningsomgångar'].sum())
    state.Mun_value3 = df_mun.query("Beslut == 'Ej beviljad'").shape[0]
    state.Mun_value4 = df_mun.query("Beslut == 'Beviljad'").shape[0]
    tempMun_value5 = df_mun.query("`Studietakt %` == 100").shape[0]
    state.Mun_value6 = df_mun.shape[0]
    if state.Mun_value6 == 0: state.Mun_value5 = "0"
    else:state.Mun_value5 = str(round((tempMun_value5 / state.Mun_value6) * 100, 2)) + "%"
    

def filter_busdata(state):
    df_sum = df_platser.copy()
    educational_area = state.bus_educational_area
    df_sum = df_sum.query('Utbildningsområde == @educational_area')
    df_sum = df_sum.groupby('År')[['Sökta platser totalt', 'Beviljade platser totalt']].sum().reset_index()
    df_time = filter_year(df_merged, state.bus_years[0], state.bus_years[1])
    df_time_course = filter_year(df_course, state.bus_years[0], state.bus_years[1])

    df_business = filter_df_bar(
        df_time, educational_area=state.bus_educational_area, area="Utbildningsanordnare administrativ enhet"
    )

    df_max = df_business[df_business["Ansökta utbildningar"] !=0]

    state.max_business = len(df_max)

    if state.business_amount > state.max_business:
        state.business_amount = state.max_business

    state.business_chart = create_data_bar(
        df_business.head(state.business_amount), area="Utbildningsanordnare administrativ enhet", xlabel="Antal ansökta utbildningar", ylabel="Anordnare"
    )

    df_bus_chart_course = filter_df_bar(df_time_course, educational_area=state.bus_educational_area, area='Anordnare')
    state.bus_chart_course = create_data_bar(
        df_bus_chart_course.head(state.business_amount), area='Anordnare', xlabel="Antal ansökta kurser", ylabel="Anordnare"
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
    if state.bus_value6 == 0: state.bus_value5 = "0"
    else: state.bus_value5 = str(round((tempbus_value5 / state.bus_value6) * 100, 2)) + "%"

def update_course_charts(state):
    """Uppdaterar populära och mindre populära utbildningsdiagram baserat på valt state."""

    kommun = getattr(state, "selected_kommun", None)
    year = getattr(state, "selected_year", None)
    top_n = int(getattr(state, "top_n_courses", 5) or 5)

    def empty_chart(title="Ingen data"):
        fig = px.pie(names=["Ingen data tillgänglig"], values=[1], title=title)
        fig.update_traces(textinfo="none", showlegend=False)
        fig.update_layout(margin=dict(t=30, b=10, l=10, r=10))
        return fig

    try:
        year = int(year)
    except (TypeError, ValueError):
        empty = empty_chart("Årtal saknas eller ogiltigt")
        state.popular_courses_chart = empty
        state.unpopular_courses_chart = empty
        return

    if not kommun:
        empty = empty_chart("Kommun saknas")
        state.popular_courses_chart = empty
        state.unpopular_courses_chart = empty
        return

    df_filtered = df_course[
        (df_course["Kommun"] == kommun) &
        (df_course["År"] == year)
    ].copy()

    if df_filtered.empty:
        empty = empty_chart(f"Ingen data för {kommun} ({year})")
        state.popular_courses_chart = empty
        state.unpopular_courses_chart = empty
        return

    df_filtered["Totalt beviljade platser"] = (
        df_filtered["Antal beviljade platser 1"].fillna(0) +
        df_filtered["Antal beviljade platser 2"].fillna(0)
    )

    course_counts = (
        df_filtered.groupby("Utbildningsnamn")["Totalt beviljade platser"]
        .sum()
        .reset_index()
        .sort_values("Totalt beviljade platser", ascending=False)
    )

    popular = course_counts.head(top_n)
    unpopular = course_counts[course_counts["Totalt beviljade platser"] > 0].tail(top_n)

    def make_pie(data, title, colors):
        if data.empty:
            return empty_chart(title)
        fig = px.pie(
            data,
            names="Utbildningsnamn",
            values="Totalt beviljade platser",
            title=title,
            hole=0.4,
            color_discrete_sequence=colors
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Platser: %{value}<br>Andel: %{percent}"
        )
        fig.update_layout(
            margin=dict(t=40, b=20, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3),
            title_font_size=16
        )
        return fig

    state.popular_courses_chart = make_pie(
        popular, f"Populära utbildningar i {kommun} ({year})", px.colors.sequential.Reds
    )
    state.unpopular_courses_chart = make_pie(
        unpopular, f"Mindre populära utbildningar i {kommun} ({year})", px.colors.sequential.Blues
    )

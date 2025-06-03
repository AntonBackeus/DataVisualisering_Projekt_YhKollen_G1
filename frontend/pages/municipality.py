import taipy.gui.builder as tgb
from frontend.charts import create_data_bar
from backend.data_processing import filter_df_bar, df_merged, df_course
from backend.updates import filter_mundata

#Filter constants
mun_educational_area = "Data/IT"
mun_years = [2020,2024]


#Creating a bar chart for municipalities
municipality_amount = 10
df_municipality = filter_df_bar(df_merged)
municipality_chart = create_data_bar(
    df_municipality.head(municipality_amount), area="Kommun", xlabel="Ansökta Utbildningar", ylabel="Kommun"
)

#Statistic data values
mun_kommun = 'Stockholm'
df_mun = df_merged.query('Kommun == @mun_kommun and Utbildningsområde == @mun_educational_area')
Mun_value1 = int(df_mun['Sökta utbildningsomgångar'].sum())
Mun_value2 = int(df_mun['Beviljade utbildningsomgångar'].sum())
Mun_value3 = df_mun.query("Beslut == 'Ej beviljad'").shape[0]
Mun_value4 = df_mun.query("Beslut == 'Beviljad'").shape[0]
Mun_value5 = df_mun.query("`Studietakt %` == 100").shape[0]
Mun_value6 = df_mun.query('Utbildningsområde == @mun_educational_area').shape[0]
if Mun_value6 == 0: Mun_value5="0"
else: Mun_value5 = str(round((Mun_value5 / Mun_value6) * 100, 2)) + "%"

#Creating a bar chart able to be filtered for courses
df_bar_chart_course = filter_df_bar(df_course,educational_area=mun_educational_area, area='Kommun')
mun_bar_chart_course = create_data_bar(
    df_bar_chart_course.head(municipality_amount), area='Kommun', xlabel="Ansökta kurser", ylabel="Kommun"
)

with tgb.Page() as municipality_page:
    #Background
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()
        #Title
        with tgb.part(class_name="card"):
            tgb.text("# Yh Kollen", mode="md")
            tgb.text(
                "Denna sida visar statestik om ansökningarna fördelat över Sveriges kommuner",
                mode="md",
                )
        #Filters
        with tgb.layout(columns="1 1"):
            #Education
            with tgb.part(class_name="card"):
                tgb.text("Filtrera datan på utbildingsområde")
                tgb.selector(
                    value="{mun_educational_area}",
                    lov=df_merged["Utbildningsområde"].unique(),
                    dropdown=True,
                    on_change=filter_mundata
                )
            #Time
            with tgb.part(class_name="card"):
                tgb.text("Filtrera data på år.")
                tgb.slider(
                    value="{mun_years}",
                    min=2020,
                    max=2024,
                    continuous=False,
                    on_change=filter_mundata
                )
                tgb.text("Filtering från {mun_years[0]} till {mun_years[1]}")
        #Charts
        with tgb.part(class_name="card"):
            tgb.text("Mängd kommuner.")
            tgb.slider(
                value="{municipality_amount}",
                min=5,
                max=len(df_municipality),
                continuous=False,
                on_change=filter_mundata
            )

        with tgb.layout(columns="1 1"):
            #Municipality bar chart
            with tgb.part(class_name="card"):
                tgb.chart(figure="{municipality_chart}")
            #Map
            with tgb.part(class_name="card"):
                tgb.chart(figure="{mun_bar_chart_course}")

        #Statistic data
        with tgb.part(class_name="card"):
            tgb.text("Välj en kommun")
            tgb.selector(
                value="{mun_kommun}",
                lov=df_merged['Kommun'].unique(),
                dropdown=True,
                on_change=filter_mundata
            )
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card"):
                tgb.text("{Mun_value1}")
                tgb.text("Antalet sökta utbildningsomgångar")
            with tgb.part(class_name="card"):
                tgb.text("{Mun_value2}")
                tgb.text("Antalet beviljade utbildningsomgångar")
            with tgb.part(class_name="card"):
                tgb.text("{Mun_value3}")
                tgb.text("Antalet nekade utbildningar")
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card"):
                tgb.text("{Mun_value4}")
                tgb.text("Antalet godkända utbildningar")
            with tgb.part(class_name="card"):
                tgb.text("{Mun_value5}")
                tgb.text("Procenten av sökta utbildningar på heltakt")
            with tgb.part(class_name="card"):
                tgb.text("{Mun_value6}")
                tgb.text("Antalet sökta utbildningar")
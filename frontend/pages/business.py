import taipy.gui.builder as tgb
from frontend.charts import create_data_bar
from backend.data_processing import filter_df_bar, df_merged
from backend.updates import filter_busdata

#Filter constants
bus_educational_area = "Data/IT"
bus_years = [2020,2024]


#Creating a bar chart for businesses
business_amount = 20
df_business = filter_df_bar(df_merged, educational_area=bus_educational_area, area="Utbildningsanordnare administrativ enhet")
business_chart = create_data_bar(
    df_business.head(business_amount), area="Utbildningsanordnare administrativ enhet", xlabel="# ANSÖKTA UTBILDNINGAR"
)
max_business = len(df_business)

#Statistic data values
bus_anordnare = "JENSEN Education School AB"
df_bus = df_merged.query('`Utbildningsanordnare administrativ enhet` == @bus_anordnare and Utbildningsområde == @bus_educational_area')
bus_value1 = int(df_bus['Sökta utbildningsomgångar'].sum())
bus_value2 = int(df_bus['Beviljade utbildningsomgångar'].sum())
bus_value3 = df_bus.query("Beslut == 'Ej beviljad'").shape[0]
bus_value4 = df_bus.query("Beslut == 'Beviljad'").shape[0]
bus_value5 = df_bus.query("`Studietakt %` == 100").shape[0]
bus_value6 = df_bus.shape[0]
bus_value5 = str(round((bus_value5 / bus_value6) * 100, 2)) + "%"


with tgb.Page() as business_page:
    #Background
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()
        #Title
        with tgb.part(class_name="card"):
            tgb.text("# Yh Kollen", mode="md")
            tgb.text(
                "En dashboard för att visa statistik och information om ansökningsomgångar per anordnare",
                mode="md",
                )
        #Filters
        with tgb.layout(columns="1 1"):
            #Education
            with tgb.part(class_name="card"):
                tgb.text("Filtrera datan på utbildingsområde")
                tgb.selector(
                    value="{bus_educational_area}",
                    lov=df_merged["Utbildningsområde"].unique(),
                    dropdown=True,
                    on_change=filter_busdata
                )
            #Time
            with tgb.part(class_name="card"):
                tgb.text("Filtrera data på år.")
                tgb.slider(
                    value="{bus_years}",
                    min=2020,
                    max=2024,
                    continuous=False,
                    on_change=filter_busdata
                )
                tgb.text("Filtering från {bus_years[0]} till {bus_years[1]}")
        #Charts
        with tgb.part(class_name="card"):
            tgb.text("Mängd anordnare.")
            tgb.slider(
                value="{business_amount}",
                min=5,
                max="{max_business}",
                continuous=False,
                on_change=filter_busdata
            )
            tgb.chart(figure="{business_chart}")
        #Statistic data
        with tgb.part(class_name="card"):
            tgb.text("Välj en kommun")
            tgb.selector(
                value="{bus_anordnare}",
                lov=df_merged['Utbildningsanordnare administrativ enhet'].unique(),
                dropdown=True,
                on_change=filter_busdata
            )
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card"):
                tgb.text("{bus_value1}")
                tgb.text("Antalet sökta utbildningsomgångar")
            with tgb.part(class_name="card"):
                tgb.text("{bus_value2}")
                tgb.text("Antalet beviljade utbildningsomgångar")
            with tgb.part(class_name="card"):
                tgb.text("{bus_value3}")
                tgb.text("Antalet nekade utbildningar")
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card"):
                tgb.text("{bus_value4}")
                tgb.text("Antalet godkända utbildningar")
            with tgb.part(class_name="card"):
                tgb.text("{bus_value5}")
                tgb.text("Procenten av sökta utbildningar på heltakt")
            with tgb.part(class_name="card"):
                tgb.text("{bus_value6}")
                tgb.text("Antalet sökta utbildningar")
import taipy.gui.builder as tgb
from frontend.charts import create_data_bar, create_line_dia
from backend.data_processing import filter_df_bar, df_merged, df_sum
from backend.updates import filter_swedata

#Filter constants
swe_educational_area = "Data/IT"
field_type = "Län"
swe_years = [2020,2024]
line_select = 'Sökta platser totalt'

#Creating a bar chart able to be filtered
bar_amount = 10
df_bar_chart = filter_df_bar(df_merged, area=field_type)
swe_bar_chart = create_data_bar(
    df_bar_chart.head(bar_amount), area=field_type, xlabel="# ANSÖKTA UTBILDNINGAR"
)

#Creating a line chart able to be filtered
swe_line = create_line_dia(
            df_sum,
            title='Antalet sökta platser över åren',
            x_title='År',
            y_title='Sökta studentplatser',
            filter_=line_select)

#Statistic data values
Data_value1 = int(df_merged.query('Utbildningsområde == @swe_educational_area')['Sökta utbildningsomgångar'].sum())
Data_value2 = int(df_merged.query('Utbildningsområde == @swe_educational_area')['Beviljade utbildningsomgångar'].sum())
Data_value3 = df_merged.query("Beslut == 'Ej beviljad' and Utbildningsområde == @swe_educational_area").shape[0]
Data_value4 = df_merged.query("Beslut == 'Beviljad' and Utbildningsområde == @swe_educational_area").shape[0]
Data_value5 = df_merged.query("`Studietakt %` == 100 and Utbildningsområde == @swe_educational_area").shape[0]
Data_value6 = df_merged.shape[0]
Data_value5 = str(round((Data_value5 / Data_value6) * 100, 2)) + "%"

with tgb.Page() as sweden_page:
    #Background
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()
        #Title
        with tgb.part(class_name="card"):
            tgb.text("# Yh Kollen", mode="md")
            tgb.text(
                "En dashboard för att visa statistik och information om ansökningsomgångar för kommuner",
                mode="md",
                )
        #Filters
        with tgb.layout(columns="1 1"):
            #Education
            with tgb.part(class_name="card"):
                tgb.text("Filtrera datan på utbildingsområde")
                tgb.selector(
                    value="{swe_educational_area}",
                    lov=df_merged["Utbildningsområde"].unique(),
                    dropdown=True,
                    on_change=filter_swedata
                )
            #Time
            with tgb.part(class_name="card"):
                tgb.text("Filtrera data på år.")
                tgb.slider(
                    value="{swe_years}",
                    min=2020,
                    max=2024,
                    continuous=False,
                    on_change=filter_swedata
                )
                tgb.text("Filtering från {swe_years[0]} till {swe_years[1]}")
        
        #Figures
        with tgb.layout(columns="1 1"):
            #Filterable bar chart
            with tgb.part(class_name="card"):
                tgb.text("Antal.")
                tgb.slider(
                    value="{bar_amount}",
                    min=5,
                    max=len(df_bar_chart),
                    continuous=False,
                    on_change=filter_swedata
                )
                tgb.chart(figure="{swe_bar_chart}")
            #To be changed into a line chart
            with tgb.part(class_name="card"):
                tgb.text("Filtrera datan på område")
                tgb.selector(
                    value="{line_select}",
                    lov=['Sökta platser totalt', 'Beviljade platser totalt'],
                    dropdown=True,
                    on_change=filter_swedata)
                tgb.chart(figure="{swe_line}")
        
        #Statistic data
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card"):
                tgb.text("{Data_value1}")
                tgb.text("Antalet sökta utbildningsomgångar")
            with tgb.part(class_name="card"):
                tgb.text("{Data_value2}")
                tgb.text("Antalet beviljade utbildningsomgångar")
            with tgb.part(class_name="card"):
                tgb.text("{Data_value3}")
                tgb.text("Antalet nekade utbildningar")
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card"):
                tgb.text("{Data_value4}")
                tgb.text("Antalet godkända utbildningar")
            with tgb.part(class_name="card"):
                tgb.text("{Data_value5}")
                tgb.text("Procenten av sökta utbildningar på heltakt")
            with tgb.part(class_name="card"):
                tgb.text("{Data_value6}")
                tgb.text("Antalet sökta utbildningar")

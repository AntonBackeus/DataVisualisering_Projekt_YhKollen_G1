import taipy.gui.builder as tgb
from frontend.charts import create_data_bar, create_line_dia
from frontend.maps import swe_map
from backend.data_processing import filter_df_bar, filter_education, df_merged, df_sum, df_course, df_course_sum
from backend.updates import filter_swedata

#Filter constants
swe_educational_area = "Data/IT"
field_type = "Län"
swe_years = [2020,2024]
line_select = 'Sökta platser totalt'

#Creating a bar chart able to be filtered for programs
bar_amount = 10
df_bar_chart = filter_df_bar(df_merged, educational_area=swe_educational_area, area=field_type)
swe_bar_chart = create_data_bar(
    df_bar_chart.head(bar_amount), area=field_type, xlabel="Antal ansökta utbildningar", ylabel='Län'
)

#Creating a line chart able to be filtered for programs
swe_line = create_line_dia(
            df_sum,
            title='Antalet sökta platser över åren',
            x_title='År',
            y_title='Sökta utbildningsplatser',
            filter_=line_select)


#Creating a swedish map showing data about the areas
swe_map_df = filter_education(df_merged)
swe_fig = swe_map(swe_map_df)

#Creating a line chart able to be filtered for courses
swe_line_course = create_line_dia(
            df_course_sum,
            title='Antalet beviljade kursplatser över åren',
            x_title='År',
            y_title= 'Beviljade kursplatser',
            filter_= 'Total_Beviljade_Platser')

#Statistic data values
Data_value1 = int(df_merged.query('Utbildningsområde == @swe_educational_area')['Sökta utbildningsomgångar'].sum())
Data_value2 = int(df_merged.query('Utbildningsområde == @swe_educational_area')['Beviljade utbildningsomgångar'].sum())
Data_value3 = df_merged.query("Beslut == 'Ej beviljad' and Utbildningsområde == @swe_educational_area").shape[0]
Data_value4 = df_merged.query("Beslut == 'Beviljad' and Utbildningsområde == @swe_educational_area").shape[0]
Data_value5 = df_merged.query("`Studietakt %` == 100 and Utbildningsområde == @swe_educational_area").shape[0]
Data_value6 = df_merged.query("Utbildningsområde == @swe_educational_area").shape[0]
if Data_value6 == 0: Data_value5="0"
else: Data_value5 = str(round((Data_value5 / Data_value6) * 100, 2)) + "%"

with tgb.Page() as sweden_page:
    #Background
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()
        #Title
        with tgb.part(class_name="card"):
            tgb.text("# Yh Kollen", mode="md")
            tgb.text(
                "Se hur datan ser ut för yrkeshögskolor som söker nya utbildningar eller kurser",
                mode="md",
                )
            tgb.text("Översikt visar generell data inom Sverige")
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
                tgb.text("Filteras från åren {swe_years[0]} till {swe_years[1]}")
                tgb.slider(
                    value="{swe_years}",
                    min=2020,
                    max=2024,
                    continuous=False,
                    on_change=filter_swedata
                )

        
        #Figures
        with tgb.layout(columns="1 1"):
            #Filterable bar chart
            with tgb.part(class_name="card"):
                tgb.text("Antal län visade: {bar_amount}")
                tgb.slider(
                    value="{bar_amount}",
                    min=5,
                    max=len(df_bar_chart),
                    continuous=False,
                    on_change=filter_swedata
                )
                tgb.chart(figure="{swe_bar_chart}")
                tgb.chart(figure="{swe_fig}")
            #To be changed into a line chart
            with tgb.part(class_name="card"):
                tgb.text("Filtrera utbildningsdatan på område")
                tgb.selector(
                    value="{line_select}",
                    lov=['Sökta platser totalt', 'Beviljade platser totalt'],
                    dropdown=True,
                    on_change=filter_swedata)
                tgb.chart(figure="{swe_line}")
                tgb.chart(figure="{swe_line_course}")
        
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
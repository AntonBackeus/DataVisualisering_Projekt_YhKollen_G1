import taipy.gui.builder as tgb
from frontend.charts import create_data_bar
from backend.data_processing import filter_df_municipality, df_merged, df
from backend.updates import filter_swedata

swe_educational_area = "Data/IT"
field_type = "Kommun"
swe_years = [2020,2024]

df_municipality = filter_df_municipality(df_merged)
municipality_chart = create_data_bar(
    df_municipality, area=field_type, xlabel="# ANSÖKTA UTBILDNINGAR"
)
test_municipality = filter_df_municipality(df)
test_chart = create_data_bar(
    test_municipality, area=field_type, xlabel="# ANSÖKTA UTBILDNINGAR"
)

with tgb.Page() as sweden_page:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()
        with tgb.part(class_name="card"):
            tgb.text("# Yh Kollen", mode="md")
            tgb.text(
                "En dashboard för att visa statistik och information om ansökningsomgångar",
                mode="md",
                )
        
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card"):
                tgb.text("Filtrera datan på utbildingsområde")
                tgb.selector(
                    value="{swe_educational_area}",
                    lov=df_merged["Utbildningsområde"].unique(),
                    dropdown=True,
                    on_change=filter_swedata
                )
            with tgb.part(class_name="card"):
                tgb.text("Filtrera datan på område")
                tgb.selector(
                    value="{field_type}",
                    lov=["Kommun", "Län", "Utbildningsanordnare administrativ enhet"],
                    dropdown=True,
                    on_change=filter_swedata
                )
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
        
        with tgb.layout(columns="1 1"):
            with tgb.part(class_name="card"):
                tgb.chart(figure="{municipality_chart}")
            with tgb.part(class_name="card"):
                tgb.chart(figure="{test_chart}")
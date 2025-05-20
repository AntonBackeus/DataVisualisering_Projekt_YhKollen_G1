import taipy.gui.builder as tgb
from backend.data_processing import filter_education, filter_decision, df
from backend.updates import filter_mydata
from backend.maps import swe_map

gen_df = filter_education(df)

beslut_df = filter_decision(gen_df)

swe_data, swe_prop = swe_map()

gen_educational_area = "Data/IT"
geducational_area_title = gen_educational_area

years = [2015, 2025]

with tgb.Page() as general_page:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()

        tgb.text("## Generell data", mode="md")
        tgb.text("Byt tabell till vår generella data")
        tgb.selector(
                    value="{gen_educational_area}",
                    lov=df["Utbildningsområde"].unique(),
                    dropdown=True,
                )
        tgb.slider(
                    value="{years}",
                    min=2015,
                    max=2025,
                    continuous=False,
        )
        tgb.text("Filtering from {years[0]} to {years[1]}")
        tgb.button("FILTRERA DATA", on_action=filter_mydata, class_name="plain")

        tgb.text("Tabeller ska filtreras på åren från slider")
        tgb.table("{gen_df}")

        tgb.table("{beslut_df}")

        tgb.chart("{swe_data}", properties="{swe_prop}")


    
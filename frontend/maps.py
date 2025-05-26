import plotly.graph_objects as go
import numpy as np
import duckdb
import json
from difflib import get_close_matches

def swe_map(df):
    df_regions = duckdb.query(
        """
        SELECT 
            län, 
            COUNT_IF(beslut ='Beviljad') AS Beviljade
        FROM df 
        WHERE län != 'Flera kommuner'
        GROUP BY
            län
        ORDER BY 
            beviljade 
        DESC
    """
    ).df()

    with open("assets/swedish_regions.geojson", "r", encoding='utf-8') as fp:
        json_data = json.load(fp)

    properties = [feature.get("properties") for feature in json_data.get("features")]
    regions_codes = {
        property.get("name"): property.get("ref:se:länskod") for property in properties
    }

    region_codes_map = []

    for region in df_regions["Län"]:
        region_name = get_close_matches(region, regions_codes.keys(), n=1)[0]
        code = regions_codes[region_name]
        region_codes_map.append(code)

    approved = df["Beslut"].value_counts()["Beviljad"]
    total_applications = df["Beslut"].value_counts().sum()

    df_regions["log_beviljade"] = np.log(df_regions["Beviljade"] + 1)

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=json_data,
            locations=region_codes_map,
            z=df_regions["log_beviljade"],
            featureidkey="properties.ref:se:länskod",
            colorscale="Blues",
            customdata=df_regions["Beviljade"],
            marker_opacity=0.9,
            marker_line_width=0.1,
            text=df_regions["Län"],
            hovertemplate="<b>%{text}</b><br>Beviljade utbildningar: %{customdata}<extra></extra>",
            showscale=False,
        )
    )

    fig.update_layout(
        title=dict(
            text=f"""
                    <b>Antal beviljade</b>
                    <br>utbildningar per län
                    <br>inom YH i Sverige för 
                    <br>omgång 2024. Ju mörkare 
                    <br>blå färg, desto fler
                    <br>beviljade utbildningar
                    <br>
                    <br><b>{approved}</b> av totalt <b>{total_applications}</b>
                    <br>ansökningar har
                    <br>godkänts, vilket innebär 
                    <br><b>27%</b> beviljandegrad
                    <br>
                    <br><b>I ledningen är</b>
                    <br>1. Stockholm, 
                    <br>2. Västra Götaland
                    <br>3. Skåne""",
            x=0.06,
            y=0.75,
            font=dict(size=13),
        ),
        mapbox=dict(style="white-bg", zoom=3.3, center=dict(lat=62.6952, lon=13.9149)),
        margin=dict(r=0, t=50, l=0, b=0),
        dragmode=False,
        width=470,
        height=500,
    )

    fig.update_xaxes(fixedrange=True)

    return fig
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
from backend.data_processing import df_course

# Globala state-variabler
selected_kommun = None
selected_year = None
top_n_courses = 5
popular_courses_chart = None
unpopular_courses_chart = None
popularity_over_time_chart = None
chart_data = None

def create_popular_unpopular_pie_year(state):
    kommun = state.selected_kommun
    year = state.selected_year
    top_n = state.top_n_courses

    if kommun is None or year is None:
        empty_fig = px.pie(names=["Ingen data tillgänglig"], values=[1], title="Ingen data vald")
        empty_fig.update_traces(textinfo="none", showlegend=False)
        return empty_fig, empty_fig

    year = int(year)
    top_n = int(top_n)

    df_filtered = df_course[(df_course['Kommun'] == kommun) & (df_course['År'] == year)].copy()
    if df_filtered.empty:
        empty_fig = px.pie(names=["Ingen data tillgänglig"], values=[1], title=f"Ingen data för {kommun} ({year})")
        empty_fig.update_traces(textinfo="none", showlegend=False)
        return empty_fig, empty_fig

    df_filtered["Totalt beviljade platser"] = (
        df_filtered["Antal beviljade platser 1"].fillna(0).astype(int) +
        df_filtered["Antal beviljade platser 2"].fillna(0).astype(int)
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
        fig = px.pie(
            data,
            names="Utbildningsnamn",
            values="Totalt beviljade platser",
            title=title,
            hole=0.4,
            color_discrete_sequence=colors,
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Platser: %{value}<br>Andel: %{percent}",
        )
        fig.update_layout(
            margin=dict(t=40, b=20, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3),
            title_font_size=16,
        )
        return fig

    popular_fig = make_pie(popular, f"Populära utbildningar i {kommun} ({year})", px.colors.sequential.Reds)
    unpopular_fig = make_pie(unpopular, f"Mindre populära utbildningar i {kommun} ({year})", px.colors.sequential.Blues)

    return popular_fig, unpopular_fig

def create_popularity_over_time_line(state):
    kommun = state.selected_kommun
    top_n = state.top_n_courses

    if kommun is None:
        empty_fig = px.line(title="Ingen kommun vald")
        return empty_fig

    top_n = int(top_n)

    df_filtered = df_course[df_course['Kommun'] == kommun].copy()
    if df_filtered.empty:
        empty_fig = px.line(title=f"Ingen data för {kommun}")
        return empty_fig

    df_filtered["Totalt beviljade platser"] = (
        df_filtered["Antal beviljade platser 1"].fillna(0).astype(int) +
        df_filtered["Antal beviljade platser 2"].fillna(0).astype(int)
    )

    # Summa per utbildning och år
    course_year_sum = (
        df_filtered.groupby(["Utbildningsnamn", "År"])["Totalt beviljade platser"]
        .sum()
        .reset_index()
    )

    # Hitta topp N populära utbildningar totalt
    top_courses = (
        course_year_sum.groupby("Utbildningsnamn")["Totalt beviljade platser"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .index
        .tolist()
    )

    # Filtrera till bara topp N
    df_top = course_year_sum[course_year_sum["Utbildningsnamn"].isin(top_courses)]

    # Skapa linjediagram
    fig = px.line(
        df_top,
        x="År",
        y="Totalt beviljade platser",
        color="Utbildningsnamn",
        title=f"Utbildningars popularitet över år i {kommun}",
        markers=True,
    )
    fig.update_layout(
        xaxis=dict(dtick=1),
        margin=dict(t=50, b=40, l=40, r=40),
        legend=dict(title="Utbildningsnamn", orientation="h", yanchor="bottom", y=-0.3),
        title_font_size=16,
    )
    fig.update_traces(mode="lines+markers")

    return fig

def update_pie_charts(state, var_name=None, var_value=None):
    if var_name in ["selected_kommun", "selected_year", "top_n_courses", None]:
        popular_fig, unpopular_fig = create_popular_unpopular_pie_year(state)
        state.popular_courses_chart = popular_fig
        state.unpopular_courses_chart = unpopular_fig
        state.popularity_over_time_chart = create_popularity_over_time_line(state)

def init_state(state):
    if state.selected_kommun is None:
        kommuner = sorted(df_course['Kommun'].dropna().unique())
        state.selected_kommun = kommuner[0] if kommuner else ""

    if state.selected_year is None:
        years = sorted([int(y) for y in df_course['År'].dropna().unique()], reverse=True)
        state.selected_year = years[0] if years else 2024
    else:
        state.selected_year = int(state.selected_year)

    state.top_n_courses = int(state.top_n_courses) if state.top_n_courses else 5

    if state.chart_data is None:
        state.chart_data = pd.DataFrame([
            {"Område": "Teknik och tillverkning", "Antal": 14000},
            {"Område": "Vård och omsorg", "Antal": 12000},
            {"Område": "Data/IT", "Antal": 10000},
            {"Område": "Bygg och anläggning", "Antal": 8500},
            {"Område": "Ekonomi och administration", "Antal": 7000},
            {"Område": "Transport", "Antal": 5000},
            {"Område": "Pedagogik", "Antal": 4000},
            {"Område": "Övrigt", "Antal": 3000},
        ])
        state.chart_data = state.chart_data.sort_values("Antal", ascending=False)

    update_pie_charts(state)


# ----------------------------
# GUI Page
# ----------------------------

with tgb.Page(name="Kursanalys") as course_analysis_page:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()

        with tgb.part(class_name="card"):
            tgb.text("# 🎓 Utbildningsanalys er kommun", mode="md")
            tgb.text("Analysera de mest och minst populära utbildningarna, samt totala beviljade platser per område.", mode="md")

        with tgb.part(class_name="card"):
            with tgb.layout(columns="1 1 1", gap="1em"):
                with tgb.part():
                    tgb.text("Välj kommun:", mode="md")
                    tgb.selector(
                        value="{selected_kommun}",
                        lov=sorted(df_course["Kommun"].dropna().unique()),
                        dropdown=True,
                        class_name="fullwidth",
                        on_change=update_pie_charts,
                    )
                with tgb.part():
                    tgb.text("Välj år:", mode="md")
                    tgb.selector(
                        value="{selected_year}",
                        lov=sorted([int(y) for y in df_course["År"].dropna().unique()], reverse=True),
                        dropdown=True,
                        class_name="fullwidth",
                        on_change=update_pie_charts,
                    )
                with tgb.part():
                    tgb.text("Antal utbildningar att visa:", mode="md")
                    tgb.slider(
                        value="{top_n_courses}",
                        min=3,
                        max=10,
                        step=1,
                        class_name="fullwidth",
                        on_change=update_pie_charts,
                    )

        # 🔴 Flytta ut dessa layout-delar ur det inre slidern-part blocket

        with tgb.layout(columns="1 1", gap="2em"):
            with tgb.part(class_name="card"):
                tgb.chart(figure="{popular_courses_chart}")
            with tgb.part(class_name="card"):
                tgb.chart(figure="{unpopular_courses_chart}")

        # 🔵 Linjediagrammet med bred layout under
        with tgb.part(class_name="card", style="margin-top: 2em;"):
            tgb.chart(figure="{popularity_over_time_chart}", height="450px", width="100%")

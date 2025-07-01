import plotly.express as px

def create_data_bar(df_bar, area="Kommun", **options):
    df = df_bar.copy()
    df["Ansökta_label"] = df["Ansökta utbildningar"].apply(
        lambda row: " " * 2 + f"{row}" + " " * 2
    )

    fig = px.bar(
        df,
        y=area,
        x="Ansökta utbildningar",
        text="Ansökta_label",
    )
    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(t=0, l=40, r=30, b=50),
        yaxis=dict(
            autorange="reversed",
            ticklabelposition="outside left",
            showline=True,
            linecolor="lightgray",
            title=dict(text=f"<b>{options.get('ylabel')}</b>"),
        ),
        xaxis=dict(
            linecolor="lightgray",
            showticklabels=False,
            title=f"<b>{options.get('xlabel')}</b>",
        ),
    )
    
    max_val = df['Ansökta utbildningar'].max()
    fig.update_xaxes(range=[0, max_val * 1.2])

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Ansökta utbildningar: %{x}",
    )

    return fig

def create_line_dia(df, title='Antal per år', x_title='År', y_title='Antal', filter_='Sökta platser totalt'):
    fig = px.line(df, x='År', y=filter_, title=title, markers=True)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=x_title,
        yaxis_title=y_title
    )
    fig.update_xaxes(showgrid=False, tickmode='array', tickvals=df['År'])
    fig.update_yaxes(showgrid=False)
    fig.update_traces(line=dict(width=4, color='cyan', dash='dot'),
        marker=dict(size=10))

    return fig
import plotly.graph_objects as go


def create_weekly_chart(df):

    if df.empty:
        fig = go.Figure()

        fig.update_layout(
            height=450,
            paper_bgcolor="#0D1117",
            plot_bgcolor="#0D1117",
            font=dict(color="white"),
            annotations=[
                dict(
                    text="No weekly data yet 📅",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=18)
                )
            ]
        )

        return fig

    categories = df["weekday"].tolist()
    values = df["score"].tolist()

    # إغلاق الدائرة
    categories += [categories[0]]
    values += [values[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            line=dict(
                color="#39D353",
                width=3
            ),
            fillcolor="rgba(57,211,83,0.35)",
            marker=dict(
                size=8,
                color="#39D353"
            ),
            hovertemplate="<b>%{theta}</b><br>%{r:.1f}%<extra></extra>"
        )
    )

    fig.update_layout(

        height=500,

        paper_bgcolor="#0D1117",
        plot_bgcolor="#0D1117",

        showlegend=False,

        font=dict(
            color="white",
            size=14
        ),

        margin=dict(
            l=30,
            r=30,
            t=30,
            b=30
        ),

        polar=dict(

            bgcolor="#0D1117",

            radialaxis=dict(
                range=[0, 100],
                showline=False,
                gridcolor="#30363d",
                tickfont=dict(color="gray")
            ),

            angularaxis=dict(
                gridcolor="#30363d",
                tickfont=dict(
                    color="white",
                    size=14
                )
            )
        )
    )

    return fig
import plotly.graph_objects as go


def create_trend_chart(df):

    fig = go.Figure()

    # لو مفيش بيانات
    if df.empty:

        fig.update_layout(
            height=300,
            paper_bgcolor="#0D1117",
            plot_bgcolor="#0D1117",
            font=dict(color="white"),
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),
            annotations=[
                dict(
                    text="No productivity data yet 📈",
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

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["score"],

            mode="lines+markers",

            line=dict(
                color="#7C5CFC",
                width=3,
                shape="spline",
                smoothing=0.5
            ),

            marker=dict(
                size=7,
                color="#7C5CFC",
                line=dict(
                    color="white",
                   width=1
                )
            ),

            fill="tozeroy",
            fillcolor="rgba(124,92,252,0.12)",

            hovertemplate=
            "<b>%{x|%d %b %Y}</b><br>"
            "Productivity: %{y}%<extra></extra>"
        )
    )

    fig.update_layout(
        height=320,

        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",

        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),

        showlegend=False,

        hovermode="x unified",

        hoverlabel=dict(
            bgcolor="#7C5CFC",
            font_color="white",
            bordercolor="#7C5CFC"
        ),

        font=dict(
            color="white"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks="outside",
        tickfont=dict(color="#B8C0CC"),

        tickformat="%b %d",
        
        nticks=6

    )

    fig.update_yaxes(
        range=[0, 100],
        gridcolor="#30363D",
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont=dict(color="#B8C0CC")
    )

    return fig
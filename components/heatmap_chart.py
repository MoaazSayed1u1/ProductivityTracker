import plotly.graph_objects as go


def create_heatmap(df):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["week"],

            y=df["weekday"],

            mode="markers",

            marker=dict(

                symbol="square",

                size=11,

                color=df["color"],

                line=dict(
                    width=0
                )

            ),

            text=df["date"].dt.strftime("%d %b %Y"),

            customdata=df["score"],

            hovertemplate=
            "<b>%{text}</b><br>"
            "Productivity: %{customdata}%"
            "<extra></extra>"
        )

    )

    fig.update_yaxes(
        fixedrange=True,
        autorange="reversed",

        tickmode="array",

        tickvals=[0, 2, 4],

        ticktext=["Mon", "Wed", "Fri"],

        showgrid=False,

        zeroline=False

    )

    fig.update_xaxes(

    showgrid=False,
    zeroline=False,
    showticklabels=False,
    fixedrange=True
    )

    fig.update_layout(

        height=180,

        paper_bgcolor="#0D1117",

        plot_bgcolor="#0D1117",

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=10
        ),

        showlegend=False

    )
    # أسماء الشهور
    month_positions = (
        df.groupby("month")["week"]
        .min()
        .reset_index()
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=month_positions["week"],
        ticktext=month_positions["month"],
        side="top",
        showticklabels=True,
        showgrid=False,
        zeroline=False,
        fixedrange=True
    )

    return fig

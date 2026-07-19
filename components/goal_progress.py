import plotly.graph_objects as go


def create_goal_progress(score, goal=80):

    remaining = max(goal - score, 0)

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",

            value=score,

            number={
                "suffix": "%",
                "font": {"size": 40}
            },

            gauge={
                "axis": {
                    "range": [0, 100]
                },

                "bar": {
                    "color": "#39D353"
                },

                "bgcolor": "#161B22",

                "steps": [
                    {
                        "range": [0, goal],
                        "color": "#21262D"
                    },
                    {
                        "range": [goal, 100],
                        "color": "#0D1117"
                    }
                ],

                "threshold": {
                    "line": {
                        "color": "#FFD33D",
                        "width": 4
                    },
                    "value": goal
                }
            }
        )
    )

    fig.update_layout(

        height=280,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        paper_bgcolor="#0D1117",

        font=dict(
            color="white"
        )
    )

    return fig
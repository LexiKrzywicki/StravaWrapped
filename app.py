from dash import Dash, html, dcc, Input, Output, callback
from stravaWrapped import StravaWrapped
import pandas as pd

df = pd.read_csv('activities.csv')
wrapped_25 = StravaWrapped(df, "2025")
wrapped_24 = StravaWrapped(df, "2024")

app = Dash()

def new_activities() -> str:
    new_activities = len(wrapped_25.get_activties()) - len(wrapped_24.get_activties())
    if new_activities > 0:
        return f"This year you discovered {new_activities} new activites"
    else:
        return "This year you discovered no new activites"
    
def no_name() -> str:
    max_pair = max(wrapped_25.get_occurences().items(), key=lambda item: item[1])
    return f" but the activity you kept coming back to was {max_pair[0]}"
    


# Requires Dash 2.17.0 or later
app.layout = html.Div(children=[
    html.H1(children='Your Strava Wrapped',
            style={
                'display': 'flex',
                'justifyContent': 'center'
    }),
    html.Div(children=new_activities() + no_name(),
             style={
                 'display': 'flex',
                 'justifyContent': 'center'
    }),
    dcc.Graph(
        id='Occurence Graph',
        figure=wrapped_25.graph_occurences()
    )
    ],
)



if __name__ == '__main__':
    app.run(debug=True)
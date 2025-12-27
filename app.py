from dash import Dash, html, dcc
from stravaWrapped import StravaWrapped
import pandas as pd

df = pd.read_csv('activities.csv')
wrapped_25 = StravaWrapped(df, "2025")

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div(children=[
    html.H1(children='Your Strava Wrapped'),
    html.Div(children='''
             Add graphs below
             '''),
    dcc.Graph(
        id='Occurence Graph',
        figure=wrapped_25.graph_occurences()
    )
    ])

if __name__ == '__main__':
    app.run(debug=True)
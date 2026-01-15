from dash import Dash, html, dcc, Input, Output, callback
from stravaWrapped import StravaWrapped
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('activities.csv')
wrapped_25 = StravaWrapped(df, "2025")
wrapped_24 = StravaWrapped(df, "2024")

app = Dash()

def new_activities() -> str:
    new_activities = len(wrapped_25.get_activties()) - len(wrapped_24.get_activties())
    if new_activities > 0:
        return f"This year you discovered {new_activities} new activites, and choose to keep coming back to {wrapped_25.max_occurence()}"
    else:
        return f"This year you discovered no new activites but the activity you kept coming back to was {wrapped_25.max_occurence()}"
    
def compare_time() -> str:
    activity = wrapped_25.max_occurence()
    curr_year_time = wrapped_25.overview()[activity]["elapsed time"]
    prev_year_time = wrapped_24.overview()[activity]["elapsed time"]
    if curr_year_time > prev_year_time:
        change = ((curr_year_time - prev_year_time) / prev_year_time) * 100
        direction = "up"
    else:
        change = ((prev_year_time - curr_year_time) /prev_year_time) * 100
        direction = "down"
    return f"Your {activity} time was {direction} {int(change)}% compared to last year!\nLet's check out how this compares to time spent doing other activities this year."
    
def went_the_distance() -> str:
    return f"You really went the distance with {wrapped_25.get_greatest_distance()} sport"

def graph_compare_distances() -> go.Figure:
    df_25 = pd.DataFrame(list(wrapped_25.get_total_distance().items()), columns=['Key', 'Value'])
    df_24 = pd.DataFrame(list(wrapped_24.get_total_distance().items()), columns=['Key', 'Value'])
    fig = go.Figure()
    trace1 = go.Bar(
        x=df_24['Key'], y=df_24['Value']
    )
    trace2 = go.Bar(
        x=df_25["Key"], y=df_25['Value']
    )
    fig = go.Figure(data=[trace1, trace2])
    fig.update_layout(
        xaxis_title='Activity',
        yaxis_title='Distnace in miles'
    )

def compare_distance() -> str:
    activity = wrapped_25.get_greatest_distance()
    curr_year_distance = wrapped_25.overview()[activity]['distance']
    prev_year_distance = wrapped_24.overview()[activity]['distance']
    if curr_year_distance > prev_year_distance:
        change = curr_year_distance - prev_year_distance
        direction = "more"
    else:
        change = prev_year_distance - curr_year_distance
        direction = "less"
    return f"You went {change} {direction} miles"

# Requires Dash 2.17.0 or later
app.layout = html.Div(children=[
    html.H1(children='Your Strava Wrapped',
            style={
                'display': 'flex',
                'justifyContent': 'center'
    }),
    html.Div(children=new_activities(),
             style={
                 'display': 'flex',
                 'justifyContent': 'center'
    }),
    html.Div(children=compare_time(),
             style={
                 'display': 'flex',
                 'justifyContent' : 'center'
             }),
    dcc.Graph(
        id='Occurence Graph',
        figure=wrapped_25.graph_times()
    ),
    html.Div(children=went_the_distance(),
             style={
                 'display': 'flex',
                 'justifyContent' : 'center'
             }),
    html.Div(children=compare_distance(),
             style={
                 'display': 'flex',
                 'justifyContent' : 'center'
             }),
    html.Div(children="Let check the distance you went with other sports",
             style={
                 'display': 'flex',
                 'justifyContent' : 'center'
             }),
    dcc.Graph(
        id='Distnace Graph',
        figure=graph_compare_distances()
    ),
    html.Div(children=str(wrapped_25.overview()),
             style={
                 'display': 'flex',
                 'justifyContent': 'center'
    }),
    html.Div(children=str(wrapped_24.overview()),
             style={
                 'display': 'flex',
                 'justifyContent': 'center'
    })  
    ],
)



if __name__ == '__main__':
    app.run(debug=True)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class StravaWrapped():
    def __init__(self, data: pd.DataFrame, year: str):
        self.data = data
        self.year = year
        mask = self.data['Activity Date'].str.contains(self.year, case=False)
        self.df = self.data[mask]
        self.activities = sorted(self.get_activties())

    def get_activties(self) -> set:
        activities = set(self.df['Activity Type'])
        return activities

    def total_time(self) -> dict:
        total_times = []
        for acitivty in self.activities:
            matches = self.df['Activity Type'] == acitivty
            total_time = float(self.df[matches]['Elapsed Time'].sum())
            # TODO: Covert mins to min : sec
            total_times.append(total_time/60)  # Convert to minutes
        return dict(list(zip(self.activities, total_times)))

    # Returns distance in miles
    def total_distance(self) -> dict:
        total_distances = []
        for activity in self.activities:
            matches = self.df['Activity Type'] == activity
            total_distance = float(self.df[matches]['Distance'].sum())
            total_distances.append(total_distance)
        return dict(list(zip(self.activities, total_distances)))
    
    # Number times for each activity
    def get_occurences(self):
        counts = []
        for acitivity in self.activities:
            count = int(self.df['Activity Type'].value_counts()[acitivity])
            counts.append(count)

        occurences = list(zip(self.activities, counts))
        return dict(occurences)
    
    def get_furthest(self) -> dict:
        furthests = []
        for activity in self.activities:
            matches = self.df['Activity Type'] == activity
            furthest = float(self.df[matches]['Distance'].max())
            furthests.append(furthest)
        return dict(list(zip(self.activities, furthests)))
    
    # TODO: add units?
    def overview(self) -> dict:
        overview = dict.fromkeys(self.activities, None)
        for activity in self.activities:
            matches = self.df['Activity Type'] == activity
            total_distance = float(self.df[matches]['Distance'].sum())  # Need to convert from meters to feet?
            furthest = float(self.df[matches]['Distance'].max())
            # TODO: convert time to min : sec
            elapsed_time = float(self.df[matches]['Elapsed Time'].sum()) / 60 
            count = int(self.df['Activity Type'].value_counts()[activity])
            overview[activity] = {"distance": total_distance, "furthest": furthest, "elapsed time": elapsed_time, "occurences": count}
        return overview
    
    def graph_occurences(self) -> go.Figure:
        df = pd.DataFrame(list(self.get_occurences().items()), columns=['Key', 'Value'])
        fig = px.bar(df, x='Key', y='Value', title='Number of times per acitivity', labels={'Key': 'Activity', 'Value': 'Occurences'})
        return fig


def main():
    df = pd.read_csv('activities.csv')
    wrapped_24 = StravaWrapped(df, "2024")
    wrapped_25 = StravaWrapped(df, "2025")
    print(wrapped_24.get_occurences())
    print(wrapped_25.overview())

if __name__ == "__main__":
    main()
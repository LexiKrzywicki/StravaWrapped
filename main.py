import pandas as pd

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
            overview[activity] = {"distance": total_distance, "furthest": furthest, "elapsed time": elapsed_time, "times": count}
        return overview



def main():
    df = pd.read_csv('activities.csv')
    wrapped_24 = StravaWrapped(df, "2024")
    wrapped_25 = StravaWrapped(df, "2025")
    print(wrapped_24.overview())
    print(wrapped_25.overview())


if __name__ == "__main__":
    main()
import pandas as pd

class StravaWrapped():
    def __init__(self, data: pd.DataFrame, year: str):
        self.data = data
        self.year = year
        mask = self.data['Activity Date'].str.contains(self.year, case=False)
        self.df = self.data[mask]

    def get_activties(self) -> set:
        activities = set(self.df['Activity Type'])
        return activities
    
    # Returns time in minutes
    def total_time(self) -> dict:
        total_times = []
        for acitivty in self.get_activties():
            matches = self.df['Activity Type'] == acitivty
            total_time = float(self.df[matches]['Elapsed Time'].sum())
            total_times.append(total_time/60)  # Convert to minutes
        return dict(list(zip(self.get_activties(), total_times)))
    
    # Returns distance in miles
    def total_distance(self) -> dict:
        total_distances = []
        for activity in self.get_activties():
            matches = self.df['Activity Type'] == activity
            total_distance = float(self.df[matches]['Distance'].sum())
            total_distances.append(total_distance)
        return dict(list(zip(self.get_activties(), total_distances)))
    
    # Number times for each activity
    def get_occurences(self):
        counts = []
        for acitivity in self.get_activties():
            count = int(self.df['Activity Type'].value_counts()[acitivity])
            counts.append(count)
        
        occurences = list(zip(self.get_activties(), counts))
        return dict(occurences)


def main():
    df = pd.read_csv('activities.csv')
    wrapped_24 = StravaWrapped(df, "2024")
    wrapped_25 = StravaWrapped(df, "2025")
    print(wrapped_24.total_distance())
    print(wrapped_25.total_time())
    #print(dfs['Activity Date'][1])


if __name__ == "__main__":
    main()
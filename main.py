import pandas as pd

class StravaWrapped():
    def __init__(self, data: pd.DataFrame, year: str):
        self.data = data
        self.year = year
        mask = self.data['Activity Date'].str.contains(self.year, case=False)
        self.df = self.data[mask]
        self.activities = self.get_activties()

    def get_activties(self) -> set:
        activities = set(self.df['Activity Type'])
        return activities
    
    # Returns time in minutes
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


def main():
    df = pd.read_csv('activities.csv')
    wrapped_24 = StravaWrapped(df, "2024")
    wrapped_25 = StravaWrapped(df, "2025")
    print(wrapped_24.get_occurences())
    print(wrapped_24.total_distance())
    print(wrapped_24.total_time())
    print(wrapped_24.get_furthest())


if __name__ == "__main__":
    main()
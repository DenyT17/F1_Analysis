import pandas as pd
from functions import top3_stand_num,plot_top, season_stats

## Loading data from csv files
circuits_data = pd.read_csv("data/circuits.csv")
constructor_results_data = pd.read_csv("data/constructor_results.csv")
constructor_standings_data = pd.read_csv("data/constructor_standings.csv")
constructors_data = pd.read_csv("data/constructors.csv")
driver_standings_data = pd.read_csv("data/driver_standings.csv")
drivers_data = pd.read_csv("data/drivers.csv")
lap_times_data = pd.read_csv("data/lap_times.csv")
pit_stops_data = pd.read_csv("data/pit_stops.csv")
qualifying_data = pd.read_csv("data/qualifying.csv")
races_data = pd.read_csv("data/races.csv")
results_data = pd.read_csv("data/results.csv")
seasons_data = pd.read_csv("data/seasons.csv")
sprint_results_data = pd.read_csv("data/sprint_results.csv")
status_data = pd.read_csv("data/status.csv")

# Drivers stats
# drivers_stats = drivers_data[["driverId","forename","surname"]]
# drivers_stats = drivers_stats.merge(top3_stand_num(driver_standings_data),on="driverId")
# drivers_stats = drivers_stats.loc[:, ~drivers_stats.columns.duplicated()]
# plot_top(5,drivers_stats,"surname",["First","Second","Third"])

# Title fight animation
print(season_stats(2022,races_data,drivers_data,driver_standings_data))



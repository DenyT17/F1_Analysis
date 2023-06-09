import pandas as pd
from functions import top3_stand_num,plot_top, season_stats, animation_plot, download_img, constructors_points, best_lap_time, drivers_points

pd.set_option('display.max_rows', None)

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


# # Downloading main wikipedia image at every driver
download_img(drivers_data)

# # Drivers stats
drivers_stats = drivers_data[["driverId","forename","surname"]]
drivers_stats = drivers_stats.merge(top3_stand_num(driver_standings_data),on="driverId")
drivers_stats = drivers_stats.loc[:, ~drivers_stats.columns.duplicated()]
plot_top(5,drivers_stats,"surname",["First","Second","Third"])

# # Title fight animation
season_stats, year = season_stats(2008,races_data,drivers_data,driver_standings_data)
print(season_stats)
animation_plot(season_stats, year)

# # Summary number of constructors points over the years
constructors_points(results_data,races_data,constructors_data)

# # Summary number of drivers points over the years
drivers_points(results_data,races_data,drivers_data)

# # History of fastest laps over the years on selected tracks
best_lap_time(circuits_data,races_data,lap_times_data)
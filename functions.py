import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib
import bar_chart_race as bcr
import requests, os
import datetime

## Function calculating the number of places on the podium for each competitor
def top3_stand_num(data : pandas.DataFrame):
    positions = {1:"First",2:"Second",3:"Third"}
    for key in positions:
        data[positions[key]] = np.where(data["position"] == key,1,0)

    top3 = data[["driverId","First","Second","Third"]].groupby(by="driverId").sum()
    top3["Top3_Sum"] = top3.sum(axis=1)
    top3 = top3.reset_index()
    return top3
## Function plotting ranking based on  any columns
def plot_top(number:int, data:pandas.DataFrame, x_label: str,columns:list):
    title = "driver's" if x_label=="surname" else "constructor's"
    data.sort_values(by=columns,ascending=False,inplace=True)
    data.head(number).plot(x=x_label,y=columns,kind='bar',rot=0)
    plt.title("Number of {}  {},places".format(title,', '.join(columns)))
    plt.tight_layout()
    plt.show()

def season_stats(year:int, races_data : pandas.DataFrame, drivers_data : pandas.DataFrame,driver_standings : pandas.DataFrame):
    season_data = races_data.loc[races_data["year"] == year]
    season_data = season_data[["raceId","year","round","sprint_date"]]
    season_results = pd.DataFrame()
    for raceId in season_data["raceId"].values:
        season_results = pd.concat([season_results,driver_standings.loc[(driver_standings["raceId"]) == raceId]])
    table = pd.DataFrame(season_results["driverId"].drop_duplicates())
    drivers = pd.DataFrame()
    for driver in table["driverId"].values:
        drivers = pd.concat([drivers,drivers_data[["driverId","driverRef"]].loc[(drivers_data["driverId"]) == driver]])
    drivers = drivers.drop_duplicates().reset_index(drop=True)

    race_number = 1
    for race in season_results["raceId"].unique():
        race_stat = season_results.loc[(season_results["raceId"]==race)]
        new_name = f"Points after {race_number} races"
        race_stat = race_stat.rename(columns={"points":new_name})
        drivers = pd.merge(drivers,race_stat[["driverId",new_name]],how='outer',on = "driverId")
        race_number+=1
    drivers = drivers.drop(["driverId"],axis=1)
    drivers = drivers.set_index("driverRef")
    drivers = drivers.fillna(0).T
    return drivers, year

#Function to downloading main wikipedia image at every driver
def download_img(drivers_data : pandas.DataFrame):
    os.makedirs("data/Drivers Image", exist_ok=True)
    i = 1
    query = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

    for index, row in drivers_data.iterrows():
        if os.path.isfile(f"data/Drivers Image/{row['driverRef']}.jpg"):
            print(f"data/Drivers Image/{row['driverRef']}.jpg - existing")
        else:
            try:
                api_res = requests.get(query + row["url"].split("wiki/",1)[1]).json()

                first_part = api_res['query']['pages']
                for key, value in first_part.items():
                    if (value['original']['source']):
                        data = value['original']['source']
            except Exception as exc:
                data = "https://snworksceo.imgix.net/dtc/3f037af6-87ce-4a37-bb37-55b48029727d.sized-1000x1000.jpg?w=1000"
            urllib.request.urlretrieve(data, f"data/Drivers Image/{row['driverRef']}.jpg")
            print(f"{row['driverRef']} image downloaded  \n {i}/{len(drivers_data.index)}")
        i+=1
#
def animation_plot(data : pandas.DataFrame,  year : int):
    bcr.bar_chart_race(
        df=data,
        filename=f'Title fight animation - {year} season.mp4',
        orientation='h',
        sort='desc',
        n_bars=10,
        fixed_order=False,
        fixed_max=True,
        steps_per_period=10,
        interpolate_period=False,
        label_bars=True,
        bar_size=.95,
        period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
        period_length=500,
        figsize=(5, 3),
        dpi=320,
        cmap='dark12',
        title=f'Title fight animation - {year} season',
        title_size='',
        bar_label_size=7,
        tick_label_size=7,
        shared_fontdict={'family': 'Helvetica', 'color': '.1'},
        scale='linear',
        writer=None,
        fig=None,
        bar_kwargs={'alpha': .7},
        filter_column_colors=False)

# Number of constructors points over the years
def constructors_points(results_data : pandas.DataFrame,
                        race_data : pandas.DataFrame,
                        constructors_data : pandas.DataFrame):
    constructors = pd.merge(race_data[["raceId","year"]],results_data[["raceId","constructorId","points"]],
                            how='outer',on = "raceId")
    constructors = constructors.dropna()
    constructors = constructors.sort_values(by= ["year","raceId","constructorId","points"])
    constructors['sum'] = constructors.groupby(['constructorId'])['points'].cumsum()
    constructors = constructors.drop_duplicates(subset=["raceId","year","constructorId"],keep='last')
    constructors = constructors.drop(["points", "raceId"], axis=1)
    constructors = pd.merge(constructors, constructors_data[["constructorId","name"]],how='outer',on = "constructorId")
    constructors = constructors.drop(["constructorId"],axis=1)
    constructors = constructors.dropna()

    constructors["year"] = constructors["year"].astype(np.int64)
    constructors = constructors.pivot_table(index='year', columns='name', values='sum')
    constructors = constructors.fillna(value=0)
    max = 0
    for data in constructors.columns.values:
        for index, row in constructors.iterrows():
            if max < row[data]:
                max = row[data]
            if row[data] == 0:
                row[data] = max
        max = 0
    bcr.bar_chart_race(
        df=constructors,
        filename=f'Summary number of constructors points over the yearss.mp4',
        orientation='h',
        sort='desc',
        n_bars=10,
        fixed_order=False,
        fixed_max=False,
        steps_per_period=10,
        interpolate_period=False,
        label_bars=True,
        bar_size=.90,
        period_label={'x': .8, 'y': .10, 'ha': 'right', 'va': 'center'},
        period_fmt='Year : {x:.0f}',
        period_length=600,
        figsize=(8, 5),
        dpi=320,
        cmap='dark12',
        title=f'Summary number of constructors points over the years',
        title_size='',
        bar_label_size=7,
        tick_label_size=7,
        shared_fontdict={'family': 'Helvetica', 'color': '.1'},
        scale='linear',
        writer=None,
        fig=None,
        bar_kwargs={'alpha': .2, 'ec': 'black', 'lw': 3},
        filter_column_colors=False)

def best_lap_time(circuits : pandas.DataFrame,
                  races : pandas.DataFrame,
                  lap_times : pandas.DataFrame):
    races_data = races.loc[(races["circuitId"] == 18)]
    races_data = races_data[["raceId","year"]]
    lap = pd.DataFrame()
    for raceId in races_data["raceId"].values:
        lap = pd.concat([lap, lap_times[["raceId","milliseconds"]].loc[(lap_times["raceId"]) == raceId]])

    lap = lap.groupby(["raceId"]).min()
    best_time = pd.merge(races_data,lap,how='outer',on = "raceId")
    best_time = best_time.sort_values(by="year")
    best_time = best_time.dropna()
    plt.plot(best_time["year"],best_time["milliseconds"])
    plt.show()


def drivers_points(results_data : pandas.DataFrame,
                        race_data : pandas.DataFrame,
                        drivers_data : pandas.DataFrame):
    drivers = pd.merge(race_data[["raceId","year"]],results_data[["raceId","driverId","points"]],
                            how='outer',on = "raceId")
    drivers = drivers.dropna()
    drivers = drivers.sort_values(by= ["year","raceId","driverId","points"])
    drivers['sum'] = drivers.groupby(['driverId'])['points'].cumsum()
    drivers = drivers.drop_duplicates(subset=["raceId","year","driverId"],keep='last')
    drivers = drivers.drop(["points", "raceId"], axis=1)
    drivers = pd.merge(drivers, drivers_data[["driverId","driverRef"]],how='outer',on = "driverId")
    drivers = drivers.drop(["driverId"],axis=1)
    drivers = drivers.dropna()

    drivers["year"] = drivers["year"].astype(np.int64)
    drivers = drivers.pivot_table(index='year', columns='driverRef', values='sum')
    drivers = drivers.fillna(value=0)
    max = 0
    for data in drivers.columns.values:
        for index, row in drivers.iterrows():
            if max < row[data]:
                max = row[data]
            if row[data] == 0:
                row[data] = max
        max = 0
    print(drivers)
    bcr.bar_chart_race(
        df=drivers,
        filename=f'Summary number of drivers points over the years.mp4',
        orientation='h',
        sort='desc',
        n_bars=10,
        fixed_order=False,
        fixed_max=False,
        steps_per_period=10,
        interpolate_period=False,
        label_bars=True,
        bar_size=.90,
        period_label={'x': .8, 'y': .10, 'ha': 'right', 'va': 'center'},
        period_fmt='Year : {x:.0f}',
        period_length=600,
        figsize=(8, 5),
        dpi=320,
        cmap='dark12',
        title=f'Summary number of drivers points over the years',
        title_size='',
        bar_label_size=7,
        tick_label_size=7,
        shared_fontdict={'family': 'Helvetica', 'color': '.1'},
        scale='linear',
        writer=None,
        fig=None,
        bar_kwargs={'alpha': .7},
        filter_column_colors=False)
import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ffmpeg
import bar_chart_race as bcr




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
        dpi=50,
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
import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




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
    drivers = drivers.pivot_table(index=None,columns="driverRef",values=None).reset_index(drop=True).drop([0],axis=0)

    return drivers


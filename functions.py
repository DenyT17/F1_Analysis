import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function calculating the number of places on the podium for each competitor
def top3_stand_num(data : pandas.DataFrame):
    positions = {1:"First",2:"Second",3:"Third"}
    for key in positions:
        data[positions[key]] = np.where(data["position"] == key,1,0)

    top3 = data[["driverId","First","Second","Third"]].groupby(by="driverId").sum()
    top3["Top3_Sum"] = top3.sum(axis=1)
    top3 = top3.reset_index()
    return top3
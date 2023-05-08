import pandas as pd
from sjvisualizer import DataHandler, Canvas, BarRace, StaticImage
from funcitons import new_column
data = pd.read_csv("Data/La_Liga_Matches/matches.csv")
data.dropna()
data = data[["season","team","round","result"]]
data['Points'] = data.result.apply(new_column)
data['round'] = data['round'].map(lambda x: x.lstrip('Matchweek '))
data['round'] = data["round"].astype(int)
data = data.sort_values(by=["season","round"]).reset_index(drop=True)
data["Sum"] = data.groupby(['team'])['Points'].cumsum()
data["Season_round"] = data["season"].astype(str) +"-"+ data["round"].astype(str)
data = data[["team", "season","round", "Sum"]].pivot_table(index=["season","round"], columns="team",                                                                          values="Sum")
data = data.fillna(value=0)
max = 0
for x in data.columns.values:
    for index, row in data.iterrows():
        if max < row[x]:
            max = row[x]
        if row[x] == 0:
             row[x] = max
    max = 0
year = [d[0] for d in data.index]
print(data)
canvas = Canvas.canvas()
bar_chart = BarRace.bar_race(df=data, canvas=canvas.canvas)
canvas.add_sub_plot(bar_chart)
canvas.add_title("La Liga Teams points", color=(0,0,0))
canvas.add_sub_title("From 1999 - 2023", color=(150,150,150))
canvas.play(fps=60)
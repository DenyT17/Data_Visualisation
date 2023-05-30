import pandas as pd
from funcitons import new_column, select_club_and_season
from matplotlib.animation import FuncAnimation, FFMpegWriter
from itertools import count
import sys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

Real_IMG =Image.open(r"C:\Users\Dtopa\OneDrive\Pulpit\ML\Data_Visualisation\clubs_img\Real Madrid.png").convert('RGB')
Barcelona_IMG = Image.open(r"C:\Users\Dtopa\OneDrive\Pulpit\ML\Data_Visualisation\clubs_img\Barcelona.png").convert('RGB')

Real_IMG = Real_IMG.resize((np.array(Real_IMG.size)/4).astype(int))
Barcelona_IMG = Barcelona_IMG.resize((np.array(Barcelona_IMG.size)/4).astype(int))

data = pd.read_csv("Data/La_Liga_Matches/matches.csv")
data.dropna()
data = data[["season","team","round","result"]]
data['Points'] = data.result.apply(new_column)
data['round'] = data['round'].map(lambda x: x.lstrip('Matchweek '))
data['round'] = data["round"].astype(int)
data = data.sort_values(by=["season","round"]).reset_index(drop=True)
data["Sum"] = data.groupby(['team'])['Points'].cumsum()
data["Season_round"] = data["season"].astype(str) +"-"+ data["round"].astype(str)
data = data[["team", "season","round", "Sum"]].pivot_table(index=["season","round"], columns="team",values="Sum")
data = data.fillna(value=0)
max = 0
for x in data.columns.values:
    for index, row in data.iterrows():
        if max < row[x]:
            max = row[x]
        if row[x] == 0:
             row[x] = max
    max = 0

clubs = {}
data = data[["Real Madrid","Barcelona"]]
for club in data.columns:
    clubs[club] = []
x = []
plt.style.use("Solarize_Light2")
rounds = [t[1] for t in data.index]
years =  [t[0] for t in data.index]
fig, ax = plt.subplots(figsize=(12, 5))
for key in clubs:
    if key == "Barcelona":
        color = "blue"
    elif key == "Real Madrid":
        color = "yellow"
    ax.plot(x, clubs[key], linewidth=5, label=key,color=color)
counter = count(0, 1)

def update(i):
    ax.cla()
    ax.set_ylabel('Points')
    ax.set_title("Real Madrid vs Barcelona\nPoint Battle 1999 - 2023")
    time = ax.annotate(
        "Time", xy=(0, 0), xytext=(0, 0), )
    Real = ax.annotate(
        "Real", xy=(0, 0), xytext=(0, 0), )
    Barcelona = ax.annotate(
        "Barcelona", xy=(0, 0), xytext=(0, 0), )
    idx = next(counter)
    max = 0
    try:
        x.append(idx)
        for key in clubs:
            clubs[key].append(data[key].iloc[idx])
            if data[key].iloc[idx] > max:
                max = data[key].iloc[idx]
    except IndexError:
        time.sleep(2)
        sys.exit(1)
    if x[i] > 30:
        ax.set_xlim(idx-30, idx+10)
        ax.set_ylim(max - 50, max + 20)
        x_text = idx - 27
    else:
        ax.set_xlim(0, idx + 10)
        ax.set_ylim(max - 50, max + 20)
        x_text = idx/10
    for key in clubs:
        if key == "Barcelona":
            color = "blue"
            ax.add_artist(AnnotationBbox(OffsetImage(Barcelona_IMG),
                                         (idx, data[key].iloc[idx]),
                                         bboxprops =dict(edgecolor=color,boxstyle="Circle, pad=1")))

        elif key == "Real Madrid":
            color = "yellow"
            ax.add_artist(AnnotationBbox(OffsetImage(Real_IMG),
                                         (idx, data[key].iloc[idx]),
                                         bboxprops =dict(edgecolor=color,boxstyle="Circle, pad=1")))

        ax.plot(x, clubs[key], linewidth=10, label=key,color=color)
        ax.legend(loc='upper right')

        if data[key].iloc[idx] > max:
            max = data[key].iloc[idx]
    time.xy = (x_text, max+10)
    time.set_position((x_text,  max+10))
    time.set_text(f"Year - {years[i]}, round {rounds[i]} ")

    Real.xy = (x_text, max+5)
    Real.set_position((x_text, max+5))
    Real.set_text(f"Real Madrid - {data['Real Madrid'].iloc[idx]} points")

    Barcelona.xy = (x_text, max)
    Barcelona.set_position((x_text, max))
    Barcelona.set_text(f"Barcelona  - {data['Barcelona'].iloc[idx]} points")


ani = FuncAnimation(fig=fig, func=update, interval=10)

FFwriter = FFMpegWriter(fps=30)
ani.save('Real_Barca.mp4', writer=FFwriter)

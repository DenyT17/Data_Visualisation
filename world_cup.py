import pandas as pd
from funcitons import new_column, select_club_and_season
import bar_chart_race as bcr

from matplotlib.animation import FuncAnimation, FFMpegWriter
from itertools import count
import sys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time
import random
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import flagpy as fp
data = pd.read_csv(r"C:\Users\Dtopa\OneDrive\Pulpit\ML\Data_Visualisation\Data\World_cup")
data = data[["date","result","representation"]]
data['points'] = data.result.apply(new_column)
data = data.sort_values(by="date").reset_index(drop=True)
data["sum"] = data.groupby(['representation'])['points'].cumsum()
data = data.drop_duplicates(subset=['date', 'representation'], keep='last')
data = data[["representation", "date", "sum"]].pivot_table(index="date", columns="representation",values="sum",fill_value=0,aggfunc='sum')
data = data.fillna(value=0)
max = 0
for x in data.columns.values:
    for index, row in data.iterrows():
        if max < row[x]:
            max = row[x]
        if row[x] == 0:
             row[x] = max
    max = 0
data["Germany"] = data["Germany"] + data["West Germany"]
data = data[["Brazil","Germany","Italy","Argentina","France"]]
index = count()
team_img = {}
x = []
colors = ["blue","green","red","cyan","magenta","yellow","black","white"]
teams_colors = {}
plt.style.use("bmh")
fig, ax = plt.subplots(figsize=(12, 5))
img_path = r"C:\Users\Dtopa\OneDrive\Pulpit\ML\Data_Visualisation\Data\National"
for team in data.columns:
    team_img[team] = fp.get_flag_img(team)
    team_img[team] = team_img[team].resize((np.array(team_img[team].size) / 5).astype(int))
teams = {}
for team in data.columns:
    teams[team] = []
for key in teams:
    teams_colors[key] = random.choice(colors)
    colors.remove(teams_colors[key])
    ax.plot(x, teams[key], linewidth=5, label=key, color=teams_colors[key])
counter = count(0, 1)
i_list = []
def update(i):
    if not i in i_list:
        i_list.append(i)
    else:
        i+=1
        i_list.append(i)
    ax.cla()
    ax.set_ylabel('Points')
    ax.set_xlabel('Year')
    ax.set_title("Top 5 countries with the most points at the\n World Cup (1930 - 2022)")
    idx = next(counter)
    max = 0
    min = 1000
    try:
        x.append(data.index[i])
        for key in teams:
            teams[key].append(data[key].iloc[idx])
            if data[key].iloc[idx] > max:
                max = data[key].iloc[idx]
            if data[key].iloc[idx] < min:
                min = data[key].iloc[idx]
    except IndexError:
        time.sleep(2)
        sys.exit(1)

    ax.set_xlim(data.index[i]-8, data.index[i]+4)
    if data.index[i]-8 < 1930:
        ax.set_xlim(1930, max + 20)
    else:
        ax.set_xlim(data.index[i]-8, data.index[i]+4)

    if min - 20 < 0:
        ax.set_ylim(0, max + 20)
    else:
        ax.set_ylim(min - 20, max + 20)


    for key in teams:
        for img in team_img:
            if key == img:
                color = teams_colors[key]
                ax.add_artist(AnnotationBbox(OffsetImage(team_img[img]),
                                             (data.index[i], data[key].iloc[idx]),
                                             bboxprops=dict(edgecolor=color, boxstyle="Circle, pad=0.5")))

    path = rf"C:\Users\Dtopa\OneDrive\Pulpit\ML\Data_Visualisation\Data\World_Cup_IMG\{str(data.index[i])}" + ".png"
    world_cup_img = Image.open(path).convert('RGB')
    world_cup_img = world_cup_img.resize((np.array(world_cup_img.size) / 1.5).astype(int))
    ax.add_artist(AnnotationBbox(OffsetImage(world_cup_img),
                                 (data.index[i]+3, (max+min)/2),
                                 bboxprops=dict(boxstyle="Square, pad=0.5")))

    for key in teams:
        ax.plot(x, teams[key], linewidth=10, label=key, color=teams_colors[key])
        ax.legend(loc='upper right',facecolor="white")
        if data[key].iloc[idx] > max:
            max = data[key].iloc[idx]
ani = FuncAnimation(fig=fig, func=update,frames=len(data.index), interval=600)
# plt.show()
FFwriter = FFMpegWriter(fps=2)
ani.save(r'C:\Users\Dtopa\OneDrive\Pulpit\ML\Data_Visualisation\results\WC.mp4', writer=FFwriter)

# bcr.bar_chart_race(
#         df=data,
#         filename=f'World_Cup.mp4',
#         orientation='h',
#         sort='desc',
#         n_bars=5,
#         fixed_order=False,
#         fixed_max=False,
#         steps_per_period=20,
#         interpolate_period=False,
#         bar_size=.90,
#         period_label={'x': .8, 'y': .10, 'ha': 'right', 'va': 'center'},
#         period_length=800,
#         title=f'Top 5 countries with the most points at the World Cup',
#         shared_fontdict={'family': 'Helvetica', 'color': '.1'},
#         scale='linear',
#         writer=None,
#         fig=None,
#         bar_kwargs={'alpha': .7},
#         filter_column_colors=False)
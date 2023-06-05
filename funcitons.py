import pandas as pd
from matplotlib import style
import bar_chart_race as bcr
from matplotlib.animation import FuncAnimation, FFMpegWriter
from itertools import count
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import sys
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
import time
import mplcyberpunk
from PIL import Image
import numpy as np
def salary_calculated(x):
    if "Loan fee:€" in x["fee"]:
        if "m" in x["fee"]:
            return x["fee"][10:len(x["fee"])-4] + "000000"
        elif "Th." in x["fee"] or "k" in x["fee"]:
            return x["fee"][10:len(x["fee"]) - 3] + "000"
        else:
            return x["fee"][10:]
    elif "Th." in x["fee"] or "k" in x["fee"]:
        return x["fee"][1:len(x["fee"])-3] + "000"
    elif "m" in x["fee"]:
        return x["fee"][1:len(x["fee"])-4] + "000000"
    elif "€" in x["fee"]:
        return x["fee"][1:]
    else:
        return 0
def result_calculated(x):
    if x["transfer_movement"] == "in":
        return  x["Price"]
    elif x["transfer_movement"] == "out":
        return 0


def sum_expense(league_data):
    data = league_data.dropna(subset=["fee"])
    data["Price"] = data.apply(salary_calculated, axis=1)
    data["Price"] = data["Price"].astype(int)
    data["Result"] = data.apply(result_calculated, axis=1)
    data["Sum"] = data.groupby(['club_name'])['Result'].cumsum()
    data["Sum"] = data["Sum"]
    data = data[["club_name", "year", "Sum"]].pivot_table(index="year", columns="club_name",
                                                                              values="Sum")
    data = data.fillna(value=0)
    max = 0
    for x in data.columns.values:
        for index, row in data.iterrows():
            if max < row[x]:
                max = row[x]
            if row[x] == 0:
                row[x] = max
        max = 0
    return data
def bar_chart_race(data,title):
    bcr.bar_chart_race(
        df=data,
        filename=f'{title}.mp4',
        orientation='h',
        sort='desc',
        n_bars=5,
        fixed_order=False,
        fixed_max=False,
        steps_per_period=20,
        interpolate_period=False,
        label_bars=True,
        bar_size=.90,
        period_label={'x': .8, 'y': .10, 'ha': 'right', 'va': 'center'},
        period_fmt='Year : {x:.0f}',
        period_length=1000,
        figsize=(8, 5),
        dpi=320,
        cmap='plotly3',
        title=f'{title}',
        title_size='',
        bar_label_size=7,
        tick_label_size=7,
        shared_fontdict={'family': 'Helvetica', 'color': '.1'},
        scale='linear',
        writer=None,
        fig=None,
        bar_kwargs={'alpha': .7},
        filter_column_colors=False)

def top_5(data,league_name):
    data = data.dropna(subset=["fee"])
    data["Price"] = data.apply(salary_calculated, axis=1)
    data["Price"] = data["Price"].astype(int)
    data["Result"] = data.apply(result_calculated, axis=1)
    data["Sum"] = data['Result'].cumsum()
    data["League"] = league_name
    data = data[["League", "year", "Sum"]].pivot_table(index="year", columns="League",
                                                          values="Sum")
    return data



def line_plot(data):
    x = []
    Serie_A = []
    La_Liga = []
    Premier_League = []
    Bundesliga = []
    Ligue = []
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(x, Serie_A, linewidth=5, color="b", label='Serie A')
    ax.plot(x, La_Liga, linewidth=5, color="r", label='La Liga')
    ax.plot(x, Premier_League, linewidth=5, color="g", label='Premier League')
    ax.plot(x, Bundesliga, linewidth=5, color="y", label='Bundesliga ')
    ax.plot(x, Ligue, linewidth=5, color="c", label='Ligue 1')
    ax.set_xlim(1990,2023)
    ax.set_ylim(10**6,3*10**10)
    ax.legend(loc='upper left')
    ax.set_xlabel('Year')
    ax.set_ylabel('League expenses')
    ax.set_title('Top 5 Leagues expenses')
    counter = count(0, 1)

    Serie_A_text = ax.annotate(
        "Serie A", xy=(0,0),xytext=(0, 0),)
    La_Liga_text = ax.annotate(
        "La Liga", xy=(0,0),xytext=(0, 0),)
    Premier_League_text = ax.annotate(
        "Premier League", xy=(0,0),xytext=(0, 0),)
    Bundesliga_text = ax.annotate(
        "Bundesliga", xy=(0,0),xytext=(0, 0),)
    Ligue_text = ax.annotate(
        "Ligue", xy=(0,0),xytext=(0, 0),)
    def update(i):
        idx = next(counter)
        try:
            x.append(data.index[idx])
            Serie_A.append(data["Serie A"].iloc[idx])
            La_Liga.append(data["La Liga"].iloc[idx])
            Premier_League.append(data["Premier League"].iloc[idx])
            Bundesliga.append(data["Bundesliga"].iloc[idx])
            Ligue.append(data["Ligue 1"].iloc[idx])

            Serie_A_text.xy = (1991,1.8 *10**10)
            Serie_A_text.set_position((1991,1.8 *10**10))
            Serie_A_text.set_text(f"Serie A - {round(round(Serie_A[-1])/10**6,1)} milion €")

            La_Liga_text.xy = (1991, 1.6 * 10 ** 10)
            La_Liga_text.set_position((1991, 1.6 * 10 ** 10))
            La_Liga_text.set_text(f"La Liga - {round(round(La_Liga[-1]) / 10 ** 6,1)} milion €")

            Premier_League_text.xy = (1991, 1.4 * 10 ** 10)
            Premier_League_text.set_position((1991, 1.4 * 10 ** 10))
            Premier_League_text.set_text(f"Premier League - {round(round(Serie_A[-1]) / 10 ** 6,1)} milion €")

            Bundesliga_text.xy = (1991, 1.2 * 10 ** 10)
            Bundesliga_text.set_position((1991, 1.2 * 10 ** 10))
            Bundesliga_text.set_text(f"Bundesliga - {round(round(Serie_A[-1]) / 10 ** 6,1)} milion €")

            Ligue_text.xy = (1991, 1 * 10 ** 10)
            Ligue_text.set_position((1991, 1 * 10 ** 10))
            Ligue_text.set_text(f"Ligue 1 - {round(round(Serie_A[-1]) / 10 ** 6, 1)} milion €")
        except IndexError:
            time.sleep(2)
            sys.exit(1)


        ax.plot(x, Serie_A,linewidth=5, color="b", label='Serie A')
        ax.plot(x, La_Liga,linewidth=5, color="r",label='La Liga')
        ax.plot(x, Premier_League,linewidth=5, color="g",label='Premier League')
        ax.plot(x, Bundesliga,linewidth=5, color="y",label='Bundesliga ')
        ax.plot(x, Ligue,linewidth=5, color="c",label='Ligue 1')


    ani = FuncAnimation(fig=fig, func=update, interval=400)
    # plt.show()
    FFwriter = FFMpegWriter(fps=3)
    ani.save('Top_5.mp4', writer=FFwriter)

def new_column(result):
    if result == "D":
        return 1
    elif result == "W":
        return 3
    else:
        return 0

def select_club_and_season(data : pd.DataFrame, club : list, seasons : int ):
    data = data[club]
    data = data[[seasons == s[0] for s in data.index]]
    return  data

def season_data_preparation(data: pd.DataFrame):
    data.dropna()
    data = data[["season", "team", "round", "result"]]
    data['Points'] = data.result.apply(new_column)
    data['round'] = data['round'].map(lambda x: x.lstrip('Matchweek '))
    data['round'] = data["round"].astype(int)
    data = data.sort_values(by=["season", "round"]).reset_index(drop=True)
    data["Sum"] = data.groupby(['team'])['Points'].cumsum()
    data["Season_round"] = data["season"].astype(str) + "-" + data["round"].astype(str)
    data = data[["team", "season", "round", "Sum"]].pivot_table(index=["round"], columns="team", values="Sum")
    data = data.fillna(value=0)
    max = 0
    for x in data.columns.values:
        for index, row in data.iterrows():
            if max < row[x]:
                max = row[x]
            if row[x] == 0:
                row[x] = max
        max = 0
    data.loc[0] = 0
    data.sort_index(inplace=True)
    return data

def season_plot(data: pd.DataFrame, img_path:str):
    print(data)
    PL_img = Image.open(r"C:\Users\Dtopa\OneDrive\Pulpit\ML\Data_Visualisation\Data\SA.png").convert('RGB')
    PL_img = PL_img.resize((np.array(PL_img.size)/2.5).astype(int))
    clubs = {}
    teams_img = {}
    teams = {}
    for team in data.columns:
        teams[team] = []
    for team in data.columns:
        teams_img[team] = Image.open(
            fr"{img_path}\{team}.png").convert('RGB')
        teams_img[team] = teams_img[team].resize((np.array(teams_img[team].size) / 5).astype(int))
    for club in data.columns:
        clubs[club] = []
    x = []
    teams_colors = {}
    plt.style.use("cyberpunk")
    fig, ax = plt.subplots(figsize=(12, 6))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width*0.85, box.height * 0.9])
    for key in clubs:
        teams_colors[key] = (np.random.random(), np.random.random(), np.random.random())
        ax.plot(x, clubs[key], linewidth=5, label=key, color=teams_colors[key])
    counter = count(0, 1)
    def update(i):
        ax.cla()
        ax.set_ylabel('Points')
        ax.set_xlabel('Round')
        ax.set_title("Serie A - Title Battle\nSeason 2022/2023")

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
        for key in teams:
            for img in teams_img:
                if key == img:
                    color = teams_colors[key]
                    ax.add_artist(AnnotationBbox(OffsetImage(teams_img[img]),
                                                 (idx, data[key].iloc[idx]),
                                                 bboxprops=dict(edgecolor=color, boxstyle="Circle, pad=1")))
        if idx - 10 > 0:
            ax.set_xlim(idx - 10, idx + 2)
            ax.set_ylim(max - 22, max + 5)
            pl_x = idx - 9
            pl_y = max
        else:
            ax.set_xlim(0, 12)
            ax.set_ylim(0, 30)
            pl_x = 1
            pl_y = 25
        for key in clubs:

            ax.plot(x, clubs[key], linewidth=9, label=key, color=teams_colors[key])
            ax.add_artist(AnnotationBbox(OffsetImage(PL_img),
                                         (pl_x, pl_y),
                                         bboxprops=dict(boxstyle="Circle, pad=1.2",ec="Green", lw=2)))
            ax.legend(bbox_to_anchor=(1.315, 1.009), borderaxespad=0,facecolor="white")
            if data[key].iloc[idx] > max:
                max = data[key].iloc[idx]
    ani = FuncAnimation(fig=fig, func=update, frames=38,interval=10)
    FFwriter = FFMpegWriter(fps=3)
    ani.save('SA2022_2023.mp4', writer=FFwriter)
    # plt.show()

def disney(data:pd.DataFrame):
    films = {}
    film_colors = {}
    for film in data.columns:
        films[film] = []
    x = []
    plt.style.use("cyberpunk")
    fig, ax = plt.subplots(figsize=(12, 6))
    for key in films:
        film_colors[key] = (np.random.random(), np.random.random(), np.random.random())
        ax.barh(x, films[key], linewidth=5, label=key, color=film_colors[key])
    counter = count(0, 1)
    def update(i):
        ax.cla()
        idx = next(counter)
        max = 0
        ax.set_ylim(0, 5)
        ax.set_xlim(0, max)
        try:
            x.append(idx)
            for key in films:
                films[key].append(data[key].iloc[idx])
                if data[key].iloc[idx] > max:
                    max = data[key].iloc[idx]
        except IndexError:
            time.sleep(2)
            sys.exit(1)

        for key in films:

            ax.barh(x, films[key], linewidth=9, label=key, color=film_colors[key])

    ani = FuncAnimation(fig=fig, func=update, frames=38,interval=10)
    # FFwriter = FFMpegWriter(fps=3)
    # ani.save('SA2022_2023.mp4', writer=FFwriter)
    plt.show()
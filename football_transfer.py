import pandas as pd
import matplotlib.pyplot as plt
import sys
from matplotlib.animation import FuncAnimation
from funcitons import salary_calculated, result_calculated, bar_chart_race, sum_expense, top_5

pd.set_option("mode.chained_assignment", None)
sp = pd.read_csv("Data/Football_transfer/la_liga.csv")
eng = pd.read_csv("Data/Football_transfer/premier_league.csv")
it = pd.read_csv("Data/Football_transfer/serie_a.csv")
de = pd.read_csv("Data/Football_transfer/bundesliga.csv")
fr = pd.read_csv("Data/Football_transfer/ligue.csv")


# la_liga = sum_expense(sp)
# premier_league = sum_expense(eng)
# serie_a = sum_expense(it)
# bundesliga = sum_expense(de)
# ligue = sum_expense(fr)


# top_5(eng,"Premier League")
# top_5(it,"Serie A")
# top_5(de,"Bundesliga")
# top_5(fr,"Ligue 1")
x = []
y = []
top_5_data = pd.merge(pd.merge(pd.merge(pd.merge(top_5(sp,"La Liga"),top_5(eng,"Premier League"),on='year'),
                      top_5(it,"Serie A"),on='year'),
                      top_5(de,"Bundesliga"),on='year'),
                       top_5(fr,"Ligue 1"),on='year')

fig = plt.figure(figsize=(12,8))
axes = fig.add_subplot(1,1,1)

def animate(i):
        x.append(t[i])
        y.append((y1[i]))
        plt.plot(x, y, scaley=True, scalex=True, color="blue")







ani = FuncAnimation(fig=fig, func=animate, interval=100)

# bar_chart_race(top_5_data,"Top 5 League clubs expenses")
# bar_chart_race(premier_league,"Premier League League club expenses")
# print("premier")
# bar_chart_race(la_liga,"La Liga League club expenses")
# print("la liga")
# bar_chart_race(bundesliga,"Bundesliga League club expenses")
# print("bundes")
# bar_chart_race(serie_a,"Serie A League club expenses")
# print("serie a")
# bar_chart_race(ligue,"Ligue 1 League club expenses")
# print("ligue")
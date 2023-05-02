import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
from funcitons import salary_calculated, result_calculated, bar_chart_race, sum_expense, top_5
import sys
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

top_5_data = pd.merge(pd.merge(pd.merge(pd.merge(top_5(sp,"La Liga"),top_5(eng,"Premier League"),on='year'),
                      top_5(it,"Serie A"),on='year'),
                      top_5(de,"Bundesliga"),on='year'),
                       top_5(fr,"Ligue 1"),on='year')


x=[]
y=[]

fig,ax=plt.subplots()
ax.plot(x,y)
ax.set_xlim(0, len(top_5_data))
ax.set_ylim(0, top_5_data["Premier League"].max() * 1.04)
ax.set_xlabel('Year')
ax.set_ylabel('League expenses')
ax.set_title('Top 5 Leagues expenses')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.set_size_inches(12.8, 7.2)

counter=count(0,1)

# Get the shape of the DataFrame
n_rows, n_cols = top_5_data.shape

def update(i):
    idx=next(counter)
    try:
      x.append(top_5_data.index[idx])
      y.append(top_5_data.iloc[idx])
    except IndexError:
       print("Index out of range!")
       sys.exit(1)
    plt.cla()
    ax.plot(x,y)


ani=FuncAnimation(fig=fig,func=update,interval=400)
plt.show()
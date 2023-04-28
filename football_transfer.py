import pandas as pd

from funcitons import salary_calculated, result_calculated, bar_chart_race, sum_expense

sp = pd.read_csv("Data/Football_transfer/la_liga.csv")
eng = pd.read_csv("Data/Football_transfer/premier_league.csv")
it = pd.read_csv("Data/Football_transfer/serie_a.csv")
de = pd.read_csv("Data/Football_transfer/bundesliga.csv")
fr = pd.read_csv("Data/Football_transfer/ligue.csv")

la_liga = sum_expense(sp)
premier_league = sum_expense(eng)
serie_a = sum_expense(it)
bundesliga = sum_expense(de)
ligue = sum_expense(fr)

# bar_chart_race(premier_league,"Premier League League club expenses in million of euro")
# bar_chart_race(la_liga,"La Liga League club expenses in million of euro")
# bar_chart_race(bundesliga,"Bundesliga League club expenses in million of euro")
# bar_chart_race(serie_a,"Serie A League club expenses in million of euro")
# bar_chart_race(ligue,"Ligue 1 League club expenses in million of euro")
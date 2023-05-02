import pandas as pd
import bar_chart_race as bcr

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

import fastf1
from fastf1 import plotting
import os
import plotly.express as px
import pandas as pd


team_color_map = {
    "Red Bull Racing": "blue",
    "Aston Martin": "green",
    "Ferrari": "red",
    "Mercedes": "mediumturquoise",
    "Alfa Romeo": "darkred",
    "Apline": "deeppink",
    "Williams": "lightblue",
    "AlphaTauri": "blueviolet",
    "Haas F1 Team": "White",
    "McLaren": "orange",
}


def get_laps():
    # lec_laps = race.laps.pick_driver('LEC')
    # lap = race.laps.pick_fastest()

    # [ 'Time', 'DriverNumber', 'LapTime', 'LapNumber', 'PitOutTime', 'PitInTime'
    # , 'Sector1Time', 'Sector2Time', 'Sector3Time', 'Sector1SessionTime', 'Sector2SessionTime', 'Sector3SessionTime'
    # , 'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'IsPersonalBest', 'Compound', 'TyreLife', 'FreshTyre', 'Stint', 'LapStartTime', 'Team', 'Driver', 'TrackStatus', 'IsAccurate', 'LapStartDate']
    return race.laps


def get_pos_data():
    pos_data = race.pos_data
    print(pos_data)
    # ['Date', 'Status', 'X', 'Y', 'Z', 'Source', 'Time', 'SessionTime']
    print(pos_data['44'].keys())


def get_tel_data(lap):
    # ['Date', 'SessionTime', 'DriverAhead', 'DistanceToDriverAhead', 'Time', 'RPM', 'Speed', 'nGear', 'Throttle', 'Brake', 'DRS', 'Source', 'Distance', 'RelativeDistance', 'Status', 'X', 'Y', 'Z']
    return lap.get_telemetry()


cache_dir = f'{os.getcwd()}\cache'

plotting.setup_mpl()

fastf1.Cache.enable_cache('H:/projects/fastf1data/sandbox/cache')

race = fastf1.get_session(2023, 'Saudi Grand Prix', 'R')
race.load()


lap_data = get_laps()

drivers = pd.DataFrame(columns=['driver', 'maxspeed', 'minspeed', 'lapnumber'])

print(lap_data.columns)

for index, row in lap_data.iterrows():
    print(f"{index} / {len(lap_data.index)} ({row['Driver']})")

    # if row['Team'] == 'Red Bull Racing':
    tel_data = get_tel_data(row)

    drivers = drivers.append({
        'driver': row['Driver'],
        # Tel Data
        'maxspeed': tel_data['Speed'].max(),
        'minspeed': tel_data['Speed'].min(),
        'meanthrottle': tel_data['Throttle'].mean(),
        # Row Data
        'lapnumber': row['LapNumber'],
        'laptime': row['LapTime'].total_seconds(),
        'team': row['Team'],
        'TyreLife': row['TyreLife'],
    }, ignore_index=True)

print(drivers)

# driver, team
x_axis = 'team'

# maxspeed, laptime
y_axis = 'laptime'

fig = px.box(drivers, x=x_axis, y=y_axis, boxmode="overlay",
             color="team", color_discrete_map=team_color_map)

fig.update_traces(median=drivers.groupby(x_axis)[y_axis].median().values)
fig.update_layout(xaxis={"categoryorder": "array", "categoryarray": drivers.groupby(
    x_axis)[y_axis].median().sort_values().index})


mean_traces_ticks = []
mean_traces_texts = []
for key, data in drivers.groupby(x_axis):
    mean_trace_tick = {
        "x": [key],
        "y": [data[y_axis].mean()],
        "mode": "markers",
        "marker": {"symbol": "x", "size": 10},
        "name": "Mean",
        "showlegend": True
    }

    mean_traces_text = {
        "x": [key],
        "y": [data[y_axis].mean()],
        "mode": "text",
        "text": [f"mean={data[y_axis].mean():.2f}"],
        "textposition": "top center",
        "showlegend": False,
        "textfont": {"size": 25}  # set font size to 14
    }
    mean_traces_ticks.append(mean_trace_tick)
    mean_traces_texts.append(mean_traces_text)

fig.add_traces(mean_traces_ticks)
fig.add_traces(mean_traces_texts)

fig.update_layout(xaxis={"tickfont": {"size": 25}})

fig.show()

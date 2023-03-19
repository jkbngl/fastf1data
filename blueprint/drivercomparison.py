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

in_team_driver_map = {
    'LEC': "Black", 'SAI': "greenyellow",
    'RUS': "Black", 'HAM': "yellow",
    'VER': "Black", 'PER': "yellow",
    'STR': "Black", 'ALO': "yellow",
    'NOR': "Black", 'PIA': "yellow",
    'BOT': "Black", 'ZHO': "yellow",
    'ALB': "Black", 'SAR': "yellow",
    'TSU': "Black", 'DEV': "yellow",
    'OCO': "Black", 'GAS': "yellow",
    'MAG': "Black", 'HUL': "yellow",
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

print(race.load())

lap_data = get_laps()

drivers = pd.DataFrame(columns=['driver', 'maxspeed', 'minspeed', 'lapnumber'])

print(lap_data.columns)

for index, row in lap_data.iterrows():
    print(f"{index} / {len(lap_data.index)} ({row['Driver']})")

    # if row['Team'] == 'Aston Martin':
    # if row['Driver'] == 'BOT':

    if row['Team'] == 'Ferrari' or row['Team'] == 'Red Bull Racing':
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




fig = px.line(drivers, x="lapnumber", y="laptime",
              color='driver', title='Laptime', color_discrete_map=in_team_driver_map)
fig.show()

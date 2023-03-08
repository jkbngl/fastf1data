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

race = fastf1.get_session(2023, 'Bahrin Grand Prix', 'R')
race.load()


lap_data = get_laps()

laps = {}

drivers = pd.DataFrame(columns=['driver', 'maxspeed', 'minspeed', 'lapnuber'])

print(lap_data.columns)

for index, row in lap_data.iterrows():
    print(f"{index} / {len(lap_data.index)}")

    tel_data = get_tel_data(row)

    drivers = drivers.append({
        'driver': row['Driver'],
        'maxspeed': tel_data['Speed'].max(),
        'minspeed': tel_data['Speed'].min(),
        'lapnuber': row['LapNumber'],
        'laptime': row['LapTime'].total_seconds(),
        'team': row['Team'],
    }, ignore_index=True)

    # print(f"{row['Driver']} - {row['LapNumber']} ({row['TyreLife']})")
    # print(f"maxspeed: ", tel_data['Speed'].max())
    # print(f"minspeed: ", tel_data['Speed'].min())
    # print(f"Throttle max: ", tel_data['Throttle'].max())
    # print(f"Throttle min: ", tel_data['Throttle'].min())
    # print(f"Throttle mean: ", tel_data['Throttle'].mean())

print(drivers)

# maxspeed, laptime
fig = px.box(drivers, x="driver", y="laptime", boxmode="overlay",
             color="team", color_discrete_map=team_color_map)
fig.show()


# all_laps.groupby(['Col1'])[Col2].max()

# print(tel_data)
# print(len(tel_data.index))
# print(tel_data.columns)

"""
[
    '_Session__fix_tyre_info',
    '_calculate_t0_date',
    '_car_data',
    '_check_lap_accuracy',
    '_drivers_from_f1_api',
    '_drivers_results_from_ergast',
    '_get_property_warn_not_loaded',
    '_laps',
    '_load_drivers_results',
    '_load_laps_data',
    '_load_race_control_messages',
    '_load_telemetry',
    '_load_weather_data',
    '_pos_data',
    '_race_control_messages',
    '_results',
    '_session_start_time',
    '_session_status',
    '_t0_date',
    '_weather_data',
    'api_path',
    'car_data',
    'date',
    'drivers',
    'event',
    'f1_api_support',
    'get_driver',
    'laps',
    'load',
    'load_laps',
    'load_telemetry',
    'name',
    'pos_data',
    'race_control_messages',
    'results',
    'session_start_time',
    'session_status',
    't0_date',
    'weather_data',
    'weekend'
"""

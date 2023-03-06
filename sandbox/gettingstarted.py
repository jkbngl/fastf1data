import fastf1
from fastf1 import plotting
from matplotlib import pyplot as plt
import os


cache_dir = f'{os.getcwd()}\cache'

print("cache_dir: ", cache_dir)

plotting.setup_mpl()

# optional but recommended
fastf1.Cache.enable_cache('H:/projects/fastf1data/sandbox/cache')

race = fastf1.get_session(2023, 'Bahrin Grand Prix', 'R')
race.load()

# lec_laps = race.laps.pick_driver('LEC')

pos_data = race.pos_data
print(pos_data)
# ['Date', 'Status', 'X', 'Y', 'Z', 'Source', 'Time', 'SessionTime']
print(pos_data['44'].keys())


lap = race.laps.pick_fastest()
tel = lap.get_telemetry()


print(tel)
print(tel.columns)

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

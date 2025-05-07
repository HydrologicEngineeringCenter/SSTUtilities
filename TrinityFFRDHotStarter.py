from hecdss import HecDss
from HotStartBasinFile import generate_hotstarted_basin_file
from ControlSpecificationGenerator import generate_control_spec

from datetime import datetime, timedelta

filepath = "C:/Users/q0hecgsk/Documents/Models/Daily_POR_data-trinity"
basin_models = ["trinity_apr_may_1990", "trinity_aug_sep_2017"]
por_run_name = "por"
states_start_date = datetime.strptime("1979-10-01", '%Y-%m-%d')
states_end_date = datetime.strptime("1981-10-01", '%Y-%m-%d')
state_dates = [states_start_date + timedelta(days = t) for t in range((states_end_date - states_start_date).days + 1)]

event_duration_hours = 72
lookback = 0
padding = 14 * 60 - event_duration_hours
base_control_spec = f"{filepath}/POR_1979_2022.control"

por_filename = f"{filepath}/{por_run_name.replace(' ', '_')}.dss"
por_dss = HecDss(por_filename)

for date in state_dates:
    generate_control_spec(date, event_duration_hours, lookback, padding, base_control_spec)
    for base in basin_models:
        generate_hotstarted_basin_file(filepath, base, por_run_name, por_dss, date)

por_dss.close()
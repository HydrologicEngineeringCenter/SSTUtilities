from datetime import datetime

from HotStartProcessingFunction import process_basin_files

filepath = "C:/Users/q0hecgsk/Documents/Models/Daily_POR_data-trinity"
basin_models = ["trinity_apr_may_1990", "trinity_aug_sep_2017"]
por_run_name = "por"
states_start_date = datetime.strptime("1979-10-01", '%Y-%m-%d')
states_end_date = datetime.strptime("1981-10-01", '%Y-%m-%d')
event_duration_hours = 72
lookback = 0
padding = 14 * 60 - event_duration_hours
base_control_spec = "POR_1979_2022"

process_basin_files(filepath, basin_models, por_run_name, states_start_date, states_end_date,
                    event_duration_hours, lookback, padding, base_control_spec)
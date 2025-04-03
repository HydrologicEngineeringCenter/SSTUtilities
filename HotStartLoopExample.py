from HotStartBasinFile import generate_hotstarted_basin_file

from datetime import datetime, timedelta

proj_path = "C:/Users/q0hecgsk/Documents/Models/4_13/Duwamish_HMSv412_Event_Continuous_PoR_23May24"
basin_models = ["1996_Feb", "2022_Mar"]
por_run_name = "POR 19802022 Daily"
# the dates below are manually coded, but you could get them from the POR run time-series result if you wanted.
states_start_date = datetime.strptime("1981-10-01", '%Y-%m-%d')
states_end_date = datetime.strptime("1981-10-03", '%Y-%m-%d') #inclusive of this date
state_dates = [states_start_date + timedelta(days = t) for t in range((states_end_date - states_start_date).days + 1)]

for base in basin_models:
    for date in state_dates:
        generate_hotstarted_basin_file(proj_path, base, por_run_name, date)
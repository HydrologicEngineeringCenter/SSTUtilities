from hecdss import HecDss

from datetime import datetime, timedelta

from ControlSpecificationGenerator import generate_control_spec
from HotStartBasinFile import generate_hotstarted_basin_file

# Method parameters
## hms_project_filepath: path on disk to the root folder for the HMS project (no trailing slash)
## basin_models: list of basin model names from the HMS project to use as base models (no .basin extension needed)
## por_run_name: name of the HMS simulation run that produced the POR results
## states_start_date, states_end_date: datetime objects for range of POR dates to use as start states, inclusive (use datetime.strptime)
## event_duration_hours: usually 72
## lookback_duration_hours: amount of time before the state date to start the control spec, usually 0
## end_padding_hours: how much to add after the event duration in hours
## base_control_spec_name: name of a control spec to use as the base for the new ones (no .control extension needed)

# Outputs
## output location for basin models is /hms_project_filepath/data/basinmodels
## output location for control specs is /hms_project_filepath/data/controlspecs
## script will generate the folders if they do not exist and overwrite existing files

def process_basin_files(hms_project_filepath: str, basin_models: list[str],
                        por_run_name: str, states_start_date: datetime,
                        states_end_date: datetime, event_duration_hours: int,
                        lookback_duration_hours: int, end_padding_hours: int,
                        base_control_spec_name: str) -> None:

    state_dates = [states_start_date + timedelta(days=t) for t in range((states_end_date - states_start_date).days + 1)]
    base_control_spec = f"{hms_project_filepath}/{base_control_spec_name}.control"
    por_filename = f"{hms_project_filepath}/{por_run_name.replace(' ', '_')}.dss"
    por_dss = HecDss(por_filename)

    for date in state_dates:
        generate_control_spec(date, event_duration_hours, lookback_duration_hours,
                              end_padding_hours, base_control_spec)
        for base in basin_models:
            generate_hotstarted_basin_file(hms_project_filepath, base, por_run_name, por_dss, date)

    por_dss.close()
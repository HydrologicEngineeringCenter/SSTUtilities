from datetime import datetime, timedelta
from pathlib import Path


# Example User Inputs
event = datetime.strptime("1981-10-01", '%Y-%m-%d')
storm_duration_hours = 72
lookback_duration_hours = 0
time_padding_hours = 0
base_control_spec = "C:/Users/q0hecgsk/Documents/Models/4_13/Duwamish_HMSv412_Event_Continuous_PoR_23May24/POR.control"

# makes a copy of an existing control specification and changes its start time and end time dependent on an event date
## and duration with additional help for padding the event in either direction
# places the result in a folder in the HMS project's data folder
def generate_control_spec(event_date: datetime, duration: int, lookback: int, padding: int, source: str) -> None:
    simulation_start = event_date + timedelta(hours = -lookback)
    simulation_end = event_date + timedelta(hours = duration) + timedelta(hours = padding)

    with open(source) as s:
        line_list = []
        for line in s:
            line_split = line.split(sep=": ", maxsplit=1)
            line_start = line_split[0]

            match line_start:
                case "     Start Date":
                    replace_value = simulation_start.strftime("%#d %B %Y")
                    line_final = f"{line_start}: {replace_value}\n"
                case "     Start Time":
                    replace_value = simulation_start.strftime("%H:%M")
                    line_final = f"{line_start}: {replace_value}\n"
                case "     End Date":
                    replace_value = simulation_end.strftime("%#d %B %Y")
                    line_final = f"{line_start}: {replace_value}\n"
                case "     End Time":
                    replace_value = simulation_end.strftime("%H:%M")
                    line_final = f"{line_start}: {replace_value}\n"
                case _:
                    line_final = line

            line_list.append(line_final)
    output_control_spec_name = f"{event_date.strftime('%Y-%m-%d')}.control"
    Path(f"{Path(source).parent}/data/controlspecs").mkdir(parents=True, exist_ok=True)
    output_filepath = f"{Path(source).parent}/data/controlspecs/{output_control_spec_name}"
    with open(output_filepath, "w") as o:
        for line in line_list:
            o.write(line)
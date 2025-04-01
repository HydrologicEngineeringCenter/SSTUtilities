from hecdss import HecDss
from datetime import datetime
from pathlib import Path

# Example User Inputs
proj_path = "C:/Users/q0hecgsk/Documents/Models/4_13/Duwamish_HMSv412_Event_Continuous_PoR_23May24"
base = "2015_Dec"
por_run_name = "POR 19802022 Daily"
synthetic_event_date = datetime.strptime("1981-10-01", '%Y-%m-%d')

## copies an existing basin file but overwrites certain initial condition parameters with states from another
#### simulation run within the same HMS project. assumes certain processes are being used:
#### deficit-constant loss, simple canopy (or none), simple surface (or none), linear reservoir baseflow (2 layers) and
###### Muskingum-Cunge reach
## canopy and surface initial condition should be depth, not percent
## linear reservoir initial baseflow should be discharge, not discharge per area
## Muskingum-Cunge reach initial condition should be specified discharge, not inflow = outflow
## it also unlinks any observed data from the model
## it also changes the name of the sqlite file to match the new basin model name
## the generated basin model file is in a subdirectory of the HMS project's data folder
def generate_hotstarted_basin_file(hms_project_path: str, base_basin: str, por_run: str, date: datetime) -> None:
    base_basin_filepath = f"{hms_project_path}/{base_basin}.basin"
    basin_override_name = f"{date.strftime('%Y-%m-%d')}_{base_basin}"

    initial_parameter_line_starts = ["     Initial Deficit", "     Initial Canopy Storage Depth",
                                     "     Initial Surface Storage Depth", "     GW-1 Initial Baseflow",
                                     "     GW-2 Initial Baseflow", "     Initial Outflow", "     Initial Elevation"]
    element_types = ["Subbasin", "Reach", "Reservoir"]
    observed_data = ["     Observed Hydrograph Gage", "     Observed Pool Elevation Gage", "     Observed Swe Gage"]

    description_updated = False

    line_list = []

    with open(base_basin_filepath) as bf:
        for line in bf:
            line_split = line.split(sep = ": ", maxsplit = 1)
            line_start = line_split[0]

            match line_start:
                case "Basin":
                    line_final = f"{line_start}: {basin_override_name}\n"
                case "     Description":
                    if not description_updated:
                        line_final = f"     Description: POR Date - {date.strftime('%d%b%Y')} |Basin - {base_basin}\n"
                        description_updated = True
                    else:
                        line_final = line
                case line_start if line_start in element_types:
                    elem = line_split[1].strip()
                    line_final = line
                case line_start if line_start in initial_parameter_line_starts:
                    line_final = retrieve_value_format_line(hms_project_path, por_run, elem, line_start, date)
                case "     File":
                    line_final = line_start + ": " + basin_override_name + ".sqlite\n"
                case line_start if line_start in observed_data:
                    line_final = ""
                case _:
                    line_final = line

            line_list.append(line_final)

    output_basin_file_name = f"{basin_override_name}.basin"
    Path(f"{hms_project_path}/data/basinmodels").mkdir(parents=True, exist_ok=True)
    output_filename = f"{hms_project_path}/data/basinmodels/{output_basin_file_name}"

    with open(output_filename, "w") as o:
        for line in line_list:
            o.write(line)

## dry - utility function to take the basin file's parameter indicator and return the line to replace it
def retrieve_value_format_line(path: str, run: str, el: str, line_start: str, date: datetime) -> str:
    par = line_start.strip()
    replace_value = retrieve_initial_value(path, run, el, par, date)
    return f"{line_start}: {replace_value:.3f}\n"

## one function for handling all the parameters so you can see which parameters are supported in one place
## this assumes your POR is at daily timestep and retrieves the data for the day ending before the start of
#### your requested event date
def retrieve_initial_value(path: str, run: str, element: str, param: str, date: datetime) -> float:
    por_filename =  f"{path}/{run.replace(' ', '_')}.dss"
    dss_file = HecDss(por_filename)

    c_part_dict = \
        {"Initial Deficit" : "MOISTURE DEFICIT",
         "Initial Canopy Storage Depth": "STORAGE-CANOPY",
         "Initial Surface Storage Depth": "STORAGE-SURFACE",
         "GW-1 Initial Baseflow": "FLOW-BASE-1",
         "GW-2 Initial Baseflow" : "FLOW-BASE-2",
         "Initial Outflow" : "FLOW-COMBINE",
         "Initial Elevation" : "ELEVATION"}

    pathname = f"//{element}/{c_part_dict.get(param)}//1Day/RUN:{run}/"
    arr = dss_file.get(pathname, date, date).values
    dss_file.close()
    value = float(arr[0])
    return value

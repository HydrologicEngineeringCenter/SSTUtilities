# Example user inputs
project = "Duwamish v412"
hms_vers = "4.13"

storm = "AORC 2015-12-07 T001"
c_x = -1998315.23011
c_y = 2855801.546618
file = r"C:\Data\AORC\Duwamish-v01-20231128\dss\20151207_T001.dss"
path = "/SHG4K/DUWAMISH/PRECIPITATION/07DEC2015:0000/07DEC2015:0100/AORC/"


def generate_file_header(project_name: str, hechms_version: str):
    lines = []
    lines.append(f"Grid Manager: {project_name.replace(' ', '_')}\n")
    lines.append(f"     Grid Manager: {project_name.replace(' ', '_')}\n")
    lines.append(f"     Version: {hechms_version}\n")
    lines.append("     Filepath Separator: \\\n")
    lines.append("End: \n")
    lines.append("\n")
    return lines

def generate_precipitation_grid(grid_name: str, center_x: float, center_y: float, filename: str, dss_path: str):
    lines = []
    lines.append(f"Grid: {grid_name}\n")
    lines.append(f"     Grid: {grid_name}\n")
    lines.append("     Grid Type: Precipitation\n")
    lines.append("     Description: \n")
    lines.append(f"     Storm Center X: {center_x}\n")
    lines.append(f"     Storm Center Y: {center_y}\n")
    lines.append(f"     Data Source Type: External DSS\n")
    lines.append(f"     Filename: {filename}\n")
    lines.append(f"     Pathname: {dss_path}\n")
    lines.append("End: \n")
    lines.append("\n")
    return lines

with open(r"C:\Temp\a.txt", "w") as o:
    for line in generate_file_header(project, hms_vers):
        o.write(line)
    for line in generate_precipitation_grid(storm, c_x, c_y, file, path):
        o.write(line)
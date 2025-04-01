# Example User Inputs
grid_filename = "C:/Data/AORC/trinity-v01-top-440-storms-with-stormtype/T_Transpose - Copy.grid"

## takes an HMS grid file and copies out only the grids following the current naming convention
## will be generalized later
## assumed naming convention: "AORC yyyy-mm-dd Tnnn STx"
## nnn is the rank of the event in the catalog
## x is the storm type (the last four characters " STx" may be omitted if storm typing wasn't performed
## the max_rank argument lets you control the smallest rank event (largest number) that's preserved
## returns the pathname of the output file so the function calls can be chained
def reduce_to_sst_storms(hms_gridfile: str, max_rank: int) -> str:

    header_length = 5 # grid manager header for an HMS grid file is 4 lines plus a blank
    header_count = 0

    grid_collector = []
    collector_count = 0

    with open(hms_gridfile) as grid_file:
        for line in grid_file:
            if header_count < header_length:
                grid_collector.append(line)
                header_count += 1
            line_start = line[0:5]
            if line_start == "Grid:" and len(line) > 22 and line[6:10] == "AORC":
                if line[22] == "T":
                    rank = int(line[23:26])
                    if 1 <= rank <= max_rank:
                        grid_collector.append(line)
                        collector_count += 1
                    if collector_count == 19:
                        collector_count = 0
            elif collector_count > 0:
                grid_collector.append(line)
                collector_count += 1
                if collector_count == 19:
                    collector_count = 0
    reduced_filename = hms_gridfile + "reduced"
    f = open(reduced_filename, "w")
    f.writelines(grid_collector)
    f.close()
    return reduced_filename


## takes the reduced gridfile produced by the "reduce_to_sst_storms" function and creates a plaintext file
## with coordinates turned off, it's just a list of all the grid names that conform to the naming convention
#### this is used to set up an Uncertainty Analysis in HMS that samples storm names
## with coordinates turned on, it's an indexed csv with the storm name and the x and y coordinates
#### it is useful for visualizing the storm centers in a GIS
def extract_grid_names(reduced_gridfile: str, coordinates: bool) -> None:
    grid_names = []
    coord_x = []
    coord_y = []
    with open(reduced_gridfile) as grid_file:
        for line in grid_file:
            line_start = line[0:5]
            if line_start == "Grid:":
                line_length = len(line)
                grid_name = line[6:line_length].strip()
                grid_names.append(grid_name)
            if coordinates:
                line_start = line[0:20]
                if line_start == "     Storm Center X:":
                    line_length = len(line)
                    x = line[21:line_length].strip()
                    coord_x.append(x)
                if line_start == "     Storm Center Y:":
                    line_length = len(line)
                    y = line[21:line_length].strip()
                    coord_y.append(y)

    ## this is ugly but changes the extension without wrecking any periods in the filename (don't do that)
    gridlist_filename = ".".join(reduced_gridfile.split(".")[:-1]) + ".gridlist"

    with open(gridlist_filename, "w") as o:
        if coordinates:
            o.write(f"Index,Grid Name,X,Y\n")
        for i, grid_name in enumerate(grid_names):
            if coordinates:
                x = coord_x[i]
                y = coord_y[i]
                o.write(f"{i+1},{grid_name},{x},{y}\n")
            else:
                o.write(f"{grid_name}\n")
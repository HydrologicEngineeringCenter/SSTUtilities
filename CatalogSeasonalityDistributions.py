import pandas as pd #I'm sorry
import numpy as np #sorry again
import datetime
import re #I owe myself the apology for this one

# Example input filename, it will look at every grid name in the file, but only the ones matching the regex are analyzed
gf = "C:/Temp/catalog.grid"
od = "C:/Temp"

# Date padding +/- (what window for each event date are we allowing, default is 7 days for a 15-day window)
dp = 7

# Valid storm name pattern, only fiddle with this if the convention changes
# Example: 19751110_72hr_ST1_r001
storm_name_pattern = "^(\d){8}_(\d){1,}hr_ST(\d){1}_r(\d){3}$"

# produces two outputs, one has counts, one has cumulative probability
def get_seasonality_from_grid_file(grid_name: str, name_convention: str,
                                   date_pad: int, output_dir: str) -> None:
    pattern = re.compile(name_convention)

    # Get the grid names out of the .grid file
    with open(grid_name) as f:
        lines = f.readlines()
        all_grid_names = [line.strip("\n").split(" ")[1] for line in lines if line.startswith("Grid: ")]

    # Check if they match the naming convention
    valid_grid_names = [grid for grid in all_grid_names if pattern.match(grid)]

    # Split up the grid names for their info
    grid_splits = [grid.split("_") for grid in valid_grid_names]

    # Use pandas to clean it up a bit
    grid_df = pd.DataFrame(grid_splits, columns = ["Date", "Duration", "Type", "Rank"])
    grid_df["Date"] = pd.to_datetime(grid_df["Date"], format='%Y%m%d')

    # use pandas to split the list up conveniently
    stypes = grid_df["Type"].unique()
    df_list = [d for _, d in grid_df.groupby(["Type"])]

    # generate the date range for each event in each storm type
    for df in df_list:
        stype = df["Type"].iloc[0]
        dates = df["Date"]
        big_list = []
        for date in dates:
            big_list.append(pd.date_range(date-datetime.timedelta(days=date_pad),
                                          date+datetime.timedelta(days=date_pad)))
        big_array = np.concatenate(big_list).ravel()
        s = pd.to_datetime(big_array)
        doy_counts = s.dayofyear.value_counts(normalize = False, sort = False).sort_index()
        doy_counts.to_csv(f"{output_dir}/{stype}_count.csv")

    for stype in stypes:
        stype_prob_df = pd.read_csv(f"{output_dir}/{stype}_count.csv",
                                    index_col=0)
        op_series = stype_prob_df["count"].cumsum() / stype_prob_df["count"].cumsum().max()
        op_series.index.name = "DOY"
        op_series.to_csv(f"{output_dir}/{stype}_cumulative.csv", header = ["Cumulative"])


# example function call (not run)
#get_seasonality_from_grid_file(gf, storm_name_pattern, dp, od)
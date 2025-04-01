from hecdss import HecDss, PairedData
import pandas as pd

# Example User Inputs
realization_name = "HUC4 A14 Normalized"
hms_project_path = "C:/Users/q0hecgsk/Desktop/Kanawha_Precip_SST"
results_b_part = "Kanawha"
number_events_per_year = 10
number_years = 1000


def extract_precipitation_results(realiz_name: str, project_path: str, b_part: str) -> PairedData :
    dss_file = f"{project_path}/{realiz_name.replace(' ', '_')}.dss"
    pathname_total_precip = \
        f"//{b_part}/Realization-Precipitation Total///MCA:{realiz_name}/"
    with HecDss(dss_file) as dss:
        total_precip = dss.get(pathname_total_precip)
    return total_precip

def extract_annual_maximum_precipitation(precip_pd: PairedData, ev_per_year: int, num_years: int) -> pd.DataFrame:
    year_list = list(range(1, num_years + 1))
    repeated_year_list = [i for i in year_list for _ in range(ev_per_year)]
    df = pd.concat([pd.Series(repeated_year_list), pd.Series(precip_pd.values.flatten())], axis = 1)
    df.columns = ['Year', 'Precip Total']
    df_ams = df.groupby('Year')['Precip Total'].max().reset_index()
    return df_ams

def write_ams_to_csv(ams_df: pd.DataFrame, realiz_name: str, project_path: str) -> None:
    san_mca_name = realiz_name.replace(" ", "_")
    op_fname = f"{project_path}/data/{san_mca_name}_ams.csv"
    ams_df.to_csv(op_fname, index = False)
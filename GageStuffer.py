from hecdss import HecDss, DssPath
import datetime

modified_datetime = datetime.datetime.now()

class HmsFlowGageGenerator:
    def __init__(self, dsspath: DssPath, filename: str):
        self.path = dsspath
        self.filename = filename

    def gageName(self) -> str:
        timestep = "D" if self.path.E == "1Day" else "Inst"
        if self.path.A == "":
            return self.path.B + " " + timestep
        else:
            return self.path.A + " " + self.path.B + " " + timestep

    def produceLines(self) -> list[str]:
        lines = ["\n",
                 f"Gage: {self.gageName()}\n",
                 f"     Gage: {self.gageName()}\n",
                 "     Gage Type: Flow\n",
                 f"     Last Modified Date: {modified_datetime.strftime("%#d %B %Y")}\n",
                 f"     Last Modified Time: {modified_datetime.strftime('%H:%M:%S')}\n",
                 "     Reference Height Units: Feet\n",
                 "     Reference Height: 32.80800\n",
                 "     Reference Height Units: Feet\n",
                 "     Station Id:\n",
                 "     Data Source Type: External DSS\n",
                 f"     Filename: {self.filename}\n",
                 f"     Pathname: {self.path}\n",
                 "     Variant: Variant-1\n",
                 "       Start Time: 1 January 2000, 00:00\n",
                 "       End Time: 2 January 2000, 00:00\n",
                 "     End Variant: Variant-1\n", "End:\n"]
        return lines

class HmsSWEGageGenerator:
    def __init__(self, dsspath: DssPath, filename: str):
        self.path = dsspath
        self.filename = filename

    def gageName(self) -> str:
        timestep = "D" if self.path.E == "1Day" else "Inst"
        if self.path.A == "":
            return self.path.B + " " + timestep
        else:
            return self.path.A + " " + self.path.B + " " + timestep

    def produceLines(self) -> list[str]:
        lines = ["\n",
                 f"Gage: {self.gageName()}\n",
                 f"     Gage: {self.gageName()}\n",
                 "     Gage Type: Snow Water Equivalent\n",
                 f"     Last Modified Date: {modified_datetime.strftime("%#d %B %Y")}\n",
                 f"     Last Modified Time: {modified_datetime.strftime('%H:%M:%S')}\n",
                 "     Reference Height Units: Feet\n",
                 "     Reference Height: 32.80800\n",
                 "     Reference Height Units: Feet\n",
                 "     Station Id:\n",
                 "     Data Source Type: External DSS\n",
                 f"     Filename: {self.filename}\n",
                 f"     Pathname: {self.path}\n",
                 "     Variant: Variant-1\n",
                 "       Start Time: 1 January 2000, 00:00\n",
                 "       End Time: 2 January 2000, 00:00\n",
                 "     End Variant: Variant-1\n", "End:\n"]
        return lines

gage_data_file = "C:/models/4_14/Iowa_River/data/UA_swe_zones.dss"
gage_dss_file = HecDss(gage_data_file)

output_file_name = "C:/data/iowa_river_ua_swe_timeseries.gage"

dss_cat = gage_dss_file.get_catalog()

dss_cat_items = dss_cat.items

master_line_list = []
for item in dss_cat_items:
    if item.C == "FLOW":
        this_generator = HmsFlowGageGenerator(item, gage_data_file)
        master_line_list.append(this_generator.produceLines())
    elif item.C == "SWE":
        this_generator = HmsSWEGageGenerator(item, gage_data_file)
        master_line_list.append(this_generator.produceLines())

gage_dss_file.close()

flat_line_list = [x for xs in master_line_list for x in xs]

with open(output_file_name, "w") as o:
    for line in flat_line_list:
        o.write(line)


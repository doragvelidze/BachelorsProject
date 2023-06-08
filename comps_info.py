import wmi
import pandas as pd
import csv
import os
ram = {
    20 : "DDR",
    21 : "DDR2",
    22 : "DDR2 FB-DIMM",
    24 : "DDR3",
    26 : "DDR4"
}
ramforms = {
    12 : "SODIMM",
    8 : "DIMM",
    0 : "Unknown"
}
drives = {
    0 : "unspecified",
    3 : "HDD",
    4 : "SSD",
    5 : "SCM"
}

csv_data = []
def check_comp(x):
    if os.system("ping /n 1 " + x) == 0:
        data_dict = {"Host Name" : x,
                     "Computer Name" : "",
                     "RAM_1_Type" : "",
                     "RAM_1_Speed" : "",
                     "RAM_1_FormFactor" : "",
                     "RAM_1_Size(GB)" : "",
                     "RAM_2_Type" : "",
                     "RAM_2_Speed" : "",
                     "RAM_2_FormFactor" : "",
                     "RAM_2_Size(GB)" : "",
                     "Drive_1_Name" : "",
                     "Drive_1_FreeSpace" : "",
                     "Drive_1_Size(GB)" : "",
                     "Drive_1_Type" : "",
                     "Drive_2_Name" : "",
                     "Drive_2_FreeSpace" : "",
                     "Drive_2_Size(GB)" : "",
                     "Drive_2_Type" : "",

                     }
        conn = wmi.WMI(x)
        for n in conn.Win32_ComputerSystem():
            data_dict["Computer Name"] = n.SystemSKUNumber
            

        i=1
        for m in conn.Win32_PhysicalMemory():
            if m.SMBIOSMemoryType in ram.keys():
                data_dict[f"RAM_{i}_Type"] = ram[int(m.SMBIOSMemoryType)]
            else:
                data_dict[f"RAM_{i}_Type"] = "Unknown"

            data_dict[f"RAM_{i}_Speed"] = f"{m.Speed}MHz"
            data_dict[f"RAM_{i}_FormFactor"] = ramforms[int(m.FormFactor)]
            data_dict[f"RAM_{i}_Size(GB)"] = f"{int(m.Capacity)//1024**3}"
            
            i+=1

        i=1
        for d in conn.Win32_LogicalDisk():
            data_dict[f"Drive_{i}_Name"] = d.Caption
            data_dict[f"Drive_{i}_FreeSpace"] = f"{int(d.FreeSpace)//1024**3}"
            data_dict[f"Drive_{i}_Size(GB)"] = f"{int(d.Size)//1024**3}"
            
            if i == 2:
                break
            i+=1


        i=1
        ws = wmi.WMI(x,namespace='root/Microsoft/Windows/Storage')
        for d in ws.MSFT_PhysicalDisk():
            data_dict[f"Drive_{i}_Type"] = drives[int(d.MediaType)]
            
            i+=1
            

        csv_data.append(data_dict)
        return ""
    else:
        return x
    
PATH_TO_CSV = "C:\\Users\\d.oragvelidze\\Desktop\\comps.csv"
data = pd.read_csv(PATH_TO_CSV)
data = data[data['Name'].str.len() > 0]
print(data)
data['Name'] = data["Name"].map(lambda x: check_comp(x))

data["Name"].to_csv(PATH_TO_CSV, mode="w+")

columns = ["Host Name", "Computer Name",
           "RAM_1_Type", "RAM_1_Speed", "RAM_1_FormFactor", "RAM_1_Size(GB)",
          "RAM_2_Type", "RAM_2_Speed", "RAM_2_FormFactor", "RAM_2_Size(GB)",
          "Drive_1_Name", "Drive_1_FreeSpace", "Drive_1_Size(GB)", "Drive_1_Type",
          "Drive_2_Name", "Drive_2_FreeSpace", "Drive_2_Size(GB)", "Drive_2_Type",]

with open("C:\\Users\\d.oragvelidze\\Desktop\\comp_info.csv", 'a+', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    for data in csv_data:
        writer.writerow(data)
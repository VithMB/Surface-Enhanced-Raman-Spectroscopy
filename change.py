import numpy as np
import pandas as pd 

data_frame1 = pd.read_csv('attempt10/E^4_attempt10_step1.csv', header=4)
data_frame2 = pd.read_csv('attempt10/E^4_attempt10_step2.csv', header=4)
data_frame3 = pd.read_csv('attempt10/E^4_attempt10_step3.csv', header=4)
data_frame4 = pd.read_csv('attempt10/E^4_attempt10_step4.csv', header=4)
data_frame5 = pd.read_csv('attempt10/E^4_attempt10_step5.csv', header=4)
data_frame6 = pd.read_csv('attempt10/E^4_attempt10_step6.csv', header=4)
data_frame7 = pd.read_csv('attempt10/E^4_attempt10_step7.csv', header=4)
data_frame8 = pd.read_csv('attempt10/E^4_attempt10_step8.csv', header=4)
data_frame9 = pd.read_csv('attempt10/E^4_attempt10_step9.csv', header=4)


for data_frame in [data_frame1, data_frame2, data_frame3, data_frame4, data_frame5, data_frame6, data_frame7]:
    header = list(data_frame.columns)
    units_L = header[0].split()[-1] 
    units_D = header[1].split()[-1]
    units_lambda = header[2].split()[-1]
    print(units_L, units_D, units_lambda)

header = list(data_frame3.columns)
data_frame3[header[0]] *= 1e9
data_frame3[header[1]] *= 1e9
data_frame3[header[2]] *= 1e6
data_frame3 = data_frame3.rename(columns={header[0]: header[0]+' (nm)',
                    header[1]: header[1]+' (nm)', header[2]: header[2]+' (µm)'})

print(data_frame3)
# save
data_frame3.to_csv('attempt10/E^4_attempt10_step3_modified.csv', index=False)
print("File saved with converted units.")

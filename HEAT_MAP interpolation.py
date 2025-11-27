import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator  
from scipy.interpolate import RegularGridInterpolator

plt.rcParams['font.family'] ='sans-serif' 
plt.rcParams['mathtext.fontset'] = 'stixsans' 

spatial_avg_plane = 1.721565067886784e17/(600**2)

def spatial_avg(pyramid_l, D, surface_integral): 
    domain_x = pyramid_l + D
    return surface_integral* 1/domain_x**2


def heatmap2d(arr: np.ndarray, x_labels, y_labels):
    fig, ax = plt.subplots(figsize = (6,4))
    im = ax.imshow(arr, cmap='jet', aspect='auto', origin='lower', norm=LogNorm(vmin=1, vmax=10000))
 
    # Set x-axis ticks and labels (L)
    x_index = [np.argmin(np.abs(np.array(x_labels) - target)) for target in [100, 200, 300, 400]]
    x_tick_labels = [f"{x_labels[i]:.0f}" for i in x_index]
    ax.set_xticks(x_index)
    ax.set_xticklabels(x_tick_labels)
    ax.set_xlabel(r'Pyramid length - $\mathbf{L}$ (nm)', fontsize=12)
    ax.set_xlim(0, len(x_labels)- 1)

    # Set y-axis ticks and labels (D)
    y_index = [np.argmin(np.abs(np.array(y_labels) - target)) for target in [100, 200, 300, 400, 500]]
    y_tick_labels = [f"{y_labels[i]:.0f}" for i in y_index]
    ax.set_yticks(y_index)
    ax.set_yticklabels(y_tick_labels)    
    ax.set_ylabel(r'Pyramid spacing - $\mathbf{D}$ (nm)', fontsize= 12,labelpad=10)
    ax.set_ylim(0, len(y_labels)- 1)

    #minor locator
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4)) 


    plt.colorbar(im, label=r'$\mathbf{EF}$')
    ax.set_title(r'$\phi = 0^\circ$', fontsize=14)
    plt.tight_layout()
    plt.show()
    return 1

#######################################
 
data_frame1 = pd.read_csv('E^4_attempt9_ate_150nm.csv', header=4)
data_frame2 = pd.read_csv('E^4_attempt9_ate_300nm.csv', header=4)
data_frame3= pd.read_csv('E^4_attempt9_ate_500nm.csv', header=4)
data_frame_total = pd.concat([data_frame1, data_frame2,data_frame3], ignore_index=True)
header = list(data_frame_total.columns)

# Filter data to only include D <= 500nm and L <= 450nm
data_frame_total = data_frame_total[
    (data_frame_total[header[0]] <= 450) &
    (data_frame_total[header[0]] >= 50) &
    (data_frame_total[header[1]] <= 500) &
    (data_frame_total[header[1]] >= 25)
]


pyramid_l = data_frame_total[header[0]] 
D = data_frame_total[header[1]] 
surface_integral = data_frame_total[header[3]]

# Getting unique values for D and pyramid_l
unique_D = sorted(D.unique())
unique_pyramid_l = sorted(pyramid_l.unique())


# Create a 2D array for the enhancement factor (EF)
EF_2d = np.zeros(( len(unique_D),len(unique_pyramid_l))) 
 

for i, row in data_frame_total.iterrows():
    pyramid_l_value = row[header[0]]
    D_value = row[header[1]]
    surface_integral_value = row[header[3]]
     
    # Calculate spatial average of surface integral
    spatial_avg_pyramid = spatial_avg(pyramid_l_value, D_value, surface_integral_value)
    # Enhancement Factor
    EF = spatial_avg_pyramid / spatial_avg_plane 
    
    # Find indices for the 2D array
    pyramid_l_index = unique_pyramid_l.index(pyramid_l_value)
    D_index = unique_D.index(D_value)
    EF_2d[D_index, pyramid_l_index] = EF
 

# General case (not always this values)
#        pyramid_l values (columns)
#         50   75   100  125  150  ...
# D  0   [EF] [EF] [EF] [EF] [EF] ...
#    25  [EF] [EF] [EF] [EF] [EF] ...
#    50  [EF] [EF] [EF] [EF] [EF] ...
#    75  [EF] [EF] [EF] [EF] [EF] ...
#    100 [EF] [EF] [EF] [EF] [EF] ...
#    ...
# (rows)

# heatmap2d(EF_2d, unique_pyramid_l, unique_D) 
# print("\n\n", [float(x) for x in unique_D], "\n\n", [float(x) for x in unique_pyramid_l])



x = np.array(unique_pyramid_l)
y = np.array(unique_D)
z = EF_2d
interpolation_function = RegularGridInterpolator((y,x), z, method='linear')
 
x_sample = np.linspace(min(x), max(x), 100) 
y_sample = np.linspace(min(y), max(y), 100)
(X, Y) = np.meshgrid(x_sample, y_sample) 
# meshgrid repeats the first as columns and the second as rows
Z = interpolation_function((Y,X))
heatmap2d(Z, x_sample, y_sample)
# print("\n\n", [float(x) for x in x_sample], "\n\n", [float(x) for x in y_sample])
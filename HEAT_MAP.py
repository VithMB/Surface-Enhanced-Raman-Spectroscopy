import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator  

plt.rcParams['font.family'] ='sans-serif' 
plt.rcParams['mathtext.fontset'] = 'stixsans' 
plt.rcParams['font.size'] = 20

spatial_avg_plane_633nm = 1.721565067886784e17/(600**2)

def spatial_avg(pyramid_l, D, surface_integral): 
    domain_x = pyramid_l + D
    return surface_integral* 1/domain_x**2


def heatmap2d(arr: np.ndarray, x_labels, y_labels):
    fig, ax = plt.subplots(figsize = (10,6))
    im = ax.imshow(arr, cmap='jet', aspect='auto', origin='lower', norm=LogNorm(vmin=1, vmax=10000))
 
    # Set x-axis ticks and labels (L)
    x_index = [i for i, value in enumerate(x_labels) if value in [100,200,300,400]]
    x_tick_labels = [f"{x_labels[i]:.0f}" for i in x_index]
    ax.set_xticks(x_index)
    ax.set_xticklabels(x_tick_labels)
    ax.set_xlabel(r'Pyramid Base Side - $\mathbf{L}$ (nm)', fontweight='bold' )
    ax.set_xlim(-1/2, len(x_labels)-1/2)

    # Set y-axis ticks and labels (D)
    y_index = [i for i, value in enumerate(y_labels) if value in [100, 200, 300, 400, 500]]
    y_tick_labels = [f"{y_labels[i]:.0f}" for i in y_index]
    ax.set_yticks(y_index)
    ax.set_yticklabels(y_tick_labels, fontsize=20)    
    ax.set_ylabel(r'Pyramid Spacing - $\mathbf{D}$ (nm)', fontweight='bold' )
    ax.set_ylim(-1/2, len(y_labels)-1/2)

    #minor locator
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4)) 
 
    ax.tick_params(which='major', length=8, width=2.1)
    ax.tick_params(which='minor', length=5, width=1.8)

    plt.colorbar(im, label=r'$\mathbf{EF}$')
    ax.set_title(r'$ \phi =0 \;\;\;\;\;\; \lambda = 633$ nm' ,fontsize=22 )
    plt.tight_layout()
    plt.show()
    return 1

#######################################
 
data_frame1 = pd.read_csv('attempt9/E^4_attempt9_ate_150nm.csv', header=4)  
data_frame2 = pd.read_csv('attempt9/E^4_attempt9_ate_300nm.csv', header=4)
data_frame3 = pd.read_csv('attempt9/E^4_attempt9_ate_500nm.csv', header=4)

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
    EF = spatial_avg_pyramid/spatial_avg_plane_633nm
    
    # Find indices for the 2D array
    pyramid_l_index = unique_pyramid_l.index(pyramid_l_value)
    D_index = unique_D.index(D_value)
    EF_2d[D_index, pyramid_l_index] = EF
 
 

heatmap2d(EF_2d, unique_pyramid_l, unique_D) 
# print("\n\n", [float(x) for x in unique_D], "\n\n", [float(x) for x in unique_pyramid_l])

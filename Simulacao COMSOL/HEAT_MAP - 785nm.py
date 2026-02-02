import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator,MaxNLocator
from os import listdir

#########################################
######### Personalized Commands #########
#########################################
PLOT = True

APPLY_FILTERS = True
SIMULATION_BEGIN_L_nm = 200
SIMULATION_END_L_nm = 450

CHOOSE_HEATMAP_VALUE_MAX = True
HEAT_MAP_VALUE_MAX = 10**5
INTERPOLATE = True

MAJOR_LOCATOR_L = 5
MAJOR_LOCATOR_D = 5
MINOR_LOCATOR_L = 4
MINOR_LOCATOR_D = 4
FONTSIZE = 20   
COLORMAP = 'jet' 

PRINT_DIMENSIONS = False
PLANE_DOMAIN_SIDE_nm = 600 # NOT TO CHANGE!
#########################################
############# Reading Files #############
######################################### 


data_frame_plano = pd.read_csv('attempt9/E^4_attempt9_Plano.csv', header=4)
read_path = 'attempt9/'

file_list = listdir(read_path)
data_frames = np.empty(len(file_list)-1, dtype=object)

for i,file in enumerate(file_list[1:]): 
    data_frames[i] = pd.read_csv(read_path + file, header=4)
data_frame_total = pd.concat([*data_frames], ignore_index=True)   

# Reading dataframe - pyramids 
header = list(data_frame_total.columns)
data_frame_total = data_frame_total.rename(columns={header[0]: 'L', header[1]: 'D',
                                                     header[2]: 'Wavelength', header[3]: 'Integral'})


# correct float point imprecision (15.99999)   
data_frame_total['L'] = data_frame_total['L'].round(5) 
data_frame_total['D'] = data_frame_total['D'].round(5)

# Wavelenght of excitation
wavelength = data_frame_total['Wavelength'].iloc[0]*1e3   

#########################################
############### Filtering ###############
######################################### 

# Filter L values within specified range 
if APPLY_FILTERS:
    if SIMULATION_BEGIN_L_nm in data_frame_total['L'].values:
        data_frame_total = data_frame_total[data_frame_total['L']>= SIMULATION_BEGIN_L_nm]
    else: 
        message = (
            f"SIMULATION_BEGIN_L_nm = {SIMULATION_BEGIN_L_nm} nm not found in data.\n"
            "No lower filter applied. Available L values:\n" 
            f"{data_frame_total['L'].unique()}"
        )
        raise ValueError(message)

    if SIMULATION_END_L_nm in data_frame_total['L'].values:
        data_frame_total = data_frame_total[data_frame_total['L']<= SIMULATION_END_L_nm]
    else:
        message = (
            f"SIMULATION_END_L_nm = {SIMULATION_END_L_nm} nm not found in data.\n"
            "No upper filter applied. Available L values:\n" 
            f"{data_frame_total['L'].unique()}"
        )
        raise ValueError(message)
     

# unique values for D and pyramid_L
unique_D = sorted(data_frame_total['D'].unique())
unique_pyramid_L = sorted(data_frame_total['L'].unique())

#########################################
########### Enhancement Factor ##########
#########################################

plane_surface_integral =  data_frame_plano.iloc[0,1] 
spatial_avg_plane = plane_surface_integral/PLANE_DOMAIN_SIDE_nm**2

def Enhancement_Factor(pyramid_L, D, surface_integral): 
    '''Calculate the Enhancement Factor (EF) given pyramid_L, D, and surface_integral.'''
    domain_x = pyramid_L + D
    spatial_avg_pyramid = surface_integral* 1/domain_x**2
    return spatial_avg_pyramid/spatial_avg_plane

def build_grid(data_frame_total, unique_D, unique_pyramid_L):
    '''Create a 2D grid for the Enhancement Factor (EF) given the data frame and unique D and L values.'''
    EF_grid = np.zeros(( len(unique_D),len(unique_pyramid_L))) 
    for i, row in data_frame_total.iterrows():
        pyramid_L_value = row['L']
        D_value = row['D']    
        # Find indices for the 2D grid
        pyramid_L_index = unique_pyramid_L.index(pyramid_L_value)
        D_index = unique_D.index(D_value)
        # Calculate and append the Enhancement Factor
        surface_integral_value = row['Integral']
        EF = Enhancement_Factor(pyramid_L_value, D_value, surface_integral_value)
        EF_grid[D_index, pyramid_L_index] = EF
    return EF_grid
 
#########################################
######### Heatmap Plot Function #########
#########################################

# Plotting font
plt.rcParams['font.family'] ='sans-serif' 
plt.rcParams['mathtext.fontset'] = 'stixsans' 
plt.rcParams['font.size'] = FONTSIZE

def heatmap2d(arr: np.ndarray, L_labels: list, D_labels: list, wavelength: float):
    ''' Plots a 2D heatmap of the given array with specified L and D labels. '''
    fig, ax = plt.subplots(figsize = (10,6))

    # Next power of 10 as max value
    if CHOOSE_HEATMAP_VALUE_MAX:
        value_max = HEAT_MAP_VALUE_MAX
    else:
        value_max = 10 ** np.ceil(np.log10(arr.max()))

    im = ax.imshow(arr, cmap=COLORMAP, aspect='auto', origin='lower',
                    norm=LogNorm(vmin=1, vmax=value_max),
                   interpolation='bicubic' if INTERPOLATE else 'None',
                   extent=[L_labels[0], L_labels[-1], D_labels[0], D_labels[-1]])
 
    # # Set x-axis ticks and labels (L)
    # L_index = [i for i, value in enumerate(L_labels)]
    # L_tick_labels = [f"{L_labels[i]:.0f}" for i in L_index]
    # ax.set_xticks(L_index)
    # ax.set_xticklabels(L_tick_labels)
    # ax.xaxis.set_major_locator(MaxNLocator(nbins=MAJOR_LOCATOR_L, integer=True)) 
    # ax.set_xlim(0,len(L_labels)-1)
    ax.set_xlabel(r'Pyramid Base Side - $\mathbf{L}$ (nm)', fontweight='bold' )

    # # Set y-axis ticks and labels (D)
    # D_index = [i for i, value in enumerate(D_labels)]
    # D_tick_labels = [f"{D_labels[i]:.0f}" for i in D_index]
    # ax.set_yticks(D_index)
    # ax.set_yticklabels(D_tick_labels)   
    # ax.yaxis.set_major_locator(MaxNLocator(nbins=MAJOR_LOCATOR_D, integer=True)) 
    # ax.set_ylim(0,len(D_labels)-1)
    ax.set_ylabel(r'Pyramid Spacing - $\mathbf{D}$ (nm)', fontweight='bold' )

    #major and minor locator
    ax.xaxis.set_minor_locator(AutoMinorLocator(MINOR_LOCATOR_L))
    ax.yaxis.set_minor_locator(AutoMinorLocator(MINOR_LOCATOR_D)) 
    ax.tick_params(which='major', length=8, width=2.1)
    ax.tick_params(which='minor', length=5, width=1.8)

    #more settings
    plt.colorbar(im, label=r'$\mathbf{EF}$')
    ax.set_title(rf'$ \phi = 0 \;\;\;\; \lambda = {wavelength:.0f}$ nm')
    plt.tight_layout()
    plt.show()
    return 1

######################################### 
############ Main Execution #############
#########################################

EF_grid = build_grid(data_frame_total, unique_D, unique_pyramid_L)

# exporta dataframe
ef_dataframe = pd.DataFrame(EF_grid, index=unique_D, columns=unique_pyramid_L)
ef_dataframe.to_csv(f'EF_Heatmap_{wavelength:.0f}nm.csv' , index_label='D\L (nm)')


if PLOT:
    heatmap2d(EF_grid, unique_pyramid_L, unique_D, wavelength) 

if PRINT_DIMENSIONS:
    print("\n Pyramid Spacing - D:",*unique_D,"\n")
    print("Pyramid Base Side - L:",*unique_pyramid_L,"\n")

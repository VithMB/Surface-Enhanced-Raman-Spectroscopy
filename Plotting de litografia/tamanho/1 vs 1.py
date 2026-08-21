import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np 
from scipy.optimize import curve_fit


circle_mask_nominal_L = [300,325,350,375,400]
circle_mask_real_L = [298,339,375,399,422]  
pyramid_cavity_real_L = [536,580, 596, 622, 656]

x_axis = circle_mask_nominal_L
y_axis = pyramid_cavity_real_L

xlabel = 'Nominal mask aperture L'
ylabel = 'Measured pyramid cavity L'  

#########################
function = lambda x, a, b : a*x + b
popt, pcov = curve_fit(function,  x_axis, y_axis) 
a,b = popt

sample_points = np.linspace(x_axis[0]-15, x_axis[-1]+15, 100)



#########################

plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'Arial' 
plt.rcParams["scatter.marker"] = 's'

plt.figure(figsize=(16*0.7,9*0.7), dpi=100)

#####################
size = 50
c1 = 'b'  
c2 = 'k'
#Infiniteeth Color Palete v1 Color Palette

plt.scatter(x_axis, y_axis, color= c1, s = size, zorder = 2)   
plt.plot(sample_points, function(sample_points, *popt), color = c2, lw = 1.5 , ls = '--' ,
         label=rf'{a:.2f}$x$ + {b:.1f}', zorder=1)
####################

plt.ylabel(f'{ylabel} (nm)', fontweight='bold',fontsize=24)  
plt.xlabel(f'{xlabel} (nm)', fontweight='bold',fontsize=24)   

plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))
# plt.gca().tick_params(axis='both', which='major', length=6, width=2.6)
# plt.gca().tick_params(axis='both', which='minor', length=3, width=1.8) 
plt.grid(which ='major', visible=True, linestyle='-',  lw =0.75, alpha=0.25, color = "black")  
plt.grid(which= 'minor', visible=True, linestyle='-',  lw =0.25, alpha=0.15, color = "black")    
 

plt.legend(loc = 'upper center', frameon=False, bbox_to_anchor=(0.5, 1), ncol=2, fontsize=18) 
plt.text(0, 1.02, 'FIB current : 50 pA', ha='left', va='center', transform=plt.gca().transAxes, fontsize=16, fontweight='bold') 
 
plt.savefig(f'{xlabel}vs {ylabel}.pdf', bbox_inches='tight')
plt.show()

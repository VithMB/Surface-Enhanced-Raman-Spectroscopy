import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np 
from scipy.optimize import curve_fit


circle_mask_nominal_L = [300,325,350,375,400]
circle_mask_real_L = [298,339,375,399,422]  
pyramid_cavity_real_L = [536,580, 596, 622, 656]

initial = circle_mask_real_L
final = pyramid_cavity_real_L

xlabel = 'Mask aperture L'
ylabel = 'Pyramid cavity L'  

#########################
function = lambda x, a, b : a*x + b
popt, pcov = curve_fit(function,  initial, final) 
a,b = popt

sample_points = np.linspace(initial[0]-15, initial[-1]+15, 100)



#########################

plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'Times New Roman' 
plt.rcParams["scatter.marker"] = 'h'

plt.figure(figsize=(16*0.7,9*0.7), dpi=100)

#####################
size = 65
c1 = '#552b16'  
c2 = '#000000'
#Infiniteeth Color Palete v1 Color Palette

plt.scatter(initial, final, color= c1, s = size, zorder = 2)   
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
 
plt.savefig(f'function.pdf', bbox_inches='tight')
plt.show()

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 
from matplotlib.ticker import AutoMinorLocator
###########################

Z_nominal = np.arange(40,130,10)
Z_AFM = [52.5, 67.4, 80, 94.7, 111.5, 121.1, 140, 162.2, 180]

function = lambda x, a, b, c: a*x**2 + b*x + c
popt, pcov = curve_fit(function, Z_nominal, Z_AFM) 
a,b,c = popt

sample_points = np.linspace(Z_nominal[0]-15, Z_nominal[-1]+15, 100)

 
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'Times New Roman' 
plt.rcParams["scatter.marker"] = 's'
plt.rcParams['mathtext.fontset'] = 'stixsans' 


plt.figure(figsize=(16*0.7,9*0.7), dpi=100)

###########################
size = 60
c1 = '#552b16'
c2 = '#ed872d'  
#Infiniteeth Color Palete v1 Color Palette

########################### 
plt.plot(sample_points, function(sample_points, *popt), color=c2, ls='-',lw = 2.3,
         label=rf'{a:.3f}$x^2$ + {b:.2f}$x$ + {c:.1f}', zorder=1)
plt.scatter(Z_nominal, Z_AFM,  color=c1 , s = size, zorder = 2)  

###########################

plt.ylabel(f'Real Z (nm)', fontweight='bold',fontsize=24)  
plt.xlabel(f'Nominal Z (nm)', fontweight='bold',fontsize=24) 
plt.title(r'Square Cavities (3 $\mu$m)', fontweight = 'bold')
 

plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))
# plt.gca().tick_params(axis='both', which='major', length=6, width=2.6)
# plt.gca().tick_params(axis='both', which='minor', length=3, width=1.8)
plt.grid(which ='major', visible=True, linestyle='-',  lw =0.75, alpha=0.25, color = "black")  
plt.grid(which= 'minor', visible=True, linestyle='-',  lw =0.25, alpha=0.15, color = "black")   
plt.xlim(30,130)
plt.ylim(40,200)
 
plt.legend(loc = 'upper center', frameon=False, bbox_to_anchor=(0.5, 1), ncol=2, fontsize=18) 
plt.text(0, 1.02, 'FIB current : 100 pA', ha='left', va='center', transform=plt.gca().transAxes, fontsize=16, fontweight='bold') 
 

plt.savefig(f'Square_Cavities.pdf', bbox_inches='tight')
plt.show()

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np 


circle_mask_nominal_L = [300,325,350,375,400]
pyramid_cavity_real_L = [536,580, 596, 622, 656]

nominal = circle_mask_nominal_L
final = pyramid_cavity_real_L

xlabel = 'Circle Mask'
ylabel = 'Pyramid Cavity' 


plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'Times New Roman' 
plt.rcParams["scatter.marker"] = 's'

plt.figure(figsize=(16*0.7,9*0.7), dpi=100)

#####################
size = 40 
c1 = '#552b16'  
#Infiniteeth Color Palete v1 Color Palette

plt.scatter(nominal, final, color= c1, s = size)   
####################
#ticks em x onde estão os pontos
plt.xticks(nominal)
####################

plt.ylabel(f'{ylabel} L (nm)', fontweight='bold',fontsize=24)  
plt.xlabel(f'{xlabel} L (nm)', fontweight='bold',fontsize=24)   

plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))
# plt.gca().tick_params(axis='both', which='major', length=6, width=2.6)
# plt.gca().tick_params(axis='both', which='minor', length=3, width=1.8) 
plt.grid(which ='major', visible=True, linestyle='-',  lw =0.75, alpha=0.25, color = "black")  
plt.grid(which= 'minor', visible=True, linestyle='-',  lw =0.25, alpha=0.15, color = "black")    

plt.xticks(fontweight='bold') 

plt.text(0, 1.02, 'FIB current : 50 pA', ha='left', va='center', transform=plt.gca().transAxes, fontsize=16, fontweight='bold') 
 
plt.savefig(f'function.pdf', bbox_inches='tight')
plt.show()

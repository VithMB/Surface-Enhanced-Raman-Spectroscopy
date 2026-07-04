import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np 

##################################### 
SIZE = 1
SIDE_SIDE = 0
PITCH = 0
 
#####################################
circle_mask_nominal_L = [300,325,350,375,400]
circle_mask_nominal_D = 450
circle_mask_nominal_pitch = [(circle_mask_nominal_D + L) for L in circle_mask_nominal_L]


circle_mask_real_L = [298,339,375,399,422]  
circle_mask_real_pitch = [768, 792, 818, 844, 870]
circle_mask_real_D = [(pitch - L) for pitch, L in zip(circle_mask_real_pitch, circle_mask_real_L)]

#####################################
circle_mask_KOH_real_L = [400, 433, 454, 489, 506]

#####################################  
pyramid_cavity_real_L = [536,580, 596, 622, 656]
pyramid_cavity_real_pitch = [763, 792, 816, 843, 870]
pyramid_cavity_real_D = [(pitch - L) for pitch, L in zip(pyramid_cavity_real_pitch, pyramid_cavity_real_L)]
#####################################
comparative = pyramid_cavity_real_L
comparative_label = 'Pyramid cavity'

#####################################
if SIZE: 
    nominal = circle_mask_nominal_L
    real = circle_mask_real_L
    xlabel = 'Nominal L'
    ylabel = 'Measured L'   
elif PITCH: 
    nominal = circle_mask_nominal_pitch
    real = circle_mask_real_pitch
    xlabel = 'Nominal Pitch'
    ylabel = 'Measured Pitch'    
elif SIDE_SIDE: 
    nominal = circle_mask_nominal_L
    real = circle_mask_real_D
    xlabel = 'Nominal L'
    ylabel = 'Measured D'   
else:
    raise ValueError("Nem SIZE nem PITCH nem SIDE_SIDE estão ativos")

####################
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'Times New Roman' 
plt.rcParams["scatter.marker"] = 's'

plt.figure(figsize=(16*0.7,9*0.7), dpi=100)

#####################
size = 40
c1 = '#ed872d'
c2 = '#552b16'  
#Infiniteeth Color Palete v1 Color Palette

plt.scatter(nominal, real, color= c1, s = size ,label='Mask aperture')   
plt.scatter(nominal, comparative, color=c2, s=size, label =comparative_label)
####################

#escreva em cima de cada ponto o valor real
labels = 16
for i in range(len(nominal)):
    plt.text(nominal[i], real[i]*1.001, f'{real[i]}', ha='center', va='bottom', fontsize=labels, fontweight='bold', color=c1) 
    
    plt.text(nominal[i], comparative[i]*1.002, f'{comparative[i]}', ha='center', va='bottom', fontsize=labels, fontweight='bold', color=c2) 

#ticks em x onde estão os pontos
plt.xticks(nominal)
####################

plt.ylabel(f'{ylabel} (nm)', fontweight='bold',fontsize=24)  
plt.xlabel(f'{xlabel} (nm)', fontweight='bold',fontsize=24) 
 

plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))
# plt.gca().tick_params(axis='both', which='major', length=6, width=2.6)
# plt.gca().tick_params(axis='both', which='minor', length=3, width=1.8) 
plt.grid(which ='major', visible=True, linestyle='-',  lw =0.75, alpha=0.25, color = "black")  
plt.grid(which= 'minor', visible=True, linestyle='-',  lw =0.25, alpha=0.15, color = "black")    

plt.xticks(fontweight='bold')
# plt.gca().set_yticklabels([]) 

plt.legend(loc = 'upper center', frameon=False, bbox_to_anchor=(0.5, 1.12), ncol=2, fontsize=18) 

plt.text(0, 1.02, 'FIB current : 50 pA', ha='left', va='center', transform=plt.gca().transAxes, fontsize=16, fontweight='bold') 

if SIDE_SIDE:
    plt.plot([nominal[0], nominal[-1]], [450,450], color='black', lw = 1.5, ls='--')
    plt.text(340, 460, 'Nominal D', ha='center', va='center', fontsize=16 ) 

plt.savefig(f'{ylabel}.pdf', bbox_inches='tight')
plt.show()

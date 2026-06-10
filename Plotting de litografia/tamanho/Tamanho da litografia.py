import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np 

#####################################
CIRCLE = 1
RECTANGLE = 0

SIZE = 0
SIDE_SIDE = 0
PITCH = 1

#####################################
circle_nominal_D = 450
circle_nominal_L = [300,325,350,375,400]
circle_real_L = [298,339,375,399,422] 

circle_nominal_pitch = [(circle_nominal_D + L) for L in circle_nominal_L]
circle_real_pitch = [768, 792, 818, 844, 870]

circle_real_D = [(pitch - L) for pitch, L in zip(circle_real_pitch, circle_real_L)]
  


if SIZE:
    if CIRCLE:
        nominal = circle_nominal_L
        real = circle_real_L
        xlabel = 'Nominal L'
        ylabel = 'Real L'
    # elif RECTANGLE:
    #     nominal = rectangle_nominal_L
    #     real = rectangle_real_L
    else:
        raise ValueError("Nenhuma forma válida selecionada")

elif PITCH:
    if CIRCLE:
        nominal = circle_nominal_pitch
        real = circle_real_pitch
        xlabel = 'Nominal Pitch'
        ylabel = 'Real Pitch' 
    else:
        raise ValueError("Nenhuma forma válida selecionada")

elif SIDE_SIDE:
    if CIRCLE:
        nominal = circle_nominal_L
        real = circle_real_D
        xlabel = 'Nominal L'
        ylabel = 'Real D' 
    else:
        raise ValueError("Nenhuma forma válida selecionada")

else:
    raise ValueError("Nem SIZE nem PITCH estão ativos")

####################
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'Times New Roman' 
plt.rcParams["scatter.marker"] = 's'

plt.figure(figsize=(16*0.7,9*0.7), dpi=100)

#####################
size = 40
c1 = '#552b16'
c2 = '#ed872d'  
#Infiniteeth Color Palete v1 Color Palette

plt.scatter(nominal, real, color= c1, s = size ,label='Circular Cavity')   
####################

#escreva em cima de cada ponto o valor real
for i in range(len(nominal)):
    plt.text(nominal[i], real[i]*1.001, f'{real[i]}', ha='center', va='bottom', fontsize=14, fontweight='bold', color=c1) 

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
# border_x= nominal[0]*0.05
# border_y = real[0]*0.05
# plt.xlim(nominal[0] - border_x, nominal[-1] + border_x)
# plt.ylim(real[0] - border_y, real[-1] + border_y)

plt.legend(loc = 'upper center', frameon=False, bbox_to_anchor=(0.5, 1.12), ncol=2, fontsize=18) 

plt.text(0, 1.02, 'FIB current : 50 pA', ha='left', va='center', transform=plt.gca().transAxes, fontsize=16, fontweight='bold') 

if SIDE_SIDE:
    plt.plot([nominal[0], nominal[-1]], [450,450], color='black', lw = 1.5, ls='--')
    plt.text(0.5, 0.3, 'Nominal D', ha='center', va='center', transform=plt.gca().transAxes, fontsize=16 ) 

plt.savefig(f'{ylabel}.pdf', bbox_inches='tight')
plt.show()

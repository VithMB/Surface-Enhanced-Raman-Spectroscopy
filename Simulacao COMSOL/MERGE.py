import pandas as pd
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator,MaxNLocator


plt.rcParams['font.family'] ='sans-serif' 
plt.rcParams['mathtext.fontset'] = 'stixsans' 
plt.rcParams['font.size'] = 14


#   Carregar os dados
dataframe_633 = pd.read_csv('EF_Heatmap_633nm.csv', index_col=0)
dataframe_785 = pd.read_csv('EF_Heatmap_785nm.csv', index_col=0) 
 
L_633 = dataframe_633.columns.astype(float).values
D_633 = dataframe_633.index.astype(float).values
value_633 = dataframe_633.values 
L_785 = dataframe_785.columns.astype(float).values
D_785 = dataframe_785.index.astype(float).values
value_785 = dataframe_785.values

#   Criar a função de interpolação para o mapa de 633nm 
interpolation_function = RegularGridInterpolator((D_633, L_633), value_633, 
                                      bounds_error=False, fill_value=0)

#   Criar a malha de pontos do gráfico de 785nm (onde queremos projetar os dados)
# meshgrid gera todas as combinações de D e L do gráfico alvo
mesh_D, mesh_L = np.meshgrid(D_785, L_785, indexing='ij')
target_points = np.array([mesh_D.flatten(), mesh_L.flatten()]).T

# Executar a interpolação e remodelar para o formato da matriz
value_633_resampled = interpolation_function(target_points).reshape(len(D_785), len(L_785))
     

EF_total = value_633_resampled * value_785
 
plt.figure(figsize=(10, 6))
ax = plt.gca()
im = ax.imshow(EF_total, origin='lower', aspect='auto', 
           extent=[ L_785.min(), L_785.max(), D_785.min(), D_785.max()],
           norm=LogNorm(), cmap='jet',
           interpolation='bicubic') 
ax.set_xlabel(r'Pyramid Base Side - $\mathbf{L}$ (nm)', fontweight='bold' )

ax.set_ylabel(r'Pyramid Spacing - $\mathbf{D}$ (nm)', fontweight='bold' )

ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(AutoMinorLocator(4)) 
ax.tick_params(which='major', length=8, width=2.1)
ax.tick_params(which='minor', length=5, width=1.8)
plt.colorbar(im, label='EF 633nm * EF 785nm')
ax.set_title(rf'633nm x 785nm ')
plt.show()
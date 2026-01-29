import pandas as pd
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator

# Configurações de fonte
plt.rcParams['font.family'] ='sans-serif' 
plt.rcParams['mathtext.fontset'] = 'stixsans' 
plt.rcParams['font.size'] = 14

# 1. Carregar os dados
dataframe_633 = pd.read_csv('EF_Heatmap_633nm.csv', index_col=0)
dataframe_785 = pd.read_csv('EF_Heatmap_785nm.csv', index_col=0) 

L_633 = dataframe_633.columns.astype(float).values
D_633 = dataframe_633.index.astype(float).values
value_633 = dataframe_633.values 

L_785 = dataframe_785.columns.astype(float).values
D_785 = dataframe_785.index.astype(float).values
value_785 = dataframe_785.values

# --- NOVIDADE: CRIAR O SUPER GRID (UNIÃO) ---
# np.unique + np.concatenate garante que todos os pontos de ambos os arquivos estejam presentes
L_union = np.sort(np.unique(np.concatenate([L_633, L_785])))
D_union = np.sort(np.unique(np.concatenate([D_633, D_785])))

# 2. Criar funções de interpolação para AMBOS os mapas
interp_633 = RegularGridInterpolator((D_633, L_633), value_633, 
                                     bounds_error=False, fill_value=None)

interp_785 = RegularGridInterpolator((D_785, L_785), value_785, 
                                     bounds_error=False, fill_value=None)

# 3. Criar a malha de pontos do SUPER GRID
mesh_D, mesh_L = np.meshgrid(D_union, L_union, indexing='ij')
target_points = np.array([mesh_D.flatten(), mesh_L.flatten()]).T

# 4. Projetar os dois mapas no Super Grid
# Agora ambos terão o mesmo formato (ex: 120 linhas x 61 colunas)
value_633_union = interp_633(target_points).reshape(len(D_union), len(L_union))
value_785_union = interp_785(target_points).reshape(len(D_union), len(L_union))

# 5. Multiplicação final (sem perda de pontos originais)
EF_total = value_633_union * value_785_union

# --- PLOTAGEM ---
plt.figure(figsize=(10, 6))
ax = plt.gca()

# O extent agora usa os limites da UNIÃO
im = ax.imshow(EF_total, origin='lower', aspect='auto', 
               extent=[L_union.min(), L_union.max(), D_union.min(), D_union.max()],
               norm=LogNorm(), cmap='jet', interpolation='bicubic') 

ax.set_xlabel(r'Pyramid Base Side - $\mathbf{L}$ (nm)', fontweight='bold' )
ax.set_ylabel(r'Pyramid Spacing - $\mathbf{D}$ (nm)', fontweight='bold' )

ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(AutoMinorLocator(4)) 
ax.tick_params(which='major', length=8, width=2.1)
ax.tick_params(which='minor', length=5, width=1.8)

plt.colorbar(im, label='EF 633nm * EF 785nm')
ax.set_title(rf'633nm $\times$ 785nm ')

plt.tight_layout()
plt.show()
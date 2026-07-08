import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# File della simulazione laterale
lateral_file = "output/dose_proton_200MeV_lateral_1000.out"

# File del profilo longitudinale
# per scegliere automaticamente la profondità del picco di Bragg
longitudinal_file = Path("output/dose_proton_200MeV_1000.out")

# Lettura dati laterali
data = np.loadtxt(lateral_file, skiprows=1)

x_index = data[:, 0].astype(int)
y_index = data[:, 1].astype(int)
z_index = data[:, 2].astype(int)
dose = data[:, 3]

# Dimensioni dei voxel usate nella simulazione
voxel_x_mm = 1.0
voxel_y_mm = 1.0

# Dimensione totale laterale del fantoccio 60 mm
size_y_mm = 60.0

# Scelta della profondità a cui estrarre il profilo laterale al massimo della dose.
if longitudinal_file.exists():
    long_data = np.loadtxt(longitudinal_file, skiprows=1)
    bragg_x_index = int(long_data[np.argmax(long_data[:, 3]), 0])
else:
    # Se non è presente il profilo longitudinale
    bragg_x_index = 260 #stima del massimo data l'energia del fascio di protoni

# Estrazione dei voxel alla profondità del picco di Bragg
mask = x_index == bragg_x_index

y_sel = y_index[mask]
dose_sel = dose[mask]

# Conversione y_index in coordinata laterale fisica
y_mm = (y_sel + 0.5) * voxel_y_mm - size_y_mm / 2.0

# Ordine per y crescente
order = np.argsort(y_mm)
y_mm = y_mm[order]
dose_sel = dose_sel[order]

# Profondità fisica corrispondente
depth_mm = (bragg_x_index + 0.5) * voxel_x_mm

plt.figure(figsize=(8, 5))
plt.plot(y_mm, dose_sel, marker=".", linewidth=1)

plt.xlabel("Posizione laterale y (mm)")
plt.ylabel("Dose (Gy)")
plt.title(f"Profilo laterale della dose - protoni 200 MeV, profondità {depth_mm:.1f} mm")

plt.grid(True)
plt.tight_layout()

plt.savefig("output/plot_lateral_proton_200MeV_1000.png", dpi=300)
plt.show()

print(f"Profilo laterale estratto a x_index = {bragg_x_index}")
print(f"Profondità circa = {depth_mm:.1f} mm")
print("Grafico salvato in output/plot_lateral_proton_200MeV_1000_on_bragg_peak.png")

######################################################################
# Estrazione dei voxel alla profondità di metà del picco di Bragg
mask = x_index == bragg_x_index/2

y_sel = y_index[mask]
dose_sel = dose[mask]

# Conversione y_index in coordinata laterale fisica
y_mm = (y_sel + 0.5) * voxel_y_mm - size_y_mm / 2.0

# Ordine per y crescente
order = np.argsort(y_mm)
y_mm = y_mm[order]
dose_sel = dose_sel[order]

# Profondità fisica corrispondente
depth_mm = (bragg_x_index/2 + 0.5) * voxel_x_mm

plt.figure(figsize=(8, 5))
plt.plot(y_mm, dose_sel, marker=".", linewidth=1)

plt.xlabel("Posizione laterale y (mm)")
plt.ylabel("Dose (Gy)")
plt.title(f"Profilo laterale della dose - protoni 200 MeV, profondità {depth_mm:.1f} mm")

plt.grid(True)
plt.tight_layout()

plt.savefig("output/plot_lateral_proton_200MeV_1000.png", dpi=300)
plt.show()

print(f"Profilo laterale estratto a x_index = {bragg_x_index}")
print(f"Profondità circa = {depth_mm:.1f} mm")
print("Grafico salvato in output/plot_lateral_proton_200MeV_1000_Before_Bragg_Peak.png")

#############################################################################

# Estrazione dei voxel alla profondità oltre il picco di Bragg (fissata a 1 cm prima della fine del fantoccio ad acqua)
mask = x_index == 290

y_sel = y_index[mask]
dose_sel = dose[mask]

# Conversione y_index in coordinata laterale fisica
y_mm = (y_sel + 0.5) * voxel_y_mm - size_y_mm / 2.0

# Ordine per y crescente
order = np.argsort(y_mm)
y_mm = y_mm[order]
dose_sel = dose_sel[order]

# Profondità fisica corrispondente
depth_mm = (290 + 0.5) * voxel_x_mm

plt.figure(figsize=(8, 5))
plt.plot(y_mm, dose_sel, marker=".", linewidth=1)

plt.xlabel("Posizione laterale y (mm)")
plt.ylabel("Dose (Gy)")
plt.title(f"Profilo laterale della dose - protoni 200 MeV, profondità {depth_mm:.1f} mm")

plt.grid(True)
plt.tight_layout()

plt.savefig("output/plot_lateral_proton_200MeV_1000_Beyond_Bragg_peak.png", dpi=300)
plt.show()

print(f"Profilo laterale estratto a x_index = {bragg_x_index}")
print(f"Profondità circa = {depth_mm:.1f} mm")
print("Grafico salvato in output/plot_lateral_proton_200MeV_1000.png")

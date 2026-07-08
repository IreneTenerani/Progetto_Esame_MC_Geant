import numpy as np
import matplotlib.pyplot as plt

# File di dose prodotto da simulazione protoni
filename = "output/dose_proton_200MeV_1000.out"

# Lettura file di dose (saltando prima linea che contiene nomi colonne)
data = np.loadtxt(filename, skiprows=1)

# Colonne:
# 0 = x_index
# 1 = y_index
# 2 = z_index
# 3 = dose in Gy
x_index = data[:, 0]
dose = data[:, 3]

# Dimensione del voxel lungo x uguale a quello scelto nella macro di simulazione (1 mm)
voxel_size_mm = 1.0

# La profondità fisica in mm corrisponde al centro della slice
depth_mm = (x_index + 0.5) * voxel_size_mm

plt.figure(figsize=(8, 5))
plt.plot(depth_mm, dose, marker=".", linewidth=1)

plt.xlabel("Profondità in acqua (mm)")
plt.ylabel("Dose (Gy)")
plt.title("Profilo longitudinale della dose - protoni 200 MeV, 1000 eventi")

plt.grid(True)
plt.tight_layout()

plt.savefig("output/plot_longitudinal_proton_200MeV_1000.png", dpi=300)
plt.show()

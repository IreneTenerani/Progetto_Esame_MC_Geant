import numpy as np
import matplotlib.pyplot as plt

# Legge il file saltando la prima riga, che contiene i nomi delle colonne
data = np.loadtxt("output/dose_default_58MeV_1000.out", skiprows=1)

# Colonne del file:
# colonna 0 = x_index
# colonna 1 = y_index
# colonna 2 = z_index
# colonna 3 = dose in Gy
x_index = data[:, 0]
dose = data[:, 3]

# Nella macro default la dimensione del voxel lungo x è 1 mm
voxel_size_mm = 1.0

# Usa il centro della slice come profondità
depth_mm = (x_index + 0.5) * voxel_size_mm

plt.figure()
plt.plot(depth_mm, dose, marker="o")
plt.xlabel("Profondità in acqua (mm)")
plt.ylabel("Dose (Gy)")
plt.title("Profilo longitudinale della dose - test Radiobiology")
plt.grid(True)
plt.tight_layout()

plt.savefig("output/bragg_default_58MeV_1000.png", dpi=300)
plt.show()

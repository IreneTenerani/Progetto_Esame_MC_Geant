import numpy as np
import matplotlib.pyplot as plt

filename = "../build_progetto/output/ESEMPIO_dose_proton_200MeV_10000_g40.out"

data = np.loadtxt(filename, skiprows=1)

x_index = data[:, 0]
dose = data[:, 3]

voxel_x_mm = 1.0
depth_mm = (x_index + 0.5) * voxel_x_mm

plt.figure(figsize=(8, 5))
plt.plot(depth_mm, dose, marker=".", linewidth=1)

plt.xlabel("Profondità in acqua (mm)")
plt.ylabel("Dose (Gy)")
plt.title("Profilo longitudinale - protoni 200 MeV, 10000 eventi")

plt.grid(True)
plt.tight_layout()

plt.savefig("output/plot_longitudinal_proton_200MeV_10000_g40.png", dpi=300)
plt.show()

print("Grafico salvato in output/plot_longitudinal_proton_200MeV_10000_g40.png")

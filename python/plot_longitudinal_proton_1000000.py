import numpy as np
import matplotlib.pyplot as plt

filename = "output/dose_proton_200MeV_1000000.out"

data = np.loadtxt(filename, skiprows=1)

x_index = data[:, 0]
dose = data[:, 3]

voxel_x_mm = 1.0
depth_mm = (x_index + 0.5) * voxel_x_mm

plt.figure(figsize=(8, 5))
plt.plot(depth_mm, dose, linewidth=1.8)

plt.xlabel("Profondità in acqua (mm)")
plt.ylabel("Dose (Gy)")
plt.title("Profilo longitudinale della dose - protoni 200 MeV, 1 000 000 eventi")

plt.grid(True)
plt.tight_layout()

plt.savefig("output/plot_longitudinal_proton_200MeV_1000000.png", dpi=300)
plt.show()

print("Grafico salvato in output/plot_longitudinal_proton_200MeV_1000000.png")

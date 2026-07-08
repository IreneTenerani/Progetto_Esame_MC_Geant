import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

voxel_x_mm = 1.0

files = {
    "Protoni 200 MeV": "output/dose_proton_200MeV_10000_g40.out",
    "He 200 MeV/u": "output/dose_He_200MeVu_10000_g40.out",
    "C 200 MeV/u": "output/dose_C_200MeVu_10000_g40.out",
    "O 200 MeV/u": "output/dose_O_200MeVu_10000_g40.out",
    "Ne 200 MeV/u": "output/dose_Ne_200MeVu_10000_g40.out",
}

plt.figure(figsize=(9, 6))

for label, filename in files.items():
    path = Path(filename)

    if not path.exists():
        print(f"File non trovato: {filename}")
        continue

    data = np.loadtxt(path, skiprows=1)

    x_index = data[:, 0]
    dose = data[:, 3]
    depth_mm = (x_index + 0.5) * voxel_x_mm

    if dose.max() > 0:
        dose_norm = dose / dose.max()
    else:
        dose_norm = dose

    plt.plot(depth_mm, dose_norm, linewidth=1.5, label=label)

plt.xlabel("Profondità in acqua (mm)")
plt.ylabel("Dose normalizzata al massimo")
plt.title("Profili longitudinali di dose in acqua - geometria 40 x 10 x 10 cm")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("output/plot_all_longitudinal_g40_10000.png", dpi=300)
plt.show()

print("Grafico salvato in output/plot_all_longitudinal_g40_10000.png")

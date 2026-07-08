import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

files = {
    "1000 eventi": "output/dose_proton_200MeV_1000.out",
    "1 000 000 eventi": "output/dose_proton_200MeV_1000000.out",
}

voxel_x_mm = 1.0

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

    # Normalizzazione al massimo della dose per confrontare la forma delle curve
    dose_norm = dose / dose.max()

    plt.plot(depth_mm, dose_norm, linewidth=1.5, label=label)

plt.xlabel("Profondità in acqua (mm)")
plt.ylabel("Dose normalizzata")
plt.title("Confronto Picco di Bragg longitudinale - protoni 200 MeV")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("output/plot_proton_1000_vs_1000000.png", dpi=300)
plt.show()

print("Grafico salvato in output/plot_proton_1000_vs_1000000.png")

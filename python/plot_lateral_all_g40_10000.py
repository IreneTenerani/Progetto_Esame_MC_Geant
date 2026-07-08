import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

voxel_x_mm = 1.0
voxel_y_mm = 1.0
size_y_mm = 100.0

particles = {
    "Protoni 200 MeV": {
        "longitudinal": "output/dose_proton_200MeV_10000_g40.out",
        "lateral": "output/dose_proton_200MeV_lateral_10000_g40.out",
        "single_plot": "output/plot_lateral_proton_200MeV_10000_g40.png",
    },
    "He 200 MeV/u": {
        "longitudinal": "output/dose_He_200MeVu_10000_g40.out",
        "lateral": "output/dose_He_200MeVu_lateral_10000_g40.out",
        "single_plot": "output/plot_lateral_He_200MeVu_10000_g40.png",
    },
    "Ca 200 MeV/u": {
        "longitudinal": "output/dose_C_200MeVu_10000_g40.out",
        "lateral": "output/dose_C_200MeVu_lateral_10000_g40.out",
        "single_plot": "output/plot_lateral_C_200MeVu_10000_g40.png",
    },
    "O 200 MeV/u": {
        "longitudinal": "output/dose_O_200MeVu_10000_g40.out",
        "lateral": "output/dose_O_200MeVu_lateral_10000_g40.out",
        "single_plot": "output/plot_lateral_O_200MeVu_10000_g40.png",
    },
}

lateral_profiles = {}

for label, info in particles.items():
    longitudinal_path = Path(info["longitudinal"])
    lateral_path = Path(info["lateral"])

    if not longitudinal_path.exists():
        print(f"File longitudinale mancante: {longitudinal_path}")
        continue

    if not lateral_path.exists():
        print(f"File laterale mancante: {lateral_path}")
        continue

    # Trova la profondità del Bragg peak dal profilo longitudinale
    long_data = np.loadtxt(longitudinal_path, skiprows=1)
    dose_long = long_data[:, 3]
    riga_massimo = np.argmax(dose_long)
    bragg_x_index = int(long_data[riga_massimo, 0])
    depth_mm = (bragg_x_index + 0.5) * voxel_x_mm

    # Legge la mappa laterale x-y
    data = np.loadtxt(lateral_path, skiprows=1)

    x_index = data[:, 0].astype(int)
    y_index = data[:, 1].astype(int)
    dose = data[:, 3]

    # Prende solo i voxel alla profondità del Bragg peak
    mask = x_index == bragg_x_index

    y_sel = y_index[mask]
    dose_sel = dose[mask]

    # Converte y_index nella coordinata fisica laterale
    y_mm = (y_sel + 0.5) * voxel_y_mm - size_y_mm / 2.0

    # Ordina i punti da sinistra a destra
    ordine = np.argsort(y_mm)
    y_mm = y_mm[ordine]
    dose_sel = dose_sel[ordine]

    lateral_profiles[label] = {
        "y_mm": y_mm,
        "dose": dose_sel,
        "depth_mm": depth_mm,
    }

    # Plot singolo non normalizzato
    plt.figure(figsize=(8, 5))
    plt.plot(y_mm, dose_sel, marker=".", linewidth=1)

    plt.xlabel("Posizione laterale y (mm)")
    plt.ylabel("Dose (Gy)")
    plt.title(f"Profilo laterale - {label}\nprofondità circa {depth_mm:.1f} mm")

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(info["single_plot"], dpi=300)
    plt.close()

    print(f"{label}: profilo laterale estratto a circa {depth_mm:.1f} mm")

# Plot unico normalizzato
plt.figure(figsize=(9, 6))

for label, prof in lateral_profiles.items():
    y_mm = prof["y_mm"]
    dose = prof["dose"]

    if dose.max() > 0:
        dose_norm = dose / dose.max()
    else:
        dose_norm = dose

    plt.plot(y_mm, dose_norm, linewidth=1.5, label=label)

plt.xlabel("Posizione laterale y (mm)")
plt.ylabel("Dose normalizzata al massimo")
plt.title("Profili laterali al Bragg peak - geometria 40 x 10 x 10 cm")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("output/plot_all_lateral_g40_10000.png", dpi=300)
plt.show()

print("Plot unico salvato in output/plot_all_lateral_g40_10000.png")

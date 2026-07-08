import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ==========================
# Impostazioni
# ==========================

output_dir = Path("output")
plot_dir = output_dir / "plots_1e6_g40"
plot_dir.mkdir(parents=True, exist_ok=True)

voxel_x_mm = 1.0
voxel_y_mm = 1.0

# Geometria 40 x 10 x 10 cm:
# larghezza y = 10 cm = 100 mm
size_y_mm = 100.0


# ==========================
# Funzioni
# ==========================

def read_dose_file(path):
    """
    Legge il file dose.out prodotto da Radiobiology.

    Colonne:
    0 = x_index
    1 = y_index
    2 = z_index
    3 = Dose (Gy)
    """
    data = np.loadtxt(path, skiprows=1)

    x_index = data[:, 0].astype(int)
    y_index = data[:, 1].astype(int)
    z_index = data[:, 2].astype(int)
    dose = data[:, 3]

    return x_index, y_index, z_index, dose


def make_label(path):
    """
    Crea una label a partire dal nome del file.
    """
    name = path.stem

    name = name.replace("dose_", "")
    name = name.replace("_1000000_g40", "")
    name = name.replace("_lateral", "")

    name = name.replace("protoni", "Protoni")
    name = name.replace("proton", "Protoni")

    name = name.replace("He", "Helium")
    name = name.replace("C", "Carbon")
    name = name.replace("O", "Oxygen")
    name = name.replace("Ne", "Neon")

    name = name.replace("200MeVu", "200 MeV/u")
    name = name.replace("200MeV", "200 MeV")
    name = name.replace("_", " ")

    return name.strip()


def find_bragg_peak(longitudinal_path):
    """
    Trova il massimo del profilo longitudinale.
    Restituisce:
    - indice x del massimo
    - profondità fisica in mm
    - dose massima
    """
    x_index, y_index, z_index, dose = read_dose_file(longitudinal_path)

    max_row = np.argmax(dose)

    bragg_x_index = int(x_index[max_row])
    bragg_depth_mm = (bragg_x_index + 0.5) * voxel_x_mm
    max_dose = dose[max_row]

    return bragg_x_index, bragg_depth_mm, max_dose


# ==========================
# Trovo i file
# ==========================

dose_files = sorted(output_dir.glob("dose_*1000000_g40.out"))

if not dose_files:
    print("Nessun file trovato con pattern: output/dose_*1000000_g40.out")
    raise SystemExit

longitudinal_files = []
lateral_files = []

for path in dose_files:
    if "_lateral_" in path.name:
        lateral_files.append(path)
    else:
        longitudinal_files.append(path)


# ==========================
# Plot longitudinali
# ==========================

summary_rows = []

print("\n=== Profili longitudinali ===")

plt.figure(figsize=(9, 6))

for path in longitudinal_files:
    label = make_label(path)

    x_index, y_index, z_index, dose = read_dose_file(path)
    depth_mm = (x_index + 0.5) * voxel_x_mm

    bragg_x_index, bragg_depth_mm, max_dose = find_bragg_peak(path)

    print(f"{label}: Bragg peak circa a {bragg_depth_mm:.1f} mm")

    summary_rows.append({
        "particle": label,
        "type": "longitudinal",
        "file": str(path),
        "bragg_x_index": bragg_x_index,
        "bragg_depth_mm": bragg_depth_mm,
        "max_dose_Gy": max_dose,
    })

    # Plot singolo in dose assoluta
    plt_single = plt.figure(figsize=(8, 5))
    plt.plot(depth_mm, dose, linewidth=1.8)
    plt.xlabel("Profondità in acqua (mm)")
    plt.ylabel("Dose (Gy)")
    plt.title(f"Profilo longitudinale - {label}")
    plt.grid(True)
    plt.tight_layout()

    safe_label = label.replace(" ", "_").replace("/", "u")
    plt.savefig(plot_dir / f"longitudinal_{safe_label}_absolute.png", dpi=300)
    plt.close(plt_single)

    # Plot unico normalizzato
    if dose.max() > 0:
        dose_norm = dose / dose.max()
    else:
        dose_norm = dose

    plt.plot(depth_mm, dose_norm, linewidth=1.5, label=label)


plt.xlabel("Profondità in acqua (mm)")
plt.ylabel("Dose normalizzata al massimo")
plt.title("Profili longitudinali di dose - 100 000 eventi")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "all_longitudinal_normalized_1e6_g40.png", dpi=300)
plt.close()

print(f"\nPlot longitudinale unico salvato in:")
print(plot_dir / "all_longitudinal_normalized_1e6_g40.png")


# ==========================
# Plot laterali
# ==========================

print("\n=== Profili laterali ===")

lateral_profiles = {}

for lateral_path in lateral_files:
    label = make_label(lateral_path)

    # Il corrispondente file longitudinale ha lo stesso nome senza "_lateral"
    longitudinal_name = lateral_path.name.replace("_lateral_", "_")
    longitudinal_path = output_dir / longitudinal_name

    if not longitudinal_path.exists():
        print(f"{label}: salto il laterale perché manca il longitudinale corrispondente")
        print(f"File cercato: {longitudinal_path}")
        continue

    bragg_x_index, bragg_depth_mm, max_dose_long = find_bragg_peak(longitudinal_path)

    x_index, y_index, z_index, dose = read_dose_file(lateral_path)

    # Estraggo la sezione laterale alla profondità del Bragg peak
    mask = x_index == bragg_x_index

    y_sel = y_index[mask]
    dose_sel = dose[mask]

    # Converto y_index in coordinata laterale fisica
    y_mm = (y_sel + 0.5) * voxel_y_mm - size_y_mm / 2.0

    # Ordino da sinistra a destra
    order = np.argsort(y_mm)
    y_mm = y_mm[order]
    dose_sel = dose_sel[order]

    print(f"{label}: laterale estratto a {bragg_depth_mm:.1f} mm")

    summary_rows.append({
        "particle": label,
        "type": "lateral_at_bragg_peak",
        "file": str(lateral_path),
        "bragg_x_index": bragg_x_index,
        "bragg_depth_mm": bragg_depth_mm,
        "max_dose_Gy": dose_sel.max() if len(dose_sel) > 0 else 0,
    })

    lateral_profiles[label] = {
        "y_mm": y_mm,
        "dose": dose_sel,
        "depth_mm": bragg_depth_mm,
    }

    # Plot laterale singolo in dose assoluta
    plt.figure(figsize=(8, 5))
    plt.plot(y_mm, dose_sel, linewidth=1.5)
    plt.xlabel("Posizione laterale y (mm)")
    plt.ylabel("Dose (Gy)")
    plt.title(f"Profilo laterale - {label}\nProfondità circa {bragg_depth_mm:.1f} mm")
    plt.grid(True)
    plt.tight_layout()

    safe_label = label.replace(" ", "_").replace("/", "u")
    plt.savefig(plot_dir / f"lateral_{safe_label}_absolute.png", dpi=300)
    plt.close()


# Plot unico laterale normalizzato
if lateral_profiles:
    plt.figure(figsize=(9, 6))

    for label, profile in lateral_profiles.items():
        y_mm = profile["y_mm"]
        dose = profile["dose"]

        if dose.max() > 0:
            dose_norm = dose / dose.max()
        else:
            dose_norm = dose

        plt.plot(y_mm, dose_norm, linewidth=1.5, label=label)

    plt.xlabel("Posizione laterale y (mm)")
    plt.ylabel("Dose normalizzata al massimo")
    plt.title("Profili laterali al Bragg peak - 100 000 eventi")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(plot_dir / "all_lateral_normalized_1e6_g40.png", dpi=300)
    plt.close()

    print(f"\nPlot laterale unico salvato in:")
    print(plot_dir / "all_lateral_normalized_1e6_g40.png")
else:
    print("Nessun laterale disponibile.")


# ==========================
# Salva riepilogo CSV
# ==========================

summary_path = plot_dir / "summary_1e6_g40.csv"

with open(summary_path, "w", newline="") as f:
    fieldnames = [
        "particle",
        "type",
        "file",
        "bragg_x_index",
        "bragg_depth_mm",
        "max_dose_Gy",
    ]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(summary_rows)

print(f"\nRiepilogo salvato in:")
print(summary_path)

print("\nFinito.")

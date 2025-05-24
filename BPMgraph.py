#
# Jacobo Nájera
# jacobo@jacobo.org
#
import os
import librosa
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

def calculate_bpm(audio_path):
    """Calcula el BPM de los archivo de audio."""
    try:
        y, sr = librosa.load(audio_path, sr=None)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        return float(tempo)
    except Exception as e:
        print(f"Error al procesar {audio_path}: {e}")
        return None

def process_directory(directory):
    """Procesa un directorio para calcular los BPM de las canciones."""
    bpm_data = []
    audio_files = [f for f in os.listdir(directory) if f.endswith(('.mp3', '.wav', '.flac', '.ogg'))]

    if not audio_files:
        print("No se encontraron archivos de audio válidos en el directorio.")
        return []

    for file_name in tqdm(audio_files, desc="Procesando canciones", unit="canción"):
        file_path = os.path.join(directory, file_name)
        bpm = calculate_bpm(file_path)
        if bpm is not None:
            bpm_data.append((file_name, bpm))

    return sorted(bpm_data, key=lambda x: x[1])

def plot_bpm_data_canciones(bpm_data, output_png):
    """Genera un gráfico de BPM con estética sonidera y lo guarda como PNG."""
    if not bpm_data:
        print("No hay datos para graficar.")
        return

    song_names = [item[0] for item in bpm_data]
    bpm_values = [item[1] for item in bpm_data]

    # Configuración del gráfico
    plt.figure(figsize=(16, 10))
    y_pos = np.arange(len(song_names))

    # Colores 
    colors = plt.cm.viridis(np.linspace(0, 1, len(song_names)))

    bars = plt.barh(y_pos, bpm_values, color=colors, edgecolor='black', linewidth=2)

    # Etiquetas al final de cada barra
    for bar, bpm in zip(bars, bpm_values):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, f'{bpm:.1f}',
                 va='center', ha='left', fontsize=12, fontweight='bold', color='white')

    # Título y etiquetas con estilo
    plt.title('BPM graph: pulsaciones por minuto', fontsize=24, fontweight='bold', color='yellow', pad=20, loc='center')
    plt.xlabel('BPM', fontsize=16, fontweight='bold', color='white')
    plt.ylabel('Canciones', fontsize=16, fontweight='bold', color='white')

    # Personalización del fondo y ejes
    plt.gca().set_facecolor('#121212')  # Fondo oscuro
    plt.gca().tick_params(colors='white', labelsize=12)
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

    plt.yticks(y_pos, song_names, fontsize=10, color='white')
    plt.tight_layout()

    # Agregar un marco de colores brillantes al gráfico
    plt.gcf().patch.set_facecolor('#1a1a1a')  # Fondo exterior oscuro
    plt.gcf().patch.set_edgecolor('lime')
    plt.gcf().patch.set_linewidth(10)

    # Guardar el gráfico
    plt.savefig(output_png, dpi=300)
    plt.close()
    print(f"Gráfico PNG guardado en: {output_png}")

if __name__ == "__main__":
    directory = input("Introduce el directorio con las canciones: ").strip()
    output_png = "BPMgraph.png"

    if not os.path.isdir(directory):
        print("El directorio especificado no existe.")
    else:
        print("Analizando canciones...")
        bpm_data = process_directory(directory)

        if bpm_data:
            print("Generando imagen BPMgraph...")
            plot_bpm_data_canciones(bpm_data, output_png)
        else:
            print("No se encontraron canciones o no se pudieron procesar.")

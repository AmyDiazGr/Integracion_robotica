"""
Procesador de Señales: Interfaz Gráfica para Manipulación de Audio.

Este programa permite cargar archivos de audio (.wav, .mp3, .aac) y aplicar filtros personalizados
a las señales de audio, así como realizar transformadas de Fourier para su análisis. Utiliza la
biblioteca `tkinter` para crear una interfaz gráfica interactiva, junto con `matplotlib` para la
visualización de datos, `scipy` para el procesamiento de señales, y `pydub` para la manipulación
de audio.

Funcionalidades:
- Carga de archivos de audio en formatos populares (wav, mp3, aac).
- Selección de filtros ("Pasa-bajas", "Pasa-altas", "Pasa-bandas").
- Ajuste de parámetros del filtro, como frecuencia de corte y orden.
- Visualización de las señales original y procesada en gráficos.
- Aplicación de transformada de Fourier para análisis en el dominio de frecuencia.
- Guardado de los resultados procesados en un archivo.

Componentes:
1. Interfaz Principal: Creada con `tkinter`, divide el programa en dos marcos principales:
   - `frame_izquierdo`: Contiene botones y entradas para carga de archivos, selección de filtro,
     ajuste de parámetros, y ejecución de acciones.
   - `frame_derecho`: Espacio reservado para la visualización de gráficos con `matplotlib`.

2. Visualización de Señales: Usa `matplotlib` para mostrar gráficos interactivos, integrados
   dentro de la interfaz gráfica con `FigureCanvasTkAgg`.

3. Procesamiento de Señales: Utiliza funciones de `scipy` para diseñar y aplicar filtros,
   junto con transformadas de Fourier para el análisis del espectro de frecuencias.

Variables Globales:
- `muestras`: Almacena los datos de audio cargados.
- `tasa_muestreo`: Almacena la tasa de muestreo del archivo de audio.
- `senal_filtrada`: Contiene los datos de la señal después de aplicar el filtro.
- `audio_original`: Representación del archivo de audio original en formato `pydub.AudioSegment`.
- `audio_filtrado`: Representación del archivo de audio filtrado en formato `pydub.AudioSegment`.

Bibliotecas Requeridas:
- `tkinter`: Para la creación de la interfaz gráfica.
- `matplotlib.pyplot`: Para la visualización de gráficos.
- `numpy`: Para manejo de datos numéricos.
- `matplotlib.backends.backend_tkagg`: Para integrar gráficos en la interfaz.
- `pydub`: Para la manipulación de archivos de audio.
- `scipy.fftpack`: Para cálculo de transformadas de Fourier.
- `scipy.signal`: Para diseño y aplicación de filtros.

Este programa ofrece una plataforma interactiva para explorar, modificar y analizar señales de
audio, adecuada para aplicaciones educativas y de investigación.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pydub import AudioSegment
from scipy.fftpack import fft
from scipy.signal import butter, filtfilt

# Variables globales
muestras = None
tasa_muestreo = None
senal_filtrada = None
audio_original = None
audio_filtrado = None

# Crear la interfaz principal
root = tk.Tk()
root.title("Procesador de Señales")
root.geometry("1500x1000")

# Marco principal
frame_izquierdo = tk.Frame(root, width=400, padx=20, pady=20)
frame_izquierdo.pack(side=tk.LEFT, fill=tk.Y)

frame_derecho = tk.Frame(root, width=800, padx=10, pady=10)
frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Sección de carga de audio
label_bienvenida = tk.Label(
    frame_izquierdo,
    text="Bienvenido a tu Procesador de Señales\nCarga un archivo .wav, .mp3, .aac",
    font=("Arial", 12),
)
label_bienvenida.pack(pady=15)

btn_cargar = tk.Button(
    frame_izquierdo,
    text="Cargar Archivo de Audio",
    font=("Arial", 10),
    command=lambda: cargar_audio(),
)
btn_cargar.pack(pady=15)

# Sección de selección de filtro
label_filtro = tk.Label(
    frame_izquierdo, text="Selecciona un filtro:", font=("Arial", 10)
)
label_filtro.pack(pady=5)

filtro_var = tk.StringVar()
filtro_menu = ttk.Combobox(
    frame_izquierdo, textvariable=filtro_var, state="readonly", font=("Arial", 10)
)
filtro_menu["values"] = ("Pasa-bajas", "Pasa-altas", "Pasa-bandas")
filtro_menu.pack(pady=5)
filtro_menu.current(0)

# Sección de parámetros del filtro
label_fc = tk.Label(
    frame_izquierdo, text="Frecuencia de corte (Hz):", font=("Arial", 10)
)
label_fc.pack(pady=5)
entry_fc = tk.Entry(frame_izquierdo, font=("Arial", 10))
entry_fc.pack(pady=5)

label_orden = tk.Label(frame_izquierdo, text="Orden del filtro:", font=("Arial", 10))
label_orden.pack(pady=5)
entry_orden = tk.Entry(frame_izquierdo, font=("Arial", 10))
entry_orden.pack(pady=5)

btn_aplicar = tk.Button(
    frame_izquierdo,
    text="Aplicar Filtro",
    font=("Arial", 10),
    command=lambda: aplicar_filtro(filtro_var.get(), entry_fc.get(), entry_orden.get()),
)
btn_aplicar.pack(pady=15)

btn_transformada = tk.Button(
    frame_izquierdo,
    text="Aplicar Transformada",
    font=("Arial", 10),
    command=lambda: aplicar_transformada(),
)
btn_transformada.pack(pady=15)

btn_guardar = tk.Button(
    frame_izquierdo,
    text="Guardar Resultado",
    font=("Arial", 10),
    command=lambda: guardar_audio(),
)
btn_guardar.pack(pady=15)

# Espacio para visualización de señales
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
canvas = FigureCanvasTkAgg(fig, master=frame_derecho)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def cargar_audio():
    """Carga un archivo de audio compatible y extrae sus muestras y tasa de muestreo.

    Archivo soportado: .wav,.mp3, .aac

    Ventana adicional:
        Muestra un cuadro de mensaje indicando èxito o error.

    Actualiza:
        -muestra: Señal normalizada de audio cargada.
        -tasa_muestreo: Feceucnia de muestreo del archivo de audio.
        -audio_original: Objeto de audio cargado.

    Returns:
        None
    """
    global muestras, tasa_muestreo, audio_original, senal_filtrada
    archivo = filedialog.askopenfilename(
        filetypes=[("Archivos de audio", "*.wav *.mp3 *.aac")]
    )
    if archivo:
        try:
            audio_original = AudioSegment.from_file(archivo)
            muestras = np.array(audio_original.get_array_of_samples(), dtype=np.float32)
            tasa_muestreo = audio_original.frame_rate
            muestras /= np.max(np.abs(muestras))
            senal_filtrada = None
            messagebox.showinfo(
                "Carga Exitosa",
                f"Archivo: {archivo.split('/')[-1]}\nTasa de Muestreo: {tasa_muestreo} Hz\nDuración: {len(muestras) / tasa_muestreo:.2f} s",
            )
            actualizar_graficos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo.\nError: {e}")


def aplicar_transformada():
    """
    Aplica la transformada de Fourier a la señal original y a la señal filtrada para vizualizar su espectro de frecuencia.

    Side Effects:

        -Modifica graficos con los espectros de frecuencia

    Returns:
    None
    """
    global muestras, senal_filtrada, tasa_muestreo

    if muestras is None:
        messagebox.showerror("Error", "Primero debes cargar un archivo de audio.")
        return

    # Calcular la Transformada de Fourier de la señal original
    transformada_original = fft(muestras)
    frecs = np.fft.fftfreq(len(muestras), d=1 / tasa_muestreo)

    # Obtener magnitud máxima para ajustar la escala
    max_magnitude = np.abs(transformada_original).max()

    # Limpiar el gráfico y actualizar con la señal original
    axs[1, 0].cla()
    axs[1, 0].plot(
        frecs[: len(frecs) // 2],
        np.abs(transformada_original[: len(transformada_original) // 2]),
        color="blue",
    )
    axs[1, 0].set_title("Espectro de Frecuencia - Señal Original")
    axs[1, 0].set_xlabel("Frecuencia (Hz)")
    axs[1, 0].set_ylabel("Magnitud")
    axs[1, 0].set_ylim(0, max_magnitude)  # Escala uniforme

    # Calcular la Transformada de Fourier de la señal filtrada si existe
    if senal_filtrada is not None:
        transformada_filtrada = fft(senal_filtrada)
        max_magnitude = max(max_magnitude, np.abs(transformada_filtrada).max())

        axs[1, 1].cla()
        axs[1, 1].plot(
            frecs[: len(frecs) // 2],
            np.abs(transformada_filtrada[: len(transformada_filtrada) // 2]),
            color="red",
        )
        axs[1, 1].set_title("Espectro de Frecuencia - Señal Filtrada")
        axs[1, 1].set_xlabel("Frecuencia (Hz)")
        axs[1, 1].set_ylabel("Magnitud")
        axs[1, 1].set_ylim(0, max_magnitude)  # Escala uniforme

    canvas.draw()


def aplicar_filtro(tipo_filtro, fc, orden):
    """Aplica el filtro especificado a la señal de audio cargada.

    Parameters:
        tipo_filtro (str): Tipo de filtro ("Pasa-bajas", "Pasa-altas", "Pasa-bandas")
         fc (float): Frecuencia de corte del filtro.
         orden (int): Orden del filtro.

    Side effects:
        -Muestra un mensaje indicando el èxito o error al aplicar el filtro.
        -Modifica 'señal_filtrada' con los datos filtrados.
        -Modifica gráficos con la señal filtrada.

    Returns:
       None
    """
    global senal_filtrada, audio_filtrado
    if muestras is None:
        messagebox.showerror("Error", "Primero debes cargar un archivo de audio.")
        return
    try:
        fc = float(fc)
        orden = int(orden)
    except ValueError:
        messagebox.showerror(
            "Error", "Frecuencia de corte y orden deben ser valores numéricos."
        )
        return
    if tipo_filtro == "Pasa-bajas":
        b, a = butter(orden, fc / (tasa_muestreo / 2), btype="low")
    elif tipo_filtro == "Pasa-altas":
        b, a = butter(orden, fc / (tasa_muestreo / 2), btype="high")
    elif tipo_filtro == "Pasa-bandas":
        b, a = butter(
            orden,
            [fc / (tasa_muestreo / 2), (fc + 1000) / (tasa_muestreo / 2)],
            btype="band",
        )
    else:
        messagebox.showerror("Error", "Filtro no reconocido.")
        return
    senal_filtrada = filtfilt(b, a, muestras)
    audio_filtrado = AudioSegment(
        (senal_filtrada / np.max(np.abs(senal_filtrada)) * 32767)
        .astype(np.int16)
        .tobytes(),
        frame_rate=tasa_muestreo,
        sample_width=2,  # 16 bits = 2 bytes
        channels=1,  # Mono
    )
    messagebox.showinfo(
        "Filtro Aplicado", f"Se ha aplicado el filtro {tipo_filtro} correctamente."
    )
    actualizar_graficos()
    print(senal_filtrada[:10])


def actualizar_graficos():
    """
    Actualiza los gráficos para mostrar la señal original y la señal filtrada (si existe).

    Side Effects:
        - Modifica axs[0, 0] para mostrar la señal original.
        - Modifica axs[0, 1] para mostrar la señal filtrada.

    Returns:
        None
    """
    axs[0, 0].cla()
    axs[0, 1].cla()

    # Calcular límites globales de amplitud
    global_min, global_max = 0, 0
    if muestras is not None:
        global_min = min(global_min, muestras.min())
        global_max = max(global_max, muestras.max())
        tiempo = np.linspace(0, len(muestras) / tasa_muestreo, num=len(muestras))
        axs[0, 0].plot(tiempo, muestras, color="blue")
        axs[0, 0].set_title("Señal Original")

    if senal_filtrada is not None:
        global_min = min(global_min, senal_filtrada.min())
        global_max = max(global_max, senal_filtrada.max())
        tiempo = np.linspace(
            0, len(senal_filtrada) / tasa_muestreo, num=len(senal_filtrada)
        )
        axs[0, 1].plot(tiempo, senal_filtrada, color="red")
        axs[0, 1].set_title("Señal Filtrada")

    # Aplicar límites a ambos gráficos
    axs[0, 0].set_ylim(global_min, global_max)
    axs[0, 1].set_ylim(global_min, global_max)

    canvas.draw()


def guardar_audio():
    """
    Guarda la señal filtrada como un archivo de audio .wav.

    Side Effects:
        - Muestra un cuadro de mensaje indicando éxito o error.

    Returns:
        None
    """
    global audio_filtrado

    if audio_filtrado is None:
        messagebox.showerror("Error", "No hay audio filtrado para guardar.")
        return

    archivo_guardado = filedialog.asksaveasfilename(
        defaultextension=".wav", filetypes=[("Archivo WAV", "*.wav")]
    )

    if archivo_guardado:
        audio_filtrado.export(archivo_guardado, format="wav")
        messagebox.showinfo(
            "Guardado Exitoso", f"El archivo se ha guardado como: {archivo_guardado}"
        )


root.mainloop()

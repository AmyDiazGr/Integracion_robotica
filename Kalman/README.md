# Kalman Filter 

## 🎯 Video Object Detection and Tracking with Roboflow and SORT

Este proyecto implementa un sistema de **detección y seguimiento de objetos en video**, combinando un modelo de visión por computadora hospedado en **Roboflow** con el algoritmo **SORT (Simple Online and Realtime Tracking)** basado en Kalman Filter.
Se toma un video como entrada, se realiza la inferencia de cada cuadro para detectar objetos, y posteriormente se realiza el seguimiento de cada objeto detectado en tiempo real.

## 📦 Requisitos

Para ejecutar este proyecto necesitas tener instaladas las siguientes librerías de Python:

- `opencv-python` 
- `numpy`
- `inference-sdk` (cliente de Roboflow)
- `filterpy`
- `scikit-image`
- `matplotlib`
- `scipy`

Puedes instalar los requisitos principales con:

```bash
pip install opencv-python numpy inference-sdk filterpy scikit-image matplotlib scipy
```


## 📁 Estructura del Proyecto

├── main.py                 # Script principal para detección y tracking \
├── sort.py                 # Algoritmo SORT para seguimiento multiobjeto \
├── balones.avi             # Video de entrada (puedes reemplazarlo por tu propio video)\
├── frame_temp.jpg          # Imagen temporal generada automáticamente\
└── README.md               # Este archivo

## 🚀 ¿Cómo funciona?

1.	Captura de video: El script lee el video balones.avi cuadro por cuadro.
2.	Inferencia Roboflow: Cada frame se convierte temporalmente a imagen y se envía a la API de Roboflow para detectar objetos.
3.	Filtrado de resultados: Solo se consideran predicciones con una confianza mayor a 0.5.
4.	Seguimiento con SORT: Se utiliza el algoritmo SORT para asociar y seguir objetos detectados entre cuadros del video.
5.	Visualización en tiempo real: Se dibujan los bounding boxes, los IDs de seguimiento y los centros de los objetos detectados sobre cada frame mostrado con OpenCV.

## 🧠 Acerca de SORT

SORT (Simple Online and Realtime Tracking) es un algoritmo de seguimiento multiobjeto basado en filtros de Kalman y el algoritmo húngaro de asignación. Está diseñado para ser eficiente y operar en tiempo real.
Principales características:
•	Seguimiento basado en predicciones y correcciones con Kalman Filter.
•	Asociación de detecciones por IoU.
•	Capacidad para rastrear objetos incluso con detecciones intermitentes.

## 🔑 API Key

•	Este proyecto utiliza una clave de API para conectarse a Roboflow:

```bash
api_key="DZQlW51niZIjUbe9sZMN"

```

## 🔐 Recomendación: 
Para un uso personalizado, crea tu propia cuenta en Roboflow y reemplaza esta clave por la tuya propia.

## 🧪 Ejecución del Proyecto

Una vez que tengas todas las dependencias instaladas y el video de entrada en la ruta correcta, simplemente ejecuta:

```bash
python main.py

```





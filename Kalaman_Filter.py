"""
Video Object Detection and Tracking with Roboflow and SORT.

This script performs object detection using a Roboflow-hosted model and tracks the detected
objects using the SORT (Simple Online and Realtime Tracking) algorithm.It processes an input video file frame by frame, sending each frame to Roboflow for inference, and visualizes the
tracking results in real time using OpenCV.

Dependencies :
- OpenCV
- NumPy
- inference-sdk (Roboflow)
- sort.py (must be present in the project directory)

"""
import cv2
import numpy as np
from inference_sdk import InferenceHTTPClient

from sort import Sort  # Asegúrate de tener sort.py en tu proyecto

# --- Roboflow Client Setup ---
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="DZQlW51niZIjUbe9sZMN",  # Reemplaza por tu propia API key si es necesario
)

# --- Video Input ---
video_path = "balones.avi"
cap = cv2.VideoCapture(video_path)

# Verifica que el video se haya abierto correctamente
if not cap.isOpened():
    raise IOError(f"No se pudo abrir el archivo de video: {video_path}")

# --- SORT Tracker Initialization ---
tracker = (
    Sort()
)  # Rastreador basado en Kalman Filter + asignación de Hungarian Algorithm

# --- Main Processing Loop ---
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Fin del video o error al leer.")
        break

    # Guardar frame temporalmente como imagen para enviarlo a Roboflow
    temp_img_path = "frame_temp.jpg"
    cv2.imwrite(temp_img_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

    # --- Roboflow Inference ---
    result = CLIENT.infer(temp_img_path, model_id="ca_proj_group4/2")

    detections = []

    # Convertir las predicciones al formato: [x1, y1, x2, y2, confidence]
    for prediction in result["predictions"]:
        if prediction["confidence"] < 0.5:
            continue

        x, y = int(prediction["x"]), int(prediction["y"])
        width, height = int(prediction["width"]), int(prediction["height"])
        conf = prediction["confidence"]

        x1 = x - width // 2
        y1 = y - height // 2
        x2 = x + width // 2
        y2 = y + height // 2

        detections.append([x1, y1, x2, y2, conf])

    # Convertir detecciones a NumPy array para pasar al rastreador
    dets = np.array(detections) if detections else np.empty((0, 5))

    # --- Actualizar el rastreador con las detecciones ---
    tracks = tracker.update(dets)

    # --- Visualización ---
    for track in tracks:
        x1, y1, x2, y2, track_id = track.astype(int)

        # Dibujar bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Etiqueta con el ID del objeto
        label = f"ID {track_id:02d}"
        cv2.putText(
            frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
        )

        # Dibujar centro de la caja
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

    # Mostrar el frame con resultados
    cv2.imshow("Detección + SORT Tracking", frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

# --- Liberar recursos ---
cap.release()
cv2.destroyAllWindows()

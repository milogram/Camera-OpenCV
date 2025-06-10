import cv2
import os
import numpy as np
from datetime import datetime, timedelta
import shutil
import schedule
import time
import sys

# Función para manejar errores
def handle_error(exception):
    print(f"Se produjo un error en el momento de la ejecución: {exception}")

# Función para cerrar el programa
def close_program():
    print("Cerrando el programa automáticamente a las 2:30 pm...")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()

# Función para detectar personas en una imagen
def detect_persons(image):
    height, width, _ = image.shape

    # Preprocesamiento de la imagen para YOLO
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Inicializar listas para almacenar información sobre las detecciones
    class_ids = []
    confidences = []
    boxes = []

    # Procesar las detecciones de YOLO
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and class_id == 0:  # 0 representa la clase "persona"
                # Escalar las coordenadas de la caja delimitadora a las dimensiones originales de la imagen
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Coordenadas de la caja delimitadora
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Aplicar Non-Maximum Suppression (NMS) si hay detecciones
    if boxes:
        # Seleccionar las detecciones con las mayores confidencias
        indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
        
        # Si hay al menos una detección
        if indices.any():
            for i in indices.flatten():
                # Obtener las coordenadas de la caja delimitadora
                x, y, w, h = boxes[i]

                # Dibujar el cuadro delimitador alrededor de la persona detectada
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Agregar etiqueta "Persona" al cuadro delimitador
                cv2.putText(image, "Persona", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image, len(boxes) > 0  # Devolver también un indicador si se detectó alguna persona

# Función para limpiar las carpetas antiguas
def cleanup_folders():
    six_days_ago = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")

    for folder_name in os.listdir('.'):
        if os.path.isdir(folder_name) and folder_name < six_days_ago:
            shutil.rmtree(folder_name)

# Configuración inicial
try: 
    cv2.setUseOptimized(True)

    # Cargar el modelo YOLO pre-entrenado
    net = cv2.dnn.readNet("C:/Users/jhoan/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/Restaurante_OpenCV/modelos/yolov3.cfg", "C:/Users/jhoan/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/Restaurante_OpenCV/modelos/yolov3.weights")
    layer_names = net.getLayerNames()
    output_layers = net.getUnconnectedOutLayers()

    # Convertir los índices de las capas de salida en nombres de capas
    output_layers = [layer_names[i - 1] for i in output_layers]

    # Directorio externo donde se guardarán las imágenes
    directorio_externo = "C:/Users/jhoan/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"

    # Limpiar las carpetas antiguas
    cleanup_folders()

    # Capturar video desde la cámara
    cap = cv2.VideoCapture(0)

    # Programar el cierre del programa a las 3:00 pm
    schedule.every().day.at("14:30").do(close_program)

    # Ciclo principal del programa
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detectar personas en el frame
        frame_with_boxes, person_detected = detect_persons(frame)

        # Si se detecta al menos una persona, guardar la imagen
        if person_detected:
            # Crear una carpeta para las imágenes del día
            current_date = datetime.now().strftime("%Y-%m-%d")
            os.makedirs(os.path.join(directorio_externo, current_date), exist_ok=True)

            # Nombre de archivo con hora actual
            current_time = datetime.now().strftime("%H-%M-%S")
            file_name = os.path.join(directorio_externo, current_date, f"{current_time}.jpg")

            # Guardar la imagen
            cv2.imwrite(file_name, frame_with_boxes)
            print(f"Imagen guardada: {file_name}")

        # Mostrar el frame con las detecciones
        cv2.imshow('Frame', frame_with_boxes)

        # Salir al presionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Ejecutar tareas programadas
        schedule.run_pending()
        time.sleep(1)

except Exception as e:
    handle_error(e)

finally:
    # Liberar la captura y cerrar las ventanas
    if 'cap' in locals():
        cap.release()
    cv2.destroyAllWindows()
    print("Programa finalizado.")

input("Presiona Enter para salir...")

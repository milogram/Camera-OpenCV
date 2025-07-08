# Cámara de Reconocimiento Humano con OpenCV y YOLOv3

Este proyecto consiste en una aplicación de visión artificial desarrollada en Python que utiliza una cámara conectada al sistema para detectar y registrar personas en tiempo real, mediante el modelo YOLOv3 y la librería OpenCV.

## Propósito del Proyecto

El sistema fue diseñado con el objetivo de monitorear y registrar el flujo de estudiantes al pasar por los servicios de **Snack** o **Lunch**. Busca reducir malas prácticas como el uso indebido de códigos de otros estudiantes, mediante la recolección visual de evidencias.

## ⚙️ Funcionalidad del Script Principal (`camarita.py`)

- Se ejecuta automáticamente al iniciar el equipo, desde la carpeta de inicio del sistema operativo.
- Detecta personas en tiempo real utilizando el modelo YOLOv3.
- Captura imágenes de los estudiantes que pasan frente a la cámara.
- Guarda las imágenes en carpetas organizadas por fecha.
- Elimina automáticamente carpetas con más de 6 días de antigüedad.
- Finaliza su ejecución todos los días a las **2:30 PM**, mostrando un mensaje.

## Tecnologías Usadas

- **Python 3**
- **OpenCV**
- **YOLOv3**
- **Sistema operativo Windows (para ejecución automática)**

## Importante: Archivos Grandes

Este repositorio **no incluye el archivo `yolov3.weights`** ya que su tamaño excede el límite de GitHub (100 MB).

🔗 Puedes descargarlo desde el sitio oficial:
[https://pjreddie.com/media/files/yolov3.weights](https://pjreddie.com/media/files/yolov3.weights)

Una vez descargado, colócalo en la siguiente ruta dentro del proyecto:


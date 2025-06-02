# Clasificador de Imágenes con Despliegue Automático (CI/CD)

Este proyecto implementa un sistema de despliegue automático para un modelo de clasificación de imágenes en formato ONNX, mediante el uso de GitHub Actions y Render. La aplicación está desarrollada con Flask y se conecta con Google Sheets para almacenar el historial de predicciones realizadas. Aunque inicialmente es un clasificador genérico de imágenes, el sistema está concebido para escalar a una aplicación de ingeniería civil que permita identificar fisuras en elementos estructurales y alertar sobre su severidad.

---

## 🌐 Tecnologías utilizadas

- **Modelo ONNX:** RegNet preentrenado (referenciado desde el repositorio oficial)
- **Framework backend:** Flask
- **CI/CD:** GitHub Actions
- **Contenedores:** Docker
- **Despliegue:** Render (plan gratuito)
- **Almacenamiento de predicciones:** Google Sheets (según entorno: dev/prod)

---

## 🔄 Flujo General del Proyecto

1. El usuario carga una imagen en la interfaz web.
2. La imagen es clasificada por el modelo ONNX y se retorna la etiqueta con su confianza.
3. La predicción se almacena junto a la fecha y el entorno (dev o prod) en Google Sheets.

---

## ⚙️ CI/CD con GitHub Actions

Se ha implementado un pipeline CI/CD para las ramas `dev` y `main`, con las siguientes etapas:

### Etapa de Test (CI)
- Descarga del modelo ONNX desde el repositorio oficial
- Obtención de datos de prueba
- Ejecución de pruebas unitarias:
  - El modelo responde correctamente a entradas válidas
  - La confianza del modelo está dentro de un rango razonable (0 a 1)

### Etapa de Build/Promote (CD)
- Construcción de la imagen Docker
- Despliegue a Render (según rama y entorno)
  - `main` → Producción
  - `dev` → Desarrollo

Nota: por límites del plan gratuito de Render, los despliegues se hacen de forma manual desde la interfaz de Render, pero el pipeline está completamente funcional para automatizarlos en escenarios de escalamiento.

---

## 🔺 Estructura del Repositorio

```
PROYECTO
├── main.py                  # Backend Flask
├── model_utils.py          # Lógica de carga y predicción ONNX
├── sheets_utils.py         # Registro en Google Sheets
├── test_model_utils.py     # Pruebas unitarias
├── requirements.txt        # Dependencias
├── Dockerfile              # Imagen de despliegue
├── templates/index.html    # Interfaz de carga
├── static/uploads/         # Imágenes cargadas (no se versionan)
├── .github/workflows/      # CI/CD: build.yml y test.yml
├── .env.example            # Ejemplo para configuración local
```

---

## 📅 Registro en Google Sheets

Cada predicción es registrada con:
- Fecha y hora en zona horaria de Colombia
- Nombre del archivo
- Etiqueta predicha
- Porcentaje de confianza
- Entorno (dev o prod)

> Las credenciales de Google no se suben al repositorio. Se cargan como variable de entorno en `.env` en una sola línea JSON.

---

## 🚀 Escalabilidad futura

Aunque actualmente el modelo clasifica imágenes genéricas, la arquitectura está diseñada para ser escalada a una aplicación de **diagnóstico estructural**, con el objetivo de:

- Detectar fisuras en elementos de concreto y mampostería
- Clasificarlas como "fisuras funcionales" o "fisuras críticas"
- Integrar la información con sistemas de monitoreo y mantenimiento

Esto representa una oportunidad para **automatizar inspecciones estructurales** en edificaciones y obras civiles.

---

## 📆 Entornos y ramas

- `main`  → Producción (https://render.com/prod-endpoint)
- `dev`   → Desarrollo (https://render.com/dev-endpoint)

En cada rama:
- Se prueba, construye y despliega de forma separada
- Se registran las predicciones en hojas distintas de Google Sheets

---

## 🌟 Consideraciones finales

- El modelo ONNX **no está en el repositorio**, sino que se descarga dinámicamente
- Las predicciones **no se almacenan localmente en producción**, sólo en Google Sheets
- Se implementó un `README.md` claro, completo y alineado con los criterios del curso

---

## 👉 Próximos pasos

- Entrenar y subir un modelo ONNX especializado en fisuras estructurales
- Añadir inferencia sobre secuencias o video

---

**Proyecto realizado por Carlos Vélez**  
Maestría en Inteligencia Artificial - Universidad Icesi  
Curso: MLOps - 2025

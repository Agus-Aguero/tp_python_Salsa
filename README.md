# 🍅 Laboratorio de Salsas con IA

Aplicación web interactiva desarrollada con Python y Streamlit para analizar la evolución de recetas de salsas a lo largo del tiempo y obtener recomendaciones personalizadas mediante Inteligencia Artificial.

## 🚀 Características Principales

1. **Interfaz Interactiva:** Construida con Streamlit, permite la carga dinámica de bitácoras de recetas en formato CSV.
2. **Análisis de Datos y Series de Tiempo:** Utiliza Pandas para procesar los datos, ordenar cronológicamente las pruebas y generar gráficos de evolución temporal de los puntajes obtenidos.
3. **Integración con LLMs:** Se conecta a la API de Inferencia de Hugging Face para enviar el peor intento registrado y devolver un consejo práctico generado por un modelo de lenguaje. Incluye un manejo robusto de excepciones y control de estados HTTP para prevenir caídas ante fallos de red o de la API externa.
4. **Gestión Segura de Credenciales:** Implementación de `st.secrets` para ocultar los tokens de acceso en el despliegue público, evitando fugas de seguridad en el repositorio.

## 📂 Estructura del CSV (`bitacora_salsas_ampliada.csv`)

La aplicación requiere un archivo CSV con la siguiente estructura de columnas para funcionar correctamente:

*   `fecha_prueba` (YYYY-MM-DD): Fecha en la que se realizó la receta. Fundamental para el análisis de Series de Tiempo.
*   `tipo_salsa` (String): Categoría de la salsa (ej. Pomodoro, Blanca, Pesto).
*   `tiempo_coccion_minutos` (Int): Duración de la preparación.
*   `nivel_acidez` (Int 1-10): Escala de acidez percibida.
*   `nivel_espesor` (Int 1-10): Escala de densidad de la preparación.
*   `puntaje_final` (Int 1-10): Calificación global de la prueba.
*   `notas_modificacion` (String): Observaciones cualitativas sobre el resultado y el proceso.

## 💻 Instalación y Ejecución Local

Para correr este proyecto en tu propia máquina, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Agus-Aguero/tp_python_Salsa.git
   cd tp_python_Salsa
   ```

2. **Crear y activar el entorno virtual:**
   * En Windows:
     ```bash
     python -m venv entorno
     .\entorno\Scripts\activate
     ```
   * En macOS/Linux:
     ```bash
     python3 -m venv entorno
     source entorno/bin/activate
     ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar el Token de Hugging Face:**
   * Crear una carpeta oculta `.streamlit` en la raíz del proyecto.
   * Dentro, crear un archivo `secrets.toml` y agregar la variable:
     `HF_TOKEN = "tu_token_aqui"`

5. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

## 🌐 Despliegue Público
El proyecto se encuentra desplegado en Streamlit Community Cloud.

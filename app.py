import streamlit as st
import pandas as pd
import requests

# Configuración básica de la página
st.set_page_config(page_title="Laboratorio de Salsas IA", layout="wide")

st.title("🍅 Laboratorio de Salsas con IA")
st.write("Analizá la evolución de tus recetas y recibí consejos de un Chef virtual.")

# 1. Carga de datos (Requisito: Interacción del usuario)
archivo_subido = st.file_uploader("Subí tu bitácora de salsas (CSV)", type=["csv"])

if archivo_subido is not None:
    # 2. Análisis con Pandas (Requisito: Clase de Pandas)
    df = pd.read_csv(archivo_subido)
    
    st.subheader("Datos Cargados")
    st.dataframe(df)
    
    # Aplicamos algunas funciones de Pandas vistas en clase
    st.subheader("Métricas por Tipo de Salsa")
    
    # Agrupación simple usando groupby (similar a lo que se logra con pivot)
    resumen = df.groupby("tipo_salsa").agg({
        "puntaje_final": "mean",
        "tiempo_coccion_minutos": "mean"
    }).reset_index()
    
    st.dataframe(resumen)

    # Demostración de Time Series con Pandas
    st.subheader("📈 Evolución temporal de los puntajes")
    
    # Convertimos la columna a formato datetime nativo de Pandas
    df['fecha_prueba'] = pd.to_datetime(df['fecha_prueba'])
    
    # Ordenamos cronológicamente por si el CSV viene desordenado
    df_tiempo = df.sort_values('fecha_prueba')
    
    # Usamos Streamlit para graficar la evolución del puntaje final usando la fecha como índice
    st.line_chart(data=df_tiempo.set_index('fecha_prueba')[['puntaje_final']])



    # Detectamos la prueba con peor puntaje usando Pandas
    peor_intento = df.loc[df['puntaje_final'].idxmin()]
    
    st.warning(f"⚠️ El intento con menor puntaje fue un/a {peor_intento['tipo_salsa']} (Puntaje: {peor_intento['puntaje_final']}).")
    st.write(f"Tus notas de ese día: *'{peor_intento['notas_modificacion']}'*")

    # 3. Integración con LLM (Requisito: Clase de LLMs / Hugging Face)
    st.subheader("👨‍🍳 Consejo del Chef IA")
    
    # Armamos un prompt claro para el modelo
    prompt = f"""
    Actúa como un chef experto. Un cocinero aficionado hizo una salsa {peor_intento['tipo_salsa']}. 
    El nivel de acidez quedó en {peor_intento['nivel_acidez']}/10.
    En sus notas puso: '{peor_intento['notas_modificacion']}'.
    Dame un solo consejo práctico en español, en una sola oración, para mejorarla la próxima vez.
    """
    
    if st.button("Consultar al Chef IA"):
        with st.spinner("Pensando la receta..."):
            
            # API de Hugging Face (Usamos Mistral, un modelo abierto y sin restricciones)
            API_URL = "https://router.huggingface.co/hf-inference/models/Qwen/Qwen2.5-1.5B-Instruct"
            token = st.secrets["HF_TOKEN"]
            headers = {"Authorization": f"Bearer {token}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 100, 
                    "temperature": 0.5,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
                
                # Si Hugging Face nos rechaza, ahora leemos su mensaje exacto
                if response.status_code != 200:
                    st.error(f"⚠️ Error {response.status_code} de la API: {response.text}")
                else:
                    # Si todo sale bien, procesamos el texto
                    resultado = response.json()
                    texto_ia = resultado[0]['generated_text'].strip()
                    st.success(f"**👨‍🍳 Respuesta del modelo:** {texto_ia}")
                
            except requests.exceptions.RequestException as e:
                st.error(f"Hubo un error de conexión con la IA: {e}")

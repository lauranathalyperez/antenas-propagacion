import streamlit as st
import numpy as np
import plotly.graph_objects as go
import base64

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILO
# ==========================================
st.set_page_config(page_title="Radio-Sim V1.0", layout="wide", page_icon="📡")

# ==========================================
# FUNCIÓN PARA CARGAR EL FONDO DESDE TU CARPETA
# ==========================================
def cargar_fondo_local(archivo_imagen):
    try:
        with open(archivo_imagen, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        css_fondo = f"""
        <style>
        /* 1. Fondo general */
        .stApp {{
            background-image: linear-gradient(rgba(15, 23, 42, 0.4), rgba(15, 23, 42, 0.4)),
                             url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* 2. Evita que la barra lateral cree recuadros oscuros molestos */
        main .stMetric, main .stSlider, main .stNumberInput, main .stSelectbox, main .stExpander, main [data-testid="stMarkdownContainer"] {{
            background-color: rgba(15, 23, 42, 0.85) !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        /* 3. Forzar texto blanco */
        h1, h2, h3, p, span, label, div {{
            color: #FFFFFF !important;
        }}

        /* Ajuste para los gráficos */
        .js-plotly-plot .main-svg text {{
            fill: #FFFFFF !important;
        }}
        </style>
        """
        st.markdown(css_fondo, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"⚠️ No se encontró el archivo '{archivo_imagen}'. Asegúrate de guardarlo en la misma carpeta.")

# Llamamos a la función de fondo
cargar_fondo_local("antenas.png")

# ==========================================
# MENÚ NAVEGACIÓN LATERAL
# ==========================================
st.sidebar.title("📑 Módulos")
st.sidebar.markdown("Selecciona el módulo de interés:")
modulo = st.sidebar.radio("", [
    "Introducción",
    "1. Propagación en Espacio Libre",
    "2. Atenuación por Lluvia",
    "3. Ruido Térmico y SNR",
    "4. Reflexión y Ley de Snell",
    "5. Onda de Espacio (Tierra Curva)",
    "6. Presupuesto de Enlace (Link Budget)",
    "7. Visualización de Antenas"
])

# ==========================================
# MÓDULO: INTRODUCCION
# ==========================================
if modulo == "Introducción":
    st.title("📡 Proyecto Simulador de Antenas y Propagación")
    st.subheader("Proyecto Práctico")
    st.markdown("""
    Bienvenid@ mi nombre es Laura Perez, estudiante de Ingenieria de Telecomunicaciones. Esta herramienta está diseñada para procesar, calcular y graficar
    los fenómenos clave de las telecomunicaciones y la propagación de ondas electromagnéticas. Adicional dar un pequeño abrebocas de cada uno de los temas
    indicados.

    ### Instrucciones:
    1. Usa el menú de la izquierda para navegar por los *7 ejes temáticos*.
    2. En cada módulo encontrarás una **Infografía Digital Dinámica** integrada con conceptos clave, bases matemáticas y un **Simulador interactivo** en tiempo real.
    """)
    st.info("💡 Desarrollado en Python utilizando Streamlit, Numpy y Plotly de forma nativa.")

# ==========================================
# MÓDULO 1: ESPACIO LIBRE
# ==========================================
elif modulo == "1. Propagación en Espacio Libre":
    st.title("✨ 1. Propagación en Espacio Libre (Friis)")

    st.markdown("### 📊 Infografía Digital del Eje Temático")
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("""
            <div style="background-color: rgba(0, 242, 255, 0.1); border-left: 5px solid #00F2FF; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00F2FF !important;">📡 Concepto Clave</h4>
                <p style="font-size: 14px; margin-bottom:0;">Modela la pérdida de potencia de una señal al propagarse en un medio ideal libre de obstáculos, reflexiones o interferencias externas.</p>
            </div>""", unsafe_allow_html=True)
    with info_col2:
        st.markdown("""
            <div style="background-color: rgba(255, 184, 0, 0.1); border-left: 5px solid #FFB800; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#FFB800 !important;">⚠️ Dependencias</h4>
                <p style="font-size: 14px; margin-bottom:0;">La pérdida por trayectoria (FSPL) aumenta proporcionalmente al <b>cuadrado de la distancia</b> y al <b>cuadrado de la frecuencia</b> de operación.</p>
            </div>""", unsafe_allow_html=True)
    with info_col3:
        st.markdown("""
            <div style="background-color: rgba(0, 255, 133, 0.1); border-left: 5px solid #00FF85; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00FF85 !important;">🧮 Expresión Matemática</h4>
                <p style="font-size: 13px; margin-bottom:5px;">Ecuación de Friis expresada en decibelios (dB):</p>
            </div>""", unsafe_allow_html=True)
        st.latex(r"FSPL(dB) = 32.44 + 20\log_{10}(d_{km}) + 20\log_{10}(f_{MHz})")

    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        f = st.slider("Frecuencia (MHz)", 100, 6000, 2400, key="m1_f")
        d = st.slider("Distancia del enlace (km)", 0.1, 50.0, 10.0, key="m1_d")
    with col2:
        fspl = 32.44 + 20*np.log10(d) + 20*np.log10(f)
        st.metric("Pérdida por Trayectoria (FSPL)", f"{fspl:.2f} dB")

        d_vector = np.linspace(0.1, 50, 100)
        fspl_vector = 32.44 + 20*np.log10(d_vector) + 20*np.log10(f)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d_vector, y=fspl_vector, name="FSPL", line=dict(color='#00F2FF', width=3)))
        fig.update_layout(title="Pérdidas vs Distancia", xaxis_title="Distancia (km)", yaxis_title="Pérdidas (dB)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15, 23, 42, 0.5)')
        st.plotly_chart(fig)

# ==========================================
# MÓDULO 2: ATENUACIÓN POR LLUVIA
# ==========================================
elif modulo == "2. Atenuación por Lluvia":
    st.title("🌧️ 2. Atenuación por Lluvia e Hidrometeoro")

    st.markdown("### 📊 Infografía Digital del Eje Temático")
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("""
            <div style="background-color: rgba(0, 242, 255, 0.1); border-left: 5px solid #00F2FF; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00F2FF !important;">🌧️ Fenómeno Físico</h4>
                <p style="font-size: 14px; margin-bottom:0;">A frecuencias mayores a 10 GHz (Microondas/Milimétricas), el tamaño de las gotas de lluvia es comparable a la longitud de onda, provocando dispersión y absorción de energía.</p>
            </div>""", unsafe_allow_html=True)
    with info_col2:
        st.markdown("""
            <div style="background-color: rgba(255, 184, 0, 0.1); border-left: 5px solid #FFB800; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#FFB800 !important;">📊 Parámetros ITU</h4>
                <p style="font-size: 14px; margin-bottom:0;">La severidad depende de la tasa de precipitación climática <i>R (mm/h)</i> y los coeficientes empíricos <i>k</i> y <i>&alpha;</i> fijados por la recomendación ITU-R P.838.</p>
            </div>""", unsafe_allow_html=True)
    with info_col3:
        st.markdown("""
            <div style="background-color: rgba(0, 255, 133, 0.1); border-left: 5px solid #00FF85; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00FF85 !important;">🧮 Modelo de Cálculo</h4>
                <p style="font-size: 13px; margin-bottom:5px;">Cálculo de la atenuación específica:</p>
            </div>""", unsafe_allow_html=True)
        st.latex(r"\gamma = k \cdot R^\alpha \quad [dB/km]")

    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        r_lluvia = st.slider("Tasa de lluvia (R en mm/h)", 0, 150, 50)
        dist_enlace = st.slider("Distancia afectada (km)", 1.0, 20.0, 5.0)
    with col2:
        k, alpha = 0.22, 1.15
        atenuacion_especifica = k * (r_lluvia ** alpha)
        atenuacion_total = atenuacion_especifica * dist_enlace

        st.metric("Atenuación Específica", f"{atenuacion_especifica:.2f} dB/km")
        st.metric("Pérdida Total por Lluvia", f"{atenuacion_total:.2f} dB")

        r_vector = np.linspace(0, 150, 100)
        attn_vector = (k * (r_vector ** alpha)) * dist_enlace
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=r_vector, y=attn_vector, name="Atenuación", line=dict(color='blue', width=3)))
        fig.update_layout(title="Pérdida total vs Intensidad de Lluvia", xaxis_title="Lluvia (mm/h)", yaxis_title="Pérdida Extra (dB)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15, 23, 42, 0.5)')
        st.plotly_chart(fig)

# ==========================================
# MÓDULO 3: RUIDO TÉRMICO Y SNR
# ==========================================
elif modulo == "3. Ruido Térmico y SNR":
    st.title("🔊 3. Ruido Térmico y Factor de Ruido")

    st.markdown("### 📊 Infografía Digital del Eje Temático")
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("""
            <div style="background-color: rgba(0, 242, 255, 0.1); border-left: 5px solid #00F2FF; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00F2FF !important;">🌡️ Ruido Blanco</h4>
                <p style="font-size: 14px; margin-bottom:0;">El ruido térmico (Johnson-Nyquist) es intrínseco e inevitable. Se origina por la agitación térmica de los electrones en los componentes electrónicos conductores.</p>
            </div>""", unsafe_allow_html=True)
    with info_col2:
        st.markdown("""
            <div style="background-color: rgba(255, 184, 0, 0.1); border-left: 5px solid #FFB800; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#FFB800 !important;">📉 Degradación</h4>
                <p style="font-size: 14px; margin-bottom:0;">A mayor ancho de banda (B) o temperatura de operación (T), mayor potencia de ruido ingresará al sistema, limitando la sensibilidad del receptor.</p>
            </div>""", unsafe_allow_html=True)
    with info_col3:
        st.markdown("""
            <div style="background-color: rgba(0, 255, 133, 0.1); border-left: 5px solid #00FF85; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00FF85 !important;">🧮 Potencia de Ruido</h4>
                <p style="font-size: 13px; margin-bottom:5px;">Ecuación fundamental del piso de ruido:</p>
            </div>""", unsafe_allow_html=True)
        st.latex(r"N = k \cdot T \cdot B \quad [Watts]")

    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        bw_mhz = st.number_input("Ancho de Banda (MHz)", value=20.0)
        temp_c = st.slider("Temperatura Ambiente (°C)", -20, 50, 25)
        f_ruido_db = st.slider("Factor de Ruido del Receptor (dB)", 0.0, 15.0, 4.0)
    with col2:
        k_boltz = 1.38e-23
        t_kelvin = temp_c + 273.15
        bw_hz = bw_mhz * 1e6

        n_watts = k_boltz * t_kelvin * bw_hz
        n_dbm = 10 * np.log10(n_watts / 1e-3)
        n_total_dbm = n_dbm + f_ruido_db

        st.metric("Piso de Ruido Térmico Puro (N)", f"{n_dbm:.2f} dBm")
        st.metric("Ruido Total del Sistema (con Factor F)", f"{n_total_dbm:.2f} dBm")
        st.info("💡 A mayor ancho de banda o temperatura, el receptor 'escuchará' más ruido, dificultando la recepción de señales débiles.")

# ==========================================
# MÓDULO 4: REFLEXIÓN Y SNELL
# ==========================================
elif modulo == "4. Reflexión y Ley de Snell":
    st.title("🪞 4. Reflexión y Refracción (Leyes de Snell)")

    st.markdown("### 📊 Infografía Digital del Eje Temático")
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("""
            <div style="background-color: rgba(0, 242, 255, 0.1); border-left: 5px solid #00F2FF; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00F2FF !important;">🌍 Interfaz de Medios</h4>
                <p style="font-size: 14px; margin-bottom:0;">Cuando una onda incide sobre una superficie divisoria (atmósfera-suelo), una porción de energía se refleja reflejando el ángulo incidente, y otra se transmite variando su dirección.</p>
            </div>""", unsafe_allow_html=True)
    with info_col2:
        st.markdown("""
            <div style="background-color: rgba(255, 184, 0, 0.1); border-left: 5px solid #FFB800; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#FFB800 !important;">⚠️ Ángulo Crítico</h4>
                <p style="font-size: 14px; margin-bottom:0;">Si una onda pasa de un medio con mayor índice de refracción a uno menor, existe un ángulo límite a partir del cual ocurre la <b>Reflexión Interna Total</b>.</p>
            </div>""", unsafe_allow_html=True)
    with info_col3:
        st.markdown("""
            <div style="background-color: rgba(0, 255, 133, 0.1); border-left: 5px solid #00FF85; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00FF85 !important;">🧮 Ley de Snell</h4>
                <p style="font-size: 13px; margin-bottom:5px;">Relación física de frentes de onda:</p>
            </div>""", unsafe_allow_html=True)
        st.latex(r"n_1 \cdot \sin(\theta_1) = n_2 \cdot \sin(\theta_2)")

    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        n1 = st.number_input("Índice Medio 1 (Ej: Aire = 1.0)", value=1.0)
        n2 = st.number_input("Índice Medio 2 (Ej: Suelo/Agua)", value=1.5)
        theta1 = st.slider("Ángulo de Incidencia (Grados)", 0, 90, 30)
    with col2:
        theta1_rad = np.radians(theta1)
        sin_theta2 = (n1 * np.sin(theta1_rad)) / n2

        if sin_theta2 > 1.0:
            st.error("⚠️ Reflexión Interna Total: ¡La onda no pasa al Medio 2, se refleja por completo!")
            theta2 = 90
        else:
            theta2_rad = np.arcsin(sin_theta2)
            theta2 = np.degrees(theta2_rad)
            st.metric("Ángulo de Refracción calculado (θ₂)", f"{theta2:.2f} °")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[-np.sin(theta1_rad), 0], y=[np.cos(theta1_rad), 0], name="Rayo Incidente", line=dict(width=3, color='#00F2FF')))
        fig.add_trace(go.Scatter(x=[0, np.sin(theta1_rad)], y=[0, np.cos(theta1_rad)], name="Rayo Reflejado", line=dict(dash='dash', color='#FFB800')))
        if sin_theta2 <= 1.0:
            fig.add_trace(go.Scatter(x=[0, np.sin(theta2_rad)], y=[0, -np.cos(theta2_rad)], name="Rayo Refractado", line=dict(width=3, color='#00FF85')))

        fig.update_layout(title="Simulación Óptica/Electromagnética del Choque de Onda", showlegend=True, height=400,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15, 23, 42, 0.5)')
        st.plotly_chart(fig)

# ==========================================
# MÓDULO 5: TIERRA CURVA Y LÍNEA DE VISTA
# ==========================================
elif modulo == "5. Onda de Espacio (Tierra Curva)":
    st.title("🌍 5. Propagación por Onda de Espacio (Efecto Tierra Curva)")

    st.markdown("### 📊 Infografía Digital del Eje Temático")
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("""
            <div style="background-color: rgba(0, 242, 255, 0.1); border-left: 5px solid #00F2FF; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00F2FF !important;">🌍 Horizonte Geométrico</h4>
                <p style="font-size: 14px; margin-bottom:0;">La curvatura geométrica real de la Tierra bloquea los rayos de radio directos, determinando un límite de visibilidad física para los radioenlaces terrestres.</p>
            </div>""", unsafe_allow_html=True)
    with info_col2:
        st.markdown("""
            <div style="background-color: rgba(255, 184, 0, 0.1); border-left: 5px solid #FFB800; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#FFB800 !important;">📡 Factor K</h4>
                <p style="font-size: 14px; margin-bottom:0;">La refracción atmosférica curva los rayos hacia abajo. Para simular el rayo recto, se define una Tierra ficticia modificada por el factor <b>k</b> (típicamente 4/3).</p>
            </div>""", unsafe_allow_html=True)
    with info_col3:
        st.markdown("""
            <div style="background-color: rgba(0, 255, 133, 0.1); border-left: 5px solid #00FF85; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00FF85 !important;">🧮 Alcance LOS</h4>
                <p style="font-size: 13px; margin-bottom:5px;">Cálculo de la Distancia Máxima Line of Sight:</p>
            </div>""", unsafe_allow_html=True)
        st.latex(r"d_{max} = \sqrt{17 \cdot k \cdot h_1} + \sqrt{17 \cdot k \cdot h_2} \quad [km]")

    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        h1 = st.slider("Altura Antena Transmisora h1 (m)", 1, 100, 30)
        h2 = st.slider("Altura Antena Receptora h2 (m)", 1, 100, 15)
        k_factor = st.selectbox("Factor de Tierra Ficticia (k)", [1.333, 1.0])
    with col2:
        d_max = np.sqrt(17 * k_factor * h1) + np.sqrt(17 * k_factor * h2)
        st.metric("Distancia Máxima de Línea de Vista (LOS)", f"{d_max:.2f} km")

        x_terra = np.linspace(-d_max, d_max, 100)
        y_terra = -(x_terra**2) / (2 * 6371 * k_factor)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_terra, y=y_terra, name="Curvatura Terrestre", fill='tozeroy', fillcolor='rgba(0, 242, 255, 0.1)'))
        fig.add_trace(go.Scatter(x=[-d_max/2, -d_max/2], y=[0, h1/1000], name="Tx", line=dict(width=5, color='#00FF85')))
        fig.add_trace(go.Scatter(x=[d_max/2, d_max/2], y=[0, h2/1000], name="Rx", line=dict(width=5, color='#FFB800')))

        fig.update_layout(title="Esquema de Enlace sobre Tierra Curva (Escala Exagerada)", xaxis_title="Distancia", yaxis_title="Altura Relativa",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15, 23, 42, 0.5)')
        st.plotly_chart(fig)

# ==========================================
# MÓDULO 6: LINK BUDGET
# ==========================================
elif modulo == "6. Presupuesto de Enlace (Link Budget)":
    st.title("📊 6. Cálculo de Propagación (Link Budget Completo)")

    st.markdown("### 📊 Infografía Digital del Eje Temático")
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("""
            <div style="background-color: rgba(0, 242, 255, 0.1); border-left: 5px solid #00F2FF; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00F2FF !important;">📈 Suma de Ganancias</h4>
                <p style="font-size: 14px; margin-bottom:0;">Suma la potencia de transmisión (dBm) más las eficiencias y ganancias electromagnéticas directivas enfocadas de las antenas Tx y Rx (dBi).</p>
            </div>""", unsafe_allow_html=True)
    with info_col2:
        st.markdown("""
            <div style="background-color: rgba(255, 184, 0, 0.1); border-left: 5px solid #FFB800; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#FFB800 !important;">📉 Resta de Pérdidas</h4>
                <p style="font-size: 14px; margin-bottom:0;">Contabiliza las pérdidas intrínsecas por atenuación en espacio libre (FSPL), pérdidas de inserción en conectores/cables, y márgenes por desvanecimiento.</p>
            </div>""", unsafe_allow_html=True)
    with info_col3:
        st.markdown("""
            <div style="background-color: rgba(0, 255, 133, 0.1); border-left: 5px solid #00FF85; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00FF85 !important;">🧮 Balance de Potencia</h4>
                <p style="font-size: 13px; margin-bottom:5px;">Ecuación general del balance de potencias:</p>
            </div>""", unsafe_allow_html=True)
        st.latex(r"P_{Rx} = P_{Tx} + G_{Tx} + G_{Rx} - FSPL - Pérdidas_{Extra}")

    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Parámetros del Sistema")
        ptx = st.number_input("Potencia de Transmisión (dBm)", value=20.0)
        gtx = st.number_input("Ganancia Antena Transmisora (dBi)", value=15.0)
        grx = st.number_input("Ganancia Antena Receptora (dBi)", value=15.0)
        sensibilidad = st.number_input("Sensibilidad del Receptor (dBm)", value=-85.0)

        st.subheader("Pérdidas")
        dist = st.slider("Distancia del Enlace (km)", 0.5, 30.0, 5.0, key="m6_d")
        frec = st.number_input("Frecuencia de Operación (MHz)", value=2400, key="m6_f")
        otras_perdidas = st.slider("Pérdidas por Cables/Obstáculos (dB)", 0, 20, 3)
    with col2:
        fspl_calc = 32.44 + 20*np.log10(dist) + 20*np.log10(frec)
        prx = ptx + gtx + grx - fspl_calc - otras_perdidas
        margen = prx - sensibilidad

        st.subheader("Resultado del Balance de Potencias")
        st.metric("Pérdida de Trayectoria (FSPL)", f"{fspl_calc:.2f} dB")
        st.metric("Potencia que llega al Receptor (Prx)", f"{prx:.2f} dBm")
        st.metric("Margen de Enlace", f"{margen:.2f} dB")

        if margen >= 0:
            st.success("🟢 ¡ENLACE VIABLE! La potencia recibida supera la sensibilidad del receptor.")
        else:
            st.error("🔴 ¡ENLACE INVIABLE! La señal se pierde en el camino y no llega con suficiente fuerza.")

# ==========================================
# MÓDULO 7: ANTENAS (EXPANDIDO CON 4 TIPOS)
# ==========================================
elif modulo == "7. Visualización de Antenas":
    st.title("📡 7. Diseño e Integración de Antenas (Vista Dual)")

    st.markdown("### 📊 Infografía Digital del Eje Temático")
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("""
            <div style="background-color: rgba(0, 242, 255, 0.1); border-left: 5px solid #00F2FF; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00F2FF !important;">📊 Plano Polar 2D</h4>
                <p style="font-size: 14px; margin-bottom:0;">Muestra el corte transversal de radiación (normalmente plano E o plano H), permitiendo medir los anchos de haz (HPBW) y lóbulos secundarios.</p>
            </div>""", unsafe_allow_html=True)
    with info_col2:
        st.markdown("""
            <div style="background-color: rgba(255, 184, 0, 0.1); border-left: 5px solid #FFB800; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#FFB800 !important;">🧊 Superficie 3D</h4>
                <p style="font-size: 14px; margin-bottom:0;">Representación espacial tridimensional completa que describe cómo viaja y se distribuye geométricamente la densidad de potencia irradiada al espacio.</p>
            </div>""", unsafe_allow_html=True)
    with info_col3:
        st.markdown("""
            <div style="background-color: rgba(0, 255, 133, 0.1); border-left: 5px solid #00FF85; padding: 15px; border-radius: 8px; min-height: 120px;">
                <h4 style="margin-top:0; color:#00FF85 !important;">🎯 Directividad</h4>
                <p style="font-size: 14px; margin-bottom:0;">Mide la propiedad de la antena de concentrar la energía en una dirección angular privilegiada en comparación con una antena isotrópica teórica.</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    tipo_antena = st.selectbox("Seleccione el Tipo de Antena:", [
        "Dipolo de Media Onda", 
        "Antena Parabólica Direccional",
        "Antena Yagi-Uda",
        "Arreglo de Fase (Phased Array)"
    ])

    # --- DESCRIPCIONES DETALLADAS DE LAS ANTENAS ---
    if tipo_antena == "Dipolo de Media Onda":
        st.markdown("""
        ### 🔹 Dipolo de Media Onda ($\lambda/2$)
        * **Descripción:** Es la antena lineal fundamental. Consiste en dos conductores alineados con una longitud eléctrica total igual a la mitad de la longitud de onda de operación.
        * **Comportamiento Electromagnético:** Presenta un patrón de radiación **omni-direccional** en el plano azimutal (forma de toroide o rosquilla en 3D). Posee ganancia máxima en el plano perpendicular al eje del conductor y nulos en los extremos directos del conductor (Eje Z).
        * **Uso Común:** Sistemas de radiodifusión FM, estaciones base de radio móvil terrestre de baja frecuencia y routers Wi-Fi.
        """)
    elif tipo_antena == "Antena Parabólica Direccional":
        st.markdown("""
        ### 🔹 Antena Parabólica Direccional
        * **Descripción:** Sistema reflector que concentra la energía electromagnética emitida por un iluminador primario situado en su foco óptico.
        * **Comportamiento Electromagnético:** Funciona colimando las ondas esféricas en un **haz plano, angosto y sumamente directivo**. Logra altas ganancias (dBi) minimizando la dispersión lateral de potencia.
        * **Uso Común:** Radioenlaces de microondas terrestres punto a punto a largas distancias, estaciones terrenas satelitales e instrumentación de radar.
        """)
    elif tipo_antena == "Antena Yagi-Uda":
        st.markdown("""
        ### 🔹 Antena Yagi-Uda
        * **Descripción:** Estructura direccional compuesta por elementos resonantes paralelos dispuestos sobre una pluma: un elemento excitador (dipolo alimentado), un reflector posterior largo y directores delanteros más cortos.
        * **Comportamiento Electromagnético:** Los elementos parásitos actúan por acoplamiento mutuo, reforzando los frentes de onda hacia adelante y cancelándolos en dirección opuesta, generando un haz frontal de directividad moderada con pequeños lóbulos menores traseros.
        * **Uso Común:** Recepción hogareña de televisión digital aérea terrestre (VHF/UHF), estaciones de radioaficionados y enlaces de datos punto a punto en zonas rurales.
        """)
    elif tipo_antena == "Arreglo de Fase (Phased Array)":
        st.markdown("""
        ### 🔹 Arreglo de Fase (Phased Array)
        * **Descripción:** Matriz planar/lineal constituida por múltiples antenas individuales idénticas sincronizadas, donde la fase relativa de alimentación de cada radiador se controla electrónicamente.
        * **Comportamiento Electromagnético:** El patrón total es el producto del elemento base y el factor de arreglo. Modificando progresivamente las fases se logra el **direccionamiento dinámico del haz (Beamforming)** sin realizar movimientos mecánicos del conjunto, exhibiendo crestas principales y nulos de interferencia destructiva controlables.
        * **Uso Común:** Estaciones base celulares avanzadas de tecnología 5G, radares militares de barrido electrónico (AESA) y terminales satelitales móviles de órbita baja.
        """)

    tab1, tab2 = st.tabs(["📊 Gráfico Polar 2D", "🧊 Modelado Espacial 3D"])

    # Vectores base del mallado computacional
    theta_2d = np.linspace(0, 2*np.pi, 500)
    t = np.linspace(0, np.pi, 60)
    p = np.linspace(0, 2*np.pi, 60)
    THETA, PHI = np.meshgrid(t, p)

    # --- MOTOR DE PROCESAMIENTO MATEMÁTICO ---
    if tipo_antena == "Dipolo de Media Onda":
        r_2d = np.abs(np.sin(theta_2d))
        R_3d = np.abs(np.sin(THETA))
    elif tipo_antena == "Antena Parabólica Direccional":
        r_2d = np.exp(-15 * (theta_2d - np.pi)**2) + 0.02
        R_3d = np.exp(-15 * ((THETA - np.pi/2)**2 + (PHI - np.pi)**2)) + 0.05
    elif tipo_antena == "Antena Yagi-Uda":
        r_2d = np.abs(np.cos(theta_2d - np.pi) * np.exp(-2 * (theta_2d - np.pi)**2)) + 0.04 * np.abs(np.cos(4*theta_2d))
        R_3d = np.abs(np.sin(THETA) * np.cos(PHI - np.pi) * np.exp(-1.5 * ((THETA - np.pi/2)**2 + (PHI - np.pi)**2))) + 0.04
    elif tipo_antena == "Arreglo de Fase (Phased Array)":
        r_2d = np.abs(np.sinc(4 * np.sin(theta_2d - np.pi)))
        R_3d = np.abs(np.sinc(3 * np.sin(THETA - np.pi/2)) * np.sinc(3 * np.cos(PHI)))

    # --- GRÁFICO POLAR 2D ---
    with tab1:
        fig_2d = go.Figure(data=go.Scatterpolar(
            r=r_2d, theta=np.degrees(theta_2d), mode='lines',
            line_color='#00F2FF', fill='toself', fillcolor='rgba(0, 242, 255, 0.2)'
        ))
        fig_2d.update_layout(
            polar=dict(radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.2)"),
                       angularaxis=dict(gridcolor="rgba(255,255,255,0.2)")),
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white")
        )
        st.plotly_chart(fig_2d, use_container_width=True)

    # --- MODELADO TRIDIMENSIONAL 3D ---
    with tab2:
        X = R_3d * np.sin(THETA) * np.cos(PHI)
        Y = R_3d * np.sin(THETA) * np.sin(PHI)
        Z = R_3d * np.cos(THETA)

        fig_3d = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict(title="Ganancia", tickfont=dict(color="white")))])
        fig_3d.update_layout(
            scene=dict(xaxis=dict(title='X', showbackground=False), yaxis=dict(title='Y', showbackground=False), zaxis=dict(title='Z', showbackground=False)),
            paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=0), height=600
        )
        st.plotly_chart(fig_3d, use_container_width=True)

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
            background-image: linear-gradient(rgba(15, 23, 42, 0.5), rgba(15, 23, 42, 0.5)),
                             url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* 2. Contenedores de elementos nativos */
        main .stMetric, main .stSlider, main .stNumberInput, main .stSelectbox, main .stExpander, main [data-testid="stMarkdownContainer"] {{
            background-color: rgba(15, 23, 42, 0.85) !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        /* 3. Forzar texto blanco global */
        h1, h2, h3, h4, p, span, label, div {{
            color: #FFFFFF !important;
        }}

        /* Ajuste para los gráficos */
        .js-plotly-plot .main-svg text {{
            fill: #FFFFFF !important;
        }}

        /* Clases de utilidad para las infografías en 4 cuadrantes */
        .info-card {{
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 15px;
            min-height: 250px;
            border: 2px solid;
        }}
        .card-title {{
            font-size: 18px;
            font-weight: bold;
            margin-top: 0px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            text-transform: uppercase;
        }}
        .card-body {{
            font-size: 14px;
            line-height: 1.5;
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
    st.subheader("Estudio Detallado de Fenómenos Electromagnéticos")
    st.markdown("""
    Bienvenid@, mi nombre es Laura Pérez, estudiante de Ingeniería de Telecomunicaciones. Esta herramienta está diseñada para procesar, calcular y graficar
    los fenómenos clave de las telecomunicaciones y la propagación de ondas electromagnéticas, integrando laboratorios analíticos interactivos y bases teóricas de alta fidelidad.

    ### Instrucciones:
    1. Usa el menú de la izquierda para navegar por los *7 ejes temáticos*.
    2. En cada módulo encontrarás una **Infografía Estructurada en 4 Cuadrantes** Basada en Modelos de Estudio Detallado (Concepto, Dependencias, Fórmulas y Casos de Uso) junto a su respectivo **Simulador en Tiempo Real**.
    """)
    st.info("💡 Desarrollado en Python utilizando Streamlit, Numpy y Plotly de forma nativa con inyección de layouts dinámicos en CSS.")

# ==========================================
# MÓDULO 1: ESPACIO LIBRE
# ==========================================
elif modulo == "1. Propagación en Espacio Libre":
    st.title("✨ 1.0 ESTUDIO DETALLADO: PROPAGACIÓN EN ESPACIO LIBRE (Friis)")
    st.markdown("### 📊 INFOGRAFÍA DINÁMICA DEL SISTEMA")
    
    # Fila 1 de la infografía (Concepto y Dependencias)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 150, 255, 0.1); border-color: #0096FF;">
                <div class="card-title" style="color: #0096FF !important;">📡 CONCEPTO</div>
                <div class="card-body">
                    <ul>
                        <li><b>Modelado de pérdidas:</b> Cuantifica la disminución de la densidad de potencia de la onda conforme viaja.</li>
                        <li><b>Medio Ideal:</b> Considera un vacío absoluto sin obstáculos, gases ni atenuación atmosférica.</li>
                        <li><b>Sin interferencias:</b> La señal se propaga de manera limpia desde una antena isotrópica teórica.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(255, 165, 0, 0.1); border-color: #FFA500;">
                <div class="card-title" style="color: #FFA500 !important;">⚠️ DEPENDENCIAS</div>
                <div class="card-body">
                    <p>La atenuación del trayecto en espacio libre (FSPL) es directamente proporcional a:</p>
                    <ul>
                        <li><b>Distancia al cuadrado:</b> Al duplicar la distancia, las pérdidas se cuadruplican.</li>
                        <li><b>Frecuencia al cuadrado:</b> Frecuencias más altas sufren mayor atenuación en la apertura del receptor.</li>
                    </ul>
                    <p style="text-align: center; font-weight: bold; margin-top: 10px; color: #FFA500 !important;">FSPL ∝ Distancia² y Frecuencia²</p>
                </div>
            </div>""", unsafe_allow_html=True)

    # Fila 2 de la infografía (Fórmula y Usos)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 200, 100, 0.1); border-color: #00C864;">
                <div class="card-title" style="color: #00C864 !important;">🧮 FÓRMULA MATEMÁTICA</div>
                <div class="card-body">
                    <p>Cálculo práctico de pérdidas en decibelios (dB):</p>
                </div>
            </div>""", unsafe_allow_html=True)
        st.latex(r"FSPL(dB) = 32.44 + 20\log_{10}(f_{MHz}) + 20\log_{10}(d_{km})")
    with c4:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(150, 0, 200, 0.1); border-color: #9600C8;">
                <div class="card-title" style="color: #9600C8 !important;">🚀 USOS Y APLICACIONES</div>
                <div class="card-body">
                    <ul>
                        <li><b>A. Enlace Satelital:</b> Análisis de trayectorias espaciales (Satélite a Tierra).</li>
                        <li><b>B. Telemetría Dron:</b> Conectividad LOS (Línea de vista) entre estaciones base y UAVs.</li>
                        <li><b>C. GPS / GNSS:</b> Recepción de señales de posicionamiento global desde órbitas MEO.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    # INTERFAZ DEL SIMULADOR
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables en Tiempo Real")
        f = st.slider("Frecuencia de Operación (MHz)", 100, 6000, 2400, key="m1_f")
        d = st.slider("Distancia del enlace (km)", 0.1, 50.0, 10.0, key="m1_d")
    with col2:
        fspl = 32.44 + 20*np.log10(d) + 20*np.log10(f)
        st.metric("Pérdida por Trayectoria Calculada (FSPL)", f"{fspl:.2f} dB")

        d_vector = np.linspace(0.1, 50, 100)
        fspl_vector = 32.44 + 20*np.log10(d_vector) + 20*np.log10(f)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d_vector, y=fspl_vector, name="FSPL", line=dict(color='#0096FF', width=3)))
        fig.update_layout(title="Curva Analítica de Pérdidas vs Distancia", xaxis_title="Distancia (km)", yaxis_title="Pérdidas (dB)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15, 23, 42, 0.5)')
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MÓDULO 2: ATENUACIÓN POR LLUVIA
# ==========================================
elif modulo == "2. Atenuación por Lluvia":
    st.title("🌧️ 2.0 ESTUDIO DETALLADO: ATENUACIÓN POR LLUVIA E HIDROMETEOROS")
    st.markdown("### 📊 INFOGRAFÍA DINÁMICA DEL SISTEMA")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 150, 255, 0.1); border-color: #0096FF;">
                <div class="card-title" style="color: #0096FF !important;">🌧️ CONCEPTO</div>
                <div class="card-body">
                    <ul>
                        <li><b>Absorción Electromagnética:</b> Las gotas de agua absorben energía resonante convirtiéndola en calor.</li>
                        <li><b>Dispersión de Energía:</b> Las ondas chocan con las gotas redirigiéndose en múltiples trayectorias no deseadas.</li>
                        <li><b>Efecto de Longitud de Onda:</b> Crítico en bandas de microondas y ondas milimétricas superiores a 10 GHz.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(255, 165, 0, 0.1); border-color: #FFA500;">
                <div class="card-title" style="color: #FFA500 !important;">⚠️ DEPENDENCIAS</div>
                <div class="card-body">
                    <ul>
                        <li><b>Tasa de Precipitación (R):</b> Volumen e intensidad de la lluvia medido en mm/h.</li>
                        <li><b>Coeficientes Geométricos (k, &alpha;):</b> Dependen de la frecuencia y la polarización de la antena (Horizontal/Vertical) regulados por la norma ITU-R P.838.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 200, 100, 0.1); border-color: #00C864;">
                <div class="card-title" style="color: #00C864 !important;">🧮 FÓRMULA MATEMÁTICA</div>
                <div class="card-body">
                    <p>Atenuación específica por kilómetro lineal:</p>
                </div>
            </div>""", unsafe_allow_html=True)
        st.latex(r"\gamma = k \cdot R^\alpha \quad [dB/km] \qquad A_{total} = \gamma \cdot d")
    with c4:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(150, 0, 200, 0.1); border-color: #9600C8;">
                <div class="card-title" style="color: #9600C8 !important;">🚀 USOS Y APLICACIONES</div>
                <div class="card-body">
                    <ul>
                        <li><b>A. Enlaces Troncales de Microondas:</b> Dimensionamiento de disponibilidad anual en bandas K/Ku.</li>
                        <li><b>B. Conectividad 5G:</b> Planeación de celdas pequeñas de ondas milimétricas (mmWave).</li>
                        <li><b>C. Televisión Satelital (DTH):</b> Cálculo del factor de caída de señal (Rain Fade).</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        r_lluvia = st.slider("Tasa de Lluvia Crítica (R en mm/h)", 0, 150, 50)
        dist_enlace = st.slider("Longitud expuesta del enlace (km)", 1.0, 20.0, 5.0)
    with col2:
        k, alpha = 0.22, 1.15
        atenuacion_especifica = k * (r_lluvia ** alpha)
        atenuacion_total = atenuacion_especifica * dist_enlace

        st.metric("Atenuación Específica Unitaria", f"{atenuacion_especifica:.2f} dB/km")
        st.metric("Degradación Total por Lluvia", f"{atenuacion_total:.2f} dB")

        r_vector = np.linspace(0, 150, 100)
        attn_vector = (k * (r_vector ** alpha)) * dist_enlace
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=r_vector, y=attn_vector, name="Atenuación", line=dict(color='#FFA500', width=3)))
        fig.update_layout(title="Pérdidas Totales en función de la Intensidad Pluviométrica", xaxis_title="Lluvia (mm/h)", yaxis_title="Pérdida Extra (dB)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15, 23, 42, 0.5)')
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MÓDULO 3: RUIDO TÉRMICO Y SNR
# ==========================================
elif modulo == "3. Ruido Térmico y SNR":
    st.title("🔊 3.0 ESTUDIO DETALLADO: RUIDO TÉRMICO Y SENSIBILIDAD")
    st.markdown("### 📊 INFOGRAFÍA DINÁMICA DEL SISTEMA")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 150, 255, 0.1); border-color: #0096FF;">
                <div class="card-title" style="color: #0096FF !important;">🌡️ CONCEPTO</div>
                <div class="card-body">
                    <ul>
                        <li><b>Ruido de Johnson-Nyquist:</b> Generado por la agitación estocástica de portadores de carga eléctrica.</li>
                        <li><b>Ruido Blanco:</b> Espectralmente uniforme, afecta por igual a todas las frecuencias del canal de comunicación.</li>
                        <li><b>Límite Físico Fundamental:</b> Dictamina el piso mínimo de potencia detectable en cualquier sistema receptor.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(255, 165, 0, 0.1); border-color: #FFA500;">
                <div class="card-title" style="color: #FFA500 !important;">⚠️ DEPENDENCIAS</div>
                <div class="card-body">
                    <p>La potencia del ruido térmico responde linealmente ante:</p>
                    <ul>
                        <li><b>Ancho de Banda (B):</b> Canales más anchos recolectan más potencia de ruido.</li>
                        <li><b>Temperatura Absoluta (T):</b> Mayor energía térmica molecular incrementa las fluctuaciones eléctricas.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 200, 100, 0.1); border-color: #00C864;">
                <div class="card-title" style="color: #00C864 !important;">🧮 FÓRMULA MATEMÁTICA</div>
                <div class="card-body">
                    <p>Potencia absoluta de ruido y conversión logarítmica (dBm):</p>
                </div>
            </div>""", unsafe_allow_html=True)
        st.latex(r"N = k \cdot T \cdot B \quad [W] \qquad N_{dBm} = -174 + 10\log_{10}(B_{Hz})")
    with c4:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(150, 0, 200, 0.1); border-color: #9600C8;">
                <div class="card-title" style="color: #9600C8 !important;">🚀 USOS Y APLICACIONES</div>
                <div class="card-body">
                    <ul>
                        <li><b>A. Redes LTE / 5G NR:</b> Establecimiento de los umbrales mínimos de recepción (Sensibilidad).</li>
                        <li><b>B. Receptores de Radar:</b> Optimización del amplificador de bajo ruido (LNA).</li>
                        <li><b>C. Radioastronomía:</b> Implementación de sistemas criogénicos para reducir el piso de ruido.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        bw_mhz = st.number_input("Ancho de Banda del Canal (MHz)", value=20.0)
        temp_c = st.slider("Temperatura de Operación de Circuitos (°C)", -20, 50, 25)
        f_ruido_db = st.slider("Factor de Ruido Intrínseco F (dB)", 0.0, 15.0, 4.0)
    with col2:
        k_boltz = 1.38e-23
        t_kelvin = temp_c + 273.15
        bw_hz = bw_mhz * 1e6

        n_watts = k_boltz * t_kelvin * bw_hz
        n_dbm = 10 * np.log10(n_watts / 1e-3)
        n_total_dbm = n_dbm + f_ruido_db

        st.metric("Piso de Ruido Térmico Ideal (N)", f"{n_dbm:.2f} dBm")
        st.metric("Piso de Ruido Total del Sistema (N + F)", f"{n_total_dbm:.2f} dBm")

# ==========================================
# MÓDULO 4: REFLEXIÓN Y SNELL
# ==========================================
elif modulo == "4. Reflexión y Ley de Snell":
    st.title("🪞 4.0 ESTUDIO DETALLADO: FENÓMENOS DE INTERFAZ Y LEY DE SNELL")
    st.markdown("### 📊 INFOGRAFÍA DINÁMICA DEL SISTEMA")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 150, 255, 0.1); border-color: #0096FF;">
                <div class="card-title" style="color: #0096FF !important;">🪞 CONCEPTO</div>
                <div class="card-body">
                    <ul>
                        <li><b>Cambio de Medio:</b> Modificación de la velocidad de fase de la onda electromagnética al cruzar fronteras físicas.</li>
                        <li><b>Rayo Reflejado:</b> Energía devuelta al medio original bajo el mismo ángulo de incidencia.</li>
                        <li><b>Rayo Refractado:</b> Energía desviada que penetra el nuevo medio variando su ángulo según los índices de refracción.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(255, 165, 0, 0.1); border-color: #FFA500;">
                <div class="card-title" style="color: #FFA500 !important;">⚠️ DEPENDENCIAS</div>
                <div class="card-body">
                    <ul>
                        <li><b>Índice de Refracción (n):</b> Razón entre la velocidad de la luz en el vacío y en el medio en estudio.</li>
                        <li><b>Ángulo de Incidencia (θ₁):</b> Geometría de choque de la onda con respecto a la línea normal de la superficie.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 200, 100, 0.1); border-color: #00C864;">
                <div class="card-title" style="color: #00C864 !important;">🧮 FÓRMULA MATEMÁTICA</div>
                <div class="card-body">
                    <p>Conservación del vector de onda en fronteras dieléctricas:</p>
                </div>
            </div>""", unsafe_allow_html=True)
        st.latex(r"n_1 \cdot \sin(\theta_1) = n_2 \cdot \sin(\theta_2)")
    with c4:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(150, 0, 200, 0.1); border-color: #9600C8;">
                <div class="card-title" style="color: #9600C8 !important;">🚀 USOS Y APLICACIONES</div>
                <div class="card-body">
                    <ul>
                        <li><b>A. Guiado en Fibra Óptica:</b> Confinamiento de luz mediante Reflexión Interna Total.</li>
                        <li><b>B. Propagación Ionosférica:</b> Reflexión de ondas de HF en las capas de la atmósfera superior.</li>
                        <li><b>C. Radares Geotécnicos (GPR):</b> Detección de capas terrestres por cambio dieléctrico.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables de Frontera")
        n1 = st.number_input("Índice Medio Emisor n1 (Aire = 1.0)", value=1.0)
        n2 = st.number_input("Índice Medio Receptor n2 (Suelo/Vidrio)", value=1.5)
        theta1 = st.slider("Ángulo de Incidencia Crítico θ₁ (Grados)", 0, 90, 30)
    with col2:
        theta1_rad = np.radians(theta1)
        sin_theta2 = (n1 * np.sin(theta1_rad)) / n2

        if sin_theta2 > 1.0:
            st.error("⚠️ REFLEXIÓN INTERNA TOTAL: La onda se refleja al 100%, sin penetración refractiva en el Medio 2.")
            theta2_rad = np.pi / 2
        else:
            theta2_rad = np.arcsin(sin_theta2)
            theta2 = np.degrees(theta2_rad)
            st.metric("Ángulo de Refracción Resultante (θ₂)", f"{theta2:.2f} °")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[-np.sin(theta1_rad), 0], y=[np.cos(theta1_rad), 0], name="Rayo Incidente", line=dict(width=3, color='#0096

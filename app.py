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
# MÓDULO: INTRODUCCIÓN
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
                </div>
            </div>""", unsafe_allow_html=True)

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
                        <li><b>C. GPS / GNSS:</b> Recepción de señales desde órbitas MEO.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
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
                        <li><b>Dispersión de Energía:</b> Las ondas chocan con las gotas redirigiéndose en múltiples trayectorias.</li>
                        <li><b>Efecto de Longitud de Onda:</b> Crítico en bandas superiores a 10 GHz (Microondas y mmWave).</li>
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
                        <li><b>Coeficientes Geométricos (k, &alpha;):</b> Dependen de la frecuencia y la polarización (ITU-R P.838).</li>
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
                        <li><b>A. Enlaces Troncales:</b> Dimensionamiento de disponibilidad en bandas K/Ku.</li>
                        <li><b>B. Conectividad 5G:</b> Planeación de celdas pequeñas de ondas milimétricas.</li>
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
                        <li><b>Ruido Blanco:</b> Espectralmente uniforme, afecta por igual a todas las frecuencias del canal.</li>
                        <li><b>Límite Físico Fundamental:</b> Dictamina el piso mínimo de potencia detectable.</li>
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
                        <li><b>Temperatura Absoluta (T):</b> Incrementa las fluctuaciones eléctricas moleculares.</li>
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
                        <li><b>C. Radioastronomía:</b> Implementación de sistemas criogénicos extremos.</li>
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
# MÓDULO 4: REFLEXIÓN Y SNELL (CORREGIDO)
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

        # Configuración del objeto de Plotly con indentación estricta a 8 espacios
        fig = go.Figure()

        # Rayo Incidente
        fig.add_trace(go.Scatter(
            x=[-np.sin(theta1_rad), 0],
            y=[np.cos(theta1_rad), 0],
            name="Rayo Incidente",
            line=dict(width=3, color='#0096FF')
        ))

        # Rayo Reflejado
        fig.add_trace(go.Scatter(
            x=[0, np.sin(theta1_rad)],
            y=[0, np.cos(theta1_rad)],
            name="Rayo Reflejado",
            line=dict(dash='dash', color='#FFA500')
        ))

        # Rayo Refractado
        if sin_theta2 <= 1.0:
            fig.add_trace(go.Scatter(
                x=[0, np.sin(theta2_rad)],
                y=[0, -np.cos(theta2_rad)],
                name="Rayo Refractado",
                line=dict(width=3, color='#00C864')
            ))

        fig.update_layout(
            title="Simulación Gráfica de Vector de Onda en Interfaz",
            showlegend=True,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 23, 42, 0.5)'
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MÓDULO 5: TIERRA CURVA Y LÍNEA DE VISTA
# ==========================================
elif modulo == "5. Onda de Espacio (Tierra Curva)":
    st.title("🌍 5.0 ESTUDIO DETALLADO: ONDA DE ESPACIO Y CURVATURA TERRESTRE")
    st.markdown("### 📊 INFOGRAFÍA DINÁMICA DEL SISTEMA")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 150, 255, 0.1); border-color: #0096FF;">
                <div class="card-title" style="color: #0096FF !important;">🌍 CONCEPTO</div>
                <div class="card-body">
                    <ul>
                        <li><b>Horizonte de Radio:</b> Distancia máxima donde el rayo electromagnético roza tangencialmente el relieve terrestre.</li>
                        <li><b>Onda de Espacio Directa:</b> Enlace punto a punto directo que viaja entre las estructuras aéreas de Tx y Rx.</li>
                        <li><b>Bloqueo Geométrico:</b> La convexidad natural del planeta obstruye físicamente trayectorias muy largas.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(255, 165, 0, 0.1); border-color: #FFA500;">
                <div class="card-title" style="color: #FFA500 !important;">⚠️ DEPENDENCIAS</div>
                <div class="card-body">
                    <ul>
                        <li><b>Alturas de Estructura (h₁, h₂):</b> Elevación física de los mástiles sobre el terreno plano.</li>
                        <li><b>Factor de Radio Equivalente (K):</b> Ajuste matemático de refracción troposférica estándar (K=4/3).</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 200, 100, 0.1); border-color: #00C864;">
                <div class="card-title" style="color: #00C864 !important;">🧮 FÓRMULA MATEMÁTICA</div>
                <div class="card-body">
                    <p>Rango de visibilidad LOS en Km considerando refracción atmosférica:</p>
                </div>
            </div>""", unsafe_allow_html=True)
        st.latex(r"d_{max} = \sqrt{17 \cdot k \cdot h_1} + \sqrt{17 \cdot k \cdot h_2} \quad [km]")
    with c4:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(150, 0, 200, 0.1); border-color: #9600C8;">
                <div class="card-title" style="color: #9600C8 !important;">🚀 USOS Y APLICACIONES</div>
                <div class="card-body">
                    <ul>
                        <li><b>A. Radioenlaces Terrestres VHF/UHF:</b> Cálculo de la viabilidad de trayectorias.</li>
                        <li><b>B. Despliegue de Radio Móvil:</b> Ubicación estratégica de torres de telefonía celular.</li>
                        <li><b>C. Sistemas de Navegación Aérea:</b> Cobertura de radar aeronáutico de aproximación.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        h1 = st.slider("Altura de Torre Transmisora h1 (m)", 1, 100, 30)
        h2 = st.slider("Altura de Torre Receptora h2 (m)", 1, 100, 15)
        k_factor = st.selectbox("Factor Atmosférico K (Tierra Estándar vs Vacío)", [1.333, 1.0])
    with col2:
        d_max = np.sqrt(17 * k_factor * h1) + np.sqrt(17 * k_factor * h2)
        st.metric("Límite de Distancia en Línea de Vista (LOS)", f"{d_max:.2f} km")

        x_terra = np.linspace(-d_max, d_max, 100)
        y_terra = -(x_terra**2) / (2 * 6371 * k_factor)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_terra, y=y_terra, name="Curvatura de Superficie", fill='tozeroy', fillcolor='rgba(0, 150, 255, 0.1)'))
        fig.add_trace(go.Scatter(x=[-d_max/2, -d_max/2], y=[0, h1/1000], name="Tx", line=dict(width=5, color='#00C864')))
        fig.add_trace(go.Scatter(x=[d_max/2, d_max/2], y=[0, h2/1000], name="Rx", line=dict(width=5, color='#FFA500')))

        fig.update_layout(title="Perfil del Enlace sobre la Curvatura Ficticia", xaxis_title="Distancia Horizontal", yaxis_title="Altura Relativa (km)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15, 23, 42, 0.5)')
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MÓDULO 6: LINK BUDGET
# ==========================================
elif modulo == "6. Presupuesto de Enlace (Link Budget)":
    st.title("📊 6.0 ESTUDIO DETALLADO: PRESUPUESTO DE ENLACE COMPLETO")
    st.markdown("### 📊 INFOGRAFÍA DINÁMICA DEL SISTEMA")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 150, 255, 0.1); border-color: #0096FF;">
                <div class="card-title" style="color: #0096FF !important;">📈 CONCEPTO</div>
                <div class="card-body">
                    <ul>
                        <li><b>Contabilidad de Potencia:</b> Balance logarítmico detallado de todas las ganancias y pérdidas presentes en el sistema.</li>
                        <li><b>Potencia Recibida (Prx):</b> Nivel neto de potencia real que incide sobre el decodificador receptor.</li>
                        <li><b>Margen de Desvanecimiento:</b> Colchón de seguridad para mitigar anomalías atmosféricas.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(255, 165, 0, 0.1); border-color: #FFA500;">
                <div class="card-title" style="color: #FFA500 !important;">⚠️ DEPENDENCIAS</div>
                <div class="card-body">
                    <ul>
                        <li><b>Ganancia de Antenas (Gt, Gr):</b> Eficiencia directiva electromagnética de los transductores.</li>
                        <li><b>Atenuación Estructural:</b> Pérdidas en cables, conectores tipo N/SMA y guías de onda.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 200, 100, 0.1); border-color: #00C864;">
                <div class="card-title" style="color: #00C864 !important;">🧮 FÓRMULA MATEMÁTICA</div>
                <div class="card-body">
                    <p>Ecuación matricial de Balance en Decibelios (dB/dBm):</p>
                </div>
            </div>""", unsafe_allow_html=True)
        st.latex(r"P_{Rx}(dBm) = P_{Tx} + G_{Tx} + G_{Rx} - FSPL - Pérdidas_{Lineas}")
    with c4:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(150, 0, 200, 0.1); border-color: #9600C8;">
                <div class="card-title" style="color: #9600C8 !important;">🚀 USOS Y APLICACIONES</div>
                <div class="card-body">
                    <ul>
                        <li><b>A. Diseño Punto a Punto:</b> Dimensionamiento comercial de enlaces de microondas.</li>
                        <li><b>B. Certificación de Cobertura:</b> Auditorías de red e ingeniería de preventa.</li>
                        <li><b>C. Auditorías Satelitales:</b> Verificación de disponibilidad de transpondedores.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Configuración RF")
        ptx = st.number_input("Potencia Inyectada Tx (dBm)", value=20.0)
        gtx = st.number_input("Ganancia de Antena de Transmisión (dBi)", value=15.0)
        grx = st.number_input("Ganancia de Antena de Recepción (dBi)", value=15.0)
        sensibilidad = st.number_input("Sensibilidad Límite del Umbral Receptor (dBm)", value=-85.0)

        st.subheader("Atenuaciones del Entorno")
        dist = st.slider("Distancia Total de Enlace (km)", 0.5, 30.0, 5.0, key="m6_d")
        frec = st.number_input("Frecuencia Central de Canal (MHz)", value=2400, key="m6_f")
        otras_perdidas = st.slider("Pérdidas de Conectores e Inserción (dB)", 0, 20, 3)
    with col2:
        fspl_calc = 32.44 + 20*np.log10(dist) + 20*np.log10(frec)
        prx = ptx + gtx + grx - fspl_calc - otras_perdidas
        margen = prx - sensibilidad

        st.subheader("Reporte Analítico del Enlace")
        st.metric("Pérdida de Trayectoria por Espacio Libre", f"{fspl_calc:.2f} dB")
        st.metric("Potencia Neta Recibida (Prx)", f"{prx:.2f} dBm")
        st.metric("Margen de Seguridad Operacional", f"{margen:.2f} dB")

        if margen >= 0:
            st.success("🟢 ¡ENLACE COMPATIBLE! El margen es positivo, asegurando resiliencia del canal.")
        else:
            st.error("🔴 ¡ENLACE FUERA DE RANGO! Pérdidas excesivas, la potencia recibida cae por debajo de la sensibilidad.")

# ==========================================
# MÓDULO 7: ANTENAS
# ==========================================
elif modulo == "7. Visualización de Antenas":
    st.title("📡 7.0 ESTUDIO DETALLADO: INTEGRACIÓN Y PATRONES DE RADIACIÓN")
    st.markdown("### 📊 INFOGRAFÍA DINÁMICA DEL SISTEMA")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 150, 255, 0.1); border-color: #0096FF;">
                <div class="card-title" style="color: #0096FF !important;">📡 CONCEPTO</div>
                <div class="card-body">
                    <ul>
                        <li><b>Patrón de Radiación:</b> Gráfica de la distribución relativa de la potencia irradiada en función de las coordenadas angulares.</li>
                        <li><b>Directividad y Ganancia:</b> Capacidad física de focalizar la energía en direcciones preferenciales.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(255, 165, 0, 0.1); border-color: #FFA500;">
                <div class="card-title" style="color: #FFA500 !important;">⚠️ DEPENDENCIAS</div>
                <div class="card-body">
                    <ul>
                        <li><b>Geometría Estructural:</b> La forma de los conductores e iluminadores altera físicamente los frentes de onda.</li>
                        <li><b>Fase Eléctrica:</b> La temporización de las señales genera interferencias constructivas o destructivas controladas.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(0, 200, 100, 0.1); border-color: #00C864;">
                <div class="card-title" style="color: #00C864 !important;">🧮 BASE MATEMÁTICA</div>
                <div class="card-body">
                    <p>Ecuación electromagnética de campo para arreglos y dipolos fundamentales:</p>
                </div>
            </div>""", unsafe_allow_html=True)
        st.latex(r"E(\theta) = \cos\left(\frac{\pi}{2}\cos\theta\right)\Big/\sin\theta \qquad AF(\theta) = \sum_{n=1}^{N} e^{j n (k d \cos\theta + \beta)}")
    with c4:
        st.markdown("""
            <div class="info-card" style="background-color: rgba(150, 0, 200, 0.1); border-color: #9600C8;">
                <div class="card-title" style="color: #9600C8 !important;">🚀 USOS Y APLICACIONES</div>
                <div class="card-body">
                    <ul>
                        <li><b>A. Redes Móviles 5G:</b> Beamforming activo por arreglos de fase avanzados.</li>
                        <li><b>B. Sistemas de Radar:</b> Conmutación de haces electrónicos ultrarrápidos sin partes móviles.</li>
                        <li><b>C. Redes de Distribución:</b> Cobertura de amplio rango sectorial y enlaces dedicados.</li>
                    </ul>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    tipo_antena = st.selectbox("Seleccione el Tipo de Antena a Modelar:", [
        "Dipolo de Media Onda", 
        "Antena Parabólica Direccional",
        "Antena Yagi-Uda",
        "Arreglo de Fase (Phased Array)"
    ])

    if tipo_antena == "Dipolo de Media Onda":
        st.markdown("""
        ### 🔹 Dipolo de Media Onda ($\lambda/2$)
        * **Geometría:** Estructura lineal elemental simétrica cortada exactamente a la mitad de la longitud de onda de resonancia del canal.
        * **Campos E/H:** Genera una distribución toroidal simétrica perfecta. Máxima densidad perpendicular al eje metálico, nulos axiales completos.
        * **Aplicaciones Reales:** Estaciones de radiodifusión FM, pasarelas de baja frecuencia industriales y antenas Wi-Fi estándar de routers de consumo.
        """)
    elif tipo_antena == "Antena Parabólica Direccional":
        st.markdown("""
        ### 🔹 Antena Parabólica Direccional
        * **Geometría:** Reflector parabólico con un iluminador activo (bocina) fijado precisamente en el punto focal óptico.
        * **Campos E/H:** Colima frentes de onda esféricos en un haz de rayos paralelos angostos de alta coherence. Logra ganancias colosales superiores a 30 dBi.
        * **Aplicaciones Reales:** Estaciones terrestres de comunicación satelital profunda, radioenlaces de microondas de alta capacidad de transporte.
        """)
    elif tipo_antena == "Antena Yagi-Uda":
        st.markdown("""
        ### 🔹 Antena Yagi-Uda
        * **Geometría:** Arreglo en línea sobre una pluma común: un reflector trasero (más largo), un dipolo excitador alimentado y múltiples directores delanteros (más cortos).
        * **Campos E/H:** Acoplamiento mutuo de ondas parásitas que cancela la radiación posterior e incrementa la directividad frontal en un haz moderado.
        * **Aplicaciones Reales:** Captación de televisión digital aérea abierta terrestre (VHF/UHF) y redes de radioaficionados de baja potencia.
        """)
    elif tipo_antena == "Arreglo de Fase (Phased Array)":
        st.markdown("""
        ### 🔹 Arreglo de Fase (Phased Array)
        * **Geometría:** Matriz planar integrada por múltiples antenas individuales idénticas alimentadas de forma independiente mediante desfasadores electrónicos digitales.
        * **Campos E/H:** Interferencia constructiva programable en tiempo real. Permite apuntar el lóbulo principal (Beamforming) electrónicamente en microsegundos.
        * **Aplicaciones Reales:** Sistemas avanzados MIMO masivos de estaciones base 5G y radares militares de escaneo electrónico síncrono.
        """)

    tab1, tab2 = st.tabs(["📊 Patrón de Radiación Polar 2D", "🧊 Representación Espacial 3D"])

    theta_2d = np.linspace(0, 2*np.pi, 500)
    t = np.linspace(0, np.pi, 60)
    p = np.linspace(0, 2*np.pi, 60)
    THETA, PHI = np.meshgrid(t, p)

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

    with tab1:
        fig_2d = go.Figure(data=go.Scatterpolar(
            r=r_2d, theta=np.degrees(theta_2d), mode='lines',
            line_color='#0096FF', fill='toself', fillcolor='rgba(0, 150, 255, 0.2)'
        ))
        fig_2d.update_layout(
            polar=dict(radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.2)"),
                       angularaxis=dict(gridcolor="rgba(255,255,255,0.2)")),
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white")
        )
        st.plotly_chart(fig_2d, use_container_width=True)

    with tab2:
        X = R_3d * np.sin(THETA) * np.cos(PHI)
        Y = R_3d * np.sin(THETA) * np.sin(PHI)
        Z = R_3d * np.cos(THETA)

        fig_3d = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict(title="Ganancia Relativa", tickfont=dict(color="white")))])
        fig_3d.update_layout(
            scene=dict(xaxis=dict(title='Eje X', showbackground=False), yaxis=dict(title='Eje Y', showbackground=False), zaxis=dict(title='Eje Z', showbackground=False)),
            paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=0), height=600
        )
        st.plotly_chart(fig_3d, use_container_width=True)

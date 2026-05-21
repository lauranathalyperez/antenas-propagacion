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
        /* 1. Fondo con la capa negra muy suave (solo 0.4 de opacidad) para que la IA se vea clara */
        .stApp {{
            background-image: linear-gradient(rgba(15, 23, 42, 0.4), rgba(15, 23, 42, 0.4)), 
                             url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* 2. El TRUCO: Contenedores con fondo oscuro sólido para proteger la lectura del texto */
        .stMetric, .stSlider, .stNumberInput, .stSelectbox, .stExpander, [data-testid="stMarkdownContainer"] {{
            background-color: rgba(15, 23, 42, 0.85) !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        /* 3. Forzar texto blanco dentro de los bloques de contenido */
        h1, h2, h3, p, span, label, div {{
            color: #FFFFFF !important;
        }}
        
        /* Ajuste para que los textos de los gráficos no se dañen */
        .js-plotly-plot .main-svg text {{
            fill: #FFFFFF !important;
        }}
        </style>
        """
        st.markdown(css_fondo, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"⚠️ No se encontró el archivo '{archivo_imagen}'. Asegúrate de guardarlo en la misma carpeta.")

# Llamamos a la función
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
    2. En cada módulo encontrarás una pestaña *Educativa* (Teoría y Fórmulas) y un *Simulador* con variables en tiempo real.
    """)
    st.info("💡 Desarrollado en Python utilizando Streamlit, Numpy y Plotly de forma nativa.")

# ==========================================
# MÓDULO 1: ESPACIO LIBRE
# ==========================================
elif modulo == "1. Propagación en Espacio Libre":
    st.title("✨ 1. Propagación en Espacio Libre (Friis)")
    
    with st.expander("📖 Módulo Educativo: Fundamento Teórico"):
        st.write("El modelo de pérdidas en espacio libre (FSPL) asume una antena isotrópica radiando en un ambiente ideal sin obstáculos.")
        st.latex(r"FSPL (dB) = 32.44 + 20\log_{10}(d_{km}) + 20\log_{10}(f_{MHz})")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        f = st.slider("Frecuencia (MHz)", 100, 6000, 2400, key="m1_f")
        d = st.slider("Distancia del enlace (km)", 0.1, 50.0, 10.0, key="m1_d")
    with col2:
        fspl = 32.44 + 20*np.log10(d) + 20*np.log10(f)
        st.metric("Pérdida por Trayectoria (FSPL)", f"{fspl:.2f} dB")
        
        # Gráfica
        d_vector = np.linspace(0.1, 50, 100)
        fspl_vector = 32.44 + 20*np.log10(d_vector) + 20*np.log10(f)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d_vector, y=fspl_vector, name="FSPL"))
        fig.update_layout(title="Pérdidas vs Distancia", xaxis_title="Distancia (km)", yaxis_title="Pérdidas (dB)")
        st.plotly_chart(fig)

# ==========================================
# MÓDULO 2: ATENUACIÓN POR LLUVIA
# ==========================================
elif modulo == "2. Atenuación por Lluvia":
    st.title("🌧️ 2. Atenuación por Lluvia e Hidrometeoro")
    
    with st.expander("📖 Módulo Educativo: Fundamento Teórico"):
        st.write("A frecuencias altas (mayores a 10 GHz), las gotas de lluvia absorben y dispersan la energía de la onda.")
        st.latex(r"\gamma = k \cdot R^\alpha \quad [dB/km]")
        st.caption("Donde R es la tasa de lluvia en mm/h, y k, alpha dependen de la frecuencia.")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        r_lluvia = st.slider("Tasa de lluvia (R en mm/h)", 0, 150, 50)
        dist_enlace = st.slider("Distancia afectada (km)", 1.0, 20.0, 5.0)
    with col2:
        # Valores simplificados de la ITU para 28 GHz (Banda Ka)
        k, alpha = 0.22, 1.15
        atenuacion_especifica = k * (r_lluvia ** alpha)
        atenuacion_total = atenuacion_especifica * dist_enlace
        
        st.metric("Atenuación Específica", f"{atenuacion_especifica:.2f} dB/km")
        st.metric("Pérdida Total por Lluvia", f"{atenuacion_total:.2f} dB")
        
        # Gráfica de impacto
        r_vector = np.linspace(0, 150, 100)
        attn_vector = (k * (r_vector ** alpha)) * dist_enlace
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=r_vector, y=attn_vector, name="Atenuación", line=dict(color='blue')))
        fig.update_layout(title="Pérdida total vs Intensidad de Lluvia", xaxis_title="Lluvia (mm/h)", yaxis_title="Pérdida Extra (dB)")
        st.plotly_chart(fig)

# ==========================================
# MÓDULO 3: RUIDO TÉRMICO Y SNR
# ==========================================
elif modulo == "3. Ruido Térmico y SNR":
    st.title("🔊 3. Ruido Térmico y Factor de Ruido")
    
    with st.expander("📖 Módulo Educativo: Fundamento Teórico"):
        st.write("El ruido térmico o ruido de Johnson-Nyquist es inevitable debido a la agitación de electrones.")
        st.latex(r"N = k \cdot T \cdot B \quad [Watts]")
        st.write("Donde $k = 1.38 \times 10^{-23}$ J/K, $T$ es temperatura en Kelvin y $B$ es Ancho de Banda en Hz.")

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
        
        # Potencia de ruido en Watts y luego en dBm
        n_watts = k_boltz * t_kelvin * bw_hz
        n_dbm = 10 * np.log10(n_watts / 1e-3)
        n_total_dbm = n_dbm + f_ruido_db
        
        st.metric("Piso de Ruido Térmico Puro (N)", f"{n_dbm:.2f} dBm")
        st.metric("Ruido Total del Sistema (con Factor F)", f"{n_total_dbm:.2f} dBm")
        st.info("A mayor ancho de banda o temperatura, el receptor 'escuchará' más ruido, dificultando la recepción.")
# ==========================================
# MÓDULO 4: REFLEXIÓN Y SNELL
# ==========================================
elif modulo == "4. Reflexión y Ley de Snell":
    st.title("🪞 4. Reflexión y Refracción (Leyes de Snell)")
    
    with st.expander("📖 Módulo Educativo: Fundamento Teórico"):
        st.write("Cuando una onda cambia de medio, una parte se refleja (rebota) y otra se refracta (se transmite desviándose).")
        st.latex(r"n_1 \cdot \sin(\theta_1) = n_2 \cdot \sin(\theta_2)")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        n1 = st.number_input("Índice Medio 1 (Ej: Aire = 1.0)", value=1.0)
        n2 = st.number_input("Índice Medio 2 (Ej: Suelo/Agua)", value=1.5)
        theta1 = st.slider("Ángulo de Incidencia (Grados)", 0, 90, 30)
    with col2:
        # Cálculo de Snell en radianes
        theta1_rad = np.radians(theta1)
        sin_theta2 = (n1 * np.sin(theta1_rad)) / n2
        
        if sin_theta2 > 1.0:
            st.error("⚠️ Reflexión Interna Total: ¡La onda no pasa al Medio 2, se refleja por completo!")
            theta2 = 90
        else:
            theta2_rad = np.arcsin(sin_theta2)
            theta2 = np.degrees(theta2_rad)
            st.metric("Ángulo de Refracción calculado (θ₂)", f"{theta2:.2f} °")
        
        # Simulación Gráfica de los Rayos 2D
        fig = go.Figure()
        # Medio 1 e Incidente
        fig.add_trace(go.Scatter(x=[-np.sin(theta1_rad), 0], y=[np.cos(theta1_rad), 0], name="Rayo Incidente", line=dict(width=3)))
        # Rayo Reflejado
        fig.add_trace(go.Scatter(x=[0, np.sin(theta1_rad)], y=[0, np.cos(theta1_rad)], name="Rayo Reflejado", line=dict(dash='dash')))
        # Rayo Refractado (si no hay reflexión total)
        if sin_theta2 <= 1.0:
            fig.add_trace(go.Scatter(x=[0, np.sin(theta2_rad)], y=[0, -np.cos(theta2_rad)], name="Rayo Refractado", line=dict(width=3)))
            
        fig.update_layout(title="Simulación Óptica/Electromagnética del Choque de Onda", showlegend=True, height=400)
        st.plotly_chart(fig)
# ==========================================
# MÓDULO 5: TIERRA CURVA Y LÍNEA DE VISTA
# ==========================================
elif modulo == "5. Onda de Espacio (Tierra Curva)":
    st.title("🌍 5. Propagación por Onda de Espacio (Efecto Tierra Curva)")
    
    with st.expander("📖 Módulo Educativo: Fundamento Teórico"):
        st.write("Debido a la curvatura de la Tierra, las antenas deben tener una altura mínima para poder 'verse'.")
        st.latex(r"d_{max} = \sqrt{17 \cdot k \cdot h_1} + \sqrt{17 \cdot k \cdot h_2} \quad [km]")
        st.caption("Donde h1 y h2 son las alturas en metros, y k es el factor de modificación del radio terrestre (típicamente 4/3).")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables")
        h1 = st.slider("Altura Antena Transmisora h1 (m)", 1, 100, 30)
        h2 = st.slider("Altura Antena Receptora h2 (m)", 1, 100, 15)
        k_factor = st.selectbox("Factor de Tierra Ficticia (k)", [1.333, 1.0])
    with col2:
        d_max = np.sqrt(17 * k_factor * h1) + np.sqrt(17 * k_factor * h2)
        st.metric("Distancia Máxima de Línea de Vista (LOS)", f"{d_max:.2f} km")
        
        # Dibujo de curvatura terrestre interactiva
        x_terra = np.linspace(-d_max, d_max, 100)
        # Aproximación de arco para graficación
        y_terra = -(x_terra**2) / (2 * 6371 * k_factor) 
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_terra, y=y_terra, name="Curvatura Terrestre", fill='tozeroy'))
        # Marcar Antenas
        fig.add_trace(go.Scatter(x=[-d_max/2, -d_max/2], y=[0, h1/1000], name="Tx", line=dict(width=5)))
        fig.add_trace(go.Scatter(x=[d_max/2, d_max/2], y=[0, h2/1000], name="Rx", line=dict(width=5)))
        
        fig.update_layout(title="Esquema de Enlace sobre Tierra Curva (Escala Exagerada)", xaxis_title="Distancia", yaxis_title="Altura Relativa")
        st.plotly_chart(fig)
# ==========================================
# MÓDULO 6: LINK BUDGET
# ==========================================
elif modulo == "6. Presupuesto de Enlace (Link Budget)":
    st.title("📊 6. Cálculo de Propagación (Link Budget Completo)")
    
    with st.expander("📖 Módulo Educativo: Fundamento Teórico"):
        st.write("El presupuesto de enlace reúne todas las ganancias y pérdidas desde el transmisor hasta el receptor.")
        st.latex(r"P_{Rx} = P_{Tx} + G_{Tx} + G_{Rx} - FSPL - Atenuaciones_{Extra}")

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
        # Operación matemática del Motor de Cálculo
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
# MÓDULO 7: ANTENAS (VISTA DUAL 2D Y 3D)
# ==========================================
elif modulo == "7. Visualización de Antenas":
    st.title("📡 7. Diseño e Integración de Antenas (Vista Dual)")
    
    with st.expander("📖 Módulo Educativo: Fundamento Teórico"):
        st.write("El análisis de antenas se realiza en dos planos principales:")
        st.write("- **Vista 2D (Polar):** Muestra el corte transversal del haz.")
        st.write("- **Vista 3D (Espacial):** Muestra cómo se distribuye la energía en todo el espacio real.")

    tipo_antena = st.selectbox("Seleccione el Tipo de Antena:", ["Dipolo de Media Onda", "Antena Parabólica Direccional"])

    tab1, tab2 = st.tabs(["📊 Gráfico Polar 2D", "🧊 Modelado Espacial 3D"])

    theta_2d = np.linspace(0, 2*np.pi, 500)
    t = np.linspace(0, np.pi, 60)
    p = np.linspace(0, 2*np.pi, 60)
    THETA, PHI = np.meshgrid(t, p)

    if tipo_antena == "Dipolo de Media Onda":
        r_2d = np.abs(np.sin(theta_2d))
        R_3d = np.abs(np.sin(THETA))
        descripcion = "El dipolo radia energía perpendicularmente a su eje, creando un patrón omnidireccional en el plano horizontal."
    else:
        r_2d = np.exp(-15 * (theta_2d - np.pi)**2) + 0.02
        R_3d = np.exp(-15 * ((THETA - np.pi/2)**2 + (PHI - np.pi)**2)) + 0.05
        descripcion = "La parábola concentra la energía en un haz muy fino para radioenlaces de larga distancia."

    with tab1:
        st.write(f"**Análisis de Corte Transversal:** {descripcion}")
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

    with tab2:
        st.write("**Análisis Volumétrico:** Rota el gráfico para explorar el lóbulo principal.")
        X = R_3d * np.sin(THETA) * np.cos(PHI)
        Y = R_3d * np.sin(THETA) * np.sin(PHI)
        Z = R_3d * np.cos(THETA)

        fig_3d = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict(title="Ganancia", tickfont=dict(color="white")))])
        fig_3d.update_layout(
            scene=dict(xaxis=dict(title='X', showbackground=False), yaxis=dict(title='Y', showbackground=False), zaxis=dict(title='Z', showbackground=False)),
            paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=0), height=600
        )
        st.plotly_chart(fig_3d, use_container_width=True)

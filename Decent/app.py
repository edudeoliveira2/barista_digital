import streamlit as st
import json
from datetime import datetime
from ristretto_engine import RistrettoEngine

# Configuração da página
st.set_page_config(page_title="Ristretto Engine", layout="centered")
st.title("☕ Ristretto Engine v1.5 – Registro de Extração com Feedback")

# Instancia o motor
engine = RistrettoEngine()
setup = engine.load_user_setup()

# Campos sensoriais + técnicos
st.subheader("🎯 Perfil Sensorial Desejado")
desired_profile = st.text_input("Descreva o perfil desejado (ex: doce com final prolongado)")

st.subheader("🔧 Setup da Extração")
method = st.selectbox("Método de preparo", setup.get("methods", []))
equipment = st.selectbox("Equipamento", setup.get("equipment", []))
grinder = st.selectbox("Moedor", setup.get("grinders", []))
burr = st.selectbox("Rebarba ativa", setup.get("burrs", []))

st.subheader("📋 Dados Técnicos")
coffee_name = st.text_input("Nome do café")
origin = st.text_input("Origem / Variedade / Processamento (opcional)")
roast = st.selectbox("Tipo de torra", ["Clara", "Média", "Escura"])
dose = st.number_input("Dose (g)", min_value=0.0, step=0.1)
basket = st.text_input("Cesto (se aplicável)")
ambient_temp = st.number_input("Temperatura ambiente (°C)", step=0.5)
time_of_day = st.selectbox("Hora do dia", ["Manhã", "Tarde", "Noite"])

st.subheader("🔄 Etapas da Extração")
extraction_steps = st.text_area("Descreva as etapas com tempo / fluxo / pressão / temp")

st.subheader("✅ Após a Extração")
total_time = st.number_input("Tempo total (s)", min_value=0.0)
yield_weight = st.number_input("Rendimento final (g)", min_value=0.0)
perceived_notes = st.text_input("Notas sensoriais percebidas (ex: chocolate, frutas amarelas)")
descriptive_notes = st.text_input("Notas descritivas")
satisfaction = st.slider("Grau de satisfação (1 = ruim / 10 = excelente)", 1, 10, 7)
observations = st.text_area("Observações pessoais")

# Botão de salvar
if st.button("💾 Registrar extração"):
    extraction_data = {
        "timestamp": datetime.now().isoformat(),
        "desired_profile": desired_profile,
        "method": method,
        "equipment": equipment,
        "grinder": grinder,
        "burr": burr,
        "coffee_name": coffee_name,
        "origin": origin,
        "roast": roast,
        "dose": dose,
        "basket": basket,
        "ambient_temp": ambient_temp,
        "time_of_day": time_of_day,
        "extraction_steps": extraction_steps,
        "total_time": total_time,
        "yield": yield_weight,
        "perceived_notes": perceived_notes,
        "descriptive_notes": descriptive_notes,
        "satisfaction": satisfaction,
        "observations": observations
    }

    # Salvar no arquivo JSON
    try:
        with open("extractions_data.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    history.append(extraction_data)

    with open("extractions_data.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    st.success("Extração registrada com sucesso! ☕📝")

    if satisfaction < 7:
        st.warning("Essa extração será marcada como 'aprendizado negativo' para ajustar sugestões futuras. 🧠")

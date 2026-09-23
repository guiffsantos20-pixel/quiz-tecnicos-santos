import streamlit as st
import unicodedata
import time

st.set_page_config(page_title="Quiz dos Técnicos do Santos", page_icon="🐳", layout="centered")

def normalizar_texto(texto):
    if not texto: return ""
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.lower().strip()

st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-color: #000000;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    .acerto-box, .falta-box {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        display: flex; 
        align-items: center; 
        font-weight: 500;
    }
    .acerto-box {
        background-color: #e6f4ea;
        color: #137333;
        border: 1px solid #ceead6;
    }
    .falta-box {
        background-color: #f1f3f4;
        color: #5f6368;
        border: 1px dashed #bdc1c6;
    }
    .tipo-tecnico {
        font-weight: 600;
        margin-right: 8px;
        background: #e2e8f0;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        color: #1e293b;
        white-space: nowrap;
    }
    .timer-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #d32f2f;
        text-align: center;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

tecnicos = [
    {"nome": "Giba", "tipo": "Técnico brasileiro"},
    {"nome": "Carlos Alberto Parreira", "tipo": "Técnico brasileiro"},
    {"nome": "Geninho", "tipo": "Técnico brasileiro"},
    {"nome": "Serginho Chulapa", "tipo": "Técnico brasileiro"},
    {"nome": "Cabralzinho", "tipo": "Técnico brasileiro"},
    {"nome": "Celso Roth", "tipo": "Técnico brasileiro"},
    {"nome": "Emerson Leão", "tipo": "Técnico brasileiro"},
    {"nome": "Vanderlei Luxemburgo", "tipo": "Técnico brasileiro"},
    {"nome": "Oswaldo de Oliveira", "tipo": "Técnico brasileiro"},
    {"nome": "Alexandre Gallo", "tipo": "Técnico brasileiro"},
    {"nome": "Nelsinho Baptista", "tipo": "Técnico brasileiro"},
    {"nome": "Cuca", "tipo": "Técnico brasileiro"},
    {"nome": "Márcio Fernandes", "tipo": "Técnico brasileiro"},
    {"nome": "Vagner Mancini", "tipo": "Técnico brasileiro"},
    {"nome": "Dorival Júnior", "tipo": "Técnico brasileiro"},
    {"nome": "Adílson Batista", "tipo": "Técnico brasileiro"},
    {"nome": "Muricy Ramalho", "tipo": "Técnico brasileiro"},
    {"nome": "Claudinei Oliveira", "tipo": "Técnico brasileiro"},
    {"nome": "Enderson Moreira", "tipo": "Técnico brasileiro"},
    {"nome": "Levir Culpi", "tipo": "Técnico brasileiro"},
    {"nome": "Jair Ventura", "tipo": "Técnico brasileiro"},
    {"nome": "Jorge Sampaoli", "tipo": "Técnico argentino"},
    {"nome": "Jesualdo Ferreira", "tipo": "Técnico português"},
    {"nome": "Fernando Diniz", "tipo": "Técnico brasileiro"},
    {"nome": "Fábio Carille", "tipo": "Técnico brasileiro"},
    {"nome": "Fabián Bustos", "tipo": "Técnico argentino"},
    {"nome": "Lisca", "tipo": "Técnico brasileiro"},
    {"nome": "Odair Hellmann", "tipo": "Técnico brasileiro"},
    {"nome": "Paulo Turra", "tipo": "Técnico brasileiro"},
    {"nome": "Diego Aguirre", "tipo": "Técnico uruguaio"},
    {"nome": "Pedro Caixinha", "tipo": "Técnico português"},
    {"nome": "Cléber Xavier", "tipo": "Técnico brasileiro"},
    {"nome": "Juan Pablo Vojvoda", "tipo": "Técnico argentino"}
]

if 'acertos' not in st.session_state:
    st.session_state.acertos = []
if 'jogo_iniciado' not in st.session_state:
    st.session_state.jogo_iniciado = False
if 'jogo_terminado' not in st.session_state:
    st.session_state.jogo_terminado = False
if 'input_palpite' not in st.session_state:
    st.session_state.input_palpite = ""

def processar_palpite():
    palpite = st.session_state.input_palpite
    palpite_norm = normalizar_texto(palpite)
    
    if not palpite_norm:
        return

    for tecnico in tecnicos:
        nome_tecnico = tecnico["nome"]
        nome_norm = normalizar_texto(nome_tecnico)
        
       
        palavras_nome = nome_norm.split()
        
    
        if (palpite_norm == nome_norm) or (palpite_norm in palavras_nome):
            if nome_tecnico not in st.session_state.acertos:
                st.session_state.acertos.append(nome_tecnico)
                st.toast(f'Acertou: {nome_tecnico}!', icon='✅')
                
                if len(st.session_state.acertos) == len(tecnicos):
                     st.session_state.jogo_terminado = True
                     st.session_state.venceu = True
                break
                
    st.session_state.input_palpite = ""

TEMPO_LIMITE_SEGUNDOS = 900 

st.title("🐳 Quiz dos Técnicos do Peixão")
st.markdown("**Desafio:** Adivinhe todos os técnicos (efetivos) que comandaram o Santos de **2000 a 2026**!")

if not st.session_state.jogo_iniciado and not st.session_state.jogo_terminado:
    if st.button("▶️ Iniciar Jogo", use_container_width=True):
        st.session_state.jogo_iniciado = True
        st.session_state.tempo_inicio = time.time()
        st.rerun()

if st.session_state.jogo_iniciado and not st.session_state.jogo_terminado:
    
    timer_placeholder = st.empty()
    
    st.text_input("Nome do técnico:", key="input_palpite", on_change=processar_palpite)

    col_stats1, col_stats2 = st.columns(2)
    with col_stats1:
        st.metric(label="Acertos", value=f"{len(st.session_state.acertos)} / {len(tecnicos)}")
    with col_stats2:
        progresso = len(st.session_state.acertos) / len(tecnicos)
        st.progress(progresso)

    st.markdown("---")

    col1, col2 = st.columns(2)
    for i, tecnico in enumerate(tecnicos):
        nome = tecnico["nome"]
        tipo = tecnico["tipo"]
        caixa_tipo = f'<span class="tipo-tecnico">{tipo}</span>'
        
        if nome in st.session_state.acertos:
            html_mostrar = f'<div class="acerto-box">{caixa_tipo} <b>{nome}</b></div>'
        else:
            html_mostrar = f'<div class="falta-box">{caixa_tipo} ____________________</div>'
            
        if i % 2 == 0:
            col1.markdown(html_mostrar, unsafe_allow_html=True)
        else:
            col2.markdown(html_mostrar, unsafe_allow_html=True)

    tempo_passado = int(time.time() - st.session_state.tempo_inicio)
    tempo_restante = max(0, TEMPO_LIMITE_SEGUNDOS - tempo_passado)
    
    minutos = tempo_restante // 60
    segundos = tempo_restante % 60
    
    timer_placeholder.markdown(f'<div class="timer-text">⏱️ {minutos:02d}:{segundos:02d}</div>', unsafe_allow_html=True)
    
    if tempo_restante <= 0:
        st.session_state.jogo_terminado = True
        st.session_state.venceu = False
        st.rerun()
        
    time.sleep(1)
    st.rerun()

if st.session_state.jogo_terminado:
    if getattr(st.session_state, 'venceu', False):
        st.success("🎉 PARABÉNS! Você gabaritou a lista inteira!")
        st.balloons()
    else:
        st.error(f"⏰ O TEMPO ACABOU! Você acertou {len(st.session_state.acertos)} de {len(tecnicos)}.")
    
    st.markdown("### Aqui estão os resultados:")
    col1, col2 = st.columns(2)
    for i, tecnico in enumerate(tecnicos):
        nome = tecnico["nome"]
        tipo = tecnico["tipo"]
        caixa_tipo = f'<span class="tipo-tecnico">{tipo}</span>'
        
        if nome in st.session_state.acertos:
            html_mostrar = f'<div class="acerto-box">{caixa_tipo} <b>{nome}</b></div>'
        else:
            html_mostrar = f'<div class="falta-box" style="color:red; border-color:red;">{caixa_tipo} {nome}</div>'
            
        if i % 2 == 0:
            col1.markdown(html_mostrar, unsafe_allow_html=True)
        else:
            col2.markdown(html_mostrar, unsafe_allow_html=True)
            
    if st.button("🔄 Jogar Novamente"):
        st.session_state.acertos = []
        st.session_state.jogo_iniciado = False
        st.session_state.jogo_terminado = False
        st.session_state.input_palpite = ""
        st.rerun()

import streamlit as st
import pandas as pd
import random
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente para desenvolvimento local
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Simulador Copa do Mundo 2026",
    page_icon="⚽",
    layout="wide"
)

# Inicialização do Cliente Supabase
def get_supabase_client() -> Client:
    try:
        url = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
        key = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]
    except:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        st.error("Credenciais do Supabase não encontradas. Verifique st.secrets ou o arquivo .env")
        st.stop()
        
    return create_client(url, key)

# Dados dos Grupos (Copa 2026 - 48 times, 12 grupos)
GROUPS = {
    "Grupo A": ["🇲🇽 México", "🇿🇦 África do Sul", "🇰🇷 Coreia do Sul", "🇨🇿 República Tcheca"],
    "Grupo B": ["🇨🇦 Canadá", "🇧🇦 Bósnia", "🇶🇦 Catar", "🇨🇭 Suíça"],
    "Grupo C": ["🇧🇷 Brasil", "🇲🇦 Marrocos", "🇭🇹 Haiti", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escócia"],
    "Grupo D": ["🇺🇸 Estados Unidos", "🇵🇾 Paraguai", "🇦🇺 Austrália", "🇹🇷 Turquia"],
    "Grupo E": ["🇩🇪 Alemanha", "🇨🇼 Curaçao", "🇨🇮 Costa do Marfim", "🇪🇨 Equador"],
    "Grupo F": ["🇳🇱 Holanda", "🇯🇵 Japão", "🇸🇪 Suécia", "🇹🇳 Tunísia"],
    "Grupo G": ["🇦🇷 Argentina", "🇺🇿 Uzbequistão", "🇦🇴 Angola", "🇵🇱 Polônia"],
    "Grupo H": ["🇫🇷 França", "🇮🇶 Iraque", "🇬🇭 Gana", "🇷🇸 Sérvia"],
    "Grupo I": ["🇪🇸 Espanha", "🇻🇳 Vietnã", "🇨🇲 Camarões", "🇦🇹 Áustria"],
    "Grupo J": ["🇵🇹 Portugal", "🇯🇴 Jordânia", "🇲🇱 Mali", "🇩🇰 Dinamarca"],
    "Grupo K": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "🇹🇭 Tailândia", "🇳🇬 Nigéria", "🇳🇴 Noruega"],
    "Grupo L": ["🇧🇪 Bélgica", "🇴🇲 Omã", "🇪🇬 Egito", "🇷🇴 Romênia"]
}

def save_all_data(user_data, group_predictions, knockout_prediction):
    supabase = get_supabase_client()
    user_data["knockout_prediction"] = knockout_prediction
    
    try:
        # 1. Salvar Usuário
        user_response = supabase.table("users").upsert(user_data, on_conflict="email").execute()
        user_id = user_response.data[0]["id"]
        
        # 2. Limpar palpites antigos e salvar novos
        supabase.table("predictions").delete().eq("user_id", user_id).execute()
        
        final_group_preds = []
        for gp_name, sel in group_predictions.items():
            final_group_preds.append({
                "user_id": user_id,
                "group_name": gp_name,
                "first_place": sel['first'],
                "second_place": sel['second'],
                "third_place": sel.get('third')
            })
        
        supabase.table("predictions").insert(final_group_preds).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")
        return False

def shuffle_thirds():
    """Callback para sortear os terceiros colocados aleatoriamente."""
    candidates = []
    for g_name, sel in st.session_state.selections.items():
        if sel["first"] and sel["second"]:
            remaining = [t for t in GROUPS[g_name] if t not in [sel["first"], sel["second"]]]
            candidates.append(remaining[0])
    
    if len(candidates) >= 8:
        st.session_state.best_thirds = random.sample(candidates, 8)
        # Sincroniza o valor do widget diretamente no session_state usando a chave
        st.session_state.thirds_selector = st.session_state.best_thirds
    else:
        st.session_state.warning_msg = "Selecione os 1º e 2º de todos os grupos antes de sortear."

def render_match(label, t1, t2, k):
    with st.container(border=True):
        st.markdown(f"**{label}**")
        return st.radio("Vence:", [t1, t2], key=k, horizontal=True, index=None)

def main():
    st.markdown("# 🏆 Simulador da Copa do Mundo 2026")
    st.caption("Por Gemini CLI - De grupos ao Campeão")

    # Inicialização do estado
    if 'step' not in st.session_state:
        st.session_state.step = 'user_info'
    if 'selections' not in st.session_state:
        st.session_state.selections = {g: {"first": None, "second": None, "third": None} for g in GROUPS}
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'best_thirds' not in st.session_state:
        st.session_state.best_thirds = []
    if 'warning_msg' not in st.session_state:
        st.session_state.warning_msg = None

    # --- PASSO 1: DADOS DO USUÁRIO ---
    if st.session_state.step == 'user_info':
        with st.container(border=True):
            st.subheader("📝 Seus Dados")
            nome = st.text_input("Nome Completo", placeholder="Ex: João Silva")
            email = st.text_input("E-mail", placeholder="seu@email.com")
            telefone = st.text_input("Telefone", placeholder="(00) 00000-0000")
            
            if st.button("Ir para Fase de Grupos", type="primary"):
                if nome and email and telefone:
                    st.session_state.user_data = {"name": nome, "email": email, "phone": telefone}
                    st.session_state.step = 'groups'
                    st.rerun()
                else:
                    st.warning("Preencha todos os campos.")

    # --- PASSO 2: FASE DE GRUPOS ---
    elif st.session_state.step == 'groups':
        st.subheader("📊 Fase de Grupos")
        
        if st.session_state.warning_msg:
            st.warning(st.session_state.warning_msg)
            st.session_state.warning_msg = None

        # Layout de 3 colunas para os grupos
        group_list = list(GROUPS.keys())
        for i in range(0, len(group_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(group_list):
                    g_name = group_list[i + j]
                    teams = GROUPS[g_name]
                    with cols[j].container(border=True):
                        st.markdown(f"#### {g_name}")
                        f = st.selectbox("1º Colocado", teams, key=f"f_{g_name}", index=None, placeholder="Selecione...")
                        rem_s = [t for t in teams if t != f] if f else teams
                        s = st.selectbox("2º Colocado", rem_s, key=f"s_{g_name}", index=None, placeholder="Selecione...")
                        
                        st.session_state.selections[g_name]["first"] = f
                        st.session_state.selections[g_name]["second"] = s

        st.divider()
        
        # Seleção dos 8 Melhores Terceiros
        st.subheader("🥉 Melhores Terceiros Colocados")
        st.info("Escolha os 8 times que avançam como melhores terceiros ou use o sorteio aleatório.")
        
        # Identificar candidatos
        candidates = []
        for g_name, sel in st.session_state.selections.items():
            if sel["first"] and sel["second"]:
                remaining = [t for t in GROUPS[g_name] if t not in [sel["first"], sel["second"]]]
                candidates.append({"group": g_name, "team": remaining[0]})
        
        candidate_names = [c["team"] for c in candidates]
        
        # O botão agora força a atualização do thirds_selector no session_state
        st.button("🎲 Sortear 8 Aleatórios", type="secondary", on_click=shuffle_thirds)

        selected_thirds = st.multiselect(
            "Selecione exatamente 8 times:",
            options=candidate_names,
            max_selections=8,
            key="thirds_selector",
            placeholder="Escolha os times..."
        )
        # Atualiza o best_thirds com o valor atual do widget
        st.session_state.best_thirds = selected_thirds

        if st.button("Avançar para o Mata-Mata", type="primary", use_container_width=True):
            incomplete = [g for g, sel in st.session_state.selections.items() if not sel["first"] or not sel["second"]]
            if incomplete:
                st.warning(f"Complete os grupos: {', '.join(incomplete)}")
            elif len(selected_thirds) != 8:
                st.warning(f"Você selecionou {len(selected_thirds)} terceiros colocados. Selecione exatamente 8.")
            else:
                for c in candidates:
                    st.session_state.selections[c["group"]]["third"] = c["team"] if c["team"] in selected_thirds else None
                
                advancing = []
                for g_name, sel in st.session_state.selections.items():
                    advancing.append(sel["first"])
                    advancing.append(sel["second"])
                advancing.extend(selected_thirds)
                
                st.session_state.advancing_teams = advancing
                st.session_state.step = 'knockout'
                st.rerun()

    # --- PASSO 3: MATA-MATA (Progressivo) ---
    elif st.session_state.step == 'knockout':
        st.subheader("⚔️ Fase de Mata-Mata")
        teams = st.session_state.advancing_teams.copy()
        random.seed(42)
        random.shuffle(teams)
        
        # --- R32 (Round of 32) ---
        st.markdown("### 1️⃣6️⃣ avos de Final (32)")
        r32_w = []
        c1, c2 = st.columns(2)
        for i in range(0, 32, 2):
            with (c1 if i < 16 else c2):
                r32_w.append(render_match(f"Jogo {i//2 + 1}", teams[i], teams[i+1], f"r32_{i}"))
        
        if all(r32_w):
            st.divider()
            # --- R16 (Round of 16) ---
            st.markdown("### 8️⃣ Oitavas de Final")
            r16_w = []
            c3, c4 = st.columns(2)
            for i in range(0, 16, 2):
                with (c3 if i < 8 else c4):
                    r16_w.append(render_match(f"Oitavas {i//2 + 1}", r32_w[i], r32_w[i+1], f"r16_{i}"))

            if all(r16_w):
                st.divider()
                # --- QF (Quarter Finals) ---
                st.markdown("### 4️⃣ Quartas de Final")
                qf_w = []
                c5, c6 = st.columns(2)
                for i in range(0, 8, 2):
                    with (c5 if i < 4 else c6):
                        qf_w.append(render_match(f"Quartas {i//2 + 1}", r16_w[i], r16_w[i+1], f"qf_{i}"))

                if all(qf_w):
                    st.divider()
                    # --- SF (Semi Finals) ---
                    st.markdown("### 2️⃣ Semifinais")
                    sf_w = []
                    c7, c8 = st.columns(2)
                    for i in range(0, 4, 2):
                        with (c7 if i < 2 else c8):
                            sf_w.append(render_match(f"Semi {i//2 + 1}", qf_w[i], qf_w[i+1], f"sf_{i}"))

                    if all(sf_w):
                        st.divider()
                        # --- FINAL ---
                        st.markdown("### 🏆 FINAL")
                        champion = render_match("FINALÍSSIMA", sf_w[0], sf_w[1], "final_game")
                        
                        if champion:
                            st.divider()
                            if st.button("💾 Finalizar e Salvar Tudo", type="primary", use_container_width=True):
                                knockout_data = {"r32": r32_w, "r16": r16_w, "qf": qf_w, "sf": sf_w, "champion": champion}
                                if save_all_data(st.session_state.user_data, st.session_state.selections, knockout_data):
                                    st.balloons()
                                    st.success(f"🎊 PARABÉNS! {champion} é o seu campeão!")
                                    if st.button("Começar Novo Bolão"):
                                        st.session_state.clear()
                                        st.rerun()
        else:
            st.info("👆 Selecione todos os vencedores da fase atual para liberar a próxima.")

if __name__ == "__main__":
    main()

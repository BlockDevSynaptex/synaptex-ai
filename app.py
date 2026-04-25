import streamlit as st
import time
import os
import random
from groq import Groq

# --- 1. Настройка страницы ---
st.set_page_config(page_title="Synaptex by BlockDev", page_icon="✨", layout="wide")

# --- 2. PREMIUM CSS (Исправленный интерфейс) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');

    .stApp {
        background-color: #0e0e0e; 
        color: #e3e3e3;
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stHeader"] {background-color: transparent !important;}

    /* Элегантное переливающееся название */
    .synaptex-title {
        font-size: 4.5rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        background: linear-gradient(110deg, #b084f5 0%, #7c3aed 50%, #4c1d95 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 5s linear infinite;
        text-align: center;
        margin-bottom: 2rem;
        margin-top: -30px;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* Центрирование чата */
    .user-msg-container, .ai-msg-container {
        width: 100%;
        max-width: 850px;
        margin: 0 auto 24px auto;
        display: flex;
    }

    .user-msg-container {
        justify-content: flex-end;
        animation: slideInRight 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    }
    .user-msg {
        background-color: #1f1f1f;
        color: #ffffff;
        padding: 16px 24px;
        border-radius: 28px 28px 6px 28px;
        max-width: 75%;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .ai-msg-container {
        justify-content: flex-start;
        animation: slideInLeft 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    }
    .ai-msg {
        background: linear-gradient(145deg, #121212, #0a0a0a);
        color: #f1f3f4;
        padding: 18px 26px;
        border-radius: 28px 28px 28px 6px;
        max-width: 85%;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.06); 
    }

    @keyframes slideInRight { from { opacity: 0; transform: translateX(30px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes slideInLeft { from { opacity: 0; transform: translateX(-30px); } to { opacity: 1; transform: translateX(0); } }

    /* === АНИМИРОВАННОЕ ПРИВЕТСТВИЕ === */
    .animated-greeting {
        position: relative;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 15vh;
    }
    .animated-greeting span {
        position: absolute;
        font-size: 2rem;
        font-weight: 600;
        color: #b084f5; /* Фиолетовый */
        opacity: 0;
        animation: fadeCycle 20s infinite cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        width: 100%;
    }
    .greeting-1 { animation-delay: 0s !important; }
    .greeting-2 { animation-delay: 5s !important; }
    .greeting-3 { animation-delay: 10s !important; }
    .greeting-4 { animation-delay: 15s !important; }

    @keyframes fadeCycle {
        0% { opacity: 0; transform: translateY(15px); filter: blur(4px); }
        5%, 20% { opacity: 1; transform: translateY(0); filter: blur(0px); }
        25%, 100% { opacity: 0; transform: translateY(-15px); filter: blur(4px); }
    }

    /* === ИСПРАВЛЕННАЯ ПАНЕЛЬ ВВОДА === */
    div[data-testid="stChatInput"] {
        max-width: 750px !important;
        margin: 0 auto 20px auto !important;
        border-radius: 30px !important;
        background: linear-gradient(90deg, #000000 40%, #7c3aed 100%) !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5) !important;
    }
    
    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        font-size: 16px !important;
        background-color: transparent !important;
    }

    /* Фокус на панели ввода */
    div[data-testid="stChatInput"]:focus-within {
        box-shadow: 0 0 25px rgba(124, 58, 237, 0.4) !important;
    }
    
    /* Стилизация боковой панели */
    [data-testid="stSidebar"] {
        background-color: #121212 !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    .sidebar-title {
        color: #b084f5; 
        font-weight: 600;
        margin-bottom: 12px;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .stButton > button {
        border: none !important;
        background-color: transparent !important;
        text-align: left !important;
        justify-content: flex-start !important;
        color: #b0b0b0 !important;
    }
    .stButton > button:hover {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0e0e0e; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #555; }

    /* === ФОНОВОЕ СВЕЧЕНИЕ (АУРА) С ПРАВОЙ СТОРОНЫ === */
    .ambient-glow {
        position: fixed;
        top: 20%;
        right: -150px;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(176,132,245,0.08) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
        z-index: -1;
        pointer-events: none;
    }

    /* === ПЛАВАЮЩИЕ ПОДСКАЗКИ (СПРАВА) === */
    .right-suggestions-panel {
        position: fixed;
        top: 30%;
        right: 40px;
        width: 250px;
        z-index: 100;
        pointer-events: none;
    }
    .suggestions-header {
        color: #b084f5;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 20px;
        padding-left: 5px;
    }
    .sugg-group {
        position: absolute;
        top: 40px;
        width: 100%;
        opacity: 0;
        animation: cycleGroup 21s infinite;
    }
    .group-1 { animation-delay: 0s; }
    .group-2 { animation-delay: 7s; }
    .group-3 { animation-delay: 14s; }

    @keyframes cycleGroup {
        0%, 28% { opacity: 1; transform: translateY(0); }
        33%, 95% { opacity: 0; transform: translateY(-10px); }
        100% { opacity: 0; transform: translateY(10px); }
    }

    .suggestion-card {
        background-color: rgba(30,30,30, 0.4);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: flex-start;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    .suggestion-icon {
        font-size: 16px;
        margin-right: 12px;
        opacity: 0.8;
    }
    .suggestion-text {
        color: #d0d0d0;
        font-size: 12px;
        line-height: 1.4;
    }
    /* Прячем на маленьких экранах */
    @media (max-width: 1300px) {
        .right-suggestions-panel { display: none !important; }
        .ambient-glow { display: none !important; }
    }

    /* Скрываем элементы Streamlit Cloud для чистоты UI */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .viewerBadge_container {display: none !important;}
    #viewerBadge_container {display: none !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="manage-app-button"] {display: none !important;}
    [data-testid="stAppDeployButton"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# --- 3. ИНИЦИАЛИЗАЦИЯ ИСТОРИИ И НАСТРОЕК ---
if "chats" not in st.session_state:
    st.session_state.chats = {"Новый чат": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Новый чат"

# Настройки темы
themes = {
    "По умолчанию (Фиолетовый)": {"base": "#b084f5", "dark": "#7c3aed", "darkest": "#4c1d95"},
    "Красный (Ruby)": {"base": "#ff4b4b", "dark": "#d32f2f", "darkest": "#b71c1c"},
    "Синий (Ocean)": {"base": "#2196f3", "dark": "#1976d2", "darkest": "#0d47a1"},
    "Зеленый (Emerald)": {"base": "#4caf50", "dark": "#388e3c", "darkest": "#1b5e20"},
    "Оранжевый (Sunset)": {"base": "#ff9800", "dark": "#f57c00", "darkest": "#e65100"}
}

if "theme" not in st.session_state:
    st.session_state.theme = themes["По умолчанию (Фиолетовый)"]

# Применение динамической темы
t_base = st.session_state.theme["base"]
t_dark = st.session_state.theme["dark"]
t_darkest = st.session_state.theme["darkest"]

dynamic_css = f"""
<style>
    .synaptex-title {{ background: linear-gradient(110deg, {t_base} 0%, {t_dark} 50%, {t_darkest} 100%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .animated-greeting span {{ color: {t_base} !important; }}
    div[data-testid="stChatInput"] {{ background: linear-gradient(90deg, #000000 40%, {t_dark} 100%) !important; }}
    div[data-testid="stChatInput"]:focus-within {{ box-shadow: 0 0 25px {t_dark}66 !important; }}
    .sidebar-title {{ color: {t_base} !important; }}
    .suggestions-header {{ color: {t_base} !important; }}
    .ambient-glow {{ background: radial-gradient(circle, {t_base}15 0%, rgba(0,0,0,0) 70%) !important; }}
    
    /* Кнопка настроек (шестеренка) в правом верхнем углу */
    div[data-testid="stPopover"] {{ 
        position: fixed !important; 
        top: 20px !important; 
        right: 20px !important; 
        z-index: 1000 !important; 
        width: auto !important;
    }}
    div[data-testid="stPopover"] > button {{ 
        background-color: rgba(30,30,30, 0.7) !important; 
        border: 1px solid rgba(255,255,255,0.1) !important; 
        border-radius: 50% !important; 
        width: 46px !important; 
        height: 46px !important; 
        padding: 0 !important; 
        display: flex !important; 
        align-items: center !important; 
        justify-content: center !important; 
        backdrop-filter: blur(10px); 
    }}
    div[data-testid="stPopover"] > button:hover {{ 
        border-color: {t_base} !important; 
        box-shadow: 0 0 15px {t_base}66 !important; 
    }}
    div[data-testid="stPopover"] > button p {{
        font-size: 22px !important;
        margin: 0 !important;
        line-height: 1 !important;
    }}
    div[data-testid="stPopover"] > button svg {{
        display: none !important;
    }}
</style>
"""
st.markdown(dynamic_css, unsafe_allow_html=True)

# --- 4. БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:white; font-weight: 800; letter-spacing: -1px;'>Synaptex</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("＋ Новый чат", use_container_width=True):
        st.session_state.current_chat = "Новый чат"
        if "Новый чат" not in st.session_state.chats:
            st.session_state.chats["Новый чат"] = []
        st.rerun()
        
    st.divider()
    st.markdown("<div class='sidebar-title'>История диалогов</div>", unsafe_allow_html=True)
    
    for chat_name in list(st.session_state.chats.keys()):
        if chat_name == "Новый чат" and len(st.session_state.chats[chat_name]) == 0 and st.session_state.current_chat != "Новый чат":
            continue
        if st.button(f"›  {chat_name}", key=f"chat_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.divider()
    st.markdown("<div class='sidebar-title'>О системе</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: #1a1a1a; padding: 15px; border-radius: 12px; border: 1px solid #333; margin-bottom: 20px;'>
        <p style='color: #b084f5; font-weight: 600; margin-bottom: 5px; font-size: 14px;'>Synaptex AI</p>
        <p style='color: #b0b0b0; font-size: 12px; line-height: 1.5; margin-bottom: 10px;'>Передовая нейросеть с премиальным дизайном, созданная для решения самых сложных задач.</p>
        <p style='color: #888; font-size: 11px; margin-bottom: 2px;'>Версия: 1.0.0</p>
        <p style='color: #888; font-size: 11px; letter-spacing: 1px;'>ENGINEERED BY BLOCKDEV</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. ГЛАВНЫЙ ИНТЕРФЕЙС ---

with st.popover("⚙️"):
    st.markdown(f"<div style='color: {t_base}; font-weight: 600; margin-bottom: 10px; font-size: 14px;'>Цвет интерфейса</div>", unsafe_allow_html=True)
    selected_theme_name = st.selectbox("Цвет", list(themes.keys()), label_visibility="collapsed")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Применить", use_container_width=True):
            st.session_state.theme = themes[selected_theme_name]
            st.rerun()
    with col2:
        if st.button("Сброс", use_container_width=True):
            st.session_state.theme = themes["По умолчанию (Фиолетовый)"]
            st.rerun()

st.markdown("<div class='synaptex-title'>Synaptex</div>", unsafe_allow_html=True)

# Динамические подсказки
chat_history_for_sugg = st.session_state.chats.get(st.session_state.current_chat, [])

if len(chat_history_for_sugg) == 0:
    all_suggestions = [
        ("✍️", "Напиши пост для соцсетей про искусственный интеллект"),
        ("💻", "Объясни сложный код простыми словами"),
        ("🧠", "Придумай идеи для нового стартапа"),
        ("✈️", "Спланируй маршрут для поездки на выходные"),
        ("🧘", "Как быстро расслабиться после тяжелого дня?"),
        ("📚", "Помоги с домашним заданием по математике"),
        ("🍳", "Что приготовить на ужин из простых продуктов?"),
        ("🎬", "Посоветуй интересный фильм на вечер"),
        ("🏋️", "Составь план тренировок для начинающих")
    ]

    # Размешиваем подсказки и делим на 3 группы
    random.shuffle(all_suggestions)
    group1 = all_suggestions[0:3]
    group2 = all_suggestions[3:6]
    group3 = all_suggestions[6:9]

    # Фоновое свечение и панель подсказок (справа)
    suggestions_html = f"""
    <div class="ambient-glow"></div>
    <div class="right-suggestions-panel">
    <div class="suggestions-header">✨ Попробуйте спросить</div>

    <div class="sugg-group group-1">
    <div class="suggestion-card"><div class="suggestion-icon">{group1[0][0]}</div><div class="suggestion-text">{group1[0][1]}</div></div>
    <div class="suggestion-card"><div class="suggestion-icon">{group1[1][0]}</div><div class="suggestion-text">{group1[1][1]}</div></div>
    <div class="suggestion-card"><div class="suggestion-icon">{group1[2][0]}</div><div class="suggestion-text">{group1[2][1]}</div></div>
    </div>

    <div class="sugg-group group-2">
    <div class="suggestion-card"><div class="suggestion-icon">{group2[0][0]}</div><div class="suggestion-text">{group2[0][1]}</div></div>
    <div class="suggestion-card"><div class="suggestion-icon">{group2[1][0]}</div><div class="suggestion-text">{group2[1][1]}</div></div>
    <div class="suggestion-card"><div class="suggestion-icon">{group2[2][0]}</div><div class="suggestion-text">{group2[2][1]}</div></div>
    </div>

    <div class="sugg-group group-3">
    <div class="suggestion-card"><div class="suggestion-icon">{group3[0][0]}</div><div class="suggestion-text">{group3[0][1]}</div></div>
    <div class="suggestion-card"><div class="suggestion-icon">{group3[1][0]}</div><div class="suggestion-text">{group3[1][1]}</div></div>
    <div class="suggestion-card"><div class="suggestion-icon">{group3[2][0]}</div><div class="suggestion-text">{group3[2][1]}</div></div>
    </div>

    </div>
    """
    st.markdown(suggestions_html, unsafe_allow_html=True)

chat_history = st.session_state.chats[st.session_state.current_chat]

# Если чат пустой - показываем красивую анимацию текста по центру
if len(chat_history) == 0:
    st.markdown("""
    <div class="animated-greeting">
        <span class="greeting-1">Чем Вам сегодня помочь?</span>
        <span class="greeting-2">Synaptex на связи!</span>
        <span class="greeting-3">Мой создатель - Лучший человек!</span>
        <span class="greeting-4">Что вы сегодня желаете?</span>
    </div>
    """, unsafe_allow_html=True)

# Отрисовка истории
for msg in chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg-container"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg-container"><div class="ai-msg"><b>Synaptex</b><br><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

# --- 6. ЗАПРОС К ИИ ---
if prompt := st.chat_input("Спросите Synaptex..."):
    
    if st.session_state.current_chat == "Новый чат":
        first_word = prompt.strip().split(" ")[0].capitalize()
        new_chat_name = first_word[:15] + "..." if len(first_word) > 15 else first_word
        base_name = new_chat_name
        counter = 1
        while new_chat_name in st.session_state.chats:
            new_chat_name = f"{base_name} ({counter})"
            counter += 1
        st.session_state.chats[new_chat_name] = st.session_state.chats.pop("Новый чат")
        st.session_state.current_chat = new_chat_name
        chat_history = st.session_state.chats[new_chat_name]

    st.markdown(f'<div class="user-msg-container"><div class="user-msg">{prompt}</div></div>', unsafe_allow_html=True)
    chat_history.append({"role": "user", "content": prompt})

    # УПРАВЛЕНИЕ КЛЮЧОМ GROQ
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = "DEMO" 

    if api_key == "DEMO":
        user_text = prompt.strip().lower()
        if "кто ты" in user_text:
            error_msg = "Я - **Synaptex**! Нейросеть, которая создана **BlockDev**. Мой дизайн вдохновлен лучшими ИИ-помощниками, а интерфейс разработан специально для вашего удобства. \n\n*(P.S. Ключ API еще не подключен, поэтому я работаю в демо-режиме).* "
        else:
            error_msg = f"Вы спросили: '{prompt}'. \n\n⚠️ Внимание: Нейромодуль не подключен. Разработчик еще не установил секретный ключ API в Streamlit Secrets. Система работает в демо-режиме."
        
        st.markdown(f'<div class="ai-msg-container"><div class="ai-msg"><b>Synaptex:</b><br><br>{error_msg}</div></div>', unsafe_allow_html=True)
        chat_history.append({"role": "assistant", "content": error_msg})
        st.rerun()
    else:
        try:
            client = Groq(api_key=api_key)
            api_messages = [{"role": "system", "content": "Ты - Synaptex. Ультра-современная, сверхточная нейросеть, созданная разработчиком BlockDev. Отвечай всегда на РУССКОМ языке. Будь максимально точным, логичным и опирайся только на факты. Если ты не знаешь ответа на вопрос или сомневаешься — честно скажи 'Я не знаю', НИКОГДА не выдумывай несуществующие факты. Если тебя спросят, кто ты, отвечай, что ты Synaptex от BlockDev."}]
            
            for m in chat_history[-11:-1]:
                api_messages.append({"role": m["role"], "content": m["content"]})
            api_messages.append({"role": "user", "content": prompt})

            # Температура снижена до 0.2 для максимальной точности и уменьшения ошибок
            stream = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=api_messages, temperature=0.2, stream=True)
            res_box = st.empty()
            full_response = ""
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    res_box.markdown(f'<div class="ai-msg-container"><div class="ai-msg"><b>Synaptex</b><br><br>{full_response}▌</div></div>', unsafe_allow_html=True)
            
            res_box.markdown(f'<div class="ai-msg-container"><div class="ai-msg"><b>Synaptex</b><br><br>{full_response}</div></div>', unsafe_allow_html=True)
            chat_history.append({"role": "assistant", "content": full_response})
            st.rerun()

        except Exception as e:
            error_msg = f"❌ Системный сбой API: {e}"
            st.markdown(f'<div class="ai-msg-container"><div class="ai-msg"><b>System:</b><br><br>{error_msg}</div></div>', unsafe_allow_html=True)
            chat_history.append({"role": "assistant", "content": error_msg})

import streamlit as st
from router import router
from faq import ingest_faq_data, faq_chain
from pathlib import Path
from sql import sql_chain
from smalltalk import talk

faqs_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(faqs_path)
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShopBot AI",
    page_icon="🛍️",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #0d0d0f;
    --surface:   #17171a;
    --card:      #1e1e23;
    --border:    #2a2a32;
    --accent:    #ff6b35;
    --accent2:   #ffb347;
    --text:      #f0f0f4;
    --muted:     #7a7a8c;
    --user-bg:   #ff6b3520;
    --bot-bg:    #1e1e23;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide streamlit default elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 780px !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ff6b3530, #ffb34720);
    border: 1px solid #ff6b3540;
    border-radius: 100px;
    padding: 0.3rem 1rem;
    font-size: 0.72rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent2);
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.8rem !important;
    line-height: 1.1 !important;
    background: linear-gradient(135deg, #ffffff 0%, #ff6b35 60%, #ffb347 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin: 0 0 0.5rem !important;
}
.hero p {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}

/* ── Suggestion chips ── */
.chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    margin: 1.5rem 0 0.5rem;
}
.chip {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.45rem 1rem;
    font-size: 0.8rem;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}
.chip:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: #ff6b3510;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.4rem 0 !important;
}

/* User message bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--user-bg) !important;
    border: 1px solid #ff6b3525 !important;
    border-radius: 16px !important;
    padding: 0.8rem 1rem !important;
    margin-left: 3rem !important;
}

/* Bot message bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: var(--bot-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 0.8rem 1rem !important;
    margin-right: 3rem !important;
}

/* ── Avatar icons ── */
[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    border-radius: 10px !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #2a2a40, #3a3a55) !important;
    border-radius: 10px !important;
}

/* ── Chat input ── */
# CORRECT - single border only
[data-testid="stChatInput"] {
    background: var(--card) !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 0.2rem 0.5rem !important;
    outline: 1.5px solid var(--border) !important;
    transition: outline-color 0.2s !important;
}
[data-testid="stChatInput"]:focus-within {
    outline: 1.5px solid var(--accent) !important;
    box-shadow: 0 0 0 3px #ff6b3515 !important;
}
}
[data-testid="stChatInput"] textarea {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    color: var(--text) !important;
    background: transparent !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* ── Route badge ── */
.route-tag {
    display: inline-block;
    font-size: 0.68rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 100px;
    margin-bottom: 0.4rem;
}
.route-faq       { background: #3b82f620; color: #60a5fa; border: 1px solid #3b82f640; }
.route-sql       { background: #10b98120; color: #34d399; border: 1px solid #10b98140; }
.route-small_talk{ background: #f59e0b20; color: #fbbf24; border: 1px solid #f59e0b40; }
.route-other     { background: #6b728020; color: #9ca3af; border: 1px solid #6b728040; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1rem 0;
}

/* ── Clear button ── */
.stButton button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    border-radius: 100px !important;
    font-size: 0.78rem !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.3rem 1rem !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    border-color: #ff6b3560 !important;
    color: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Route helper ──────────────────────────────────────────────────────────────
def ask(query):
    route = router(query).name
    if route == "faq":
        return route, faq_chain(query)
    elif route == "sql":
        return route, sql_chain(query)
    elif route == "small_talk":
        return route, talk(query)
    else:
        return "other", f"Sorry, I'm not sure how to help with that. Try asking about products or policies!"


def route_badge(route):
    labels = {
        "faq":        "📋 FAQ",
        "sql":        "🔍 Product Search",
        "small_talk": "💬 Chat",
        "other":      "❓ Unknown",
    }
    label = labels.get(route, "❓ Unknown")
    return f'<span class="route-tag route-{route}">{label}</span>'


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ── Hero section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI Powered Shopping Assistant</div>
    <h1>ShopBot AI 🛍️</h1>
    <p>Search products · Get answers · Just chat</p>
</div>
""", unsafe_allow_html=True)

# ── Suggestion chips ──────────────────────────────────────────────────────────
if not st.session_state["messages"]:
    st.markdown("""
    <div class="chips-row">
        <div class="chip">👟 Nike shoes under ₹3000</div>
        <div class="chip">⭐ Top rated running shoes</div>
        <div class="chip">🔄 What is your return policy?</div>
        <div class="chip">💳 Payment methods accepted?</div>
        <div class="chip">📦 How to track my order?</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "route" in message:
            st.markdown(route_badge(message["route"]), unsafe_allow_html=True)
        st.markdown(message["content"])

# ── Clear chat button ─────────────────────────────────────────────────────────
# CORRECT - always visible in top right

col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🗑 Clear"):
        st.session_state["messages"] = []
        st.rerun()
# ── Input & response ──────────────────────────────────────────────────────────
query = st.chat_input("Ask about products, prices, policies...")

if query:
    # show user message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            route, response = ask(query)
        st.markdown(route_badge(route), unsafe_allow_html=True)
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "route": route
    })
import streamlit as st
import wikipediaapi

# Seitenkonfiguration für mobile Geräte
st.set_page_config(
    page_title="WikiAgent Summarizer",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS für Dark Theme und Mobile-Optimierung
st.markdown("""
    <style>
    .main {
        background-color: #121212;
        color: #E0E0E0;
    }
    h1 {
        color: #BB86FC;
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stButton>button {
        background-color: #6200EE;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3700B3;
        color: white;
    }
    .summary-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #03DAC6;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 WikiAgent Summarizer")
st.write("Dein persönlicher KI-Agent, der Wikipedia-Artikel filtert und zusammenfasst.")

# Eingabefeld
search_query = st.text_input("Welches Thema möchtest du erforschen?", placeholder="Wos willsch wissn? Ha?")

# Schieberegler für die Informationstiefe
summary_depth = st.select_slider(
    "Zusammenfassungs-Tiefe wählen:",
    options=["Kurz & Knackig (Bulletpoints)", "Kompakte Übersicht", "Ausführliche Analyse"]
)

if st.button("Artikel analysieren"):
    if not search_query.strip():
        st.warning("Bitte gib zuerst ein Thema ein!")
    else:
        with st.spinner("Agent kontaktiert Wikipedia und verarbeitet Daten..."):
            # Wikipedia API initialisieren (Wikipedia verlangt einen eindeutigen User-Agent)
            wiki = wikipediaapi.Wikipedia(
                user_agent="WikiAgentSummarizerApp/1.0 (contact: deine-mail@example.com)",
                language="de"
            )
            
            page = wiki.page(search_query)
            
            if not page.exists():
                st.error("Dieser Artikel wurde auf Wikipedia leider nicht gefunden. Versuche es mit einem anderen Begriff.")
            else:
                st.success(f"Artikel gefunden: **{page.title}**")
                
                st.markdown("### 📝 Generierte Zusammenfassung")
                st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                
                # Logik je nach Slider-Einstellung
                if summary_depth == "Kurz & Knackig (Bulletpoints)":
                    sentences = page.summary.split('. ')
                    bullets = "\n".join([f"- {s.strip()}." for s in sentences if s.strip()])
                    st.markdown(bullets)
                    
                elif summary_depth == "Kompakte Übersicht":
                    st.write(page.summary)
                    
                else: # Ausführliche Analyse
                    st.write(page.summary)
                    sections = page.sections
                    display_count = 0
                    for section in sections:
                        if display_count >= 3: # Auf Mobilgeräten nicht zu lang werden lassen
                            break
                        if section.text.strip() and section.title not in ["Literatur", "Weblinks", "Einzelnachweise", "Siehe auch"]:
                            st.markdown(f"#### {section.title}")
                            st.write(section.text[:600] + "..." if len(section.text) > 600 else section.text)
                            display_count += 1
                            
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Link zur Quelle
                st.markdown(f"[🔗 Originalen Wikipedia-Artikel ansehen]({page.fullurl})")

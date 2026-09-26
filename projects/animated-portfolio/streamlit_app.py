"""Streamlit Cloud adaptation of the Northstar front-end concept."""
import streamlit as st

st.set_page_config(page_title="Northstar · Design in motion", page_icon="✦", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;800&display=swap');
.stApp {background:#0d1720;color:#f7f4ec;font-family:'DM Sans',system-ui,sans-serif}
[data-testid="stHeader"] {background:transparent}
.block-container {max-width:1200px;padding-top:2rem}
.hero {position:relative;overflow:hidden;padding:5rem 3rem;border-radius:28px;background:radial-gradient(circle at 82% 20%,#314e5d 0,#172c38 35%,#0e1d28 75%);min-height:470px}
.eyebrow {color:#a5f5d8;letter-spacing:.2em;font-size:.78rem;font-weight:800}
.hero h1 {font-size:clamp(3rem,7vw,6.4rem);line-height:1.02;letter-spacing:-.06em;margin:1.5rem 0;color:#fff}
.hero h1 em,.accent {color:#b6f37f;font-style:normal}
.hero p {max-width:570px;color:#c4d3d5;font-size:1.1rem}
.orb {position:absolute;right:5%;top:12%;width:20rem;height:20rem;border-radius:50%;background:linear-gradient(140deg,#c0f383,#48bfc0);filter:blur(2px);opacity:.23;animation:float 8s ease-in-out infinite}
.section-title {font-size:clamp(2rem,4vw,3.4rem);letter-spacing:-.04em;margin:3rem 0 1rem;color:#fff}
.card {min-height:220px;border-radius:20px;padding:1.5rem;background:linear-gradient(140deg,#83dccc,#407391);color:#0d1720;transition:transform .3s}
.card:hover {transform:translateY(-6px)}
.card.two {background:linear-gradient(140deg,#ffc687,#f67e74)}
.card.three {background:linear-gradient(140deg,#d7b6f5,#7466b4);color:#fff}
.card strong {display:block;margin-top:5rem;font-size:1.5rem}
@keyframes float {50% {transform:translate(-1.5rem,1.5rem) scale(1.07)}}
@media(max-width:700px){.hero{padding:3rem 1.5rem;min-height:390px}.orb{width:12rem;height:12rem}}
@media(prefers-reduced-motion:reduce){.orb{animation:none}.card{transition:none}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("✦ northstar.")
    section = st.radio("Navigation", ["Home", "Work", "Process", "About"], label_visibility="collapsed")
    st.caption("Fictional digital studio · Streamlit edition")

if section == "Home":
    st.markdown('''<div class="hero"><div class="orb"></div><div class="eyebrow">INDEPENDENT DIGITAL STUDIO</div>
    <h1>Ideas made<br><em>impossible</em><br>to ignore.</h1>
    <p>A concept portfolio exploring layout, colour, motion, and navigation, now adapted for Streamlit.</p></div>''', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Design with purpose. Build with curiosity.</h2>', unsafe_allow_html=True)
    st.write("Use the sidebar to browse projects, process, and the story behind this demo.")
elif section == "Work":
    st.markdown('<h1 class="section-title">Things worth looking at.</h1>', unsafe_allow_html=True)
    cols = st.columns(3)
    cards = [("Orbit Identity", "Brand system · Art direction", ""), ("New Day", "Campaign · Editorial", "two"), ("Field Notes", "Digital experience · Motion", "three")]
    for col, (title, subtitle, klass) in zip(cols, cards):
        col.markdown(f'<div class="card {klass}"><span>{subtitle}</span><strong>{title}</strong></div>', unsafe_allow_html=True)
    st.caption("These are fictional case studies with CSS-only artwork.")
elif section == "Process":
    st.markdown('<h1 class="section-title">A little wonder. A lot of intention.</h1>', unsafe_allow_html=True)
    for n, title, description in [("01", "Find the story", "Understand the audience and what matters most."), ("02", "Shape the idea", "Make type, colour and interaction work together."), ("03", "Make it real", "Build responsive pages and refine the details.")]:
        st.subheader(f"{n} · {title}")
        st.write(description)
else:
    st.markdown('<h1 class="section-title">Good design feels like an invitation.</h1>', unsafe_allow_html=True)
    st.write("Northstar is a fictional studio. The original HTML, CSS, and JavaScript site remains in this project folder for comparison with this Streamlit adaptation.")
    st.info("This demonstration has no real contact form or client work.")

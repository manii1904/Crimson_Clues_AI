from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path
from textwrap import dedent

import streamlit as st

from ai import (
    generate_case,
    generate_crime_scene_image,
    generate_victim_image,
    investigate_scene,
    judge_case,
    talk_to_suspect,
)
from styles import load_css


ASSETS_DIR = Path("assets")
DEFAULT_STATE = {
    "case_started": False,
    "case_data": None,
    "selected_suspect": None,
    "chat_history": {},
    "crime_scene": "",
    "notes": "",
    "evidence": [],
    "achievements": [],
    "crime_scene_image": "",
    "victim_image": "",
}
SUSPECT_STATUSES = ["😐 Calm", "😰 Nervous", "😠 Angry", "🧐 Suspicious"]


def read_base64(path: Path) -> str:
    """Return a file's contents encoded for use in an HTML data URL."""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def play_background_music() -> None:
    """Embed looping background music in the page."""
    audio_base64 = read_base64(ASSETS_DIR / "sounds" / "background.mp3")
    st.markdown(
        f'''<audio autoplay loop>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg">
        </audio>''',
        unsafe_allow_html=True,
    )


def initialize_session_state() -> None:
    for key, value in DEFAULT_STATE.items():
        st.session_state.setdefault(key, value)


def reset_case_state(case: dict) -> None:
    st.session_state.case_data = case
    st.session_state.crime_scene_image = generate_crime_scene_image(case)
    st.session_state.victim_image = generate_victim_image(case)
    st.session_state.case_started = True
    st.session_state.selected_suspect = None
    st.session_state.chat_history = {}
    st.session_state.crime_scene = ""
    st.session_state.evidence = []
    st.session_state.achievements = []


def detective_score() -> int:
    return min(len(st.session_state.evidence) * 2 + len(st.session_state.chat_history), 10)


def detective_rank(score: int) -> str:
    if score <= 2:
        return "🟢 Rookie Detective"
    if score <= 4:
        return "🔵 Junior Detective"
    if score <= 6:
        return "🟡 Detective"
    if score <= 8:
        return "🟠 Senior Detective"
    return "🔴 Chief Detective"


def info_card(title: str, body: str, accent: str = "#FFD700") -> None:
    st.markdown(
        f'''<div style="background:#1E1E2F;padding:18px;border-radius:15px;
                         border-left:6px solid {accent};">
            <h3>{title}</h3>{body}
        </div>''',
        unsafe_allow_html=True,
    )


def render_start_screen(background_base64: str) -> None:
    """Render the landing-page banner without Markdown turning HTML into code."""
    hero_html = dedent(
        f"""\
        <style>
            .crimson-hero {{
                min-height: 480px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                background-image:
                    linear-gradient(rgba(0, 0, 0, 0.64), rgba(0, 0, 0, 0.72)),
                    url("data:image/jpeg;base64,{background_base64}");
                background-size: cover;
                background-position: center;
                border-radius: 18px;
                padding: 48px 24px;
                box-sizing: border-box;
            }}

            .crimson-hero h1 {{
                color: #FFD700;
                font-size: clamp(2.3rem, 5vw, 4.5rem);
                line-height: 1.1;
                margin: 0 0 56px;
                text-shadow: 0 0 12px rgba(255, 215, 0, 0.55);
            }}

            .crimson-hero p {{
                color: #FFFFFF;
                font-size: clamp(1.15rem, 2vw, 1.55rem);
                font-weight: 600;
                line-height: 1.65;
                margin: 0;
            }}
        </style>
        <section class="crimson-hero">
            <h1>🕵️ CRIMSON CLUES AI</h1>
            <p>Every clue matters.<br>Every suspect lies.<br>Solve the impossible.</p>
        </section>
        """
    )
    # `dedent` is essential here: four leading spaces make Markdown render the
    # HTML as a code block, which is why the original screen showed raw tags.
    st.markdown(hero_html, unsafe_allow_html=True)


st.set_page_config(
    page_title="Crimson Clues AI",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(load_css(), unsafe_allow_html=True)
initialize_session_state()

background_base64 = read_base64(ASSETS_DIR / "images" / "background.jpg")
score = detective_score()
rank = detective_rank(score)

with st.sidebar:
    st.image(ASSETS_DIR / "suspects" / "suspect1.jpg", width=120)
    st.markdown("# 🕵️ Crimson Clues")
    st.caption("Detective Intelligence System")
    st.divider()
    st.markdown("### 📂 Navigation")
    st.markdown("🏠 Home  \n📄 Case File  \n👥 Suspects  \n🔍 Crime Scene  \n📁 Evidence  \n📓 Notebook  \n⚖️ Solve Case")
    st.divider()
    st.markdown("### 📊 Detective")
    st.progress(score / 10)
    st.caption(rank)
    st.divider()
    st.markdown("### 📓 Notebook")
    st.session_state.notes = st.text_area(
        "Notes", value=st.session_state.notes, height=250, placeholder="Write your observations..."
    )
    play_music = st.toggle("🎵 Background Music", value=True)

dashboard_columns = st.columns(3)
dashboard_columns[0].metric("📂 Status", "Ready")
dashboard_columns[1].metric(
    "🚨 Current Case",
    st.session_state.case_data["case_number"] if st.session_state.case_started else "None",
)
dashboard_columns[2].metric(
    "👥 Suspects",
    len(st.session_state.case_data["suspects"]) if st.session_state.case_started else 0,
)
st.divider()

if not st.session_state.case_started:
    render_start_screen(background_base64)
    _, start_column, _ = st.columns([2, 1, 2])
    with start_column:
        if st.button("🚔 START INVESTIGATION", use_container_width=True):
            reset_case_state(generate_case())
            st.rerun()
    st.stop()

case = st.session_state.case_data
if play_music:
    play_background_music()

st.image(st.session_state.crime_scene_image, use_container_width=True, caption="🧸 AI-generated crime scene")
st.divider()
st.markdown("## 📂 Case File")

victim_column, details_column = st.columns(2)
with victim_column:
    image_column, information_column = st.columns([1, 2])
    with image_column:
        st.image(st.session_state.victim_image, width=250)
    with information_column:
        info_card(
            "👤 Victim",
            f"<p><b>{case['victim']}</b></p><hr><p>📍 <b>Location:</b> {case['location']}</p>"
            f"<p>🕒 <b>Time:</b> {case['time']}</p>",
        )
with details_column:
    info_card(
        "☠ Crime Details",
        f"<p>🌧 <b>Weather:</b> {case['weather']}</p><p>💀 <b>Cause:</b> {case['cause_of_death']}</p>"
        f"<hr><h4>🎯 Mission</h4><p>{case['mission']}</p>",
        "red",
    )

investigation_column, evidence_column = st.columns([2, 1])
with investigation_column:
    st.markdown("## 🔍 Crime Scene Investigation")
    if st.button("🔎 Investigate Crime Scene", use_container_width=True):
        with st.spinner("Searching for clues..."):
            st.session_state.crime_scene = investigate_scene(case)
            st.session_state.evidence = case.get("evidence", [])
    if st.session_state.crime_scene:
        info_card("🧸 Crime Scene Report", st.session_state.crime_scene)

with evidence_column:
    st.markdown("## 📁 Evidence Board")
    if st.session_state.evidence:
        for clue in st.session_state.evidence:
            info_card("🧸 Evidence", f"<p>{clue}</p>")
    else:
        st.warning("No evidence collected yet.")

st.divider()
st.markdown("## 📊 Investigation Progress")
statistics = st.columns(4)
statistics[0].metric("👥 Suspects", len(case["suspects"]))
statistics[1].metric("📁 Evidence", len(st.session_state.evidence))
statistics[2].metric("💬 Conversations", len(st.session_state.chat_history))
statistics[3].metric("🏆 Solved", "No")

st.divider()
st.markdown("## 👥 Suspects")
suspect_columns = st.columns(2)
for index, suspect in enumerate(case["suspects"]):
    with suspect_columns[index % 2], st.container(border=True):
        image_column, information_column = st.columns([1, 3])
        with image_column:
            st.image(ASSETS_DIR / "suspects" / f"suspect{(index % 4) + 1}.jpg", width=110)
        with information_column:
            status = SUSPECT_STATUSES[index % len(SUSPECT_STATUSES)]
            info_card(
                f"🕵️ {suspect['name']}",
                f"<p><b>{status}</b></p><p>🎂 <b>Age:</b> {suspect['age']}</p>"
                f"<p>💼 <b>Occupation:</b> {suspect['occupation']}</p>"
                f"<p>🧠 <b>Personality:</b> {suspect['personality']}</p>",
            )
            if st.button("💬 Interrogate", key=f"talk_{index}", use_container_width=True):
                st.session_state.selected_suspect = suspect["name"]
                st.rerun()

st.divider()
if selected_suspect := st.session_state.selected_suspect:
    st.markdown(f"# 🕵️ Interrogation Room\n### Currently Questioning: **{selected_suspect}**")
    history = st.session_state.chat_history.setdefault(selected_suspect, [])
    question = st.text_area("Ask your question", height=120, placeholder="Where were you during the murder?")
    if st.button("📤 Send", use_container_width=True) and question.strip():
        with st.spinner("Suspect is answering..."):
            answer = talk_to_suspect(case, selected_suspect, question)
        history.extend((("You", question), (selected_suspect, answer)))
        st.rerun()
    st.markdown("# 💬 Interrogation Transcript\n---")
    for sender, message in history:
        with st.chat_message("user" if sender == "You" else "assistant"):
            st.write(message)
else:
    st.info("👆 Select a suspect to start questioning.")

st.divider()
st.markdown("# ⚖️ Solve the Case")
st.write("Think carefully before accusing someone.")
suspect_names = [suspect["name"] for suspect in case["suspects"]]
accused = st.selectbox("👤 Choose the Murderer", suspect_names)
reason = st.text_area("📝 Explain your reasoning", height=170, placeholder="Why do you think this suspect is the killer?")

if st.button("🚨 Submit Final Report", use_container_width=True):
    if not reason.strip():
        st.warning("Please write your reasoning first.")
    else:
        with st.spinner("Detective AI is analyzing your report..."):
            report = judge_case(case, accused, reason)
        st.markdown("# 🧠 Detective Report")
        st.success(report)
        if accused == case["killer"]:
            st.balloons()
            st.success("🏆 CASE SOLVED!")
            certificate = f"""CRIMSON CLUES AI\n\nDETECTIVE CERTIFICATE\n\nThis certifies that the detective successfully solved\n\nCase Number: {case['case_number']}\nMurderer: {case['killer']}\nDetective Rank: {rank}\nDetective Score: {score}/10\nDate: {datetime.now():%d-%m-%Y}\n\nCongratulations!\n"""
            st.download_button("📜 Download Detective Certificate", certificate, f"Detective_Certificate_{case['case_number']}.txt", "text/plain")
        else:
            st.error("❌ Wrong accusation!")
            st.markdown(f"The real murderer was:\n\n## 🔪 {case['killer']}")

st.divider()
st.markdown("# 📊 Detective Dashboard")
score = detective_score()
dashboard = st.columns(4)
for column, icon, value, label in zip(
    dashboard,
    ("👥", "📁", "💬", "⭐"),
    (len(case["suspects"]), len(st.session_state.evidence), len(st.session_state.chat_history), f"{score}/10"),
    ("Suspects", "Evidence", "Interviews", "Detective Score"),
):
    with column:
        info_card(icon, f"<h1 style='color:#FFD700;'>{value}</h1><p>{label}</p>")

achievement_conditions = {
    "Crime Scene Investigator": bool(st.session_state.crime_scene),
    "Expert Interrogator": len(st.session_state.chat_history) >= 2,
    "Evidence Collector": len(st.session_state.evidence) >= 4,
    "Master Detective": score >= 8,
}
for achievement, earned in achievement_conditions.items():
    if earned and achievement not in st.session_state.achievements:
        st.session_state.achievements.append(achievement)

st.divider()
st.markdown("# 🏆 Achievements")
for achievement in st.session_state.achievements:
    st.success(f"🏅 {achievement}")

st.divider()
st.markdown("<div style='text-align:center;color:gray;'>🕵️ Crimson Clues AI<br>Version 1.2</div>", unsafe_allow_html=True)

import os
import json
import random
import urllib.parse

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash"

# -----------------------------
# Generate New Case
# -----------------------------
def generate_case():

    with open("cases.json", "r", encoding="utf-8") as file:

        cases = json.load(file)

    return random.choice(cases)

# -----------------------------
# Talk To Suspect
# -----------------------------
def talk_to_suspect(case_data, suspect_name, question):

    prompt = f"""
You are roleplaying as this suspect.

Suspect:
{suspect_name}

Complete hidden case:

{json.dumps(case_data, indent=2)}

Rules:

Stay in character.

Never reveal who the killer is.

If you ARE the killer,
lie naturally.

If innocent,
answer honestly.

Keep answers under 80 words.

Question:

{question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


# -----------------------------
# Investigate Scene
# -----------------------------
def investigate_scene(case_data):

    prompt = f"""
You are describing a murder scene.

Case:

{json.dumps(case_data, indent=2)}

Reveal only observations.

Do NOT reveal the murderer.

Keep it under 150 words.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


# -----------------------------
# Judge Final Answer
# -----------------------------
def judge_case(case_data, accused, reason):

    prompt = f"""
You are the judge.

Hidden case:

{json.dumps(case_data, indent=2)}

Player accused:

{accused}

Reason:

{reason}

Explain

1. Correct or Wrong

2. Why

3. Detective score out of 10

Keep under 200 words.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


# -----------------------------
# Generate Crime Scene Image
# -----------------------------
def generate_crime_scene_image(case_data):

    prompt = f"""
Cinematic detective crime scene.

Location: {case_data['location']}

Weather: {case_data['weather']}

Cause of death: {case_data['cause_of_death']}

Dark realistic atmosphere.

Police tape.

Police lights.

Ultra realistic.

8k.

Highly detailed.

No text.
"""

    prompt = urllib.parse.quote(prompt)

    return f"https://image.pollinations.ai/prompt/{prompt}"

# -----------------------------
# Victim Portrait
# -----------------------------
def generate_victim_image(case_data):

    prompt = f"""
Ultra realistic portrait.

Victim.

Name: {case_data['victim']}

Detective style.

Cinematic lighting.

Realistic face.

8k.

No text.
"""

    prompt = urllib.parse.quote(prompt)

    return f"https://image.pollinations.ai/prompt/{prompt}"


# -----------------------------
# Suspect Portrait
# -----------------------------

def generate_suspect_image(suspect):

    prompt = f"""
Portrait of {suspect['name']},
{suspect['occupation']},
{suspect['personality']},
cinematic detective,
realistic face
"""

    prompt = urllib.parse.quote(prompt)

    seed = abs(hash(suspect["name"])) % 100000

    return (
        f"https://image.pollinations.ai/prompt/{prompt}"
        f"?width=512&height=512&seed={seed}&nologo=true"
    )

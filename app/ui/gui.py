
import streamlit as st
import toml
import os
import uuid
import time  # For measuring generation time
from app.services.voice import VoiceService
from app.services.subtitle import SubtitleService

# Function to load translations
def load_translation(lang):
    try:
        with open(f"locales/{lang}.toml", "r", encoding="utf-8") as f:
            return toml.load(f)
    except FileNotFoundError:
        st.error(f"Translation file for {lang} not found.")
        return {}

# Load configuration
if os.path.exists("config.toml"):
    config = toml.load("config.toml")
else:
    config = toml.load("config.example.toml")

# Initialize services
voice_service = VoiceService(config)
subtitle_service = SubtitleService(config)

def set_language():
    st.session_state.lang = st.session_state.lang_selector

# Language selection
if 'lang' not in st.session_state:
    st.session_state.lang = 'zh_TW'  # Default language

# Initialize storage for generated task results
if 'task' not in st.session_state:
    st.session_state['task'] = None

lang_data = load_translation(st.session_state.lang)

# Create a row for title and language selection
title_col, lang_col = st.columns([0.8, 0.2])

with lang_col:
    selected_lang = st.selectbox(
        lang_data["app"]["language_select_label"],
        options=['zh_TW', 'en'],
        format_func=lambda x: '繁體中文' if x == 'zh_TW' else 'English',
        key='lang_selector',
        label_visibility="collapsed",
        on_change=set_language,
        index=0 if st.session_state.lang == 'zh_TW' else 1 # Set initial index based on current language
    )

st.set_page_config(layout="wide", page_title=lang_data["app"]["page_title"], page_icon="🎤")

with title_col:
    st.title(lang_data["app"]["title"])
st.write(lang_data["app"]["description"])
st.markdown("--- ")

col_input, col_settings = st.columns(2)

with col_input:
    st.header(lang_data["app"]["input_section_header"])
    text_input = st.text_area(lang_data["app"]["input_text_area_label"], height=350, key="text_input_main")

with col_settings:
    st.header(lang_data["app"]["settings_section_header"])

    st.subheader(lang_data["app"]["voice_selection_subheader"])
    voice_options = list(config["voices"].keys())
    selected_voice_name = st.selectbox(lang_data["app"]["voice_select_label"], voice_options, key="voice_select_main")
    voice_name = config["voices"][selected_voice_name]["name"]

    st.subheader(lang_data["app"]["voice_params_subheader"])
    col_rate, col_pitch, col_volume = st.columns(3)
    with col_rate:
        rate = st.slider(lang_data["app"]["rate_slider_label"], -100, 100, 0, key="rate_slider_main")
    with col_pitch:
        pitch = st.slider(lang_data["app"]["pitch_slider_label"], -100, 100, 0, key="pitch_slider_main")
    with col_volume:
        volume = st.slider(lang_data["app"]["volume_slider_label"], -100, 100, 0, key="volume_slider_main")

    st.subheader(lang_data["app"]["subtitle_settings_subheader"])
    max_line_length = st.slider(lang_data["app"]["max_line_length_slider_label"], 5, 20, 10, key="line_length_slider_main")

st.markdown("--- ")

generate_clicked = st.button(
    lang_data["app"]["generate_button_label"],
    key="generate_button_main",
    use_container_width=True,
)

if generate_clicked:
    if text_input:
        start_time = time.time()

        task_id = str(uuid.uuid4())
        output_dir = os.path.join("task", task_id)
        os.makedirs(output_dir, exist_ok=True)

        with st.spinner(lang_data["app"]["generating_spinner"]):
            try:
                audio_file_path, word_boundaries = voice_service.synthesize(
                    text_input, voice_name, rate, pitch, volume, output_dir
                )

                srt_content = subtitle_service.generate_srt(word_boundaries, max_line_length)
                srt_file_path = os.path.join(output_dir, "output.srt")
                with open(srt_file_path, "w", encoding="utf-8") as f:
                    f.write(srt_content)

                end_time = time.time()

                st.session_state["task"] = {
                    "output_dir": output_dir,
                    "audio_file_path": audio_file_path,
                    "srt_file_path": srt_file_path,
                    "srt_content": srt_content,
                    "gen_time": end_time - start_time,
                }

            except Exception as e:
                st.error(f"{lang_data['app']['error_message']} {e}")
                st.session_state["task"] = None
    else:
        st.warning(lang_data["app"]["warning_no_text"])
        st.session_state["task"] = None

task = st.session_state.get("task")
if task:
    st.success(
        f"{lang_data['app']['generation_success']}{task['gen_time']:.2f} {lang_data['app']['seconds']}"
    )

    st.header(lang_data["app"]["output_section_header"])

    st.subheader(lang_data["app"]["audio_output_subheader"])
    st.audio(task["audio_file_path"])

    st.subheader(lang_data["app"]["srt_output_subheader"])
    st.text_area(
        lang_data["app"]["srt_content_preview"],
        task["srt_content"],
        height=200,
        key="srt_output_main",
    )

    st.subheader(lang_data["app"]["download_files_subheader"])
    col_dl_audio, col_dl_srt = st.columns(2)
    with col_dl_audio:
        with open(task["audio_file_path"], "rb") as f:
            st.download_button(
                lang_data["app"]["download_audio_button"],
                f,
                file_name=os.path.basename(task["audio_file_path"]),
                key="download_audio_main",
                use_container_width=True,
            )
    with col_dl_srt:
        with open(task["srt_file_path"], "r", encoding="utf-8") as f:
            st.download_button(
                lang_data["app"]["download_srt_button"],
                f,
                file_name=os.path.basename(task["srt_file_path"]),
                key="download_srt_main",
                use_container_width=True,
            )

    st.info(f"{lang_data['app']['files_saved_info']}`{task['output_dir']}`")

st.markdown("---")
st.markdown("<p style=\"text-align: center; color: grey;\">v1.0.1</p>", unsafe_allow_html=True)

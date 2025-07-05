import streamlit as st
import toml
import os
import uuid
import time
from pathlib import Path
from app.services.voice import VoiceService
from app.services.subtitle import SubtitleService

# Configure page settings
st.set_page_config(
    page_title="Text to Speech & Subtitle Generator",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load translations


def load_translation(lang):
    """Load translation file for the specified language."""
    try:
        with open(f"locales/{lang}.toml", "r", encoding="utf-8") as f:
            return toml.load(f)
    except FileNotFoundError:
        st.error(f"Translation file for {lang} not found.")
        return {}

# Language management


def set_language():
    """Set the language from the selector."""
    st.session_state.lang = st.session_state.lang_selector


def get_language_display_name(lang_code):
    """Get display name for language code."""
    language_names = {
        'zh_TW': '繁體中文',
        'en': 'English'
    }
    return language_names.get(lang_code, lang_code)


# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = 'zh_TW'  # Default language

if 'task' not in st.session_state:
    st.session_state['task'] = None

if 'generation_in_progress' not in st.session_state:
    st.session_state['generation_in_progress'] = False

# Load configuration
config_path = "config.toml" if os.path.exists(
    "config.toml") else "config.example.toml"
config = toml.load(config_path)

# Initialize services
voice_service = VoiceService(config)
subtitle_service = SubtitleService(config)

# Load translations
lang_data = load_translation(st.session_state.lang)

# SIDEBAR SETTINGS
st.sidebar.header("🌐 " + lang_data["app"]["language_select_label"])
selected_lang = st.sidebar.selectbox(
    label="Language",
    options=['zh_TW', 'en'],
    format_func=get_language_display_name,
    key='lang_selector',
    on_change=set_language,
    index=0 if st.session_state.lang == 'zh_TW' else 1,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Voice Settings in Sidebar
st.sidebar.header("🎙️ " + lang_data["app"]["voice_selection_subheader"])
voice_options = list(config["voices"].keys())
selected_voice_name = st.sidebar.selectbox(
    lang_data["app"]["voice_select_label"],
    voice_options,
    key="voice_select_main",
    help="Choose the voice that best fits your content"
)

# Display voice info
if selected_voice_name in config["voices"]:
    voice_info = config["voices"][selected_voice_name]
    st.sidebar.info(f"🎙️ Voice: {voice_info['name']}")

st.sidebar.markdown("---")

# Voice Parameters in Sidebar
st.sidebar.header("🎛️ " + lang_data["app"]["voice_params_subheader"])

rate = st.sidebar.slider(
    lang_data["app"]["rate_slider_label"],
    min_value=-50,
    max_value=50,
    value=0,
    step=5,
    key="rate_slider_main",
    help="Adjust speech speed: negative values slow down, positive values speed up"
)

pitch = st.sidebar.slider(
    lang_data["app"]["pitch_slider_label"],
    min_value=-50,
    max_value=50,
    value=0,
    step=5,
    key="pitch_slider_main",
    help="Adjust pitch: negative values lower pitch, positive values raise pitch"
)

volume = st.sidebar.slider(
    lang_data["app"]["volume_slider_label"],
    min_value=-50,
    max_value=50,
    value=0,
    step=5,
    key="volume_slider_main",
    help="Adjust volume: negative values decrease volume, positive values increase volume"
)

st.sidebar.markdown("---")

# Subtitle Settings in Sidebar
st.sidebar.header("📜 " + lang_data["app"]["subtitle_settings_subheader"])

max_line_length = st.sidebar.slider(
    lang_data["app"]["max_line_length_slider_label"],
    min_value=20,
    max_value=80,
    value=40,
    step=5,
    key="line_length_slider_main",
    help="Maximum characters per subtitle line for better readability"
)

preserve_punctuation = st.sidebar.checkbox(
    "Preserve punctuation in subtitles",
    value=True,
    key="preserve_punctuation",
    help="Keep punctuation marks in subtitle text"
)

st.sidebar.markdown("---")

# Version info in sidebar
st.sidebar.markdown("**🔧 Version:** v1.1.0")
st.sidebar.markdown(
    "**📚 [Documentation](https://github.com/sheng1111/text2srt_tts)**")

# MAIN CONTENT AREA
st.title("🎤 " + lang_data["app"]["title"])
st.markdown(lang_data["app"]["description"])

# Input Section
st.header("📝 " + lang_data["app"]["input_section_header"])

text_input = st.text_area(
    label=lang_data["app"]["input_text_area_label"],
    height=300,
    key="text_input_main",
    placeholder=lang_data["app"]["input_text_area_label"]
)

# Character count and status
col1, col2 = st.columns([3, 1])
with col1:
    char_count = len(text_input) if text_input else 0
    st.caption(f"📊 {char_count} characters")

with col2:
    if st.session_state.generation_in_progress:
        st.info("⏳ Processing...")
    elif text_input:
        st.success("✅ Ready")
    else:
        st.warning("⚠️ Enter text")

# Quick tips expander
with st.expander("💡 Tips for Better Results"):
    st.markdown("""
    - Use proper punctuation for natural speech pauses
    - Keep sentences clear and concise
    - Avoid excessive special characters
    - Test with shorter texts first for optimal results
    """)

# Generation Button
st.markdown("---")
generate_clicked = st.button(
    f"🎯 {lang_data['app']['generate_button_label']}",
    key="generate_button_main",
    use_container_width=True,
    type="primary",
    disabled=st.session_state.generation_in_progress
)

# Generation Logic
if generate_clicked:
    if text_input:
        st.session_state.generation_in_progress = True
        start_time = time.time()

        # Progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()

        task_id = str(uuid.uuid4())
        output_dir = os.path.join("task", task_id)
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Step 1: Voice synthesis
            status_text.text(lang_data["app"]["generating_spinner"])
            progress_bar.progress(25)

            voice_name = config["voices"][selected_voice_name]["name"]
            audio_file_path, word_boundaries = voice_service.synthesize(
                text_input, voice_name, rate, pitch, volume, output_dir
            )

            # Step 2: Subtitle generation
            status_text.text("🔄 Generating subtitles...")
            progress_bar.progress(75)

            srt_content = subtitle_service.generate_srt(
                word_boundaries,
                max_line_length,
                preserve_punctuation
            )
            srt_file_path = os.path.join(output_dir, "output.srt")
            with open(srt_file_path, "w", encoding="utf-8") as f:
                f.write(srt_content)

            # Step 3: Complete
            progress_bar.progress(100)
            status_text.text("✅ Generation complete!")

            end_time = time.time()

            st.session_state["task"] = {
                "output_dir": output_dir,
                "audio_file_path": audio_file_path,
                "srt_file_path": srt_file_path,
                "srt_content": srt_content,
                "gen_time": end_time - start_time,
                "voice_name": selected_voice_name,
                "settings": {
                    "rate": rate,
                    "pitch": pitch,
                    "volume": volume,
                    "max_line_length": max_line_length,
                    "preserve_punctuation": preserve_punctuation
                }
            }

            st.session_state.generation_in_progress = False
            st.rerun()

        except Exception as e:
            st.session_state.generation_in_progress = False
            st.error(f"❌ {lang_data['app']['error_message']} {e}")
            st.session_state["task"] = None

    else:
        st.warning(f"⚠️ {lang_data['app']['warning_no_text']}")

# Display Results
task = st.session_state.get("task")
if task and not st.session_state.generation_in_progress:
    st.markdown("---")
    st.header("🎉 " + lang_data["app"]["output_section_header"])

    # Success message
    st.success(f"""
    🎉 {lang_data['app']['generation_success']}
    **⏱️ Time:** {task['gen_time']:.2f} {lang_data['app']['seconds']}
    **🎙️ Voice:** {task['voice_name']}
    **📁 Location:** `{task['output_dir']}`
    """)

    # Results display
    col_audio, col_subtitle = st.columns([1, 1])

    with col_audio:
        st.subheader("🔊 " + lang_data["app"]["audio_output_subheader"])

        # Audio player
        st.audio(task["audio_file_path"])

        # Audio file info
        audio_path = Path(task["audio_file_path"])
        audio_size = audio_path.stat().st_size / 1024  # Size in KB
        st.caption(f"📊 File: {audio_path.name} ({audio_size:.1f} KB)")

    with col_subtitle:
        st.subheader("📜 " + lang_data["app"]["srt_output_subheader"])

        # SRT preview
        st.text_area(
            label="SRT Preview",
            value=task["srt_content"],
            height=200,
            key="srt_output_main",
            label_visibility="collapsed"
        )

        # SRT info
        srt_lines = len(
            [line for line in task["srt_content"].split('\n') if line.strip()])
        st.caption(f"📊 Total lines: {srt_lines}")

    # Download section
    st.subheader("⬇️ " + lang_data["app"]["download_files_subheader"])

    col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 1])

    with col_dl1:
        with open(task["audio_file_path"], "rb") as f:
            st.download_button(
                label=f"📥 {lang_data['app']['download_audio_button']}",
                data=f,
                file_name=os.path.basename(task["audio_file_path"]),
                mime="audio/wav" if task["audio_file_path"].endswith(
                    '.wav') else "audio/mp3",
                key="download_audio_main",
                use_container_width=True
            )

    with col_dl2:
        st.download_button(
            label=f"📝 {lang_data['app']['download_srt_button']}",
            data=task["srt_content"],
            file_name=os.path.basename(task["srt_file_path"]),
            mime="text/plain",
            key="download_srt_main",
            use_container_width=True
        )

    with col_dl3:
        if st.button("🗑️ Clear Results", key="clear_results", use_container_width=True):
            st.session_state["task"] = None
            st.rerun()

    # Settings info
    st.info(f"""
    **🎛️ Settings Used:**
    Rate: {task['settings']['rate']}%, Pitch: {task['settings']['pitch']}%, Volume: {task['settings']['volume']}%
    Max Line Length: {task['settings']['max_line_length']} chars, Preserve Punctuation: {task['settings']['preserve_punctuation']}
    """)

import streamlit as st

from logger import logger
from languages import supported_languages
from translator import detect_source_language, translate


def main():
    """Entry point"""

    st.set_page_config(page_title="howcanisay.ai", page_icon=":studio_microphone:")

    main_container = st.container()
    _, center_column, _ = main_container.columns([1, 5, 1])

    center_column.title("How can I say...")

    source_text = center_column.text_area(
        "Text",
        placeholder="Type your text here...",
        max_chars=1000,
        key="source_text",
        label_visibility="hidden",
    )

    st.session_state.source_lang = detect_source_language(source_text)

    center_column.title("in")

    destination_language = center_column.selectbox(
        "Select Language", supported_languages, key="target_lang", label_visibility="hidden"
    )

    logger.debug(f"Selected destination language as {destination_language}")

    center_column.header("")

    center_column.button("Translate", on_click=translate, type="primary", use_container_width=True)

    center_column.divider()

    # with st.spinner("Translating the input..."):
    #     sleep(3)

    result_container = st.container()
    _, col2, _ = result_container.columns([1, 5, 1])

    if not st.session_state.source_lang:
        col2.error("Failed to detect source language")
        st.stop()

    col2.write(f"**Detected source language**: {st.session_state.source_lang} :thumbsup:")

    if "translation" not in st.session_state:
        st.session_state.translation = ""

    col2.markdown(f"**{st.session_state.translation}**")

    col2.audio(None, format="audio/mp3")

    st.divider()


if __name__ == "__main__":
    main()

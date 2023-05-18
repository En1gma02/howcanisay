import os

import openai
import streamlit as st

from logger import logger

openai.api_key = (
    os.getenv("OPENAI_API_KEY_HOWCANISAY_AI") or st.secrets["OPENAI_API_KEY_HOWCANISAY_AI"]
)


def detect_source_language(text: str) -> str:
    """Detect the language of source text

    :type text: str
    :param text: Source text to detect language
    :rtype: str
    :returns: Detected language of source text
    """

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Which language is '{text}' written in? Explain in 1 word.",
        temperature=0,
    )

    source_language = response["choices"][0]["text"].strip()
    logger.debug(f"Detected source language: {source_language}")

    return source_language


def translate() -> None:
    """Translate text and write result to translation session state variable"""

    text = st.session_state.source_text
    source_language = st.session_state.source_lang
    target_language = st.session_state.target_lang

    logger.debug(f"Source text: {text}")
    logger.debug(f"Source language: {source_language}")
    logger.debug(f"Target language: {target_language}")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant that translates {source_language} text to {target_language}.",
            },
            {
                "role": "user",
                "content": f"Translate the following {source_language} text to {target_language}: '{text}'.",
            },
        ],
        temperature=0,
    )

    st.session_state.translation = (
        response["choices"][0]["message"]["content"].strip().replace("'", "")
    )

    logger.debug(f"Translation: {st.session_state.translation}")

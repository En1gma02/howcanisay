import streamlit as st
import streamlit.components.v1 as components

from logger import logger
from languages import supported_languages
from translator import detect_source_language, translate


def get_audio():
    """Get audio to translate from user"""

    audio_script = """
    <html>
        <audio id="audioPlayer"></audio>
        <button id="startButton">Start Recording</button>
        <button id="stopButton">Stop Recording</button>
        <div id="audioContainer"></div>

        <script type="text/javascript">
        const audioPlayer = document.getElementById('audioPlayer');
        const startButton = document.getElementById('startButton');
        const stopButton = document.getElementById('stopButton');
        const audioContainer = document.getElementById('audioContainer');

        let mediaRecorder;
        let recordedChunks = [];

        // Request access to the user's microphone
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            // Create a MediaRecorder instance
            mediaRecorder = new MediaRecorder(stream);

            // Set the audio element as the source of the recorded audio
            audioPlayer.srcObject = stream;

            // Listen for dataavailable event to collect recorded audio data
            mediaRecorder.addEventListener('dataavailable', function(event) {
                recordedChunks.push(event.data);
            });

            // Listen for startButton click event to start recording
            startButton.addEventListener('click', function() {
                recordedChunks = []; // Clear the previously recorded data
                mediaRecorder.start();
                console.log('Recording started...');
            });

            // Listen for stopButton click event to stop recording
            stopButton.addEventListener('click', function() {
                mediaRecorder.stop();
                console.log('Recording stopped...');
            });

            // Listen for mediaRecorder stop event to handle the recorded data
            mediaRecorder.addEventListener('stop', function() {
                // Create a Blob from the recorded chunks
                const audioBlob = new Blob(recordedChunks, { type: 'audio/webm' });

                const audioElement = document.createElement('audio');
                audioElement.controls = true;
                const audioURL = URL.createObjectURL(audioBlob);
                audioElement.src = audioURL;
                audioContainer.appendChild(audioElement);
                audioElement.play();
            });
        })
        .catch(function(error) {
            // Handle error when microphone access is denied or not available
            console.error('Error accessing microphone:', error);
        });
    </script>
    </html>
    """

    components.html(audio_script)


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

    center_column.button(
        ":studio_microphone: Say something to translate...",
        on_click=get_audio,
        use_container_width=True,
    )

    st.session_state.source_lang = detect_source_language(source_text)

    center_column.title("in")

    destination_language = center_column.selectbox(
        "Select Language",
        sorted(supported_languages.keys()),
        key="target_lang",
        label_visibility="hidden",
    )

    logger.debug(f"Selected destination language as {destination_language}")

    center_column.header("")

    center_column.button("Translate", on_click=translate, type="primary", use_container_width=True)

    center_column.divider()

    result_container = st.container()
    _, col2, _ = result_container.columns([1, 5, 1])

    if not st.session_state.source_lang:
        col2.error("Failed to detect source language")
        st.stop()

    col2.write(f"**Detected source language**: {st.session_state.source_lang} :thumbsup:")

    if "translation" not in st.session_state:
        st.session_state.translation = ""

    col2.markdown(f"**{st.session_state.translation}**")

    if st.session_state.translation:
        col2.audio("translation.mp3", format="audio/mp3")
        st.divider()

        footer_left, footer_right = st.columns(2)
        footer_left.markdown(
            "**You can find the code on my [GitHub](https://github.com/coskundeniz) page.**"
        )

        with footer_right:
            footer_right.write("**If you like this app, please consider to**")
            components.html(
                '<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="coskundeniz" data-color="#ff7800" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#FFDD00" ></script>'
            )


if __name__ == "__main__":
    main()

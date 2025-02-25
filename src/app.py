import asyncio
import io

import streamlit as st
from dotenv import load_dotenv

from graph.state import State
from graph.workflow import workflow
from utils.whisper_transcription import whisper_transcription

load_dotenv()

st.title("Asistente de migración")

initial_text = """
            Hola, ¿en qué puedo ayudarte hoy? \n
            How can I help you today?\n
            كيف يمكنني مساعدتك اليوم؟\n
            Comment puis-je vous aider aujourd’hui ?\n
        """


async def chat(messages: list):
    app = workflow()
    comment = State({"messages": messages})
    return await app.ainvoke(comment)


with st.sidebar:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Volver", type="primary"):
            st.markdown(
                '<meta http-equiv="refresh" content="0;URL=https://asistentemigracionyasilo.vercel.app/index.html">',
                unsafe_allow_html=True,
            )

    with col2:
        if st.button("Limpiar", type="secondary"):
            st.session_state.messages = [{"role": "assistant", "content": initial_text}]
    audio_value = st.audio_input("Record a voice message")

    if audio_value:
        audio_bio = io.BytesIO(audio_value.read())
        audio_bio.name = "audio.webm"

        text_input = whisper_transcription(audio_bio)

        st.session_state.messages.append({"role": "user", "content": str(text_input)})
        answer = asyncio.run(chat(st.session_state.messages))
        st.session_state.messages.append(
            {"role": "assistant", "content": answer.get("messages", [])[-1].content}
        )
        # st.write(f"Texto transcrito: {str(text_input)}")


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": initial_text}]


if text_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": text_input})
    answer = asyncio.run(chat(st.session_state.messages))
    st.session_state.messages.append(
        {"role": "assistant", "content": answer.get("messages", [])[-1].content}
    )


for message in st.session_state.messages:
    with st.chat_message(message.get("role") or "ai"):
        st.write(message.get("content"))

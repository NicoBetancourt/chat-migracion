import asyncio

import streamlit as st
from dotenv import load_dotenv

from graph.state import State
from graph.workflow import workflow

load_dotenv()

st.title("Asistente de migración")

# if "file" not in st.session_state:
#     st.session_state.file = None
# # Inicializa las variables en session_state si no existen
# if "file_uploaded" not in st.session_state:
#     st.session_state.file_uploaded = False


with st.sidebar:
    # st.markdown("### Subir archivo")
    # file = st.file_uploader("Upload a file", type=["pdf"])
    if st.button("Limpiar", type="primary"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Cómo puedo ayudarte hoy?"}
        ]


if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Cómo puedo ayudarte hoy?"}
    ]


async def chat(messages: list):
    app = workflow()
    comment = State({"messages": messages})
    return await app.ainvoke(comment)


if text_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": text_input})
    answer = asyncio.run(chat(st.session_state.messages))
    st.session_state.messages.append(
        {"role": "assistant", "content": answer.get("messages", [])[-1].content}
    )


for message in st.session_state.messages:
    with st.chat_message(message.get("role") or "ai"):
        st.write(message.get("content"))

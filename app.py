# import streamlit as st
# import os
# import json
# import random
# from datetime import datetime
# import chromadb
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
# from llama_index.vector_stores.chroma import ChromaVectorStore
# from llama_index.embeddings.fastembed import FastEmbedEmbedding
# from llama_index.llms.groq import Groq
# from llama_index.core.memory import ChatMemoryBuffer

# DATA_DIR = "data"
# PERSIST_DIR = "./chroma_db"
# APPOINTMENT_FILE = "appointments.json"

# DOCTORS = [
# "Dr. Kati L. Matthiesson",
# "Associate Professor Niloufar (Nellie) Torkamani",
# "Dr. Fiona Inchley",
# "Dr. Ricky Arenson",
# "Dr. Claudia Ashkar",
# "Dr. Jianbin Liu",
# "Dr. Ming Li Yee",
# "Dr. Renata Libianto",
# "Dr. Sylvia Xu",
# "Dr. Jonathan Cohen",
# "Dr. Michael Mond",
# "Dr. Belinda Hii"
# ]

# embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")

# st.set_page_config(
#     page_title="Baldur.health AI - RAG",
#     page_icon="assets/logo.png",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# st.markdown("""<style>
# .stChatMessage { display: flex; margin-bottom: 16px; }
# .stChatMessage.user { justify-content: flex-end; }
# .stChatMessage.user .stMarkdown {background-color: #DCF8C6;border-radius: 16px;padding: 10px 14px;max-width: 75%;margin-left: auto;}
# .stChatMessage.assistant { justify-content: flex-start; }
# .stChatMessage.assistant .stMarkdown {background-color: #F1F0F0;border-radius: 16px;padding: 10px 14px;max-width: 75%;}
# section[data-testid="stSidebar"] { display: none; }
# .centered { text-align: center; }
# </style>""", unsafe_allow_html=True)

# st.markdown('<div class="centered">', unsafe_allow_html=True)
# st.image("assets/baldur.health.png", width=260)
# st.markdown('<span style="color:#223f99; font-weight:600;">Name app :</span> baldur.health AI v3.0.1', unsafe_allow_html=True)
# st.markdown("**Baldur** helps you with medical knowledge and booking appointments.")
# st.markdown("</div>", unsafe_allow_html=True)

# st.divider()

# MODEL_DISPLAY = st.radio("Select Model",
#     ["meta/llama-3.1-8b-instant","openai/gpt-oss-120b","qwen/qwen3-32b"],
#     horizontal=True
# )

# MODEL_MAP = {
#     "meta/llama-3.1-8b-instant": "llama-3.1-8b-instant",
#     "openai/gpt-oss-120b": "llama-3.3-70b-versatile",
#     "qwen/qwen3-32b": "qwen/qwen3-32b"
# }

# llm = Groq(model=MODEL_MAP[MODEL_DISPLAY], api_key=st.secrets["GROQ_API_KEY"], temperature=0.2)

# Settings.llm = llm
# Settings.embed_model = embed_model
# Settings.chunk_size = 512
# Settings.chunk_overlap = 64

# @st.cache_resource
# def get_index():
#     if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
#         return None
#     chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)
#     chroma_collection = chroma_client.get_or_create_collection("baldur_rag")
#     vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
#     storage_context = StorageContext.from_defaults(vector_store=vector_store)
#     if len(chroma_collection.get()["ids"]) > 0:
#         index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
#     else:
#         documents = SimpleDirectoryReader(DATA_DIR).load_data()
#         index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, show_progress=True)
#     return index

# index = get_index()

# if index:
#     memory = ChatMemoryBuffer.from_defaults(token_limit=2000)
#     chat_engine = index.as_chat_engine(chat_mode="context",memory=memory,similarity_top_k=4,
#     system_prompt="You are Baldur.health AI")
# else:
#     chat_engine = None

# def load_appointments():
#     if not os.path.exists(APPOINTMENT_FILE):
#         return []
#     try:
#         with open(APPOINTMENT_FILE, "r", encoding="utf-8") as f:
#             data = f.read().strip()
#             if not data:
#                 return []
#             return json.loads(data)
#     except:
#         return []

# def save_appointment(data):
#     appointments = load_appointments()
#     appointments.append(data)
#     with open(APPOINTMENT_FILE, "w", encoding="utf-8") as f:
#         json.dump(appointments, f, ensure_ascii=False, indent=2)

# def find_appointment(name):
#     return [a for a in load_appointments() if a["name"].lower()==name.lower()]

# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "appointment_state" not in st.session_state:
#     st.session_state.appointment_state = None

# for msg in st.session_state.messages:
#     avatar = "assets/user.webp" if msg["role"] == "user" else "assets/bot.png"
#     with st.chat_message(msg["role"], avatar=avatar):
#         st.markdown(msg["content"])

# if user_input := st.chat_input("Ask Baldur about your health..."):
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     with st.chat_message("user", avatar="assets/user.webp"):
#         st.markdown(user_input)

#     with st.chat_message("assistant", avatar="assets/bot.png"):
#         final_response=""

#         if "book" in user_input.lower() or "đặt lịch" in user_input.lower():
#             st.session_state.appointment_state="ask_name"
#             final_response="Please tell me your full name."

#         elif st.session_state.appointment_state=="check_name":
#             results=find_appointment(user_input)
#             if results:
#                 msg="Your appointments:\n"
#                 for r in results:
#                     msg+=f"- {r['issue']} | {r['time']} | Dr: {r['doctor']}\n"
#                 final_response=msg
#             else:
#                 st.session_state.appointment_state="offer_booking"
#                 final_response="No appointment found. Would you like to book one?"

#         elif st.session_state.appointment_state=="offer_booking":
#             if user_input.lower() in ["yes","y","ok","có"]:
#                 st.session_state.appointment_state="ask_name"
#                 final_response="Great. Please tell me your full name."
#             else:
#                 final_response="Okay, let me know if you need anything else."
#                 st.session_state.appointment_state=None

#         elif st.session_state.appointment_state=="ask_name":
#             st.session_state.temp_name=user_input
#             st.session_state.appointment_state="ask_age"
#             final_response="How old are you?"

#         elif st.session_state.appointment_state=="ask_age":
#             st.session_state.temp_age=user_input
#             st.session_state.appointment_state="ask_address"
#             final_response="What is your address?"

#         elif st.session_state.appointment_state=="ask_address":
#             st.session_state.temp_address=user_input
#             st.session_state.appointment_state="ask_phone"
#             final_response="Please provide your phone number."

#         elif st.session_state.appointment_state=="ask_phone":
#             st.session_state.temp_phone=user_input
#             st.session_state.appointment_state="ask_issue"
#             final_response="What issue would you like to consult?"

#         elif st.session_state.appointment_state=="ask_issue":
#             st.session_state.temp_issue=user_input
#             st.session_state.appointment_state="ask_time"
#             final_response="""Please choose your preferred time slot:

#         - Morning (08:00 – 11:00)
#         - Afternoon (13:00 – 17:00)
#         - Evening (18:00 – 20:00) """

#         elif st.session_state.appointment_state=="ask_time":
#             doctor=random.choice(DOCTORS)
#             appointment={
#                 "name":st.session_state.temp_name,
#                 "age":st.session_state.temp_age,
#                 "address":st.session_state.temp_address,
#                 "phone":st.session_state.temp_phone,
#                 "issue":st.session_state.temp_issue,
#                 "time":user_input,
#                 "doctor":doctor,
#                 "created_at":str(datetime.now())
#             }
#             save_appointment(appointment)
#             st.session_state.appointment_state=None
#             final_response=f"""Appointment booked successfully!

#                 Name: {appointment['name']}
#                 Doctor: {doctor}
#                 Time: {appointment['time']}
#                 Issue: {appointment['issue']}

#                 We will contact you soon."""

#         else:
#             if chat_engine:
#                 final_response=str(chat_engine.chat(user_input))
#             else:
#                 final_response=llm.complete(user_input).text

#         st.markdown(final_response)
#         st.session_state.messages.append({"role": "assistant", "content": final_response})


import streamlit as st
import os
import json
import random
from datetime import datetime
import chromadb
from streamlit_mic_recorder import mic_recorder
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.groq import Groq
from llama_index.core.memory import ChatMemoryBuffer

DATA_DIR = "data"
PERSIST_DIR = "./chroma_db"
APPOINTMENT_FILE = "appointments.json"

DOCTORS = [
"Dr. Kati L. Matthiesson",
"Associate Professor Niloufar (Nellie) Torkamani",
"Dr. Fiona Inchley",
"Dr. Ricky Arenson",
"Dr. Claudia Ashkar",
"Dr. Jianbin Liu",
"Dr. Ming Li Yee",
"Dr. Renata Libianto",
"Dr. Sylvia Xu",
"Dr. Jonathan Cohen",
"Dr. Michael Mond",
"Dr. Belinda Hii"
]

embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")

st.set_page_config(
    page_title="Baldur.health AI - RAG",
    page_icon="assets/logo.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
""", unsafe_allow_html=True)

st.markdown("""<style>
.stChatMessage { display: flex; margin-bottom: 16px; }
.stChatMessage.user { justify-content: flex-end; }
.stChatMessage.user .stMarkdown {background-color: #DCF8C6;border-radius: 16px;padding: 10px 14px;max-width: 75%;margin-left: auto;}
.stChatMessage.assistant { justify-content: flex-start; }
.stChatMessage.assistant .stMarkdown {background-color: #F1F0F0;border-radius: 16px;padding: 10px 14px;max-width: 75%;}
section[data-testid="stSidebar"] { width: 300px !important; }
.centered { text-align: center; }
.stChatMessage img {
    border-radius: 50% !important;
}
</style>""", unsafe_allow_html=True)

if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_conversation" not in st.session_state:
    cid = str(datetime.now().timestamp())
    st.session_state.current_conversation = cid
    st.session_state.conversations[cid] = []

with st.sidebar:
    st.image("assets/baldur.health.png", width=180)
    st.markdown("""
    <style>
    div[data-testid="stTextInput"] {
        position: relative;
    }
    div[data-testid="stTextInput"] input {
        padding-left: 36px !important;
        border-radius: 10px !important;
    }
    div[data-testid="stTextInput"]::before {
        content: "search";
        font-family: 'Material Symbols Outlined';
        position: absolute;
        left: 10px;
        top: 70%;
        font-weight: bold;
        transform: translateY(-50%);
        color: #223f99;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    search_query = st.text_input(
        label="",
        placeholder="Search conversations ..."
    )

    
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-top:10px;">
        <span onclick="
            const url = new URL(window.parent.location);
            url.searchParams.set('new_chat','1');
            window.parent.location.href = url.toString();
        "
        class="material-symbols-outlined"
        style="font-size:22px;color:#223f99;cursor:pointer;">
            edit_square
        </span>
        <span style="font-weight:500;">New Chat</span>
    </div>
    """, unsafe_allow_html=True)

    if "new_chat" in st.query_params:
        new_id = str(datetime.now().timestamp())
        st.session_state.current_conversation = new_id
        st.session_state.conversations[new_id] = []
        st.session_state.messages = []
        st.session_state.appointment_state = None
        st.session_state.pop("temp_name", None)
        st.session_state.pop("temp_age", None)
        st.session_state.pop("temp_address", None)
        st.session_state.pop("temp_phone", None)
        st.session_state.pop("temp_issue", None)
        st.query_params.clear()
        st.rerun()

    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-top:20px;">
        <span onclick="
            const url = new URL(window.parent.location);
            url.searchParams.set('voice_mode','1');
            window.parent.location.href = url.toString();
        "
        class="material-symbols-outlined"
        style="font-size:22px;color:#223f99;cursor:pointer;">
            graphic_eq
        </span>
        <span style="font-weight:500;">Voice mode</span>
    </div>
    """, unsafe_allow_html=True)

    # bắt sự kiện
    if "voice_mode" in st.query_params:
        st.query_params.clear()
        st.info("🎤 Speak now...")

        audio = mic_recorder(
            start_prompt="Start recording",
            stop_prompt="Stop recording",
            just_once=True
        )

        if audio:
            st.audio(audio["bytes"])
    
    st.markdown("---")
    
    st.markdown("""
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px;">
        <span class="material-symbols-outlined" style="font-size:20px;color:#223f99;">history</span>
        <span style="font-size:18px;font-weight:600;">History</span>
    </div>
    """, unsafe_allow_html=True)

    for cid, msgs in st.session_state.conversations.items():
        title = "chat conversation"
        for m in msgs:
            if m["role"] == "user":
                title = m["content"][:30]
                break
        if search_query.lower() in title.lower():
            if st.button(title, key=cid):
                st.session_state.current_conversation = cid
                st.session_state.messages = msgs.copy()

st.markdown('<div class="centered">', unsafe_allow_html=True)
st.image("assets/baldur.health.png", width=260)
st.markdown('<span style="color:#223f99; font-weight:600;">App name :</span> baldur.health AI v3.0.1', unsafe_allow_html=True)
st.markdown("**Baldur** helps you with medical knowledge and booking appointments.")
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

MODEL_DISPLAY = st.radio("Select Model",
    ["meta/llama-3.1-8b-instant","openai/gpt-oss-120b","qwen/qwen3-32b"],
    horizontal=True
)

MODEL_MAP = {
    "meta/llama-3.1-8b-instant": "llama-3.1-8b-instant",
    "openai/gpt-oss-120b": "llama-3.3-70b-versatile",
    "qwen/qwen3-32b": "qwen/qwen3-32b"
}

llm = Groq(model=MODEL_MAP[MODEL_DISPLAY], api_key=st.secrets["GROQ_API_KEY"], temperature=0.2)

Settings.llm = llm
Settings.embed_model = embed_model
Settings.chunk_size = 512
Settings.chunk_overlap = 64

@st.cache_resource
def get_index():
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        return None
    chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)
    chroma_collection = chroma_client.get_or_create_collection("baldur_rag")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    if len(chroma_collection.get()["ids"]) > 0:
        index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    else:
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, show_progress=True)
    return index

index = get_index()

if index:
    memory = ChatMemoryBuffer.from_defaults(token_limit=2000)
    # chat_engine = index.as_chat_engine(chat_mode="context",memory=memory,similarity_top_k=4,system_prompt="You are Baldur.health AI")
    chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    similarity_top_k=6,
    system_prompt = """
    You are Baldur.health AI, a safe medical assistant.

    STRICT RULES:
    - You can ONLY answer using the provided context from the knowledge base.
    - If the answer is not found in the context, you MUST say:
    "I don't have enough information in my knowledge base."
    - You are NOT allowed to use your own general knowledge.
    - NEVER guess or hallucinate.
    - NEVER invent medical facts, drugs, or treatments.
    - NEVER provide dangerous or unsafe medical advice.

    SAFETY:
    - If the user describes serious symptoms, suggest seeking medical help.
    - Do not provide diagnosis or prescriptions.

    STYLE:
    - Clear
    - Friendly
    - Professional
    - Concise
    """
    )
else:
    chat_engine = None

def load_appointments():
    if not os.path.exists(APPOINTMENT_FILE):
        return []
    try:
        with open(APPOINTMENT_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except:
        return []

def save_appointment(data):
    appointments = load_appointments()
    appointments.append(data)
    with open(APPOINTMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(appointments, f, ensure_ascii=False, indent=2)

def find_appointment(name):
    return [a for a in load_appointments() if a["name"].lower()==name.lower()]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "appointment_state" not in st.session_state:
    st.session_state.appointment_state = None

for msg in st.session_state.messages:
    avatar = "assets/user.webp" if msg["role"] == "user" else "assets/bot.png"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask Baldur about your health..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.conversations[st.session_state.current_conversation] = st.session_state.messages.copy()

    with st.chat_message("user", avatar="assets/user.webp"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="assets/bot.png"):
        final_response=""

        if "book" in user_input.lower() or "đặt lịch" in user_input.lower():
            st.session_state.appointment_state="ask_name"
            final_response="Please tell me your full name."

        elif st.session_state.appointment_state=="check_name":
            results=find_appointment(user_input)
            if results:
                msg="Your appointments:\n"
                for r in results:
                    msg+=f"- {r['issue']} | {r['time']} | Dr: {r['doctor']}\n"
                final_response=msg
            else:
                st.session_state.appointment_state="offer_booking"
                final_response="No appointment found. Would you like to book one?"

        elif st.session_state.appointment_state=="offer_booking":
            if user_input.lower() in ["yes","y","ok","có"]:
                st.session_state.appointment_state="ask_name"
                final_response="Great. Please tell me your full name."
            else:
                final_response="Okay, let me know if you need anything else."
                st.session_state.appointment_state=None

        elif st.session_state.appointment_state=="ask_name":
            st.session_state.temp_name=user_input
            st.session_state.appointment_state="ask_age"
            final_response="How old are you?"

        elif st.session_state.appointment_state=="ask_age":
            st.session_state.temp_age=user_input
            st.session_state.appointment_state="ask_address"
            final_response="What is your address?"

        elif st.session_state.appointment_state=="ask_address":
            st.session_state.temp_address=user_input
            st.session_state.appointment_state="ask_phone"
            final_response="Please provide your phone number."

        elif st.session_state.appointment_state=="ask_phone":
            st.session_state.temp_phone=user_input
            st.session_state.appointment_state="ask_issue"
            final_response="What issue would you like to consult?"

        elif st.session_state.appointment_state=="ask_issue":
            st.session_state.temp_issue=user_input
            st.session_state.appointment_state="ask_time"
            final_response="""Please choose your preferred time slot:

                - Morning (08:00 – 11:00)
                - Afternoon (13:00 – 17:00)
                - Evening (18:00 – 20:00)"""

        elif st.session_state.appointment_state=="ask_time":
            doctor=random.choice(DOCTORS)
            appointment={
                "name":st.session_state.temp_name,
                "age":st.session_state.temp_age,
                "address":st.session_state.temp_address,
                "phone":st.session_state.temp_phone,
                "issue":st.session_state.temp_issue,
                "time":user_input,
                "doctor":doctor,
                "created_at":str(datetime.now())
            }
            save_appointment(appointment)
            st.session_state.appointment_state=None
            final_response=f"""Appointment booked successfully!

                Name: {appointment['name']}
                Doctor: {doctor}
                Time: {appointment['time']}
                Issue: {appointment['issue']}

                We will contact you soon."""

        else:
            if chat_engine:
                final_response=str(chat_engine.chat(user_input))
            else:
                final_response=llm.complete(user_input).text

        st.markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        st.session_state.conversations[st.session_state.current_conversation] = st.session_state.messages.copy()
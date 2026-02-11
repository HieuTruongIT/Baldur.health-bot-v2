import streamlit as st
import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

st.set_page_config(
    page_title="Baldur.health AI - RAG",
    page_icon="assets/logo.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    .stChatMessage { display: flex; margin-bottom: 16px; }
    .stChatMessage.user { justify-content: flex-end; }
    .stChatMessage.user .stMarkdown {
        background-color: #DCF8C6;
        border-radius: 16px;
        padding: 10px 14px;
        max-width: 75%;
        text-align: left;
        margin-left: auto;
    }
    .stChatMessage.assistant { justify-content: flex-start; }
    .stChatMessage.assistant .stMarkdown {
        background-color: #F1F0F0;
        border-radius: 16px;
        padding: 10px 14px;
        max-width: 75%;
        text-align: left;
    }
    section[data-testid="stSidebar"] { display: none; }
    .centered { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="centered">', unsafe_allow_html=True)

st.image("assets/baldur.health.png", width=280)

st.markdown("**Name app :**  baldur.health AI v2")
st.markdown("<small>**Model name :** Running on llama-3.1-8b-instant</small>", unsafe_allow_html=True)

st.markdown("**Baldur** is focused on lifting healthcare outcomes for all through the adoption of new technologies.")

st.markdown("</div>", unsafe_allow_html=True)




EMBED_MODEL = "BAAI/bge-small-en-v1.5"
DATA_DIR = "data"
PERSIST_DIR = "./chroma_db"

llm = Groq(
    model="llama-3.1-8b-instant", 
    api_key=st.secrets["GROQ_API_KEY"],
    temperature=0.2
)


embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)

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
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            storage_context=storage_context
        )
    else:
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )
    return index

index = get_index()

if index:
    query_engine = index.as_chat_engine(
        chat_mode="condense_question",
        similarity_top_k=4
    )
else:
    query_engine = None

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask Baldur about your health..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Baldur Thinking..."):
            try:
                if query_engine is None:
                    st.warning("data folder/empty")
                else:
                    response = query_engine.chat(user_input)
                    st.markdown(response.response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response.response}
                    )
            except Exception as e:
                st.error(str(e))

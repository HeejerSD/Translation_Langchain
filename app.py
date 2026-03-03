import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import os


os.environ["NVIDIA_API_KEY"] = "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"

llm = ChatNVIDIA(model="meta/llama-3.1-8b-instruct")

st.set_page_config(page_title="Translator", page_icon="🔵", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
}

.card {
    background-color: #E3F2FD;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.1);
}

.title {
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    color: #1E3A8A;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    color: #1E3A8A;
    margin-bottom: 10px;
}

.section-title {
    color: #1E3A8A;
    font-size: 20px;
    margin-top: 15px;
}

.result-box {
    background-color: #DBEAFE;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #3B82F6;
    font-size: 18px;
    margin-top: 20px;
}

.stButton>button {
    background-color: #1E3A8A;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #2563EB;
    color: white;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<div class='title'>Language Translator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Translation</div>", unsafe_allow_html=True)


with st.container():
    

    st.markdown("<div class='section-title'>From Language</div>", unsafe_allow_html=True)
    from_language = st.text_input("", "English")

    st.markdown("<div class='section-title'>To Language</div>", unsafe_allow_html=True)
    to_language = st.text_input("", "French")

    st.markdown("<div class='section-title'>Text to Translate</div>", unsafe_allow_html=True)
    text_to_translate = st.text_area("", height=120)

    col1, col2, col3 = st.columns([1,0.5,1])

    with col2:
        translate_clicked = st.button("Translate")

    if translate_clicked:

        if text_to_translate.strip() == "":
            st.warning("Please enter text to translate.")
        else:
            prompt = ChatPromptTemplate.from_template(
                """You are a professional translator.
                Translate the following from {from_language} to {to_language}.
                Provide only the translated text:
                {text}"""
            )

            chain = prompt | llm

            full_response = ""
            placeholder = st.empty()

            for chunk in chain.stream({
                "from_language": from_language,
                "to_language": to_language,
                "text": text_to_translate
            }):
                if chunk.content:
                    full_response += chunk.content
                    placeholder.markdown(
                        f"<div class='result-box'>{full_response}</div>",
                        unsafe_allow_html=True
                    )

    st.markdown("</div>", unsafe_allow_html=True)
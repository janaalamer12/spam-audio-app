import os
import re
import pickle
import tempfile
import nltk
import streamlit as st
import whisper
from nltk.corpus import stopwords

# Download stopwords
#nltk.download('stopwords')
import whisper
asr_model = whisper.load_model("base")  # ✅ This is valid *ONLY* with openai-whisper


# Load classifier model and vectorizer
with open("model_nb.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# ==================== Helper ====================
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    stop_words = set(stopwords.words("english"))
    return ' '.join([word for word in text.split() if word not in stop_words])

# ==================== UI ====================
st.set_page_config(page_title="Spam Classifier", layout="centered")
st.title("Spam Classifier from Text & Audio")

st.markdown("You can either enter a message or upload an audio clip to classify it as **Spam** or **Not Spam**.")

# ---------- Text Input ----------
st.subheader("📝 Manual Text Entry")
text_input = st.text_area("Write your message here:")

if text_input:
    cleaned = preprocess_text(text_input)
    vect = vectorizer.transform([cleaned])
    pred = model.predict(vect)[0]
    st.success("🟠 SPAM" if pred else "🟢 NOT SPAM")

# ---------- Audio Upload ----------
st.subheader("🎙️ Or Upload an Audio Clip")
audio_file = st.file_uploader("Upload a file (mp3 / wav / m4a)", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    try:
        # Save to a temporary file with original extension
        suffix = os.path.splitext(audio_file.name)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_file.read())
            temp_filename = tmp.name

        st.info("⏳ Transcribing audio...")
        result = asr_model.transcribe(temp_filename)
        transcribed_text = result["text"]
        st.text_area("🗣️ Transcribed Text:", transcribed_text)

        cleaned_audio = preprocess_text(transcribed_text)
        vect_audio = vectorizer.transform([cleaned_audio])
        pred_audio = model.predict(vect_audio)[0]
        st.success("🟠 SPAM" if pred_audio else "🟢 NOT SPAM")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

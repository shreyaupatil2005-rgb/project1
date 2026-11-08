import streamlit as st
import PyPDF2
from collections import Counter
import re

st.title("🧠 Notes Summarizer")

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text

def summarize_text(text, num_sentences=5):
    sentences = re.split(r'(?<=[.!?]) +', text)

    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(words)

    sentence_scores = {}

    for sentence in sentences:
        for word in re.findall(r'\w+', sentence.lower()):
            if word in word_freq:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_freq[word]

    summary = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    return " ".join(summary[:num_sentences])

option = st.radio("Choose Input", ["Paste Text", "Upload PDF"])

text = ""

if option == "Paste Text":
    text = st.text_area("Enter Notes")

else:
    pdf = st.file_uploader("Upload PDF", type="pdf")

    if pdf:
        text = extract_text_from_pdf(pdf)
        st.success("PDF Loaded Successfully")

if st.button("Generate Summary"):
    if text.strip():
        summary = summarize_text(text)
        st.subheader("Summary")
        st.write(summary)
    else:
        st.warning("Please enter text or upload a PDF.")
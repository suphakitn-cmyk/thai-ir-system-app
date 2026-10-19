import streamlit as st
import re
from collections import defaultdict
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Thai IR System App", page_icon="🔍")

st.title("🔍 Thai Information Retrieval System")
st.write("ระบบค้นคืนสารสนเทศภาษาไทย (Assignment 1)")

# ข้อมูลเอกสารตัวอย่าง
documents = [
    "สวัสดีครับ นี่คือข้อความทดสอบสำหรับการประมวลผลข้อความ",
    "เราจะตัดคำ ลดรูปคำ และลบคำฟุ่มเฟือยออกจากข้อความนี้",
    "จากนั้นสร้างดัชนีผกผันเพื่อค้นหาข้อมูลได้อย่างมีประสิทธิภาพ"
]

@st.cache_data
def get_stopwords():
    return set(thai_stopwords())

stopwords = get_stopwords()

def preprocess_text(text):
    tokens = word_tokenize(text, engine="newmm")
    filtered_tokens = [
        token.strip() for token in tokens 
        if token.strip() != "" and token not in stopwords and not re.match(r'^\s+$', token)
    ]
    return filtered_tokens

def build_inverted_index(docs):
    inverted_index = defaultdict(set)
    for doc_id, doc_text in enumerate(docs, start=1):
        tokens = preprocess_text(doc_text)
        for token in set(tokens):
            inverted_index[token].add(doc_id)
    return {k: sorted(list(v)) for k, v in inverted_index.items()}

inverted_index = build_inverted_index(documents)

# ส่วนแสดงข้อมูลเอกสาร
with st.expander("📄 ดูรายการเอกสารทั้งหมดในระบบ"):
    for i, doc in enumerate(documents, start=1):
        st.write(f"**Document {i}:** {doc}")

# ช่องกรอกคำค้นหา
query = st.text_input("ใส่คำค้นหาที่ต้องการ (Query):", placeholder="เช่น ข้อความ, ค้นหา")

if query:
    query_tokens = preprocess_text(query)
    st.write(f"**คำค้นหาหลัง Preprocessing:** `{query_tokens}`")
    
    matched_doc_ids = set()
    for token in query_tokens:
        if token in inverted_index:
            matched_doc_ids.update(inverted_index[token])
            
    matched_doc_ids = sorted(list(matched_doc_ids))
    
    st.subheader(f"ผลการค้นหา (พบ {len(matched_doc_ids)} รายการ)")
    if matched_doc_ids:
        for doc_id in matched_doc_ids:
            st.success(f"**Document {doc_id}:** {documents[doc_id-1]}")
    else:
        st.warning("ไม่พบเอกสารที่เกี่ยวข้อง")

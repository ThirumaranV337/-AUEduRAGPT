##final testing 
import gradio as gr
from Rag_engine import Rag_engine

dropdown_choice = gr.Dropdown(
    choices=[
        "Semester-1",
        "Semester-2",
        "Semester-3",
        "Semester-4",
        "Semester-5",
        "Semester-6",
        "My Pdf"
    ],
    label="📚 Choose Your Semester"
)

dropdown_choice_2 = gr.Dropdown(
    choices=["Learn", "16", "10", "18", "20", "2", "5"],
    label="📝 Choose Answer Type to Generate"
)

file_upload = gr.File(
    label="📄 Upload PDF Document",
    file_types=[".pdf"]
)

custom_css = """
footer {display:none !important;}

.custom-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #1f1f1f;
    color: #cccccc;
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    z-index: 9999;
    border-top: 1px solid #333333;
}

.custom-footer a {
    color: #0A66C2;
    text-decoration: none;
    font-weight: bold;
}

.custom-footer a:hover {
    text-decoration: underline;
    color: #0a85e0;
}
"""

footer_html = """
<div class="custom-footer">
    🎓 AUEduRAGPT &nbsp;|&nbsp; 
    Developed by <strong>Thirumaran V</strong> &nbsp;|&nbsp;
    🔗 <a href="https://www.linkedin.com/in/thirumaran-v-41565232a/" target="_blank">
        LinkedIn: Thirumaran V
    </a> &nbsp;|&nbsp;
    ⚠️ Beta Version — B.Tech AIDS, Anna University Reg. 2021
</div>
"""

with gr.Blocks(css=custom_css) as demo:
    gr.ChatInterface(
        fn=Rag_engine.answer_call_back,
        title="🎓 AUEduRAGPT",
        description="""
### 🎓🤖 Welcome to AUEduRAGPT
#### Anna University Education RAG-Powered Generator Pretrained Transformer

This assistant helps students:
- 📖 Learn concepts from semester subjects
- 📝 Generate 2, 5, 10, 16, 18, and 20 mark answers
- 🔍 Search answers using RAG (Retrieval-Augmented Generation)
- 📄 Upload your own PDF and ask questions from it

---

### 🏛️ Who is this for?

#### ✅ B.Tech AIDS Students (Anna University — Regulation 2021)
> You are our **primary users**! All prescribed textbooks recommended
> by Anna University for your curriculum are already processed and
> stored in our vector database. Just select your semester, choose
> your answer format, and ask your question — AUEduRAGPT will
> generate **Bloom's Taxonomy-calibrated**, standard answers
> grounded directly from your prescribed books.

#### 🌍 Students from Other Departments / Regulations
> You are also **welcome here**! Simply upload your own study
> material as a **single PDF** and AUEduRAGPT will:
> - Learn from your document
> - Answer your questions from it
> - Generate exam-ready answers in your chosen format

---

### 📌 Steps:

1. Go to **Additional Inputs** (below the chat box)

2. Select your **Semester** *(AIDS Reg. 2021 students only)*

3. Choose your **Answer Format** *(2, 5, 10, 16, 18, or 20 marks)*

4. *(Optional)* Upload your own **PDF** study material

5. Ask your **question** in the chat box

---

> ⚠️ **Beta Version** — Currently optimized for
> B.Tech AIDS students under Anna University Regulation 2021.
> Other department support via PDF upload is available.
""",
        additional_inputs=[
            dropdown_choice,
            dropdown_choice_2,
            file_upload
        ]
    )

    gr.HTML(footer_html)

demo.launch(inbrowser=True)
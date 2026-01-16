# CLARIRY

**CLARIRY** is an **offline, audio-first learning system** designed to help students *understand* long study materials instead of memorizing them.

It explains **PDF-based study content paragraph-by-paragraph**, in simple conversational language, allows real-time interruption for doubts, and supports non-linear navigation — all while working **completely offline**.

> **Tagline:** *Understanding, one paragraph at a time.*

---

## 🚩 Problem Statement

Students often struggle with long, text-heavy PDFs (30–200 pages). Reading-based study leads to:

* Skipping important sections
* Rote memorization
* Poor conceptual clarity
* Low exam performance despite effort

Existing tools either summarize aggressively or behave like chatbots, which do not support **focused, exam-oriented understanding**.

---

## 💡 Core Idea

CLARIRY replaces text-heavy studying with a **disciplined audio-first approach**:

* The student listens instead of reading
* Content is explained **one paragraph at a time**
* Explanations are short, simple, and example-driven
* The student can interrupt anytime and resume seamlessly
* The system supports jumping to *any* paragraph on demand

The goal is to bridge the gap between **conceptual understanding** and **exam performance**.

---

## ✨ Key Features

### 📄 PDF-Centric Learning

* Upload digitally typed PDFs (100–200 pages supported)
* PDF opens inside the app
* Paragraphs are automatically indexed
* Currently explained paragraph is highlighted

### 🔊 Audio-First Explanation

* Each paragraph is explained verbally
* Simple, conversational language (non-textbook tone)
* Short explanations (focused, no overloading)
* Example-based whenever possible

### 🖱️ Random-Access Navigation

* Click **any paragraph** to hear its explanation
* Jump forward or backward freely
* Re-explain previous content without penalties

> Each paragraph is treated as an **independent explainer unit**.

### ⏸️ Interrupt & Resume

* Pause explanation anytime
* Ask a doubt mid-explanation
* Receive a brief answer
* Resume explanation from the correct point

### 📝 Exam Mode (Optional)

* Converts understood content into exam-ready format
* Bullet points
* Keywords
* Formal exam tone

---

## 🧠 Design Philosophy

* **Understanding > Memorization**
* **Audio > Text** (to prevent skipping)
* **System-controlled flow**, not AI-controlled
* **Stateless AI**, state handled by the application
* **Offline-first**, privacy-safe

CLARIRY is not a chatbot. It is a **learning system**.

---

## 🏗️ High-Level Architecture

```
Desktop UI (Python)
│
├─ PDF Viewer & Highlighting
├─ User Controls (Play / Pause / Jump)
│
▼
Core Engine (Python)
│
├─ PDF Parsing & Paragraph Indexing
├─ State Management
├─ Navigation Logic
│
▼
Local AI Layer
│
├─ Offline LLM (Explanation)
├─ Offline TTS (Audio Output)
```

* The AI model has **no memory**
* All learning state is maintained by the system

---

## 🧩 Tech Stack

### Core Engine

* **Python**

### Desktop UI

* **PySide / PyQt** (native desktop application)

### PDF Processing

* PyMuPDF / pdfplumber

### AI (Offline)

* Local open-source LLM (7B–8B class)
* Executed via llama.cpp / Ollama

### Text-to-Speech

* Coqui TTS or system-level TTS

### State Storage

* Local JSON (initial)
* SQLite (future)

---

## 🗺️ Development Roadmap

### Phase 1 — Core Engine

* PDF parsing
* Paragraph indexing
* State object
* Local LLM explanation
* Audio playback

### Phase 2 — Desktop MVP

* PDF viewer
* Paragraph highlighting
* Click-to-explain
* Play / pause controls

### Phase 3 — Interrupt & Resume

* Doubt handling
* Resume logic
* Re-explain support

### Phase 4 — Exam Mode

* Exam-format conversion

### Phase 5 — Stability & Polish

* Performance optimization
* Audio improvements
* Keyboard shortcuts

---

## 📌 Why CLARIRY is Different

* Works **entirely offline**
* Audio-first by design
* Paragraph-level atomic explanations
* Non-linear learning supported
* No chat distraction
* Designed for exam-focused understanding

---

## 📄 Project Status

🚧 **In active development**

This project is being developed as a **serious CSE system design project** with potential for real-world deployment.

---

## 🧠 Final Note

> *CLARIRY is built for students who want clarity first — and marks as a consequence.*

---
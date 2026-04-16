# SiteIQ — AI-Powered Property Diagnostic Report Generator

> **UrbanRoof · Applied AI Builder Assignment**

SiteIQ is an AI workflow tool that converts raw site inspection data into structured, client-ready **Detailed Diagnostic Reports (DDR)** automatically.

---

## 🔗 Live Demo

**[siteiq-ddr-generator.streamlit.app](https://siteiq-ddr-generator.streamlit.app/)**

---

## 🧠 What it Does

Property inspectors produce two documents after every site visit:
- An **Inspection Report** — site observations, flagged items, checklist results
- A **Thermal Imaging Report** — temperature readings from a thermal camera

Manually combining these into a structured DDR takes hours. SiteIQ does it in under 60 seconds.

---

## ⚙️ How it Works

```
Inspection PDF + Thermal PDF
        ↓
  Text Extraction (PyMuPDF)
        ↓
  LLM Analysis (Llama 3.3 70B via Groq)
        ↓
  Structured JSON Output
        ↓
  7-Section DDR Report + PDF Export
```

---

## 📋 DDR Output Structure

| Section | Content |
|---------|---------|
| 01 | Property Issue Summary |
| 02 | Area-wise Observations |
| 03 | Probable Root Causes |
| 04 | Severity Assessment |
| 05 | Recommended Actions (Immediate / Short-term / Long-term) |
| 06 | Additional Notes |
| 07 | Missing / Unclear Information |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI Model | Llama 3.3 70B (via Groq API) |
| PDF Parsing | PyMuPDF (fitz) |
| PDF Export | fpdf2 |
| Deployment | Streamlit Cloud |

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Nish232003/siteiq-ddr-generator.git
cd siteiq-ddr-generator
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up API key**

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_groq_api_key_here
```

**4. Run the app**
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
siteiq-ddr-generator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .streamlit/         # Streamlit cloud config
├── .gitignore
└── README.md
```

---

## ⚠️ Limitations

- Free tier Groq API has a token rate limit — retry after a few seconds if it hits the limit
- Currently uses text extraction only — thermal images are not visually analysed
- Customer name/address show as "Not Available" if not filled in source documents (by design — no hallucination)

---

## 🔮 Future Improvements

- Vision model integration for direct thermal image analysis
- Report history and comparison across multiple inspections
- Multi-language support for client reports
- Custom branding per inspection company

---

## 👨‍💻 Built By

**Nishita Jain**
[GitHub](https://github.com/Nish232003) 

---

*Built as part of the UrbanRoof Applied AI Builder assignment.*

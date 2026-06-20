# ============================================================
# SiteIQ — Property Diagnostic Intelligence Platform
# Built by: Nishita Jain | UrbanRoof Assignment
# ============================================================

import os, re, json, base64
import streamlit as st
import fitz
from groq import Groq
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="SiteIQ — Property Diagnostics",
    page_icon="🏗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp {
    background: #0d0d0d !important;
    color: #e8e8e8 !important;
    font-family: 'Outfit', sans-serif !important;
}
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAV ── */
.topnav {
    background: rgba(13,13,13,0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid #1e1e1e;
    padding: 0 60px;
    height: 62px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.logo { font-size: 20px; font-weight: 900; color: #fff; letter-spacing: -0.8px; }
.logo span { color: #f59e0b; }
.nav-center { display: flex; gap: 28px; }
.nav-link { font-size: 13px; color: #555; font-weight: 500; cursor: pointer; }
.nav-link:hover { color: #e8e8e8; }
.nav-right { display: flex; align-items: center; gap: 12px; }
.nav-dot { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #555; }
.nd { width: 7px; height: 7px; background: #22c55e; border-radius: 50%; animation: p 2s infinite; }
@keyframes p { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
.nav-btn {
    background: #f59e0b; color: #000;
    font-size: 12px; font-weight: 700;
    padding: 8px 18px; border-radius: 8px;
    letter-spacing: 0.3px;
}

/* ── HERO ── */
.hero {
    padding: 100px 60px 80px;
    position: relative;
    overflow: hidden;
    background: #0d0d0d;
}
.hero-bg {
    position: absolute;
    top: -200px; right: -100px;
    width: 700px; height: 700px;
    background: radial-gradient(circle, rgba(245,158,11,0.06) 0%, transparent 65%);
    pointer-events: none;
}
.hero-bg2 {
    position: absolute;
    bottom: -100px; left: 200px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(99,102,241,0.04) 0%, transparent 65%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    padding: 6px 14px; border-radius: 20px;
    font-size: 11px; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    color: #f59e0b; margin-bottom: 28px;
}
.bd { width: 5px; height: 5px; background: #f59e0b; border-radius: 50%; }
.hero-h1 {
    font-size: 72px; font-weight: 900;
    color: #fff; line-height: 1.0;
    letter-spacing: -3px; margin-bottom: 24px;
    max-width: 800px;
}
.hero-h1 .hl {
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 17px; font-weight: 300; color: #666;
    line-height: 1.7; max-width: 520px; margin-bottom: 52px;
}
.hero-bottom { display: flex; align-items: center; gap: 48px; }
.hstat { }
.hstat-n { font-size: 36px; font-weight: 900; color: #fff; letter-spacing: -1.5px; }
.hstat-l { font-size: 11px; color: #444; font-weight: 500; margin-top: 2px; letter-spacing: 0.5px; }
.hero-divider { width: 1px; height: 48px; background: #222; }
.hero-tags { display: flex; gap: 8px; flex-wrap: wrap; }
.htag {
    background: #141414; border: 1px solid #222;
    color: #555; font-size: 12px; font-weight: 500;
    padding: 6px 14px; border-radius: 20px;
}

/* ── TICKER BAR ── */
.ticker {
    background: #111; border-top: 1px solid #1e1e1e;
    border-bottom: 1px solid #1e1e1e;
    padding: 12px 60px;
    display: flex; align-items: center; gap: 40px;
    overflow: hidden;
}
.tick-item { display: flex; align-items: center; gap: 8px; white-space: nowrap; }
.tick-label { font-size: 11px; color: #333; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; }
.tick-val { font-size: 11px; color: #555; font-weight: 500; }
.tick-sep { color: #222; }

/* ── UPLOAD SECTION ── */
.upload-wrap {
    padding: 64px 60px 0;
    background: #0d0d0d;
}
.section-label {
    font-size: 10px; font-weight: 700;
    letter-spacing: 4px; text-transform: uppercase;
    color: #333; margin-bottom: 6px;
}
.section-title {
    font-size: 28px; font-weight: 800;
    color: #fff; letter-spacing: -0.8px;
    margin-bottom: 6px;
}
.section-sub { font-size: 14px; color: #444; margin-bottom: 36px; }

.ucard {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 16px;
    padding: 28px;
    transition: all 0.25s ease;
    cursor: pointer;
}
.ucard:hover {
    border-color: #f59e0b;
    background: #131108;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(245,158,11,0.08);
}
.ucard-top { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
.ucard-icon {
    width: 46px; height: 46px;
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.15);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.ucard-info {}
.ucard-t { font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 2px; }
.ucard-d { font-size: 12px; color: #444; }
.ucard-footer {
    padding-top: 14px;
    border-top: 1px solid #1a1a1a;
    font-size: 11px; color: #333;
    display: flex; align-items: center; gap: 6px;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #f59e0b, #f97316) !important;
    color: #000 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important; font-size: 15px !important;
    border: none !important; border-radius: 12px !important;
    padding: 16px 32px !important; width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(245,158,11,0.3) !important;
}

/* ── REPORT HEADER ── */
.report-wrap { padding: 0 60px 80px; background: #0d0d0d; }
.rhead {
    background: linear-gradient(135deg, #111 0%, #0f0c03 100%);
    border: 1px solid #222;
    border-radius: 20px;
    padding: 40px 48px;
    margin: 48px 0 20px;
    display: grid; grid-template-columns: 1fr auto;
    gap: 32px; align-items: center;
    position: relative; overflow: hidden;
}
.rhead::before {
    content: 'DDR';
    position: absolute; right: 160px; top: 50%;
    transform: translateY(-50%);
    font-size: 130px; font-weight: 900;
    color: rgba(245,158,11,0.04);
    letter-spacing: -5px; pointer-events: none;
}
.rh-lbl {
    font-size: 10px; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    color: #f59e0b; margin-bottom: 10px;
}
.rh-title { font-size: 26px; font-weight: 800; color: #fff; margin-bottom: 14px; letter-spacing: -0.5px; }
.rh-meta { display: flex; gap: 20px; flex-wrap: wrap; }
.rh-meta-item { font-size: 12px; color: #444; display: flex; align-items: center; gap: 6px; }
.rh-meta-item span { color: #666; }
.score-box {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 16px; padding: 20px 28px; text-align: center;
    min-width: 130px;
}
.score-val { font-size: 36px; font-weight: 900; color: #f59e0b; letter-spacing: -1px; }
.score-lbl { font-size: 10px; color: #555; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 4px; }

/* ── STATS ── */
.statrow {
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 12px; margin-bottom: 20px;
}
.sc {
    background: #111; border: 1px solid #1e1e1e;
    border-radius: 14px; padding: 20px 22px;
    transition: border-color 0.2s;
}
.sc:hover { border-color: #333; }
.sc-val { font-size: 36px; font-weight: 900; color: #fff; letter-spacing: -1.5px; line-height: 1; margin-bottom: 6px; }
.sc-lbl { font-size: 10px; color: #444; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; }

/* ── SECTION BLOCK ── */
.sb {
    background: #111; border: 1px solid #1e1e1e;
    border-radius: 16px; padding: 26px 30px; margin-bottom: 12px;
}
.sb-num { font-size: 10px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #2a2a2a; margin-bottom: 2px; }
.sb-title {
    font-size: 17px; font-weight: 800; color: #fff;
    margin-bottom: 18px; padding-bottom: 14px;
    border-bottom: 1px solid #1a1a1a; letter-spacing: -0.3px;
}
.btxt { font-size: 14px; color: #888; line-height: 1.85; }

/* ── OBS CARD ── */
.oc {
    border: 1px solid #1e1e1e; border-radius: 12px;
    padding: 16px 20px 16px 24px;
    margin-bottom: 10px; background: #0d0d0d;
    position: relative;
}
.oc::before {
    content: ''; position: absolute;
    left: 0; top: 0; bottom: 0; width: 3px;
    border-radius: 12px 0 0 12px; background: #222;
}
.oc.high::before { background: linear-gradient(180deg, #ef4444, #dc2626); }
.oc.medium::before { background: linear-gradient(180deg, #f59e0b, #d97706); }
.oc.low::before { background: linear-gradient(180deg, #22c55e, #16a34a); }
.oc-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.oc-loc { font-size: 14px; font-weight: 700; color: #e8e8e8; }
.stag { font-size: 10px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; padding: 3px 10px; border-radius: 20px; }
.stag.high { background: rgba(239,68,68,0.1); color: #f87171; border: 1px solid rgba(239,68,68,0.2); }
.stag.medium { background: rgba(245,158,11,0.1); color: #fbbf24; border: 1px solid rgba(245,158,11,0.2); }
.stag.low { background: rgba(34,197,94,0.1); color: #4ade80; border: 1px solid rgba(34,197,94,0.2); }
.oc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.ofl { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #2e2e2e; margin-bottom: 3px; }
.ofv { font-size: 13px; color: #666; line-height: 1.5; }

/* ── CAUSE ── */
.cc {
    background: #0d0d0d; border: 1px solid #1e1e1e;
    border-radius: 12px; padding: 16px 20px;
    margin-bottom: 10px; display: flex; gap: 14px; align-items: flex-start;
}
.ci {
    width: 38px; height: 38px;
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.15);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.ct { font-size: 14px; font-weight: 700; color: #e8e8e8; margin-bottom: 4px; }
.cd { font-size: 13px; color: #666; line-height: 1.6; }

/* ── SEV ── */
.sevb { border-radius: 14px; padding: 22px 26px; }
.sevb.high { background: rgba(239,68,68,0.05); border: 1px solid rgba(239,68,68,0.15); }
.sevb.medium { background: rgba(245,158,11,0.05); border: 1px solid rgba(245,158,11,0.15); }
.sevb.low { background: rgba(34,197,94,0.05); border: 1px solid rgba(34,197,94,0.15); }
.sevv { font-size: 22px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.5px; }
.sevb.high .sevv { color: #f87171; }
.sevb.medium .sevv { color: #fbbf24; }
.sevb.low .sevv { color: #4ade80; }
.sevt { font-size: 14px; color: #666; line-height: 1.7; }

/* ── ACTION ── */
.ac { background: #0d0d0d; border: 1px solid #1e1e1e; border-radius: 12px; padding: 16px 20px; margin-bottom: 10px; }
.aw { font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 5px; }
.aw.im { color: #f87171; } .aw.sh { color: #fbbf24; } .aw.lo { color: #4ade80; }
.awt { font-size: 14px; font-weight: 700; color: #e8e8e8; margin-bottom: 5px; }
.awh { font-size: 13px; color: #666; line-height: 1.6; }

/* ── GAP ── */
.gi {
    background: rgba(245,158,11,0.04);
    border: 1px solid rgba(245,158,11,0.12);
    border-radius: 8px; padding: 10px 14px;
    font-size: 13px; color: #666; margin-bottom: 8px;
    display: flex; align-items: center; gap: 8px;
}

/* ── DOWNLOAD ── */
.dlarea {
    background: linear-gradient(135deg, #111 0%, #0f0c03 100%);
    border: 1px solid #222;
    border-radius: 16px; padding: 32px;
    text-align: center; margin-top: 20px;
}
.dlt { font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 6px; }
.dls { font-size: 13px; color: #444; margin-bottom: 20px; }

/* streamlit overrides */
.stFileUploader > div {
    background: #0a0a0a !important;
    border: 1px dashed #222 !important;
    border-radius: 10px !important;
}
.stFileUploader label { color: #333 !important; }
.stTabs [data-baseweb="tab-list"] {
    background: #111 !important; border-radius: 10px !important;
    padding: 4px !important; border: 1px solid #1e1e1e !important; gap: 3px !important;
}
.stTabs [data-baseweb="tab"] { color: #444 !important; font-weight: 600 !important; border-radius: 7px !important; font-size: 13px !important; }
.stTabs [aria-selected="true"] { background: #1e1e1e !important; color: #e8e8e8 !important; }
div[data-testid="stExpander"] { background: #111 !important; border: 1px solid #1e1e1e !important; border-radius: 12px !important; }
.stSuccess > div { background: rgba(34,197,94,0.08) !important; border: 1px solid rgba(34,197,94,0.2) !important; color: #4ade80 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ── Core Functions ────────────────────────────────────────────
def read_pdf(f):
    data = f.read()
    doc = fitz.open(stream=data, filetype="pdf")
    txt = "\n".join(p.get_text() for p in doc)
    doc.close()
    return txt

def run_groq(insp_text, therm_text):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("API key not set in .env file.")
    client = Groq(api_key=key)
    prompt = f"""You are a senior property diagnostics engineer. Analyze the inspection and thermal reports below.

INSPECTION REPORT:
{insp_text[:6000]}

THERMAL REPORT:
{therm_text[:3000]}

Rules:
- Only use facts from documents. Never invent.
- Missing info = "Not Available"
- Conflicting data = mention both values
- Use simple, professional, client-friendly English

Return ONLY a valid JSON object, no markdown, no code fences:

{{
  "property_info": {{
    "date": "inspection date",
    "type": "property type",
    "floors": "floors",
    "inspector": "inspector name",
    "score": "score percentage",
    "issue_count": 7
  }},
  "summary": "3-4 sentence overview of all issues",
  "observations": [
    {{
      "location": "room or area",
      "problem": "issue observed on impacted side",
      "source": "root source area observed",
      "thermal": "thermal camera reading or Not Available",
      "severity": "High or Medium or Low"
    }}
  ],
  "causes": [
    {{"title": "cause title", "description": "client-friendly explanation"}}
  ],
  "severity": {{
    "level": "High or Medium or Low",
    "reason": "why this severity level",
    "urgent_areas": ["area needing immediate attention"]
  }},
  "actions": [
    {{"when": "Immediate or Short-term or Long-term", "what": "action title", "how": "step by step details"}}
  ],
  "notes": "any other observations",
  "gaps": ["any missing or unclear information"]
}}"""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000, temperature=0.2
    )
    raw = resp.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

def build_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    def h(t):
        pdf.set_font("Helvetica","B",13); pdf.set_text_color(160,90,30)
        pdf.cell(0,8,t,ln=True)
        pdf.set_draw_color(160,90,30); pdf.set_line_width(0.4)
        pdf.line(10,pdf.get_y(),200,pdf.get_y())
        pdf.set_text_color(40,40,40); pdf.ln(3)
    def b(t):
        pdf.set_font("Helvetica","",10); pdf.set_text_color(70,70,70)
        pdf.multi_cell(0,6,str(t)); pdf.ln(2)
    pdf.set_font("Helvetica","B",22); pdf.set_text_color(28,28,28)
    pdf.cell(0,14,"DETAILED DIAGNOSTIC REPORT",ln=True,align="C")
    pdf.set_font("Helvetica","",10); pdf.set_text_color(120,120,120)
    pdf.cell(0,6,f"Generated: {datetime.now().strftime('%d %B %Y')}",ln=True,align="C")
    pdf.ln(8)
    info = data.get("property_info",{})
    h("PROPERTY INFORMATION")
    for k,v in info.items():
        pdf.set_font("Helvetica","B",10); pdf.set_text_color(40,40,40)
        pdf.cell(55,6,k.replace("_"," ").title()+":",ln=False)
        pdf.set_font("Helvetica","",10); pdf.cell(0,6,str(v),ln=True)
    pdf.ln(4)
    h("1. ISSUE SUMMARY"); b(data.get("summary","Not Available")); pdf.ln(2)
    h("2. AREA-WISE OBSERVATIONS")
    for o in data.get("observations",[]):
        pdf.set_font("Helvetica","B",11); pdf.set_text_color(20,20,20)
        pdf.cell(0,7,f"Location: {o.get('location','')}",ln=True)
        pdf.set_font("Helvetica","",10); pdf.set_text_color(70,70,70)
        pdf.multi_cell(0,6,f"  Problem: {o.get('problem','')}")
        pdf.multi_cell(0,6,f"  Source: {o.get('source','')}")
        pdf.multi_cell(0,6,f"  Thermal: {o.get('thermal','Not Available')}")
        pdf.set_font("Helvetica","B",10)
        pdf.cell(0,6,f"  Severity: {o.get('severity','')}",ln=True); pdf.ln(2)
    h("3. ROOT CAUSES")
    for c in data.get("causes",[]):
        pdf.set_font("Helvetica","B",11); pdf.set_text_color(20,20,20)
        pdf.cell(0,7,c.get("title",""),ln=True); b(f"  {c.get('description','')}")
    sv = data.get("severity",{})
    h("4. SEVERITY ASSESSMENT")
    pdf.set_font("Helvetica","B",12); pdf.set_text_color(20,20,20)
    pdf.cell(0,7,f"Overall: {sv.get('level','')}",ln=True); b(sv.get("reason",""))
    for a in sv.get("urgent_areas",[]): b(f"  - {a}")
    h("5. RECOMMENDED ACTIONS")
    for ac in data.get("actions",[]):
        pdf.set_font("Helvetica","B",11); pdf.set_text_color(20,20,20)
        pdf.cell(0,7,f"[{ac.get('when','')}] {ac.get('what','')}",ln=True)
        b(f"  {ac.get('how','')}")
    h("6. ADDITIONAL NOTES"); b(data.get("notes","Not Available"))
    gaps = data.get("gaps",[])
    if gaps:
        h("7. MISSING INFORMATION")
        for g in gaps: b(f"  - {g}")
    pdf.ln(6); pdf.set_font("Helvetica","I",8); pdf.set_text_color(160,160,160)
    pdf.cell(0,5,"SiteIQ — AI Property Diagnostics Platform",ln=True,align="C")
    return bytes(pdf.output())

def sc(s):
    s = s.lower()
    if "high" in s: return "high"
    if "medium" in s or "moderate" in s: return "medium"
    return "low"

ICONS = ["🔍","💧","🔧","🏗","⚡","🌿","🔩","📐"]


# ══════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════

# NAV
st.markdown("""
<div class="topnav">
    <div class="logo">Site<span>IQ</span></div>
    <div class="nav-center">
        <div class="nav-link">Dashboard</div>
        <div class="nav-link">Reports</div>
        <div class="nav-link">About</div>
    </div>
    <div class="nav-right">
        <div class="nav-dot"><div class="nd"></div>AI Engine Active</div>
        <div class="nav-btn">Get Started</div>
    </div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <div class="hero-bg"></div>
    <div class="hero-bg2"></div>
    <div class="hero-badge"><div class="bd"></div>AI-Powered · Built for Property Teams</div>
    <div class="hero-h1">From inspection docs<br>to <span class="hl">diagnostic reports</span><br>in seconds.</div>
    <div class="hero-sub">Upload your site inspection and thermal imaging documents.
    SiteIQ cross-references findings and generates a structured,
    client-ready Detailed Diagnostic Report automatically.</div>
    <div class="hero-bottom">
        <div class="hstat"><div class="hstat-n">7</div><div class="hstat-l">Report Sections</div></div>
        <div class="hero-divider"></div>
        <div class="hstat"><div class="hstat-n">2</div><div class="hstat-l">Input Documents</div></div>
        <div class="hero-divider"></div>
        <div class="hstat"><div class="hstat-n">&lt;60s</div><div class="hstat-l">Generation Time</div></div>
        <div class="hero-divider"></div>
        <div class="hero-tags">
            <div class="htag">🏗 Structural Analysis</div>
            <div class="htag">🌡️ Thermal Mapping</div>
            <div class="htag">📋 PDF Export</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TICKER
st.markdown("""
<div class="ticker">
    <div class="tick-item"><span class="tick-label">Platform</span><span class="tick-val">SiteIQ v1.0</span></div>
    <span class="tick-sep">·</span>
    <div class="tick-item"><span class="tick-label">Model</span><span class="tick-val">Llama 3.3 70B via Groq</span></div>
    <span class="tick-sep">·</span>
    <div class="tick-item"><span class="tick-label">Report Format</span><span class="tick-val">7-Section DDR</span></div>
    <span class="tick-sep">·</span>
    <div class="tick-item"><span class="tick-label">Export</span><span class="tick-val">PDF Download</span></div>
    <span class="tick-sep">·</span>
    <div class="tick-item"><span class="tick-label">Built for</span><span class="tick-val">UrbanRoof Assignment</span></div>
</div>
""", unsafe_allow_html=True)

# UPLOAD
st.markdown('<div class="upload-wrap">', unsafe_allow_html=True)
st.markdown("""
<div class="section-label">Step 01</div>
<div class="section-title">Upload Your Documents</div>
<div class="section-sub">Both files are required to generate a complete DDR report.</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown("""<div class="ucard">
        <div class="ucard-top">
            <div class="ucard-icon">📋</div>
            <div class="ucard-info">
                <div class="ucard-t">Inspection Report</div>
                <div class="ucard-d">Site observations · Flagged items · Checklist</div>
            </div>
        </div>
        <div class="ucard-footer">📄 PDF format · Max 200MB</div>
    </div>""", unsafe_allow_html=True)
    insp = st.file_uploader("insp", type=["pdf"], key="insp", label_visibility="collapsed")
    if insp: st.success(f"✓  {insp.name}")

with c2:
    st.markdown("""<div class="ucard">
        <div class="ucard-top">
            <div class="ucard-icon">🌡️</div>
            <div class="ucard-info">
                <div class="ucard-t">Thermal Imaging Report</div>
                <div class="ucard-d">Temperature readings · Camera findings</div>
            </div>
        </div>
        <div class="ucard-footer">📄 PDF format · Max 200MB</div>
    </div>""", unsafe_allow_html=True)
    therm = st.file_uploader("therm", type=["pdf"], key="therm", label_visibility="collapsed")
    if therm: st.success(f"✓  {therm.name}")

st.markdown("<br>", unsafe_allow_html=True)

if insp and therm:
    if st.button("⚡  Generate Diagnostic Report", use_container_width=True):
        try:
            with st.spinner("Extracting text from documents..."):
                it = read_pdf(insp); insp.seek(0)
                tt = read_pdf(therm); therm.seek(0)
            with st.spinner("AI is analysing findings and writing your DDR (~30s)..."):
                result = run_groq(it, tt)
                st.session_state["rep"] = result
            st.success("✅ DDR generated successfully! Scroll down to view.")
        except json.JSONDecodeError:
            st.error("Unexpected response format. Please try again.")
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.markdown('<div style="text-align:center;padding:20px 0;font-size:13px;color:#2a2a2a;">Upload both documents above to enable report generation.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ── REPORT OUTPUT ─────────────────────────────────────────────
if "rep" in st.session_state:
    r = st.session_state["rep"]
    info = r.get("property_info", {})
    obs  = r.get("observations", [])
    sev  = r.get("severity", {})
    acts = r.get("actions", [])

    st.markdown('<div class="report-wrap">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="rhead">
        <div>
            <div class="rh-lbl">Detailed Diagnostic Report · Generated {datetime.now().strftime('%d %b %Y')}</div>
            <div class="rh-title">{info.get('type','Residential Property')} — Full Inspection Analysis</div>
            <div class="rh-meta">
                <div class="rh-meta-item">📅 <span>{info.get('date','Not Available')}</span></div>
                <div class="rh-meta-item">👤 <span>{info.get('inspector','Not Available')}</span></div>
                <div class="rh-meta-item">🏢 <span>{info.get('floors','—')} Floors</span></div>
                <div class="rh-meta-item">🚩 <span>{info.get('issue_count',len(obs))} Issues Found</span></div>
            </div>
        </div>
        <div class="score-box">
            <div class="score-val">{info.get('score','—')}</div>
            <div class="score-lbl">Inspection Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    hn = sum(1 for o in obs if "high" in o.get("severity","").lower())
    mn = sum(1 for o in obs if "medium" in o.get("severity","").lower())
    ln = len(obs) - hn - mn

    st.markdown(f"""
    <div class="statrow">
        <div class="sc"><div class="sc-val">{info.get('issue_count',len(obs))}</div><div class="sc-lbl">Total Issues</div></div>
        <div class="sc"><div class="sc-val" style="color:#f87171;">{hn}</div><div class="sc-lbl">High Severity</div></div>
        <div class="sc"><div class="sc-val" style="color:#fbbf24;">{mn}</div><div class="sc-lbl">Medium Severity</div></div>
        <div class="sc"><div class="sc-val" style="color:#4ade80;">{ln}</div><div class="sc-lbl">Low Severity</div></div>
    </div>
    """, unsafe_allow_html=True)

    # S1
    st.markdown(f"""<div class="sb">
        <div class="sb-num">Section 01</div>
        <div class="sb-title">Property Issue Summary</div>
        <div class="btxt">{r.get('summary','Not Available')}</div>
    </div>""", unsafe_allow_html=True)

    # S2
    oh = ""
    for o in obs:
        cls = sc(o.get("severity",""))
        oh += f"""<div class="oc {cls}">
            <div class="oc-top">
                <div class="oc-loc">📍 {o.get('location','')}</div>
                <span class="stag {cls}">{o.get('severity','')}</span>
            </div>
            <div class="oc-grid">
                <div><div class="ofl">Issue Found</div><div class="ofv">{o.get('problem','Not Available')}</div></div>
                <div><div class="ofl">Root Source</div><div class="ofv">{o.get('source','Not Available')}</div></div>
                <div style="grid-column:1/-1"><div class="ofl">Thermal Reading</div><div class="ofv">{o.get('thermal','Not Available')}</div></div>
            </div>
        </div>"""
    st.markdown(f"""<div class="sb">
        <div class="sb-num">Section 02</div>
        <div class="sb-title">Area-wise Observations</div>{oh}
    </div>""", unsafe_allow_html=True)

    # S3
    ch = ""
    for i, c in enumerate(r.get("causes",[])):
        ch += f"""<div class="cc"><div class="ci">{ICONS[i%len(ICONS)]}</div>
            <div><div class="ct">{c.get('title','')}</div><div class="cd">{c.get('description','')}</div></div>
        </div>"""
    st.markdown(f"""<div class="sb">
        <div class="sb-num">Section 03</div>
        <div class="sb-title">Probable Root Causes</div>{ch}
    </div>""", unsafe_allow_html=True)

    # S4
    lvl = sev.get("level","Medium")
    sc4 = sc(lvl)
    urg = "".join(f'<div style="font-size:13px;color:#555;margin-top:6px;">🔴 {a}</div>' for a in sev.get("urgent_areas",[]))
    st.markdown(f"""<div class="sb">
        <div class="sb-num">Section 04</div>
        <div class="sb-title">Severity Assessment</div>
        <div class="sevb {sc4}">
            <div class="sevv">Overall Severity: {lvl}</div>
            <div class="sevt">{sev.get('reason','Not Available')}</div>{urg}
        </div>
    </div>""", unsafe_allow_html=True)

    # S5
    st.markdown("""<div class="sb">
        <div class="sb-num">Section 05</div>
        <div class="sb-title">Recommended Actions</div>
    </div>""", unsafe_allow_html=True)

    imm = [a for a in acts if "immediate" in a.get("when","").lower()]
    sht = [a for a in acts if "short" in a.get("when","").lower()]
    lng = [a for a in acts if "long"  in a.get("when","").lower()]

    t1,t2,t3 = st.tabs(["🔴 Immediate","🟡 Short-term","🟢 Long-term"])
    with t1:
        if imm:
            for a in imm: st.markdown(f'<div class="ac"><div class="aw im">IMMEDIATE</div><div class="awt">{a.get("what","")}</div><div class="awh">{a.get("how","")}</div></div>', unsafe_allow_html=True)
        else: st.info("No immediate actions listed.")
    with t2:
        if sht:
            for a in sht: st.markdown(f'<div class="ac"><div class="aw sh">SHORT-TERM</div><div class="awt">{a.get("what","")}</div><div class="awh">{a.get("how","")}</div></div>', unsafe_allow_html=True)
        else: st.info("No short-term actions listed.")
    with t3:
        if lng:
            for a in lng: st.markdown(f'<div class="ac"><div class="aw lo">LONG-TERM</div><div class="awt">{a.get("what","")}</div><div class="awh">{a.get("how","")}</div></div>', unsafe_allow_html=True)
        else: st.info("No long-term actions listed.")

    # S6
    st.markdown(f"""<div class="sb">
        <div class="sb-num">Section 06</div>
        <div class="sb-title">Additional Notes</div>
        <div class="btxt">{r.get('notes','Not Available')}</div>
    </div>""", unsafe_allow_html=True)

    # S7
    gaps = r.get("gaps",[])
    if gaps:
        gh = "".join(f'<div class="gi">⚠️ {g}</div>' for g in gaps)
        st.markdown(f"""<div class="sb">
            <div class="sb-num">Section 07</div>
            <div class="sb-title">Missing / Unclear Information</div>{gh}
        </div>""", unsafe_allow_html=True)

    # Download
    st.markdown("""<div class="dlarea">
        <div class="dlt">📄 Export Full Report</div>
        <div class="dls">Download the complete 7-section DDR as a formatted PDF document.</div>
    </div>""", unsafe_allow_html=True)
    try:
        pdf_data = build_pdf(r)
        st.download_button(
            label="⬇  Download PDF Report",
            data=pdf_data,
            file_name=f"SiteIQ_DDR_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.warning(f"PDF export: {e}")

    with st.expander("🔧 View Raw JSON Output"):
        st.json(r)

    st.markdown('</div>', unsafe_allow_html=True)

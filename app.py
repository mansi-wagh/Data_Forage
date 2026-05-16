"""
DataForge AI - deployable Streamlit data analytics dashboard.
"""
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from core.ai_analyst import AIAnalyst
from core.chart_engine import ChartEngine
from core.data_cleaner import DataCleaner
from core.domain_detector import DomainDetector
from core.field_analyzer import FieldAnalyzer
from core.report_builder import ReportBuilder

load_dotenv()

st.set_page_config(
    page_title="DataForge AI Analytics",
    page_icon="DF",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg: #0b0f19;
    --panel: rgba(17, 24, 39, 0.65);
    --ink: #f3f4f6;
    --muted: #9ca3af;
    --line: rgba(255, 255, 255, 0.08);
    --accent: #3b82f6;
    --accent-glow: rgba(59, 130, 246, 0.5);
    --teal: #14b8a6;
    --amber: #f59e0b;
    --rose: #ef4444;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
}

.stApp {
    background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.1), transparent 40%),
                radial-gradient(circle at bottom right, rgba(20, 184, 166, 0.05), transparent 40%),
                var(--bg);
    color: var(--ink);
}

section[data-testid="stSidebar"] {
    background: rgba(17, 24, 39, 0.8);
    backdrop-filter: blur(12px);
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

section[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
}

.block-container {
    max-width: 1480px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.hero {
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.4), rgba(17, 24, 39, 0.8));
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 12px;
    color: white;
    padding: 32px 40px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    margin-bottom: 24px;
}

.hero h1 {
    font-size: clamp(2rem, 3.5vw, 3.5rem);
    line-height: 1.1;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(to right, #ffffff, #93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}

.hero p {
    margin: 12px 0 0 0;
    color: #94a3b8;
    max-width: 800px;
    font-size: 1.1rem;
    line-height: 1.5;
}

.hero-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
}

.panel {
    background: var(--panel);
    backdrop-filter: blur(12px);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.panel:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    border-color: rgba(255, 255, 255, 0.15);
}

.panel-title {
    color: #f3f4f6;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin: 24px 0;
}

.kpi-card {
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 20px;
    min-height: 110px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.kpi-card:hover {
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--card-accent);
}

.kpi-label {
    color: var(--muted);
    font-size: 0.8rem;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.05em;
}

.kpi-value {
    color: #f8fafc;
    font-size: clamp(1.5rem, 2.5vw, 2.2rem);
    font-weight: 800;
    margin-top: 8px;
    overflow-wrap: anywhere;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.domain-card {
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.2), rgba(17, 24, 39, 0.6));
    backdrop-filter: blur(12px);
    color: white;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid rgba(59, 130, 246, 0.3);
    min-height: 160px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.domain-card .small {
    color: #94a3b8;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.domain-card .domain {
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 12px;
    background: linear-gradient(to right, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.domain-card .confidence {
    margin-top: 16px;
    height: 6px;
    background: rgba(255,255,255,0.05);
    border-radius: 999px;
    overflow: hidden;
}

.domain-card .confidence span {
    display: block;
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #10b981);
    box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

.quality-list {
    display: grid;
    gap: 12px;
}

.quality-item {
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.02);
    border-radius: 8px;
    padding: 12px 16px;
    color: var(--muted);
    font-size: 0.9rem;
    transition: background 0.2s;
}

.quality-item:hover {
    background: rgba(255,255,255,0.05);
}

.quality-item strong {
    color: #e5e7eb;
}

.field-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}

.field-badge {
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.2);
    color: #93c5fd;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

div[data-testid="stMetric"] {
    background: var(--panel);
    backdrop-filter: blur(12px);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

div[data-testid="stDownloadButton"] > button,
.stButton > button {
    border-radius: 8px;
    min-height: 48px;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    color: white;
    transition: all 0.2s ease;
}

.stButton > button:hover,
div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(255,255,255,0.1);
    border-color: rgba(255,255,255,0.2);
    transform: translateY(-1px);
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    border: 0;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    background-color: transparent;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 0;
    color: #9ca3af;
    font-weight: 600;
    font-size: 1rem;
}

.stTabs [aria-selected="true"] {
    color: #f3f4f6 !important;
}

@media (max-width: 980px) {
    .hero-row { flex-direction: column; align-items: flex-start; }
    .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>
        """,
        unsafe_allow_html=True,
    )


def kpi_cards(kpis):
    if not kpis:
        return
    cards = []
    for index, (label, value) in enumerate(kpis.items()):
        accent = ["#13b6b3", "#f5a623", "#ef5b73", "#4b8bd6", "#7bc96f"][index % 5]
        cards.append(
            f"""
            <div class="kpi-card" style="border-left-color:{accent}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """
        )
    st.markdown(f'<div class="kpi-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def field_panel(fields):
    for field_type, columns in fields.items():
        if columns:
            badges = "".join([f'<span class="field-badge">{col}</span>' for col in columns])
            st.markdown(f"**{field_type.title()}**")
            st.markdown(f'<div class="field-badges">{badges}</div>', unsafe_allow_html=True)


def render_quality_log(cleaning_log):
    if not cleaning_log:
        st.info("No cleaning operations were required.")
        return
    items = []
    for entry in cleaning_log[:8]:
        items.append(
            f"""
            <div class="quality-item">
                <strong>{entry["action"]}</strong><br>
                {entry["details"]}
            </div>
            """
        )
    st.markdown(f'<div class="quality-list">{"".join(items)}</div>', unsafe_allow_html=True)


def load_csv(uploaded_file):
    try:
        return pd.read_csv(uploaded_file), None
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, encoding="latin-1"), None
    except Exception as exc:
        return None, str(exc)


inject_css()

if "ai" not in st.session_state:
    st.session_state.ai = AIAnalyst()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.markdown("## DataForge AI")
    st.caption("Deployable AI data analytics workspace")
    st.markdown("---")

    uploaded = st.file_uploader(
        "Upload CSV dataset",
        type=["csv"],
        help="Upload employee, sales, finance, marketing, healthcare, inventory, or general business data.",
    )

    st.markdown("---")
    st.markdown("### Output")

    st.caption("Cleaned CSV and a full HTML BI dashboard are generated after upload.")

    if st.button("Reset workspace", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key != "ai":
                del st.session_state[key]
        st.session_state.chat_history = []
        st.rerun()

st.markdown(
    """
    <div class="hero">
        <div class="hero-row">
            <div>
                <h1>AI Data Analytics Dashboard</h1>
                <p>Upload a CSV and generate a PowerBI-style analytics workspace with cleaning, domain detection, KPIs, visual diagnostics, AI insights, and an executive HTML report ready to share.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not uploaded:
    st.markdown("### Start with a dataset")
    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="panel"><div class="panel-title">1. Upload</div>Drop a CSV in the sidebar to begin profiling and cleanup.</div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="panel"><div class="panel-title">2. Analyze</div>DataForge detects the domain, KPIs, fields, and best-fit charts.</div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="panel"><div class="panel-title">3. Export</div>Download cleaned data and a PowerBI-style HTML dashboard report.</div>', unsafe_allow_html=True)
    st.stop()
    raise SystemExit

raw_df, read_error = load_csv(uploaded)
if read_error:
    st.error(f"Could not read the uploaded CSV: {read_error}")
    st.stop()

st.session_state.filename = uploaded.name

with st.spinner("Cleaning data and building analytics model..."):
    cleaner = DataCleaner(raw_df)
    cleaned_df, cleaning_log = cleaner.clean()
    domain, icon, color, confidence = DomainDetector.detect(cleaned_df)
    fields = FieldAnalyzer.analyze(cleaned_df)
    charts = ChartEngine.generate(cleaned_df, domain, fields)
    kpis = ReportBuilder.get_kpis(cleaned_df, domain, FieldAnalyzer)

st.session_state.cleaned_df = cleaned_df

top_left, top_right = st.columns([1.35, 0.65])
with top_left:
    kpi_cards(kpis)
with top_right:
    st.markdown(
        f"""
        <div class="domain-card">
            <div class="small">0 analytics domain</div>
            <div class="domain">{icon} {domain}</div>
            <div style="color:#c9d8e8;margin-top:8px;">Confidence: <strong>{confidence}%</strong></div>
            <div class="confidence"><span style="width:{confidence}%;"></span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

dashboard_tab, data_tab, ai_tab, export_tab = st.tabs(
    ["Dashboard", "Data Quality", "AI Analyst", "Export Center"]
)

with dashboard_tab:
    st.markdown("### Visual analytics dashboard")
    if charts:
        for index in range(0, len(charts), 2):
            cols = st.columns(2)
            for offset, col in enumerate(cols):
                chart_index = index + offset
                if chart_index < len(charts):
                    title, fig = charts[chart_index]
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=28, r=20, t=52, b=28),
                        font=dict(family="Inter, sans-serif", color="#f3f4f6"),
                        title=dict(text=title, x=0.02, xanchor="left"),
                    )
                    with col:
                        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No chart-ready numeric or categorical patterns were found, but the report still includes profiling and cleaned data.")

with data_tab:
    summary_a, summary_b, summary_c, summary_d = st.columns(4)
    summary_a.metric("Original rows", f"{len(raw_df):,}")
    summary_b.metric("Cleaned rows", f"{len(cleaned_df):,}", f"{len(cleaned_df) - len(raw_df):,}")
    summary_c.metric("Original columns", len(raw_df.columns))
    summary_d.metric("Cleaned columns", len(cleaned_df.columns), len(cleaned_df.columns) - len(raw_df.columns))

    left, right = st.columns([0.58, 0.42])
    with left:
        st.markdown("### Cleaned data preview")
        st.dataframe(cleaned_df.head(50), use_container_width=True, hide_index=True)
    with right:
        st.markdown("### Field intelligence")
        field_panel(fields)
        st.markdown("### Cleaning log")
        render_quality_log(cleaning_log)

with ai_tab:
    st.markdown("### AI analyst report")
    if st.session_state.ai.available:
        if st.button("Generate AI insights", type="primary", use_container_width=True):
            with st.spinner("Analyzing dataset with AI..."):
                st.session_state.ai_insights = st.session_state.ai.generate_insights(
                    cleaned_df, domain, kpis, fields
                )

        if "ai_insights" in st.session_state:
            st.markdown(
                st.session_state.ai.clean_ai_html(st.session_state.ai_insights),
                unsafe_allow_html=True,
            )
        else:
            st.info("Generate insights to add an executive AI section to the downloadable report.")

        st.markdown("### Chat with your data")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask about trends, anomalies, risks, or recommendations")
        if question:
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = st.session_state.ai.chat(
                        cleaned_df,
                        domain,
                        kpis,
                        fields,
                        question,
                        st.session_state.chat_history,
                    )
                    st.markdown(answer, unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        fallback = st.session_state.ai._fallback_insights(cleaned_df, domain, kpis)
        st.markdown(fallback, unsafe_allow_html=True)

with export_tab:
    ai_insights = st.session_state.ai.clean_ai_html(st.session_state.get("ai_insights", ""))
    html_report = ReportBuilder.build(
        df=cleaned_df,
        domain=domain,
        domain_icon=icon,
        domain_color=color,
        confidence=confidence,
        cleaning_log=cleaning_log,
        fields=fields,
        charts=charts,
        kpis=kpis,
        ai_insights=ai_insights,
    )

    st.markdown("### Download outputs")
    e1, e2 = st.columns(2)
    with e1:
        st.markdown('<div class="panel"><div class="panel-title">Cleaned dataset</div>CSV output with standardized columns, missing value handling, duplicate removal, and outlier cleanup.</div>', unsafe_allow_html=True)
        st.download_button(
            "Download cleaned CSV",
            data=cleaned_df.to_csv(index=False).encode("utf-8"),
            file_name=f"dataforge_cleaned_{uploaded.name}",
            mime="text/csv",
            use_container_width=True,
        )
    with e2:
        st.markdown('<div class="panel"><div class="panel-title">PowerBI-style HTML report</div>Executive dashboard with KPIs, charts, statistical summary, field mapping, cleaning log, and optional AI insights.</div>', unsafe_allow_html=True)
        st.download_button(
            "Download dashboard report",
            data=html_report.encode("utf-8"),
            file_name=f"dataforge_dashboard_{domain.replace(' ', '_').replace('/', '_')}.html",
            mime="text/html",
            use_container_width=True,
        )

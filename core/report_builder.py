"""
DataForge AI - HTML dashboard report builder.
"""
import copy
from datetime import datetime


class ReportBuilder:

    @staticmethod
    def build(df, domain, domain_icon, domain_color,
              confidence, cleaning_log, fields, charts, kpis,
              ai_insights=""):

        chart_sections = ""
        for title, fig in charts:
            report_fig = copy.deepcopy(fig)
            report_fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(3,18,35,0.34)",
                font=dict(color="#e9f2ff", family="Inter, Segoe UI, sans-serif"),
                margin=dict(l=36, r=22, t=52, b=34),
                title=dict(text=title, x=0.02, xanchor="left", font=dict(size=17)),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
            )
            chart_html = report_fig.to_html(
                full_html=False,
                include_plotlyjs=False,
                config={"displayModeBar": False, "responsive": True},
            )
            chart_sections += f"""
            <article class="chart-card">
                <div class="card-title">{title}</div>
                <div class="chart-frame">{chart_html}</div>
            </article>
            """

        if not chart_sections:
            chart_sections = """
            <article class="chart-card empty">
                <div class="card-title">No chart-ready columns found</div>
                <p>The dataset was still cleaned, profiled, and summarized.</p>
            </article>
            """

        kpi_html = ""
        accents = ["#12b6b3", "#f5a623", "#ef5b73", "#4b8bd6", "#78c96f", "#9a72e8"]
        for index, (key, val) in enumerate(kpis.items()):
            kpi_html += f"""
            <article class="kpi" style="--accent:{accents[index % len(accents)]}">
                <span>{key}</span>
                <strong>{val}</strong>
            </article>
            """

        log_html = ""
        for entry in cleaning_log:
            log_html += f"""
            <tr>
                <td><span class="badge">{entry['action']}</span></td>
                <td>{entry['details']}</td>
            </tr>
            """

        field_html = ""
        for field_type, columns in fields.items():
            if columns:
                badges = "".join(
                    [f'<span class="field-badge">{column}</span>' for column in columns]
                )
                field_html += f"""
                <div class="field-group">
                    <div class="field-type">{field_type.title()} ({len(columns)})</div>
                    <div class="field-row">{badges}</div>
                </div>
                """

        summary_html = df.describe(include="all").round(2).to_html(
            classes="data-table",
            border=0,
        )

        ai_section = ""
        if ai_insights:
            ai_section = f"""
            <section class="section ai-section">
                <div class="section-heading">
                    <span>AI Analyst</span>
                    <h2>Executive Insights</h2>
                </div>
                <div class="ai-content">{ai_insights}</div>
            </section>
            """

        generated_at = datetime.now().strftime("%B %d, %Y %I:%M %p")

        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DataForge AI Dashboard - {domain}</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            background: #071525;
            color: #e9f2ff;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}
        .shell {{
            min-height: 100vh;
            background:
                radial-gradient(circle at 12% 4%, rgba(84,196,255,.16), transparent 28rem),
                radial-gradient(circle at 86% 8%, rgba(18,182,179,.14), transparent 24rem),
                linear-gradient(135deg, #071525 0%, #0d2542 48%, #102f56 100%);
        }}
        .topbar {{
            background:
                linear-gradient(135deg, rgba(4,16,31,.96), rgba(18,47,85,.92)),
                repeating-linear-gradient(45deg, rgba(255,255,255,.04), rgba(255,255,255,.04) 1px, transparent 1px, transparent 12px);
            color: white;
            border-bottom: 4px solid #67d7ff;
            padding: 24px 32px 22px;
        }}
        .topbar-inner {{
            max-width: 1480px;
            margin: 0 auto;
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 24px;
        }}
        h1 {{
            margin: 0;
            font-size: clamp(2rem, 4vw, 3.5rem);
            line-height: 1;
            letter-spacing: 0;
        }}
        .subtitle {{
            color: #b9cbe0;
            margin-top: 10px;
            font-weight: 600;
        }}
        .domain-chip {{
            min-width: 240px;
            background: rgba(103,215,255,.10);
            border: 1px solid rgba(103,215,255,.28);
            border-radius: 8px;
            padding: 14px 16px;
        }}
        .domain-chip span {{
            display: block;
            color: #9fd8ff;
            font-size: .72rem;
            text-transform: uppercase;
            font-weight: 800;
            margin-bottom: 5px;
        }}
        .domain-chip strong {{
            font-size: 1.1rem;
        }}
        .container {{
            max-width: 1480px;
            margin: 0 auto;
            padding: 22px 24px 42px;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 12px;
            margin-bottom: 18px;
        }}
        .kpi {{
            background: linear-gradient(180deg, rgba(23,55,94,.98), rgba(9,30,55,.98));
            border: 1px solid rgba(133,184,235,.22);
            border-left: 5px solid var(--accent);
            border-radius: 8px;
            padding: 18px 16px;
            min-height: 108px;
            box-shadow: 0 16px 34px rgba(0,0,0,.25);
        }}
        .kpi span {{
            display: block;
            color: #a9bdd3;
            font-size: .75rem;
            text-transform: uppercase;
            font-weight: 800;
        }}
        .kpi strong {{
            display: block;
            margin-top: 12px;
            color: #ffffff;
            font-size: 1.85rem;
            overflow-wrap: anywhere;
        }}
        .section {{
            background: rgba(10,32,59,.86);
            border: 1px solid rgba(133,184,235,.20);
            border-radius: 8px;
            padding: 20px;
            margin-top: 18px;
            box-shadow: 0 18px 44px rgba(0,0,0,.24);
        }}
        .section-heading {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 16px;
            border-bottom: 1px solid rgba(133,184,235,.18);
            padding-bottom: 12px;
            margin-bottom: 18px;
        }}
        .section-heading span {{
            color: #67d7ff;
            font-size: .78rem;
            text-transform: uppercase;
            font-weight: 900;
        }}
        h2 {{
            margin: 0;
            font-size: 1.25rem;
            color: #ffffff;
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px;
        }}
        .chart-card {{
            background: linear-gradient(180deg, rgba(11,38,70,.98), rgba(7,25,46,.98));
            border: 1px solid rgba(133,184,235,.22);
            border-radius: 8px;
            padding: 14px;
            min-height: 420px;
        }}
        .chart-card.empty {{
            min-height: 140px;
        }}
        .card-title {{
            color: #eaf5ff;
            font-size: .98rem;
            font-weight: 850;
            margin-bottom: 8px;
        }}
        .chart-frame {{
            min-height: 360px;
        }}
        .meta-grid {{
            display: grid;
            grid-template-columns: .8fr 1.2fr;
            gap: 18px;
        }}
        .field-group {{
            margin-bottom: 16px;
        }}
        .field-type {{
            color: #eaf5ff;
            font-weight: 850;
            margin-bottom: 8px;
        }}
        .field-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}
        .field-badge, .badge {{
            display: inline-block;
            background: rgba(103,215,255,.12);
            border: 1px solid rgba(103,215,255,.26);
            color: #dff6ff;
            border-radius: 999px;
            padding: 5px 9px;
            font-size: .78rem;
            font-weight: 800;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: .86rem;
        }}
        .data-table th, .data-table td {{
            padding: 10px 11px;
            border-bottom: 1px solid rgba(133,184,235,.18);
            text-align: left;
            vertical-align: top;
        }}
        .data-table th {{
            color: #eaf5ff;
            background: rgba(103,215,255,.12);
            font-weight: 850;
        }}
        .table-scroll {{
            overflow-x: auto;
        }}
        .ai-section {{
            border-top: 4px solid #67d7ff;
        }}
        .ai-content {{
            color: #d8e7f7;
            line-height: 1.75;
        }}
        .ai-content h3 {{
            color: #ffffff;
            margin: 22px 0 8px;
        }}
        .footer {{
            color: #9fb3c9;
            text-align: center;
            padding: 26px 16px 36px;
            font-size: .86rem;
        }}
        @media (max-width: 900px) {{
            .topbar-inner, .section-heading {{
                display: block;
            }}
            .domain-chip {{
                margin-top: 16px;
            }}
            .dashboard-grid, .meta-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
<main class="shell">
    <header class="topbar">
        <div class="topbar-inner">
            <div>
                <h1>{domain_icon} DataForge AI Dashboard</h1>
                <div class="subtitle">PowerBI-style analytics report generated on {generated_at}</div>
            </div>
            <div class="domain-chip">
                <span>Detected domain</span>
                <strong>{domain}</strong>
                <div class="subtitle">Confidence: {confidence}%</div>
            </div>
        </div>
    </header>

    <div class="container">
        <section class="kpi-grid">
            {kpi_html}
        </section>

        {ai_section}

        <section class="section">
            <div class="section-heading">
                <span>Dashboard</span>
                <h2>Visual Analytics</h2>
            </div>
            <div class="dashboard-grid">
                {chart_sections}
            </div>
        </section>

        <section class="section">
            <div class="section-heading">
                <span>Data Intelligence</span>
                <h2>Fields and Cleaning Operations</h2>
            </div>
            <div class="meta-grid">
                <div>{field_html}</div>
                <div class="table-scroll">
                    <table class="data-table">
                        <thead><tr><th>Operation</th><th>Details</th></tr></thead>
                        <tbody>{log_html}</tbody>
                    </table>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="section-heading">
                <span>Profile</span>
                <h2>Statistical Summary</h2>
            </div>
            <div class="table-scroll">{summary_html}</div>
        </section>
    </div>

    <footer class="footer">
        Generated by DataForge AI Analytics Engine
    </footer>
</main>
</body>
</html>
        """

    @staticmethod
    def get_kpis(df, domain, fa):
        """Generate domain-specific KPIs."""
        kpis = {}

        if "Employee" in domain:
            kpis["Total Employees"] = f"{len(df):,}"
            sal = fa.find_col(df, ["salary", "pay", "ctc"])
            if sal:
                kpis["Avg Salary"] = f"${df[sal].mean():,.0f}"
                kpis["Total Payroll"] = f"${df[sal].sum():,.0f}"
                kpis["Max Salary"] = f"${df[sal].max():,.0f}"

            attr = fa.find_col(df, ["attrition", "left"])
            if attr:
                rate = (df[attr].astype(str).str.lower().isin(
                    ["yes", "1", "true"]).sum() / len(df)) * 100
                kpis["Attrition Rate"] = f"{rate:.1f}%"

        elif "Sales" in domain:
            kpis["Total Orders"] = f"{len(df):,}"
            rev = fa.find_col(df, ["revenue", "sales", "amount", "total"])
            if rev:
                kpis["Total Revenue"] = f"${df[rev].sum():,.0f}"
                kpis["Avg Order"] = f"${df[rev].mean():,.2f}"
            profit = fa.find_col(df, ["profit"])
            if profit:
                kpis["Total Profit"] = f"${df[profit].sum():,.0f}"
            cust = fa.find_col(df, ["customer"])
            if cust:
                kpis["Customers"] = f"{df[cust].nunique():,}"
            prod = fa.find_col(df, ["product"])
            if prod:
                kpis["Products"] = str(df[prod].nunique())

        elif "Finance" in domain:
            kpis["Transactions"] = f"{len(df):,}"
            inc = fa.find_col(df, ["income", "credit"])
            exp = fa.find_col(df, ["expense", "debit"])
            if inc:
                kpis["Total Income"] = f"${df[inc].sum():,.0f}"
            if exp:
                kpis["Total Expense"] = f"${df[exp].sum():,.0f}"
            if inc and exp:
                kpis["Net Profit"] = f"${(df[inc].sum() - df[exp].sum()):,.0f}"

        else:
            kpis["Total Rows"] = f"{len(df):,}"
            kpis["Total Columns"] = str(len(df.columns))
            kpis["Missing Values"] = str(df.isnull().sum().sum())
            num_cols = df.select_dtypes(include="number").columns
            if len(num_cols) > 0:
                kpis[f"Avg {num_cols[0]}"] = f"{df[num_cols[0]].mean():,.2f}"

        return kpis

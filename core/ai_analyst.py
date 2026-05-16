"""
DataForge - AI Analyst powered by Groq
Provides intelligent insights based on detected domain & columns
"""
import os
import re
from dotenv import load_dotenv

load_dotenv()

try:
    from groq import Groq
except ImportError:
    Groq = None


class AIAnalyst:

    def __init__(self):
        self.model = "llama-3.3-70b-versatile"
        self.status_message = ""
        api_key = os.getenv("GROQ_API_KEY")
        if Groq is None:
            self.client = None
            self.available = False
            self.status_message = "Groq SDK is not installed. Run: pip install groq"
        elif not api_key:
            self.client = None
            self.available = False
            self.status_message = "GROQ_API_KEY is missing from .env"
        else:
            try:
                self.client = Groq(api_key=api_key)
                self.available = True
                self.status_message = f"Groq connected with {self.model}"
            except Exception as e:
                self.client = None
                self.available = False
                self.status_message = f"Groq client error: {e}"

    @staticmethod
    def clean_ai_html(content):
        """Remove markdown fences/wrappers so model HTML renders as UI, not code."""
        if not content:
            return ""

        cleaned = content.strip()
        cleaned = re.sub(r"^`{1,3}(?:html)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*`{1,3}$", "", cleaned)

        body_match = re.search(r"<body[^>]*>(.*?)</body>", cleaned, flags=re.IGNORECASE | re.DOTALL)
        if body_match:
            cleaned = body_match.group(1).strip()

        cleaned = re.sub(r"<!doctype[^>]*>", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"</?(?:html|head|body)[^>]*>", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"<script[\s\S]*?</script>", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"<style[\s\S]*?</style>", "", cleaned, flags=re.IGNORECASE)
        return cleaned.strip()

    def _build_context(self, df, domain, kpis, fields):
        """Build rich context including DOMAIN + actual COLUMNS"""

        # Get column samples
        col_info = []
        for col in df.columns[:15]:  # Limit to 15 cols for token efficiency
            dtype = str(df[col].dtype)
            sample = df[col].dropna().head(3).tolist()
            col_info.append(f"  - {col} ({dtype}): {sample}")

        context = f"""
DATASET DOMAIN: {domain}

ACTUAL COLUMNS IN DATASET:
{chr(10).join(col_info)}

KEY METRICS (KPIs) CALCULATED:
{chr(10).join([f'  - {k}: {v}' for k, v in kpis.items()])}

DATA SHAPE: {len(df)} rows × {len(df.columns)} columns

STATISTICAL SUMMARY:
{df.describe(include='all').head(8).to_string()}

FIELD MAPPING:
  - Numeric columns: {fields.get('numeric', [])}
  - Categorical columns: {fields.get('categorical', [])}
  - Date columns: {fields.get('datetime', [])}
"""
        return context

    def generate_insights(self, df, domain, kpis, fields):
        """Generate comprehensive analyst-grade insights"""

        if not self.available:
            return self._fallback_insights(df, domain, kpis)

        context = self._build_context(df, domain, kpis, fields)

        prompt = f"""You are a SENIOR DATA ANALYST with 15 years of experience specializing in {domain}.

{context}

Based on the ACTUAL DATA above (specifically the {domain} domain with the listed columns), provide a comprehensive analysis report in clean HTML format using these sections:

<h3>🎯 Executive Summary</h3>
<p>2-3 line overview of the dataset and key findings</p>

<h3>🔍 Key Insights</h3>
<ul>
<li>Insight 1 with specific numbers from the data</li>
<li>Insight 2 with specific numbers</li>
<li>Insight 3 with specific numbers</li>
<li>Insight 4 with specific numbers</li>
<li>Insight 5 with specific numbers</li>
</ul>

<h3>⚠️ Problems & Anomalies Detected</h3>
<ul>
<li>Issue 1 with explanation</li>
<li>Issue 2 with explanation</li>
<li>Issue 3 with explanation</li>
</ul>

<h3>💡 Improvement Recommendations</h3>
<ul>
<li><strong>Action 1:</strong> Specific recommendation for {domain}</li>
<li><strong>Action 2:</strong> Specific recommendation</li>
<li><strong>Action 3:</strong> Specific recommendation</li>
<li><strong>Action 4:</strong> Specific recommendation</li>
</ul>

<h3>📊 KPIs to Monitor Going Forward</h3>
<ul>
<li>Critical metric 1</li>
<li>Critical metric 2</li>
<li>Critical metric 3</li>
</ul>

<h3>🚀 Strategic Action Plan (Next 30 Days)</h3>
<ol>
<li>Week 1: Concrete action</li>
<li>Week 2: Concrete action</li>
<li>Week 3: Concrete action</li>
<li>Week 4: Concrete action</li>
</ol>

IMPORTANT:
- Use ACTUAL numbers from the data
- Be specific to {domain} domain
- Reference the actual column names
- Output ONLY clean HTML (no markdown, no code blocks)
- Be professional and actionable
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system",
                     "content": "You are an elite data analyst providing executive-level insights in clean HTML format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=2500
            )
            return self.clean_ai_html(response.choices[0].message.content)
        except Exception as e:
            return self._fallback_insights(df, domain, kpis, error=str(e))

    def chat(self, df, domain, kpis, fields, question, history=None):
        """Conversational chatbot"""

        if not self.available:
            return "⚠️ AI Chat unavailable. Please configure your GROQ_API_KEY in the .env file."

        context = self._build_context(df, domain, kpis, fields)

        messages = [
            {"role": "system", "content": f"""You are DataForge AI, an expert {domain} data analyst.
Answer questions about the dataset with specific numbers and actionable insights.
Always reference actual data values and column names. Be concise but insightful.

{context}"""}
        ]

        if history:
            for h in history[-6:]:
                messages.append(h)

        messages.append({"role": "user", "content": question})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,
                max_tokens=1000
            )
            return self.clean_ai_html(response.choices[0].message.content)
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _fallback_insights(self, df, domain, kpis, error=None):
        """Fallback when AI is unavailable"""
        msg = ""
        if error:
            msg = f"<p style='color:#FF6B6B;'>⚠️ AI Error: {error}</p>"

        kpi_list = "".join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in kpis.items()])

        return f"""
        {msg}
        <h3>📊 Basic Analysis (AI Unavailable)</h3>
        <p>Domain detected: <strong>{domain}</strong></p>
        <p>Dataset contains <strong>{len(df):,} records</strong> across <strong>{len(df.columns)} columns</strong>.</p>

        <h3>🎯 Key Metrics</h3>
        <ul>{kpi_list}</ul>

        <h3>💡 General Recommendations</h3>
        <ul>
            <li>Configure Groq API key in <code>.env</code> for AI-powered insights</li>
            <li>Visit <a href="https://console.groq.com/keys">https://console.groq.com/keys</a> for free API key</li>
            <li>Review the charts and KPIs above for data trends</li>
        </ul>
        """

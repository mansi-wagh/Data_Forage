"""
DataForge - Dynamic Chart Engine
Generates domain-specific charts as base64 images and HTML
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import base64
from core.field_analyzer import FieldAnalyzer


class ChartEngine:

    COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
              '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
              '#BB8FCE', '#85C1E9']

    @classmethod
    def generate(cls, df, domain, fields):
        charts = []
        fa = FieldAnalyzer

        # ---- EMPLOYEE / HR ----
        if "Employee" in domain:
            charts.extend(cls._employee_charts(df, fa))

        # ---- SALES ----
        elif "Sales" in domain:
            charts.extend(cls._sales_charts(df, fa))

        # ---- FINANCE ----
        elif "Finance" in domain:
            charts.extend(cls._finance_charts(df, fa))

        # ---- MARKETING ----
        elif "Marketing" in domain:
            charts.extend(cls._marketing_charts(df, fa))

        # Always add generic charts as supplement
        charts.extend(cls._generic_charts(df, fields))

        return charts[:12]  # Max 12 charts

    @classmethod
    def _employee_charts(cls, df, fa):
        charts = []
        dept = fa.find_col(df, ["department", "dept"])
        salary = fa.find_col(df, ["salary", "compensation", "pay", "ctc"])
        exp = fa.find_col(df, ["experience", "years", "tenure"])
        gender = fa.find_col(df, ["gender", "sex"])
        age = fa.find_col(df, ["age"])
        perf = fa.find_col(df, ["performance", "rating", "score"])
        desig = fa.find_col(df, ["designation", "role", "position", "title", "job"])
        attrition = fa.find_col(df, ["attrition", "left", "resigned"])

        if dept and salary:
            data = df.groupby(dept)[salary].mean().sort_values(ascending=True).reset_index()
            fig = px.bar(data, y=dept, x=salary, orientation='h',
                         title="Average Salary by Department",
                         color=salary, color_continuous_scale="Viridis")
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Average Salary by Department", fig))

        if dept:
            data = df[dept].value_counts().reset_index()
            data.columns = [dept, "count"]
            fig = px.pie(data, names=dept, values="count",
                         title="Workforce Distribution", hole=0.45,
                         color_discrete_sequence=cls.COLORS)
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Workforce Distribution", fig))

        if gender:
            data = df[gender].value_counts().reset_index()
            data.columns = [gender, "count"]
            fig = px.pie(data, names=gender, values="count",
                         title="Gender Diversity", hole=0.45,
                         color_discrete_sequence=["#FF6B6B", "#4ECDC4", "#45B7D1"])
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Gender Diversity", fig))

        if salary:
            fig = px.histogram(df, x=salary, nbins=30,
                               title="Salary Distribution",
                               color_discrete_sequence=["#4ECDC4"])
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Salary Distribution", fig))

        if age and dept:
            fig = px.box(df, x=dept, y=age,
                         title="Age Distribution by Department",
                         color=dept, color_discrete_sequence=cls.COLORS)
            fig.update_layout(template="plotly_white", height=400, showlegend=False)
            charts.append(("Age by Department", fig))

        if perf and salary:
            fig = px.scatter(df, x=perf, y=salary,
                             color=dept if dept else None,
                             title="Performance vs Salary",
                             color_discrete_sequence=cls.COLORS)
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Performance vs Salary", fig))

        if exp and salary:
            fig = px.scatter(df, x=exp, y=salary,
                             title="Experience vs Salary",
                             color_discrete_sequence=["#FF6B6B"])
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Experience vs Salary", fig))

        if attrition:
            data = df[attrition].value_counts().reset_index()
            data.columns = [attrition, "count"]
            fig = px.bar(data, x=attrition, y="count",
                         title="Attrition Overview",
                         color=attrition, color_discrete_sequence=["#4CAF50", "#FF6B6B"])
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Attrition Overview", fig))

        if desig:
            data = df[desig].value_counts().head(10).reset_index()
            data.columns = [desig, "count"]
            fig = px.bar(data, y=desig, x="count", orientation='h',
                         title="Top 10 Designations",
                         color="count", color_continuous_scale="Blues")
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Top Designations", fig))

        return charts

    @classmethod
    def _sales_charts(cls, df, fa):
        charts = []
        revenue = fa.find_col(df, ["revenue", "sales", "amount", "total", "price"])
        product = fa.find_col(df, ["product", "item", "name"])
        region = fa.find_col(df, ["region", "country", "city", "state", "location"])
        date = fa.find_col(df, ["date", "order_date"])
        customer = fa.find_col(df, ["customer", "client", "buyer"])
        qty = fa.find_col(df, ["quantity", "qty", "units"])
        profit = fa.find_col(df, ["profit", "margin"])
        category = fa.find_col(df, ["category", "type", "segment"])

        if date and revenue:
            temp = df.copy()
            temp[date] = pd.to_datetime(temp[date], errors='coerce')
            temp = temp.dropna(subset=[date])
            trend = temp.groupby(temp[date].dt.to_period("M"))[revenue].sum().reset_index()
            trend[date] = trend[date].astype(str)
            fig = px.line(trend, x=date, y=revenue,
                          title="Revenue Trend Over Time",
                          markers=True, color_discrete_sequence=["#FF6B6B"])
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Revenue Trend", fig))

        if product and revenue:
            data = df.groupby(product)[revenue].sum().nlargest(10).reset_index()
            fig = px.bar(data, y=product, x=revenue, orientation='h',
                         title="Top 10 Products by Revenue",
                         color=revenue, color_continuous_scale="Oranges")
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Top Products", fig))

        if region and revenue:
            data = df.groupby(region)[revenue].sum().reset_index()
            fig = px.pie(data, names=region, values=revenue,
                         title="Revenue by Region", hole=0.45,
                         color_discrete_sequence=cls.COLORS)
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Revenue by Region", fig))

        if category and revenue:
            data = df.groupby(category)[revenue].sum().reset_index()
            fig = px.bar(data, x=category, y=revenue,
                         title="Revenue by Category",
                         color=category, color_discrete_sequence=cls.COLORS)
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Revenue by Category", fig))

        if profit and category:
            data = df.groupby(category)[profit].sum().reset_index()
            fig = px.bar(data, x=category, y=profit,
                         title="Profit by Category",
                         color=profit, color_continuous_scale="RdYlGn")
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Profit by Category", fig))

        if customer and revenue:
            data = df.groupby(customer)[revenue].sum().nlargest(10).reset_index()
            fig = px.bar(data, y=customer, x=revenue, orientation='h',
                         title="Top 10 Customers",
                         color=revenue, color_continuous_scale="Blues")
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Top Customers", fig))

        if qty and revenue:
            fig = px.scatter(df.head(500), x=qty, y=revenue,
                             color=category if category else None,
                             title="Quantity vs Revenue",
                             color_discrete_sequence=cls.COLORS)
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Quantity vs Revenue", fig))

        if revenue:
            fig = px.histogram(df, x=revenue, nbins=30,
                               title="Revenue Distribution",
                               color_discrete_sequence=["#45B7D1"])
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Revenue Distribution", fig))

        return charts

    @classmethod
    def _finance_charts(cls, df, fa):
        charts = []
        income = fa.find_col(df, ["income", "credit", "revenue"])
        expense = fa.find_col(df, ["expense", "debit", "cost"])
        date = fa.find_col(df, ["date"])
        category = fa.find_col(df, ["category", "type"])

        if date and (income or expense):
            temp = df.copy()
            temp[date] = pd.to_datetime(temp[date], errors='coerce')
            temp = temp.dropna(subset=[date])
            cols = [c for c in [income, expense] if c]
            trend = temp.groupby(temp[date].dt.to_period("M"))[cols].sum().reset_index()
            trend[date] = trend[date].astype(str)
            fig = px.line(trend, x=date, y=cols,
                          title="Income vs Expense Trend", markers=True)
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Cash Flow Trend", fig))

        if category and expense:
            data = df.groupby(category)[expense].sum().reset_index()
            fig = px.pie(data, names=category, values=expense,
                         title="Expense Breakdown", hole=0.45,
                         color_discrete_sequence=cls.COLORS)
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Expense Breakdown", fig))

        return charts

    @classmethod
    def _marketing_charts(cls, df, fa):
        charts = []
        campaign = fa.find_col(df, ["campaign"])
        clicks = fa.find_col(df, ["click", "clicks"])
        conversions = fa.find_col(df, ["conversion", "conversions"])
        channel = fa.find_col(df, ["channel", "source", "medium"])

        if channel and clicks:
            data = df.groupby(channel)[clicks].sum().reset_index()
            fig = px.bar(data, x=channel, y=clicks,
                         title="Clicks by Channel",
                         color=channel, color_discrete_sequence=cls.COLORS)
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Clicks by Channel", fig))

        if campaign and conversions:
            data = df.groupby(campaign)[conversions].sum().nlargest(10).reset_index()
            fig = px.bar(data, y=campaign, x=conversions, orientation='h',
                         title="Top Campaigns by Conversions",
                         color=conversions, color_continuous_scale="Greens")
            fig.update_layout(template="plotly_white", height=400)
            charts.append(("Top Campaigns", fig))

        return charts

    @classmethod
    def _generic_charts(cls, df, fields):
        charts = []
        # Removed correlation heatmap as it is not required
        return charts

    @staticmethod
    def fig_to_html(fig):
        """Convert plotly figure to embeddable HTML"""
        return fig.to_html(full_html=False, include_plotlyjs=False)

    @staticmethod
    def fig_to_image_base64(fig):
        """Convert plotly figure to base64 PNG"""
        img_bytes = fig.to_image(format="png", width=700, height=400, scale=2)
        return base64.b64encode(img_bytes).decode()

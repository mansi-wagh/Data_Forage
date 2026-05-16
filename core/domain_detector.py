"""
DataForge - Smart Domain Detector
Detects: Employee, Sales, Finance, Marketing, Healthcare, Inventory
"""


class DomainDetector:

    SIGNATURES = {
        "Employee / HR": {
            "keywords": [
                "employee", "emp", "salary", "department", "designation",
                "hire", "experience", "manager", "attendance", "performance",
                "joining", "tenure", "appraisal", "leave", "gender", "age",
                "attrition", "promotion", "overtime", "satisfaction"
            ],
            "icon": "👥",
            "color": "#4CAF50"
        },
        "Sales": {
            "keywords": [
                "sales", "revenue", "product", "order", "customer",
                "quantity", "profit", "discount", "invoice", "region",
                "price", "unit", "store", "channel", "transaction"
            ],
            "icon": "💰",
            "color": "#FF9800"
        },
        "Finance": {
            "keywords": [
                "expense", "income", "balance", "account", "investment",
                "credit", "debit", "budget", "loan", "interest",
                "tax", "asset", "liability"
            ],
            "icon": "💹",
            "color": "#2196F3"
        },
        "Marketing": {
            "keywords": [
                "campaign", "click", "impression", "conversion", "ctr",
                "engagement", "channel", "lead", "audience", "reach",
                "bounce", "session"
            ],
            "icon": "📣",
            "color": "#E91E63"
        },
        "Healthcare": {
            "keywords": [
                "patient", "diagnosis", "treatment", "hospital", "doctor",
                "medication", "prescription", "disease", "symptom"
            ],
            "icon": "🏥",
            "color": "#00BCD4"
        },
        "Inventory": {
            "keywords": [
                "stock", "warehouse", "sku", "inventory", "supplier",
                "reorder", "shipment", "batch"
            ],
            "icon": "📦",
            "color": "#795548"
        },
    }

    @classmethod
    def detect(cls, df):
        cols_text = " ".join([c.lower().replace("_", " ") for c in df.columns])

        scores = {}
        for domain, config in cls.SIGNATURES.items():
            score = sum(1 for kw in config["keywords"] if kw in cols_text)
            scores[domain] = score

        best = max(scores, key=scores.get)

        if scores[best] == 0:
            return "General", "🔧", "#607D8B", 0

        confidence = min(round((scores[best] / 5) * 100, 1), 100)
        return best, cls.SIGNATURES[best]["icon"], cls.SIGNATURES[best]["color"], confidence
"""
DataForge - Intelligent Field Analyzer
Classifies every column for chart generation
"""
import pandas as pd
import numpy as np


class FieldAnalyzer:

    @staticmethod
    def analyze(df):
        result = {
            "numeric": [],
            "categorical": [],
            "datetime": [],
            "identifier": [],
            "boolean": []
        }

        for col in df.columns:
            col_lower = col.lower()

            # Boolean
            if df[col].nunique() == 2:
                vals = set(df[col].dropna().astype(str).str.lower())
                if vals.issubset({'yes', 'no', 'true', 'false', '0', '1', 'y', 'n'}):
                    result["boolean"].append(col)
                    continue

            # Identifier
            if (("id" in col_lower or "code" in col_lower)
                    and df[col].nunique() >= len(df) * 0.9):
                result["identifier"].append(col)
                continue

            # Datetime
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                result["datetime"].append(col)
                continue

            # Numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                result["numeric"].append(col)
                continue

            # Categorical
            if df[col].dtype == 'object':
                if df[col].nunique() < len(df) * 0.5:
                    result["categorical"].append(col)
                continue

        return result

    @staticmethod
    def find_col(df, keywords):
        for col in df.columns:
            cl = col.lower()
            for kw in keywords:
                if kw in cl:
                    return col
        return None
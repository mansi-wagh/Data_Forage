"""
DataForge - Smart Data Cleaning Engine
Handles: Missing values, duplicates, types, outliers, formatting
"""
import pandas as pd
import numpy as np


class DataCleaner:

    def __init__(self, df):
        self.original_df = df.copy()
        self.df = df.copy()
        self.cleaning_log = []

    def _log(self, action, details):
        self.cleaning_log.append({"action": action, "details": details})

    def remove_duplicates(self):
        """Remove duplicate rows"""
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = before - len(self.df)
        if removed > 0:
            self._log("Remove Duplicates", f"Removed {removed} duplicate rows")
        return self

    def clean_column_names(self):
        """Standardize column names"""
        original_cols = self.df.columns.tolist()
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(r'[^\w\s]', '', regex=True)
            .str.replace(r'\s+', '_', regex=True)
        )
        renamed = sum(1 for a, b in zip(original_cols, self.df.columns) if a != b)
        if renamed > 0:
            self._log("Clean Column Names", f"Standardized {renamed} column names")
        return self

    def handle_missing_values(self):
        """Smart missing value handling"""
        total_filled = 0

        for col in self.df.columns:
            missing = self.df[col].isnull().sum()
            if missing == 0:
                continue

            missing_pct = (missing / len(self.df)) * 100

            # Drop column if >60% missing
            if missing_pct > 60:
                self.df.drop(columns=[col], inplace=True)
                self._log("Drop Column", f"Dropped '{col}' ({missing_pct:.1f}% missing)")
                continue

            # Numeric: fill with median
            if pd.api.types.is_numeric_dtype(self.df[col]):
                median_val = self.df[col].median()
                self.df[col].fillna(median_val, inplace=True)
                total_filled += missing
                self._log("Fill Missing",
                          f"'{col}': Filled {missing} values with median ({median_val:.2f})")

            # Categorical: fill with mode
            else:
                mode_val = self.df[col].mode()
                if not mode_val.empty:
                    self.df[col].fillna(mode_val[0], inplace=True)
                    total_filled += missing
                    self._log("Fill Missing",
                              f"'{col}': Filled {missing} values with mode ('{mode_val[0]}')")

        return self

    def fix_data_types(self):
        """Auto-detect and fix data types"""
        for col in self.df.columns:
            # Try numeric
            if self.df[col].dtype == 'object':
                try:
                    converted = pd.to_numeric(self.df[col], errors='coerce')
                    if converted.notna().sum() > len(self.df) * 0.8:
                        self.df[col] = converted
                        self._log("Fix Type", f"'{col}': Converted to numeric")
                        continue
                except:
                    pass

                # Try datetime
                try:
                    converted = pd.to_datetime(self.df[col], errors='coerce', infer_datetime_format=True)
                    if converted.notna().sum() > len(self.df) * 0.8:
                        self.df[col] = converted
                        self._log("Fix Type", f"'{col}': Converted to datetime")
                        continue
                except:
                    pass

        return self

    def remove_outliers(self, threshold=3):
        """Remove extreme outliers using Z-score (numeric only)"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        before = len(self.df)

        for col in numeric_cols:
            if self.df[col].std() == 0:
                continue
            z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
            self.df = self.df[z_scores < threshold]

        removed = before - len(self.df)
        if removed > 0:
            self._log("Remove Outliers", f"Removed {removed} outlier rows (Z>{threshold})")
        return self

    def trim_whitespace(self):
        """Strip whitespace from string columns"""
        str_cols = self.df.select_dtypes(include=['object']).columns
        for col in str_cols:
            self.df[col] = self.df[col].str.strip()
        if len(str_cols) > 0:
            self._log("Trim Whitespace", f"Trimmed {len(str_cols)} text columns")
        return self

    def clean(self):
        """Run full cleaning pipeline"""
        self.clean_column_names()
        self.remove_duplicates()
        self.trim_whitespace()
        self.fix_data_types()
        self.handle_missing_values()
        self.remove_outliers()

        self._log("Summary",
                  f"Original: {len(self.original_df)} rows → Cleaned: {len(self.df)} rows | "
                  f"Columns: {len(self.original_df.columns)} → {len(self.df.columns)}")
        return self.df, self.cleaning_log
"""
Example: Quick test of the ETL pipeline with sample data

This script demonstrates how to use individual cleaning functions
and the utilities module.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils import (
    to_snake_case,
    anonymize_text,
    logger
)

# Example 1: Column name standardization
print("Example 1: Column Name Standardization")
print("-" * 50)
example_columns = [
    "First Name",
    "CONVERSATION ID",
    "Date-Sent",
    "Company Name",
    "MESSAGE CONTENT"
]

for col in example_columns:
    snake = to_snake_case(col)
    print(f"{col:25} → {snake}")

print("\n")

# Example 2: Text anonymization
print("Example 2: Text Anonymization (Hashing)")
print("-" * 50)
sensitive_data = [
    "John Doe",
    "jane.smith@email.com",
    "https://linkedin.com/in/johndoe",
]

for data in sensitive_data:
    hashed = anonymize_text(data)
    print(f"{data:35} → {hashed}")

print("\n")

# Example 3: Running a single dataset cleaner
print("Example 3: Testing Data Pipeline")
print("-" * 50)
print("To test the pipeline with your data:")
print("1. Add your CSV files to data/raw/")
print("2. Run: python run_pipeline.py --skip-missing")
print("3. Check data/cleaned/ for results")

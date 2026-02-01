# LinkedIn Networking Analytics - Quick Reference

## 🚀 Quick Commands

### Setup & Installation
```bash
pip install -r requirements.txt
```

### Run Complete Pipeline
```bash
python run_pipeline.py
```

### Run with Missing Files
```bash
python run_pipeline.py --skip-missing
```

### Test Utilities
```bash
python examples/test_pipeline.py
```

---

## 📊 Dataset Summary

| File | Records* | Purpose | Key Columns |
|------|----------|---------|-------------|
| `Invitations.csv` | Varies | Connection requests | from, to, sent_at, direction |
| `Connections.csv` | Varies | Accepted connections | name, company, connected_on |
| `messages.csv` | Varies | Direct messages | conversation_id, sender, date, content |
| `guide_messages.csv` | Varies | LinkedIn guided msgs | message_type, sent_at |
| `learning_coach_messages.csv` | Varies | Learning interactions | course, date |
| `Comments.csv` | Varies | Public comments | post_url, comment, date |

*Depends on your LinkedIn activity

---

## 🔧 Core Functions Reference

### From `src/utils.py`

```python
# Column standardization
to_snake_case("First Name")  # → "first_name"

# Anonymization
anonymize_text("john.doe@email.com")  # → "a3b5c7d9"

# DateTime parsing
parse_datetime_column(series, "date_column")

# Full standardization
standardize_dataframe(
    df, 
    source_name="invitations",
    datetime_columns=["sent_at", "accepted_at"],
    anonymize_columns=["first_name", "last_name"]
)

# Save cleaned data
save_cleaned_data(df, "output.csv", "data/cleaned")

# Load raw data
df = load_raw_data("Invitations.csv", "data/raw")

# Quality report
report = generate_data_quality_report(df, "invitations")
```

---

## 📁 File Locations

### Input Files
- `data/raw/` - Your LinkedIn CSV exports (git-ignored)

### Output Files
- `data/cleaned/` - Standardized datasets
- `outputs/pipeline_report.json` - Processing summary
- `powerbi/` - Power BI files

### Code
- `src/` - Core modules and cleaning scripts
- `run_pipeline.py` - Main ETL orchestrator
- `examples/` - Usage examples

---

## 🎯 Key Metrics to Calculate

### Funnel Metrics
- **Acceptance Rate**: Connections / Invitations Sent
- **Response Rate**: Replies Received / Messages Sent  
- **Conversion Rate**: Outcomes / Conversations
- **Network Velocity**: Connections / Month

### Engagement Metrics
- **Time to Accept**: Avg days from invite to connection
- **Reply Latency**: Avg time to first response
- **Conversation Depth**: Avg messages per thread
- **Outcome Rate**: % conversations with positive keywords

### Growth Metrics
- **Monthly Connection Growth**: Net new connections
- **Industry Diversification**: Unique industries
- **Company Spread**: Unique companies
- **Engagement Frequency**: Comments per week

---

## 🔍 Data Quality Checks

After running pipeline, verify:

✅ All date columns parsed correctly  
✅ No duplicate records  
✅ PII columns anonymized (check for `_hash` suffix)  
✅ `source_table` column added  
✅ Column names in snake_case  
✅ Row counts match expected values  

---

## 🛠️ Customization

### Add Custom Keywords

Edit `src/clean_messages.py`:

```python
df['has_custom_keyword'] = text_lower.str.contains(
    r'your|custom|keywords', regex=True
)
```

### Change Hash Length

Edit `src/utils.py`:

```python
def anonymize_text(text: str, hash_length: int = 12):  # Changed from 8
```

### Add New Dataset

1. Create new cleaning script: `src/clean_newdata.py`
2. Follow template from existing scripts
3. Add to pipeline in `run_pipeline.py`

---

## 📈 Analysis Ideas

### Beginner
- Basic funnel visualization
- Connection growth chart
- Industry distribution pie chart

### Intermediate  
- Response rate by day of week
- Time-to-accept distribution
- Message sentiment analysis

### Advanced
- Predictive model for acceptance
- Network clustering analysis
- A/B testing message templates
- Survival analysis for response time

---

## 🐛 Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "File not found"
Check files are in `data/raw/` and spelled correctly

### "Permission denied"
```bash
chmod +x run_pipeline.py
```

### Different column names
LinkedIn export format changed - update cleaning scripts

---

## 📚 Resources

- [LinkedIn Data Export Help](https://www.linkedin.com/help/linkedin/answer/50191)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Power BI Desktop Download](https://powerbi.microsoft.com/desktop/)

---

## 🎓 Portfolio Tips

### For Recruiters/Employers

Highlight:
- **End-to-end pipeline** from raw data to insights
- **Privacy-conscious design** with full anonymization
- **Production-quality code** with logging, error handling
- **Clear documentation** and project structure
- **Reproducible workflow** anyone can run

### Project Showcase

Include in portfolio:
1. **README.md** - Overview and setup
2. **Code samples** - From `src/` directory  
3. **Visualizations** - Power BI dashboards
4. **Key insights** - Write-up of findings
5. **Metrics** - Actual numbers from analysis

---

## ✨ Next Steps

1. ✅ **Setup** - Install dependencies, add data
2. ✅ **Clean** - Run pipeline, verify outputs
3. 🔲 **Analyze** - Calculate metrics, find patterns
4. 🔲 **Visualize** - Build Power BI dashboard
5. 🔲 **Insights** - Write up findings
6. 🔲 **Share** - Add to portfolio, GitHub

---

**Happy analyzing!** 🚀

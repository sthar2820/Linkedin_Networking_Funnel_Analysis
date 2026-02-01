# LinkedIn Networking Analytics

> Professional portfolio project analyzing LinkedIn networking effectiveness using real export data

## 🎯 Project Overview

This project demonstrates end-to-end data analytics skills by analyzing LinkedIn networking patterns, measuring funnel effectiveness, and generating actionable insights. Built with production-quality code, this showcases:

- **Data Engineering**: ETL pipeline with automated cleaning & standardization
- **Analytics**: Funnel analysis, conversion metrics, engagement patterns
- **Privacy**: Full PII anonymization while preserving analytical value
- **Visualization**: Power BI-ready datasets for interactive dashboards
- **Documentation**: Industry-standard project structure & documentation

---

## 📊 Datasets & Analytics Funnel

### Complete Networking Funnel

```
ENGAGEMENT        →  OUTREACH     →  CONNECTION  →  CONVERSATION  →  OUTCOMES
(Comments.csv)       (Invitations)    (Connections)  (Messages)        (Keywords)
```

### Dataset Breakdown

| Dataset | Purpose | Key Metrics |
|---------|---------|-------------|
| **Invitations.csv** | Top of funnel | Acceptance rate, time-to-accept, sent vs received |
| **Connections.csv** | Network growth | Connection velocity, industry distribution, conversion rate |
| **messages.csv** | Mid-funnel engagement | Response rate, reply latency, conversation depth, outcomes |
| **guide_messages.csv** | Platform engagement | LinkedIn feature usage, guided outreach patterns |
| **learning_coach_messages.csv** | Learning signals | Skill-based networking, educational engagement |
| **Comments.csv** | Pre-outreach warming | Engagement frequency, visibility, relationship building |

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/sthar2820/Linkedin_Networking_Funnel_Analysis.git
cd Linkedin_Networking_Funnel_Analysis

# Install dependencies
pip install -r requirements.txt
```

### 2. Add Your LinkedIn Data

Export your LinkedIn data:
1. Go to LinkedIn Settings → Data Privacy → Get a copy of your data
2. Select "Want something in particular?" → Select all messaging & connection data
3. Download and extract the ZIP file
4. Copy the following files to `data/raw/`:
   - `Invitations.csv`
   - `Connections.csv`
   - `messages.csv`
   - `guide_messages.csv`
   - `learning_coach_messages.csv`
   - `Comments.csv`

### 3. Run the ETL Pipeline

```bash
# Process all datasets
python run_pipeline.py

# Or skip missing files
python run_pipeline.py --skip-missing
```

### 4. View Results

Cleaned data will be saved to `data/cleaned/`:
- All timestamps standardized to datetime
- Column names converted to snake_case
- PII anonymized (names, emails, URLs hashed)
- Duplicates removed
- Empty records cleaned
- Source table tracking added

---

## 📁 Project Structure

```
Linkedin_Networking_Funnel_Analysis/
│
├── data/
│   ├── raw/                    # Your LinkedIn export files (not tracked)
│   ├── cleaned/                # Standardized, anonymized data
│   └── processed/              # Analytics-ready tables
│
├── src/
│   ├── __init__.py
│   ├── utils.py                # Core utilities (snake_case, anonymization, parsing)
│   ├── clean_invitations.py    # Invitations cleaning script
│   ├── clean_connections.py    # Connections cleaning script
│   ├── clean_messages.py       # Messages cleaning + keyword extraction
│   ├── clean_guide_messages.py # Guide messages cleaning
│   ├── clean_learning_messages.py
│   └── clean_comments.py       # Comments cleaning script
│
├── notebooks/                  # Jupyter notebooks for analysis
├── outputs/                    # Reports, charts, metrics
├── powerbi/                    # Power BI files
│
├── run_pipeline.py             # Master ETL orchestration
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 🔧 Technical Implementation

### Data Standardization Pipeline

Every dataset goes through:

1. **Column Standardization**
   - Convert to `snake_case`
   - Example: `First Name` → `first_name`

2. **Datetime Parsing**
   - Flexible format detection
   - Consistent timezone handling
   - Invalid date logging

3. **Data Quality**
   - Remove empty rows
   - Deduplicate records
   - Null value reporting

4. **Privacy Protection**
   - SHA256 hashing for PII
   - Preserve analytical value
   - GDPR-compliant anonymization

5. **Metadata Tracking**
   - Add `source_table` column
   - Track processing timestamp
   - Quality metrics logging

### Key Features

- **Keyword Extraction**: Automatically detects outcome signals (referrals, interviews, positive/negative responses)
- **Conversation Threading**: Message grouping by conversation ID
- **Time Series Ready**: All timestamps parsed for temporal analysis
- **Power BI Integration**: Clean CSV exports ready for import

---

## 📈 Analytics Use Cases

### 1. Funnel Conversion Analysis
- Invitation → Connection conversion rate
- Connection → Conversation activation rate
- Conversation → Outcome success rate

### 2. Response Rate Optimization
- Cold vs warm outreach effectiveness
- Message timing impact on response rates
- Follow-up sequence analysis

### 3. Network Growth Metrics
- Monthly connection velocity
- Industry/company targeting effectiveness
- Network composition over time

### 4. Engagement Impact
- Comment engagement → Connection acceptance correlation
- Platform feature usage → Response rates
- Learning activity → Networking outcomes

---

## 🔒 Privacy & Ethics

This project is designed with privacy-first principles:

- **All PII is anonymized** using SHA256 hashing
- **Original data stays local** in `data/raw/` (git-ignored)
- **Shareable outputs** contain no personally identifiable information
- **GDPR compliant** - you control your own data

---

## 🎓 Skills Demonstrated

### Data Engineering
- ETL pipeline design & orchestration
- Data cleaning & standardization
- Schema design & normalization
- Error handling & logging

### Analytics
- Funnel analysis
- Conversion metrics
- Time series analysis
- Behavioral pattern detection

### Software Engineering
- Modular code architecture
- Documentation & code comments
- Version control best practices
- Reproducible workflows

### Tools & Technologies
- **Python**: pandas, numpy, datetime
- **Data Processing**: CSV handling, text parsing, regex
- **Visualization**: Power BI (ready)
- **Version Control**: Git, GitHub

---

## 📊 Next Steps (Future Enhancements)

- [ ] Build funnel visualization dashboard
- [ ] Calculate key metrics (response rate, conversion rate, etc.)
- [ ] Time series analysis of network growth
- [ ] Predictive modeling for outreach success
- [ ] A/B testing framework for message templates
- [ ] Power BI dashboard templates

---

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome! Feel free to:
- Open issues for bugs or enhancement ideas
- Fork and experiment with your own LinkedIn data
- Share insights or analytics approaches

---

## 📝 License

MIT License - Feel free to use this framework for your own LinkedIn analytics

---

## 👤 Author

**Your Name**
- GitHub: [@sthar2820](https://github.com/sthar2820)

---

## 🙏 Acknowledgments

This project analyzes personal LinkedIn export data to demonstrate real-world analytics capabilities. All data shown in examples is anonymized.

---

**⭐ If this project helped you, please give it a star!**

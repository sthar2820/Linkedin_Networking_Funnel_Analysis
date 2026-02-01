# LinkedIn Networking Analytics - Setup Instructions

## Step-by-Step Setup Guide

### 1. Prerequisites

Ensure you have Python 3.8 or higher installed:

```bash
python --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/sthar2820/Linkedin_Networking_Funnel_Analysis.git
cd Linkedin_Networking_Funnel_Analysis
```

### 3. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Export Your LinkedIn Data

#### Step-by-step:

1. Log into LinkedIn
2. Click your profile picture → Settings & Privacy
3. In left sidebar, click **Data privacy**
4. Click **Get a copy of your data**
5. Select **Want something in particular?**
6. Check these options:
   - ✅ Connections
   - ✅ Messages
   - ✅ Invitations
   - ✅ Comments
   - ✅ (Any other datasets you want)
7. Click **Request archive**
8. Wait for email (usually 24 hours)
9. Download and unzip the archive

### 6. Add Data to Project

Copy the CSV files to the `data/raw/` directory:

```bash
# Example file locations (from LinkedIn export):
cp ~/Downloads/linkedin-export/Connections.csv data/raw/
cp ~/Downloads/linkedin-export/messages.csv data/raw/
cp ~/Downloads/linkedin-export/Invitations.csv data/raw/
cp ~/Downloads/linkedin-export/Comments.csv data/raw/
# ... etc
```

### 7. Run the ETL Pipeline

```bash
# Process all available datasets
python run_pipeline.py --skip-missing
```

### 8. Check Results

Cleaned data will be in `data/cleaned/`:

```bash
ls -lh data/cleaned/
```

### 9. Next Steps

- Explore cleaned data with pandas
- Build analytics notebooks
- Import to Power BI
- Calculate key metrics

---

## Troubleshooting

### "No module named 'pandas'"

```bash
pip install pandas
```

### "File not found: data/raw/Connections.csv"

Make sure you've copied your LinkedIn export files to `data/raw/`

### Different column names in LinkedIn export

LinkedIn sometimes changes export formats. If you get errors:

1. Open the CSV file to check actual column names
2. Update the cleaning script for that dataset
3. Or open an issue on GitHub with details

### Virtual environment issues

If activation fails:

```bash
# Recreate the environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Running Tests

```bash
# Test the utilities
python examples/test_pipeline.py
```

---

## Need Help?

- Check the [README.md](README.md) for full documentation
- Open an issue on GitHub
- Review the code comments in `src/` files

---

**Ready to analyze your LinkedIn networking data!** 🚀

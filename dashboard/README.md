# LinkedIn Networking Analytics Dashboard

🚀 **Live Demo:** [Deploy to Streamlit Cloud]

## Premium Storytelling Dashboard

A data-driven narrative showcasing LinkedIn networking effectiveness through interactive visualizations.

### Features

✨ **No AI Symbols** - Clean, professional design  
📊 **Story-Driven** - Guides viewers through networking insights  
🎨 **Premium UI** - LinkedIn-inspired color scheme  
📈 **Interactive Charts** - Plotly visualizations  
🔒 **Privacy-First** - All data anonymized

### Pages

1. **Overview** - The networking funnel and key metrics
2. **Network Insights** - Connection patterns and composition
3. **Message Analysis** - Response rates and conversation quality

---

## Quick Start

### Local Development

```bash
# Navigate to dashboard directory
cd dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## Deploy to Streamlit Cloud

### Step 1: Push to GitHub

Ensure your repository is pushed to GitHub with all files.

### Step 2: Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - **Repository:** `sthar2820/Linkedin_Networking_Funnel_Analysis`
   - **Branch:** `main`
   - **Main file path:** `dashboard/app.py`
5. Click "Deploy!"

### Step 3: Configure

The app will automatically use:
- `dashboard/requirements.txt` for dependencies
- `dashboard/.streamlit/config.toml` for theme settings

---

## Data Requirements

The dashboard expects cleaned data in:
```
data/cleaned/
├── invitations_cleaned.csv
├── connections_cleaned.csv
└── messages_cleaned.csv
```

Run the ETL pipeline first:
```bash
python run_pipeline.py --skip-missing
```

---

## Customization

### Update Theme Colors

Edit `dashboard/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0A66C2"  # LinkedIn blue
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F3F6F8"
```

### Modify User Name

Update in page files (search for "Rohan Shrestha"):
```python
user_name = "Your Name"
```

---

## Tech Stack

- **Streamlit** - Web framework
- **Pandas** - Data processing
- **Plotly** - Interactive charts
- **Python** - Backend logic

---

## Project Structure

```
dashboard/
├── app.py                    # Main dashboard page
├── data_loader.py            # Data loading & metrics
├── pages/
│   ├── 1_🌐_Network_Insights.py
│   └── 2_💬_Message_Analysis.py
├── .streamlit/
│   └── config.toml           # Theme configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## Performance Tips

- Data is cached using `@st.cache_data`
- Loads only cleaned datasets (not raw)
- Optimized for fast rendering

---

## Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Data files not found"
Ensure you've run the ETL pipeline:
```bash
cd ..
python run_pipeline.py --skip-missing
```

### Deployment fails
- Check file paths are correct
- Verify all dependencies in requirements.txt
- Ensure data files are in repository

---

## Support

For issues or questions:
- Open an issue on GitHub
- Check Streamlit documentation
- Review the main project README

---

**Built with care for recruiter impact** 🎯

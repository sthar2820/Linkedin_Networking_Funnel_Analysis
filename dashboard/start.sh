#!/bin/bash

# LinkedIn Networking Analytics Dashboard - Quick Start Script

echo "🚀 Starting LinkedIn Networking Analytics Dashboard..."
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the dashboard directory"
    echo "   cd dashboard && ./start.sh"
    exit 1
fi

# Check if data exists
if [ ! -d "../data/cleaned" ]; then
    echo "⚠️  Warning: Cleaned data not found"
    echo "   Please run the ETL pipeline first:"
    echo "   cd .. && python3 run_pipeline.py --skip-missing"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "📦 Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ All checks passed!"
echo ""
echo "📊 Opening dashboard at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Streamlit
streamlit run app.py

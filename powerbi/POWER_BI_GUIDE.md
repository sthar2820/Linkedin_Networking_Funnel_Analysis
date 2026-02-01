# Power BI Integration Guide

## Loading Cleaned Data into Power BI

### Step 1: Import CSV Files

1. Open Power BI Desktop
2. Click **Get Data** → **Text/CSV**
3. Navigate to `data/cleaned/` directory
4. Import each cleaned CSV file:
   - `invitations_cleaned.csv`
   - `connections_cleaned.csv`
   - `messages_cleaned.csv`
   - `guide_messages_cleaned.csv`
   - `learning_messages_cleaned.csv`
   - `comments_cleaned.csv`

### Step 2: Data Modeling

#### Create Relationships

The datasets can be linked through these common fields:

- **Date/Time fields**: All have standardized datetime columns
- **Source tracking**: `source_table` column identifies origin

#### Recommended Dimension Tables

Create additional tables for better analysis:

1. **Date Dimension**
   - Extract from all datetime columns
   - Enable time-series analysis
   - Day, week, month, quarter, year hierarchies

2. **Metrics Table**
   - Calculated measures
   - KPIs and benchmarks

### Step 3: Key Metrics to Calculate

#### Funnel Metrics

```DAX
// Acceptance Rate
Acceptance_Rate = 
DIVIDE(
    COUNTROWS(connections_cleaned),
    COUNTROWS(FILTER(invitations_cleaned, [direction] = "sent"))
)

// Response Rate
Response_Rate = 
DIVIDE(
    COUNTROWS(FILTER(messages_cleaned, [sender_type] = "them")),
    COUNTROWS(FILTER(messages_cleaned, [sender_type] = "me"))
)

// Connection Velocity (per month)
Monthly_Connections = 
CALCULATE(
    COUNTROWS(connections_cleaned),
    DATESINPERIOD(connections_cleaned[connected_on], LASTDATE(connections_cleaned[connected_on]), -30, DAY)
)
```

#### Engagement Metrics

```DAX
// Avg Time to Accept (days)
Avg_Time_to_Accept = 
AVERAGEX(
    invitations_cleaned,
    DATEDIFF(invitations_cleaned[sent_at], invitations_cleaned[accepted_at], DAY)
)

// Conversation Depth
Avg_Messages_Per_Thread = 
DIVIDE(
    COUNTROWS(messages_cleaned),
    DISTINCTCOUNT(messages_cleaned[conversation_id])
)

// Outcome Success Rate
Outcome_Rate = 
DIVIDE(
    COUNTROWS(FILTER(messages_cleaned, [has_referral_keyword] = 1 || [has_interview_keyword] = 1)),
    DISTINCTCOUNT(messages_cleaned[conversation_id])
)
```

### Step 4: Recommended Visualizations

#### Page 1: Funnel Overview
- **Funnel Chart**: Invitations → Connections → Conversations → Outcomes
- **KPI Cards**: Acceptance rate, Response rate, Outcome rate
- **Line Chart**: Network growth over time

#### Page 2: Response Analysis
- **Column Chart**: Response rate by day of week
- **Scatter Plot**: Time to first response vs conversation depth
- **Table**: Top performing message types (by keywords)

#### Page 3: Network Composition
- **Tree Map**: Connections by company
- **Bar Chart**: Connections by industry
- **Line Chart**: Connection velocity trends

#### Page 4: Engagement Impact
- **Scatter**: Comments posted vs connections made
- **Column Chart**: Engagement type vs acceptance rate
- **Heatmap**: Best times to send invitations

### Step 5: Filters & Slicers

Add these slicers for interactivity:

- **Date Range**: Filter all visuals by time period
- **Source Table**: Toggle between datasets
- **Direction**: Sent vs received invitations
- **Outcome Type**: Filter by keyword categories

---

## Sample Dashboard Layout

```
┌─────────────────────────────────────────────────┐
│  LinkedIn Networking Analytics Dashboard       │
├─────────────────────────────────────────────────┤
│                                                 │
│  [Acceptance Rate] [Response Rate] [Outcomes]   │
│       78%              45%            12%        │
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐    │
│  │  Funnel Chart    │  │ Network Growth   │    │
│  │                  │  │  (Time Series)   │    │
│  │                  │  │                  │    │
│  └──────────────────┘  └──────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  Connections by Company (Tree Map)      │   │
│  │                                          │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Date Filter: [────────|──────] Source: [All]  │
└─────────────────────────────────────────────────┘
```

---

## Tips for Best Performance

1. **Use Import Mode** for faster performance with small datasets
2. **Create Date Table** for proper time intelligence
3. **Hide unnecessary columns** to reduce model complexity
4. **Use measures instead of calculated columns** when possible
5. **Optimize data types** (dates as dates, numbers as integers where possible)

---

## Publishing & Sharing

### Option 1: Power BI Service (Cloud)

1. Save `.pbix` file
2. Click **Publish** → Select workspace
3. Share dashboard with stakeholders
4. Set up refresh schedule if needed

### Option 2: Export to PDF/PowerPoint

1. Click **File** → **Export**
2. Choose format
3. Include in portfolio or presentations

### Option 3: Share .pbix File

1. Save to `powerbi/` directory
2. Share file directly (but recipients need Power BI Desktop)

---

## Advanced: Python Integration

You can also use Python visuals in Power BI:

```python
# Python script visual example
import pandas as pd
import matplotlib.pyplot as plt

# Use dataset variable provided by Power BI
df = dataset

# Create visualization
plt.figure(figsize=(10, 6))
plt.plot(df['date_column'], df['metric_column'])
plt.title('Networking Metrics Over Time')
plt.show()
```

---

## Next Steps

- Load your cleaned data
- Build initial dashboard
- Iterate based on insights
- Share with your network!

**Happy analyzing!** 📊

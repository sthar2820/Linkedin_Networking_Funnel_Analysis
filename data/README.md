# Data Directory

## Structure

- `raw/` - Original LinkedIn export files (NOT tracked in git)
- `cleaned/` - Standardized, anonymized datasets
- `processed/` - Analytics-ready aggregated tables

## Raw Data Files (Place here)

Please add your LinkedIn export files to the `raw/` directory:

1. **Invitations.csv** - Connection requests sent/received
2. **Connections.csv** - Accepted connections
3. **messages.csv** - Direct message conversations
4. **guide_messages.csv** - LinkedIn guided messages
5. **learning_coach_messages.csv** - LinkedIn Learning interactions
6. **Comments.csv** - Public comments on posts

## How to Export LinkedIn Data

1. Go to LinkedIn Settings & Privacy
2. Click "Data privacy" in left sidebar
3. Select "Get a copy of your data"
4. Choose "Want something in particular?"
5. Select:
   - Connections
   - Messages
   - Invitations
   - Comments
6. Click "Request archive"
7. Wait for email notification (usually 24 hours)
8. Download ZIP file and extract
9. Copy relevant CSV files to this `raw/` directory

## Privacy Note

The `raw/` directory is git-ignored to protect your personal data. Only cleaned, anonymized data will be tracked.

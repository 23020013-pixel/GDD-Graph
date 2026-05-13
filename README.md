# Hetionet Explorer

A bioinformatics knowledge graph explorer built with FastAPI and Streamlit.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   Copy `.env.example` to `.env` and update the values.
   ```bash
   cp .env.example .env
   ```

3. **Run the API**:
   ```bash
   python -m api.main
   ```

4. **Run the UI**:
   ```bash
   streamlit run ui/app.py
   ```

## Features

- **Entity Search**: Look up Genes, Diseases, and Drugs.
- **Relationship Explorer**: Visualize connections using `streamlit-agraph`.
- **Drug Recommendation**: Discover potential treatments.
- **Pipeline Dashboard**: Monitor system health and data stats.

import streamlit as st
import sqlite3
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.set_page_config(page_title="🗞️ TrendPulse Dashboard", layout="wide")

# Connect to DB
def get_connection():
    return sqlite3.connect("data/trendpulse.db")

def fetch_data():
    conn = get_connection()
    articles = pd.read_sql_query("SELECT * FROM articles", conn)
    polls = pd.read_sql_query("SELECT * FROM polls", conn)
    results = pd.read_sql_query("SELECT * FROM poll_results", conn)
    conn.close()
    return articles, polls, results

articles, polls, results = fetch_data()

# Header Row with Title + KPIs
col0, col1, col2, col3 = st.columns([3, 1, 1, 1])
with col0:
    st.title("🗞️ TrendPulse Dashboard")
with col1:
    st.metric("📰 Articles", len(articles))
with col2:
    st.metric("📊 Polls", len(polls))
with col3:
    active_polls = results['tweet_id'].nunique()
    st.metric("✅ Active Polls", active_polls)

st.divider()

# Sidebar Filters for poll/run table
st.sidebar.header("📌 Filter Polls")
selected_run = st.sidebar.selectbox("Run ID", sorted(polls['run_id'].unique(), reverse=True))
selected_theme = st.sidebar.selectbox("Theme (Cluster)", ['All'] + sorted(polls['cluster_id'].dropna().unique()))
selected_date = st.sidebar.date_input("Date (Published)", None)

filtered_polls = polls.copy()
if selected_run:
    filtered_polls = filtered_polls[filtered_polls['run_id'] == selected_run]
if selected_theme != 'All':
    filtered_polls = filtered_polls[filtered_polls['cluster_id'] == selected_theme]
if selected_date:
    filtered_polls = filtered_polls[pd.to_datetime(filtered_polls['created_at']).dt.date == selected_date]

filtered_results = results[results['run_id'] == selected_run]

# Second Row - Polls Table & Details
left, right = st.columns([1.8, 1.2])

with left:
    st.subheader("📋 Polls Table")
    display_polls = filtered_polls[['run_id', 'cluster_id', 'question', 'created_at']].copy()
    st.dataframe(display_polls, use_container_width=True, height=300)

    selected_row = filtered_polls.iloc[0]

with right:
    st.subheader("📊 Poll Details")
    st.markdown(f"### 🟡 {selected_row['question']}")
    options = json.loads(selected_row['options'])
    poll_id = str(selected_row['id'])
    if poll_id in filtered_results['tweet_id'].values:
        poll_data = filtered_results[filtered_results['tweet_id'] == poll_id]
        for _, opt_row in poll_data.iterrows():
            st.progress(opt_row['vote_percent'] / 100.0, text=f"{opt_row['option_text']}: {opt_row['vote_percent']}%")
    else:
        for opt in options:
            st.write(f"🔘 {opt}")

st.divider()

# Filter for Metadata
st.sidebar.header("📁 Filter Articles")
selected_source = st.sidebar.selectbox("Source", ['All'] + sorted(articles['source'].dropna().unique()))
selected_cluster = st.sidebar.selectbox("Cluster Label", ['All'] + sorted(articles['cluster_id'].dropna().unique()))

filtered_articles = articles[articles['run_id'] == selected_run]
if selected_source != 'All':
    filtered_articles = filtered_articles[filtered_articles['source'] == selected_source]
if selected_cluster != 'All':
    filtered_articles = filtered_articles[filtered_articles['cluster_id'] == selected_cluster]

# Metadata Section
st.subheader("🧾 Article Metadata & Themes")
metadata_col1, metadata_col2 = st.columns([1.8, 1.2])

with metadata_col1:
    st.write("### 📄 Articles")
    st.dataframe(filtered_articles[['source', 'title', 'published_at', 'cluster_id']], use_container_width=True, height=300)

with metadata_col2:
    st.write("### 📈 Theme-wise Poll Trends")
    if not filtered_results.empty:
        poll_trend_df = filtered_polls.copy()
        poll_trend_df['created_at'] = pd.to_datetime(poll_trend_df['created_at'])
        poll_trend_df = poll_trend_df.groupby([poll_trend_df['created_at'].dt.date, 'cluster_id']).size().reset_index(name='Polls')
        pivot_df = poll_trend_df.pivot(index='created_at', columns='cluster_id', values='Polls').fillna(0)
        st.line_chart(pivot_df)
    else:
        st.info("No poll data available for trend visualization.")

st.caption("🔁 Auto-refreshes on new ingestion runs.")

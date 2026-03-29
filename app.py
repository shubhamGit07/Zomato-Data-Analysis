import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Zomato Dashboard", layout="wide")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/shubh/Downloads/Zomato-data-.csv")
    return df

df = load_data()

# -----------------------------
# Data Cleaning
# -----------------------------
def handleRate(value):
    try:
        return float(str(value).split('/')[0])
    except:
        return np.nan

df['rate'] = df['rate'].apply(handleRate)

df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(str)
df['approx_cost(for two people)'] = df['approx_cost(for two people)'].str.replace(',', '')
df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(float)

df.dropna(inplace=True)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filter Options")

type_options = ["All"] + list(df['listed_in(type)'].unique())
restaurant_type = st.sidebar.selectbox("Select Restaurant Type", type_options)

order_options = ["All"] + list(df['online_order'].unique())
online_order = st.sidebar.selectbox("Online Order Available", order_options)

# Apply Filters
filtered_df = df.copy()

if restaurant_type != "All":
    filtered_df = filtered_df[filtered_df['listed_in(type)'] == restaurant_type]

if online_order != "All":
    filtered_df = filtered_df[filtered_df['online_order'] == online_order]

# -----------------------------
# TITLE
# -----------------------------
st.title("🍽️ Zomato Data Analysis Dashboard")
st.markdown("### 📊 Interactive Data Dashboard for Zomato Analysis")

# -----------------------------
# CHECK DATA SIZE
# -----------------------------
if len(filtered_df) < 5:
    st.warning("⚠️ Not enough data. Try different filter options.")

# -----------------------------
# KPI METRICS
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Restaurants", len(filtered_df))
col2.metric("Average Rating", round(filtered_df['rate'].mean(), 2) if len(filtered_df) > 0 else 0)
col3.metric("Max Votes", int(filtered_df['votes'].max()) if len(filtered_df) > 0 else 0)

# -----------------------------
# SHOW DATA
# -----------------------------
if st.checkbox("Show Raw Data"):
    st.write(filtered_df.head())

# -----------------------------
# CHART 1: Restaurant Type
# -----------------------------
st.subheader("📌 Restaurant Type Distribution")

if len(filtered_df) > 0:
    fig1, ax1 = plt.subplots()
    sns.countplot(x=filtered_df['listed_in(type)'], palette='coolwarm', ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

# -----------------------------
# CHART 2: Ratings Distribution
# -----------------------------
st.subheader("⭐ Ratings Distribution")

if len(filtered_df) > 0:
    fig2, ax2 = plt.subplots()
    ax2.hist(filtered_df['rate'], bins=10)
    st.pyplot(fig2)

# -----------------------------
# CHART 3: Online Order vs Rating
# -----------------------------
st.subheader("📦 Online Order vs Rating")

if filtered_df['online_order'].nunique() > 1:
    fig3, ax3 = plt.subplots()
    sns.boxplot(x='online_order', y='rate', data=filtered_df, palette='Set2', ax=ax3)
    st.pyplot(fig3)
else:
    st.info("Not enough categories to show boxplot")

# -----------------------------
# CHART 4: Cost vs Rating
# -----------------------------
st.subheader("💰 Cost vs Rating")

if len(filtered_df) > 0:
    fig4, ax4 = plt.subplots()
    sns.scatterplot(
        x='approx_cost(for two people)',
        y='rate',
        data=filtered_df,
        ax=ax4
    )
    st.pyplot(fig4)

# -----------------------------
# TOP RESTAURANTS
# -----------------------------
st.subheader("🏆 Top 5 Restaurants")

if len(filtered_df) > 0:
    top5 = filtered_df.sort_values(by='rate', ascending=False).head(5)
    st.write(top5[['name', 'rate', 'votes']])

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("💡 Key Insights")

st.write("✔️ Online ordering restaurants tend to have better ratings")
st.write("✔️ Most restaurants fall between 3.5 to 4.5 rating")
st.write("✔️ Cost does not always guarantee higher ratings")
st.write("✔️ Customer votes indicate restaurant popularity")


# TO RUN THIS TYPE PROJECT TYPE COMMAND
#  python -m streamlit run app.py
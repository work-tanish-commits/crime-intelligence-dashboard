import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Crime Intelligence Dashboard",
    layout="wide"
)

# -------------------
# LOAD DATA
# -------------------
df = pd.read_csv(r"C:\Users\sharm\Desktop\Crime data analysis\crime_dataset_india.csv")
df.columns = df.columns.str.strip()

# Convert date
df["Date of Occurrence"] = pd.to_datetime(df["Date of Occurrence"])

# -------------------
# SIDEBAR FILTERS
# -------------------
st.sidebar.title("Crime Dashboard Filters")

city = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique())[:5]
)

domain = st.sidebar.multiselect(
    "Crime Domain",
    options=sorted(df["Crime Domain"].dropna().unique()),
    default=sorted(df["Crime Domain"].dropna().unique())
)

gender = st.sidebar.multiselect(
    "Victim Gender",
    options=sorted(df["Victim Gender"].dropna().unique()),
    default=sorted(df["Victim Gender"].dropna().unique())
)

crime_type = st.sidebar.multiselect(
    "Crime Description",
    options=sorted(df["Crime Description"].dropna().unique()),
    default=sorted(df["Crime Description"].dropna().unique())[:5]
)

weapon = st.sidebar.multiselect(
    "Weapon Used",
    options=sorted(df["Weapon Used"].dropna().unique()),
    default=sorted(df["Weapon Used"].dropna().unique())[:5]
)

case_status = st.sidebar.multiselect(
    "Case Closed",
    options=df["Case Closed"].unique(),
    default=df["Case Closed"].unique()
)

age_range = st.sidebar.slider(
    "Victim Age Range",
    int(df["Victim Age"].min()),
    int(df["Victim Age"].max()),
    (18, 60)
)

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date of Occurrence"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date of Occurrence"].max()
)

search = st.sidebar.text_input("Search Crime Description")

# -------------------
# FILTER DATA
# -------------------
filtered = df[
    (df["City"].isin(city)) &
    (df["Crime Domain"].isin(domain)) &
    (df["Victim Gender"].isin(gender)) &
    (df["Crime Description"].isin(crime_type)) &
    (df["Weapon Used"].isin(weapon)) &
    (df["Case Closed"].isin(case_status)) &
    (df["Victim Age"].between(age_range[0], age_range[1])) &
    (df["Date of Occurrence"].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))
]

if search:
    filtered = filtered[
        filtered["Crime Description"].str.contains(search, case=False)
    ]

# -------------------
# HEADER
# -------------------
st.title("Crime Intelligence Analytics Dashboard")
st.markdown("---")

# -------------------
# KPI CARDS
# -------------------
a, b, c, d = st.columns(4)

a.metric("Total Crimes", len(filtered))
b.metric("Cities", filtered["City"].nunique())
c.metric("Crime Types", filtered["Crime Description"].nunique())
d.metric("Avg Victim Age", round(filtered["Victim Age"].mean(), 1))

st.markdown("---")

# -------------------
# TABS
# -------------------
tab1, tab2, tab3 = st.tabs([
    "Overview",
    "Demographics",
    "Operational Insights"
])

# -------------------
# OVERVIEW
# -------------------
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            filtered["Crime Description"].value_counts().head(10),
            title="Top Crime Categories"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(
            filtered,
            names="Case Closed",
            title="Case Closure Status"
        )
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.bar(
        filtered["City"].value_counts().head(10),
        title="Top Cities by Crime Volume"
    )
    st.plotly_chart(fig3, use_container_width=True)

# -------------------
# DEMOGRAPHICS
# -------------------
with tab2:
    col3, col4 = st.columns(2)

    with col3:
        fig4 = px.histogram(
            filtered,
            x="Victim Age",
            title="Victim Age Distribution"
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        fig5 = px.pie(
            filtered,
            names="Victim Gender",
            title="Victim Gender Distribution"
        )
        st.plotly_chart(fig5, use_container_width=True)

# -------------------
# OPERATIONAL
# -------------------
with tab3:
    col5, col6 = st.columns(2)

    with col5:
        fig6 = px.bar(
            filtered["Weapon Used"].value_counts().head(10),
            title="Weapons Used"
        )
        st.plotly_chart(fig6, use_container_width=True)

    with col6:
        fig7 = px.bar(
            filtered["Police Deployed"].value_counts(),
            title="Police Deployment"
        )
        st.plotly_chart(fig7, use_container_width=True)

# -------------------
# DOWNLOAD + DATA VIEW
# -------------------
st.markdown("---")

st.download_button(
    "Download Filtered Data",
    filtered.to_csv(index=False),
    "filtered_crime_data.csv"
)

if st.checkbox("Show Dataset Preview"):
    st.dataframe(filtered.head(50))

# Reset button
if st.sidebar.button("Reset Filters"):
    st.experimental_rerun()
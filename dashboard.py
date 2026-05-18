

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="InventoryIQ",
    page_icon="📦",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #050816,
            #0b1023,
            #111827
        );
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .main-title {
        font-size: 56px;
        font-weight: 800;
        color: white;
        margin-bottom: 8px;
        letter-spacing: -1px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 20px;
        margin-bottom: 25px;
    }

    div[data-testid="metric-container"] {
        background: rgba(17, 25, 40, 0.75);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 20px;
        border-radius: 22px;
        backdrop-filter: blur(12px);
        box-shadow: 0px 8px 30px rgba(0,0,0,0.35);
        transition: 0.3s ease;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border: 1px solid #7c3aed;
        box-shadow: 0px 12px 35px rgba(124,58,237,0.35);
    }

    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
    }

    div[data-testid="metric-container"] div {
        color: white !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 18px;
        background: rgba(17,25,40,0.65);
        padding: 12px;
        border-radius: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 14px;
        color: white;
        padding: 12px 22px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(
            135deg,
            #7c3aed,
            #2563eb
        ) !important;
        color: white !important;
    }

    .stButton > button {
        background: linear-gradient(
            135deg,
            #7c3aed,
            #2563eb
        );
        color: white;
        border: none;
        border-radius: 14px;
        padding: 12px 22px;
        font-weight: 700;
    }

    .stDownloadButton > button {
        background: linear-gradient(
            135deg,
            #06b6d4,
            #2563eb
        );
        color: white;
        border: none;
        border-radius: 14px;
        padding: 12px 22px;
        font-weight: 700;
    }

    .ai-badge {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(
            135deg,
            #7c3aed,
            #2563eb
        );
        color: white;
        padding: 14px 22px;
        border-radius: 50px;
        font-weight: bold;
        box-shadow: 0px 8px 30px rgba(124,58,237,0.5);
        z-index: 999;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# LOGIN SYSTEM
# ------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.title("🔐 InventoryIQ Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username == "admin"
            and
            password == "inventory123"
        ):

            st.session_state.authenticated = True
            st.rerun()

        else:

            st.error("Invalid credentials")

    st.stop()

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("📦 InventoryIQ")

uploaded_file = st.sidebar.file_uploader(
    "Upload Inventory CSV",
    type=["csv"]
)

if uploaded_file is None:

    st.warning("Please upload CSV file")
    st.stop()

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

@st.cache_data

def load_data(file):

    df = pd.read_csv(file)

    df['Date'] = pd.to_datetime(df['Date'])

    return df


df = load_data(uploaded_file)

# ------------------------------------------------
# FILTERS
# ------------------------------------------------

st.sidebar.subheader("🔍 Filters")

category_filter = st.sidebar.selectbox(
    "Category",
    ["All"] + list(df['Category'].unique())
)

region_filter = st.sidebar.selectbox(
    "Region",
    ["All"] + list(df['Region'].unique())
)

season_filter = st.sidebar.selectbox(
    "Season",
    ["All"] + list(df['Seasonality'].unique())
)

filtered_df = df.copy()

if category_filter != "All":

    filtered_df = filtered_df[
        filtered_df['Category'] == category_filter
    ]

if region_filter != "All":

    filtered_df = filtered_df[
        filtered_df['Region'] == region_filter
    ]

if season_filter != "All":

    filtered_df = filtered_df[
        filtered_df['Seasonality'] == season_filter
    ]

# ------------------------------------------------
# ADVANCED METRICS
# ------------------------------------------------

filtered_df['Revenue'] = (
    filtered_df['Units Sold']
    * filtered_df['Price']
)

filtered_df['Estimated Profit'] = (
    filtered_df['Revenue'] * 0.30
)

filtered_df['Turnover Ratio'] = (
    filtered_df['Units Sold']
    / filtered_df['Inventory Level']
)

# ------------------------------------------------
# MAIN HEADER
# ------------------------------------------------

st.markdown(
    '<div class="main-title">📦 InventoryIQ</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI Inventory Forecasting Platform</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------
# TABS
# ------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "🤖 Forecasting",
    "📄 Reports",
    "🧠 AI Assistant"
])

# ------------------------------------------------
# DASHBOARD TAB
# ------------------------------------------------

with tab1:

    st.markdown(
        """
        <div style='padding:18px 0;'>
            <h2 style='color:white;'>📊 Executive Dashboard</h2>
            <p style='color:#94a3b8;'>
                Real-time inventory analytics and AI-driven forecasting insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric(
        "Total Units Sold",
        f"{int(filtered_df['Units Sold'].sum()):,}"
    )

    col2.metric(
        "Inventory Level",
        f"{int(filtered_df['Inventory Level'].sum()):,}"
    )

    col3.metric(
        "Average Price",
        round(filtered_df['Price'].mean(), 2)
    )

    col4.metric(
        "Revenue",
        f"${round(filtered_df['Revenue'].sum(),2):,}"
    )

    col5.metric(
        "Estimated Profit",
        f"${round(filtered_df['Estimated Profit'].sum(),2):,}"
    )

    col6.metric(
        "Forecast Avg",
        round(filtered_df['Demand Forecast'].mean(), 2)
    )

    st.markdown("---")

    # SALES TREND

    st.subheader("📈 Sales Trend Analysis")

    sales_trend = filtered_df.groupby(
        'Date'
    )['Units Sold'].sum().reset_index()

    fig = px.line(
        sales_trend,
        x='Date',
        y='Units Sold',
        template='plotly_dark'
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="sales_chart"
    )

    # REVENUE ANALYSIS

    st.subheader("💰 Revenue Analysis")

    revenue_trend = filtered_df.groupby(
        'Date'
    )['Revenue'].sum().reset_index()

    revenue_fig = px.area(
        revenue_trend,
        x='Date',
        y='Revenue',
        template='plotly_dark'
    )

    st.plotly_chart(
        revenue_fig,
        use_container_width=True,
        key="revenue_chart"
    )

    # TOP CATEGORIES

    st.subheader("🏆 Top Selling Categories")

    category_sales = filtered_df.groupby(
        'Category'
    )['Units Sold'].sum().reset_index()

    bar_fig = px.bar(
        category_sales,
        x='Category',
        y='Units Sold',
        color='Category',
        template='plotly_dark'
    )

    st.plotly_chart(
        bar_fig,
        use_container_width=True,
        key="category_chart"
    )

    # REGION PERFORMANCE

    st.subheader("🌍 Region Performance")

    region_sales = filtered_df.groupby(
        'Region'
    )['Units Sold'].sum().reset_index()

    pie_fig = px.pie(
        region_sales,
        names='Region',
        values='Units Sold',
        template='plotly_dark'
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True,
        key="region_chart"
    )

    # TURNOVER

    st.subheader("📦 Stock Turnover")

    turnover_data = filtered_df.groupby(
        'Category'
    )['Turnover Ratio'].mean().reset_index()

    turnover_fig = px.bar(
        turnover_data,
        x='Category',
        y='Turnover Ratio',
        color='Category',
        template='plotly_dark'
    )

    st.plotly_chart(
        turnover_fig,
        use_container_width=True,
        key="turnover_chart"
    )

    # LOW STOCK

    st.subheader("🚨 Low Stock Alerts")

    low_stock = filtered_df[
        filtered_df['Inventory Level'] < 100
    ]

    st.dataframe(
        low_stock[
            [
                'Product ID',
                'Category',
                'Inventory Level',
                'Region'
            ]
        ].head(20),
        use_container_width=True
    )

    # DATA PREVIEW

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        filtered_df.head(20),
        use_container_width=True
    )

# ------------------------------------------------
# FORECAST TAB
# ------------------------------------------------

with tab2:

    st.subheader("🤖 AI Future Sales Forecast")

    forecast_data = sales_trend.rename(
        columns={
            'Date': 'ds',
            'Units Sold': 'y'
        }
    )

    model = Prophet()

    model.fit(forecast_data)

    future = model.make_future_dataframe(
        periods=30
    )

    forecast = model.predict(future)

    forecast_fig = px.line(
        forecast,
        x='ds',
        y='yhat',
        template='plotly_dark',
        title='30-Day Future Sales Prediction'
    )

    st.plotly_chart(
        forecast_fig,
        use_container_width=True,
        key="forecast_chart"
    )

    st.subheader("📅 Future Predictions")

    future_predictions = forecast[
        ['ds', 'yhat']
    ].tail(30)

    future_predictions.columns = [
        'Date',
        'Predicted Sales'
    ]

    st.dataframe(
        future_predictions,
        use_container_width=True
    )

# ------------------------------------------------
# PDF REPORT FUNCTION
# ------------------------------------------------


def generate_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        "InventoryIQ Business Report",
        styles['Title']
    )

    story.append(title)
    story.append(Spacer(1, 20))

    metrics = [
        f"Total Units Sold: {int(filtered_df['Units Sold'].sum())}",
        f"Revenue: ${round(filtered_df['Revenue'].sum(),2)}",
        f"Estimated Profit: ${round(filtered_df['Estimated Profit'].sum(),2)}",
        f"Average Price: {round(filtered_df['Price'].mean(),2)}"
    ]

    for item in metrics:

        paragraph = Paragraph(
            item,
            styles['BodyText']
        )

        story.append(paragraph)
        story.append(Spacer(1, 10))

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

# ------------------------------------------------
# REPORT TAB
# ------------------------------------------------

with tab3:

    st.subheader("📄 Business Reports")

    pdf = generate_pdf()

    st.download_button(
        label="Download PDF Report",
        data=pdf,
        file_name="InventoryIQ_Report.pdf",
        mime="application/pdf"
    )

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download CSV Data",
        data=csv,
        file_name="InventoryIQ_Data.csv",
        mime="text/csv"
    )

# ------------------------------------------------
# AI ASSISTANT TAB
# ------------------------------------------------

with tab4:

    st.subheader("🧠 InventoryIQ AI Assistant")

    user_question = st.text_input(
        "Ask inventory-related questions"
    )

    if user_question:

        question = user_question.lower()

        if "total sales" in question:

            answer = (
                f"Total units sold are "
                f"{int(filtered_df['Units Sold'].sum())}"
            )

        elif "revenue" in question:

            answer = (
                f"Total revenue is "
                f"${round(filtered_df['Revenue'].sum(),2)}"
            )

        elif "profit" in question:

            answer = (
                f"Estimated profit is "
                f"${round(filtered_df['Estimated Profit'].sum(),2)}"
            )

        elif "top category" in question:

            top_category = category_sales.sort_values(
                by='Units Sold',
                ascending=False
            ).iloc[0]['Category']

            answer = (
                f"Top selling category is "
                f"{top_category}"
            )

        elif "top region" in question:

            top_region = region_sales.sort_values(
                by='Units Sold',
                ascending=False
            ).iloc[0]['Region']

            answer = (
                f"Top performing region is "
                f"{top_region}"
            )

        elif "low stock" in question:

            answer = (
                f"There are "
                f"{len(low_stock)} low stock products"
            )

        else:

            answer = (
                "I can answer questions about "
                "sales, revenue, categories, "
                "profit, regions, and inventory."
            )

        st.success(answer)

# ------------------------------------------------
# FLOATING AI BUTTON
# ------------------------------------------------

st.markdown(
    """
    <div class='floating-chat'>🤖 AI Assistant Active</div>
    """,
    unsafe_allow_html=True
)


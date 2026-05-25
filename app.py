import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_customer_churn_dataset.csv")

df = load_data()

# =====================================================
# COLOR PALETTE
# =====================================================

BG_COLOR = "#F4F7FB"
CARD_COLOR = "#FFFFFF"
PRIMARY = "#1E3A5F"
SECONDARY = "#4F8FBF"
ACCENT = "#7CC6A6"
TEXT = "#1C2430"
BORDER = "#DCE3EC"
SIDEBAR = "#EAF1F8"

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(f"""
<style>

/* MAIN APP */
.stApp {{
    background-color: {BG_COLOR};
}}

/* REMOVE EXTRA PADDING */
.block-container {{
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}}

/* SIDEBAR */
section[data-testid="stSidebar"] {{
    background-color: {SIDEBAR};
    border-right: 1px solid {BORDER};
    padding-top: 1rem;
}}

/* TITLES */
h1, h2, h3, h4 {{
    color: {PRIMARY};
    font-family: "Segoe UI";
}}

/* TEXT */
p, label, div {{
    color: {TEXT};
}}

/* KPI CARDS */
[data-testid="metric-container"] {{
    background: {CARD_COLOR};
    border: 1px solid {BORDER};
    border-top: 5px solid {PRIMARY};
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}}

/* CHART CONTAINERS */
.stPlotlyChart {{
    background-color: {CARD_COLOR};
    border-radius: 18px;
    border: 1px solid {BORDER};
    padding: 10px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}}

/* TABS */
button[data-baseweb="tab"] {{
    background-color: transparent;
    border-radius: 30px;
    color: {PRIMARY};
    border: 1px solid {BORDER};
    margin-right: 10px;
    font-weight: 600;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    background-color: {PRIMARY};
    color: white;
}}

/* FILTER TITLES */
.filter-title {{
    color: {PRIMARY};
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 6px;
    margin-top: 16px;
}}

/* SIDEBAR SUMMARY */
.summary-card {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 18px;
    margin-top: 20px;
}}

/* REMOVE STREAMLIT HEADER */
header {{
    visibility: hidden;
}}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(f"""
    <h1 style="
        font-size:34px;
        color:{PRIMARY};
        margin-bottom:25px;
    ">
    Filters
    </h1>
    """, unsafe_allow_html=True)

    # GENDER

    st.markdown(
        "<div class='filter-title'>Gender</div>",
        unsafe_allow_html=True
    )

    selected_gender = st.multiselect(
        "",
        options=df["Gender"].unique(),
        default=df["Gender"].unique(),
        label_visibility="collapsed"
    )

    # COUNTRY

    st.markdown(
        "<div class='filter-title'>Country</div>",
        unsafe_allow_html=True
    )

    selected_country = st.multiselect(
        "",
        options=df["Country"].unique(),
        default=df["Country"].unique(),
        label_visibility="collapsed"
    )

    # CHURN

    st.markdown(
        "<div class='filter-title'>Customer Status</div>",
        unsafe_allow_html=True
    )

    selected_churn = st.multiselect(
        "",
        options=df["Churned"].unique(),
        default=df["Churned"].unique(),
        label_visibility="collapsed"
    )

    # AGE RANGE

    st.markdown(
        "<div class='filter-title'>Age Range</div>",
        unsafe_allow_html=True
    )

    selected_age = st.slider(
        "",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (
            int(df["Age"].min()),
            int(df["Age"].max())
        ),
        label_visibility="collapsed"
    )

    # DISCOUNT RANGE

    st.markdown(
        "<div class='filter-title'>Discount Usage Rate</div>",
        unsafe_allow_html=True
    )

    discount_range = st.slider(
        "",
        float(df["Discount_Usage_Rate"].min()),
        float(df["Discount_Usage_Rate"].max()),
        (
            float(df["Discount_Usage_Rate"].min()),
            float(df["Discount_Usage_Rate"].max())
        ),
        label_visibility="collapsed"
    )

# =====================================================
# FILTER DATA
# =====================================================

filtered_df = df[
    (df["Gender"].isin(selected_gender)) &
    (df["Country"].isin(selected_country)) &
    (df["Churned"].isin(selected_churn)) &
    (df["Age"] >= selected_age[0]) &
    (df["Age"] <= selected_age[1]) &
    (df["Discount_Usage_Rate"] >= discount_range[0]) &
    (df["Discount_Usage_Rate"] <= discount_range[1])
]

# =====================================================
# SIDEBAR SUMMARY
# =====================================================

with st.sidebar:

    st.markdown(f"""
    <div class='summary-card'>

    <h4 style='margin-top:0;'>Dataset Info</h4>

    <p><b>Rows:</b> {len(filtered_df):,}</p>

    <p><b>Countries:</b> {len(selected_country)}</p>

    <p><b>Total Purchases:</b>
    {int(filtered_df['Total_Purchases'].sum()):,}
    </p>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown(f"""
<h1 style="
    font-size:52px;
    color:{PRIMARY};
    margin-bottom:10px;
">
E-Commerce Customer Behavior Dashboard
</h1>

<p style="
    font-size:18px;
    color:{TEXT};
    margin-top:0;
">
Analyze customer purchasing behavior,
engagement metrics, and churn trends.
</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Customer Trends",
    "Purchasing Behavior",
    "Correlation Analysis"
])

# =====================================================
# COMMON CHART STYLE
# =====================================================

chart_layout = dict(
    paper_bgcolor=CARD_COLOR,
    plot_bgcolor=CARD_COLOR,
    font_color=TEXT,
    height=470
)

# =====================================================
# TAB 1 - OVERVIEW
# =====================================================

with tab1:

    st.subheader("Executive Overview")

    st.markdown("<br>", unsafe_allow_html=True)

    # KPI ROW 1

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            "TOTAL PURCHASES",
            f"{int(filtered_df['Total_Purchases'].sum()):,}"
        )

    with kpi2:
        st.metric(
            "AVG ORDER VALUE",
            f"${round(filtered_df['Average_Order_Value'].mean(), 2)}"
        )

    with kpi3:
        st.metric(
            "AVG DISCOUNT",
            f"{round(filtered_df['Discount_Usage_Rate'].mean(), 2)}%"
        )

    with kpi4:
        churn_rate = filtered_df["Churned"].mean() * 100

        st.metric(
            "CHURN RATE",
            f"{round(churn_rate, 2)}%"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # CHART ROW

    col1, col2 = st.columns([1.4, 1])

    # PURCHASES BY AGE

    with col1:

        st.subheader("Purchases by Age")

        age_chart = px.scatter(
            filtered_df,
            x="Age",
            y="Total_Purchases",
            color="Gender",
            size="Average_Order_Value",
            color_discrete_sequence=[
                PRIMARY,
                SECONDARY,
                ACCENT
            ]
        )

        age_chart.update_layout(**chart_layout)

        st.plotly_chart(
            age_chart,
            use_container_width=True
        )

    # GENDER SPENDING

    with col2:

        st.subheader("Average Spending by Gender")

        gender_avg = (
            filtered_df
            .groupby("Gender")["Average_Order_Value"]
            .mean()
            .reset_index()
        )

        gender_chart = px.bar(
            gender_avg,
            x="Gender",
            y="Average_Order_Value",
            color="Gender",
            color_discrete_sequence=[
                PRIMARY,
                SECONDARY,
                ACCENT
            ]
        )

        gender_chart.update_layout(**chart_layout)

        st.plotly_chart(
            gender_chart,
            use_container_width=True
        )

# =====================================================
# TAB 2 - CUSTOMER TRENDS
# =====================================================

with tab2:

    st.subheader("Customer Engagement Trends")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # SESSION DURATION

    with col1:

        session_chart = px.scatter(
            filtered_df,
            x="Session_Duration_Avg",
            y="Total_Purchases",
            color="Country",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        session_chart.update_layout(**chart_layout)

        st.plotly_chart(
            session_chart,
            use_container_width=True
        )

    # LOGIN FREQUENCY

    with col2:

        login_chart = px.scatter(
            filtered_df,
            x="Login_Frequency",
            y="Total_Purchases",
            color="Gender",
            color_discrete_sequence=[
                PRIMARY,
                SECONDARY
            ]
        )

        login_chart.update_layout(**chart_layout)

        st.plotly_chart(
            login_chart,
            use_container_width=True
        )

# =====================================================
# TAB 3 - PURCHASING BEHAVIOR
# =====================================================

with tab3:

    st.subheader("Purchasing Behavior Analysis")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # DISCOUNT

    with col1:

        discount_chart = px.scatter(
            filtered_df,
            x="Discount_Usage_Rate",
            y="Total_Purchases",
            color="Gender",
            size="Average_Order_Value",
            color_discrete_sequence=[
                PRIMARY,
                SECONDARY
            ]
        )

        discount_chart.update_layout(**chart_layout)

        st.plotly_chart(
            discount_chart,
            use_container_width=True
        )

    # CHURN

    with col2:

        churn_chart = px.box(
            filtered_df,
            x="Churned",
            y="Total_Purchases",
            color="Churned",
            color_discrete_sequence=[
                PRIMARY,
                ACCENT
            ]
        )

        churn_chart.update_layout(**chart_layout)

        st.plotly_chart(
            churn_chart,
            use_container_width=True
        )

# =====================================================
# TAB 4 - CORRELATION ANALYSIS
# =====================================================

with tab4:

    st.subheader("Correlation Heatmap")

    st.markdown("<br>", unsafe_allow_html=True)

    corr_columns = [
        "Total_Purchases",
        "Session_Duration_Avg",
        "Pages_Per_Session",
        "Login_Frequency",
        "Wishlist_Items",
        "Discount_Usage_Rate",
        "Cart_Abandonment_Rate",
        "Customer_Service_Calls",
        "Social_Media_Engagement_Score"
    ]

    corr = filtered_df[corr_columns].corr()

    heatmap = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Tealgrn"
    )

    heatmap.update_layout(
        paper_bgcolor=CARD_COLOR,
        plot_bgcolor=CARD_COLOR,
        font_color=TEXT,
        height=650
    )

    st.plotly_chart(
        heatmap,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.caption(
    "University of Southeastern Philippines | Data Visualization | 2026"
)
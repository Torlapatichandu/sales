import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Candy Sales Executive Intelligence",
    layout="wide",
    page_icon="🍬",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS (Professional UI)
# ---------------------------------------------------
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg,#667eea,#764ba2);
    padding: 15px;
    border-radius: 12px;
    color: white;
    text-align:center;
}
.big-font {
    font-size:28px !important;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("candy_store_sales_data.csv")
    df["Profit"] = df["Revenue"] - df["Cost"]
    df["Margin"] = df["Profit"] / df["Revenue"]
    df["Margin_Percent"] = df["Margin"] * 100
    df["Cost_Per_Mile"] = df["Shipping_Cost"] / df["Shipping_Distance_Miles"]
    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("🍬 Candy Intelligence Filters")

factory = st.sidebar.multiselect(
    "Select Factory",
    df["Factory_ID"].unique(),
    default=df["Factory_ID"].unique()
)

product = st.sidebar.multiselect(
    "Select Product Line",
    df["Product_Line"].unique(),
    default=df["Product_Line"].unique()
)

customer = st.sidebar.multiselect(
    "Select Customer",
    df["Customer_ID"].unique(),
    default=df["Customer_ID"].unique()
)

df = df[
    (df["Factory_ID"].isin(factory)) &
    (df["Product_Line"].isin(product)) &
    (df["Customer_ID"].isin(customer))
]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🍬 Candy Sales Executive Intelligence Dashboard")
st.markdown("### Real-Time Revenue | Profit | Logistics | Customer Insights")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
avg_margin = df["Margin_Percent"].mean()
total_orders = df["Order_ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📊 Avg Margin", f"{avg_margin:.2f}%")
col4.metric("📦 Total Orders", total_orders)

st.divider()

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Overview",
    "💰 Sales Intelligence",
    "🚚 Logistics Intelligence",
    "👥 Customer Intelligence",
    "🧠 Advanced Analytics"
])

# ---------------------------------------------------
# EXECUTIVE TAB
# ---------------------------------------------------
with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Factory")

        factory_rev = df.groupby("Factory_ID")["Revenue"].sum().reset_index()

        fig = px.bar(
            factory_rev,
            x="Factory_ID",
            y="Revenue",
            color="Revenue",
            color_continuous_scale="Blues",
            text_auto=True
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Profit Distribution")

        fig2 = px.pie(
            df,
            names="Product_Line",
            values="Profit",
            hole=0.6,
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# SALES TAB
# ---------------------------------------------------
with tab2:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top Performing Products")

        top_products = (
            df.groupby("Product_Line")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig3 = px.bar(
            top_products,
            x="Revenue",
            y="Product_Line",
            orientation="h",
            color="Revenue",
            color_continuous_scale="Viridis"
        )

        st.plotly_chart(fig3, use_container_width=True)

    with col2:

        st.subheader("Revenue vs Profit")

        fig4 = px.scatter(
            df,
            x="Revenue",
            y="Profit",
            color="Factory_ID",
            size="Quantity",
            hover_data=["Product_Line"]
        )

        st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# LOGISTICS TAB
# ---------------------------------------------------
with tab3:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Shipping Efficiency")

        efficiency = (
            df.groupby("Factory_ID")["Cost_Per_Mile"]
            .mean()
            .reset_index()
        )

        fig5 = px.bar(
            efficiency,
            x="Factory_ID",
            y="Cost_Per_Mile",
            color="Cost_Per_Mile",
            color_continuous_scale="Reds"
        )

        st.plotly_chart(fig5, use_container_width=True)

    with col2:

        st.subheader("Distance vs Profit")

        fig6 = px.scatter(
            df,
            x="Shipping_Distance_Miles",
            y="Profit",
            color="Factory_ID",
            size="Revenue"
        )

        st.plotly_chart(fig6, use_container_width=True)

# ---------------------------------------------------
# CUSTOMER TAB
# ---------------------------------------------------
with tab4:

    st.subheader("Top Customers")

    customers = (
        df.groupby("Customer_ID")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .head(10)
    )

    fig7 = px.bar(
        customers,
        x="Customer_ID",
        y="Profit",
        color="Profit",
        color_continuous_scale="Purples"
    )

    st.plotly_chart(fig7, use_container_width=True)

# ---------------------------------------------------
# ADVANCED TAB
# ---------------------------------------------------
with tab5:

    st.subheader("🏆 Top 10 Most Profitable Product Lines")

    top_products = (
        df.groupby("Product_Line")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig1 = px.bar(
        top_products,
        x="Profit",
        y="Product_Line",
        orientation="h",
        text_auto=True,
        color="Profit",
        color_continuous_scale="Viridis",
        title="Top Profit Generating Products"
    )

    fig1.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)


    # ----------------------------------------------------------
    st.subheader("🏭 Factory Profit Performance Ranking")

    factory_rank = (
        df.groupby("Factory_ID")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig2 = px.bar(
        factory_rank,
        x="Factory_ID",
        y="Profit",
        text_auto=True,
        color="Profit",
        color_continuous_scale="Blues",
        title="Factory Profit Ranking"
    )

    fig2.update_layout(template="plotly_dark", height=450)

    st.plotly_chart(fig2, use_container_width=True)


    # ----------------------------------------------------------
    st.subheader("💰 Revenue vs Profit (Business Efficiency)")

    fig3 = px.scatter(
        df,
        x="Revenue",
        y="Profit",
        color="Factory_ID",
        size="Quantity",
        hover_name="Product_Line",
        title="Revenue vs Profit Efficiency",
        opacity=0.7
    )

    fig3.update_layout(template="plotly_dark", height=500)

    st.plotly_chart(fig3, use_container_width=True)


    # ----------------------------------------------------------
    st.subheader("🚚 Shipping Efficiency Ranking")

    efficiency = (
        df.groupby("Factory_ID")["Cost_Per_Mile"]
        .mean()
        .sort_values()
        .reset_index()
    )

    fig4 = px.bar(
        efficiency,
        x="Factory_ID",
        y="Cost_Per_Mile",
        text_auto=True,
        color="Cost_Per_Mile",
        color_continuous_scale="RdYlGn_r",
        title="Shipping Cost Efficiency (Lower is Better)"
    )

    fig4.update_layout(template="plotly_dark", height=450)

    st.plotly_chart(fig4, use_container_width=True)


    # ----------------------------------------------------------
    st.subheader("📊 Executive Business Summary")

    col1, col2, col3 = st.columns(3)

    best_factory = factory_rank.iloc[0]["Factory_ID"]
    best_product = top_products.iloc[0]["Product_Line"]
    avg_profit = int(df["Profit"].mean())

    col1.success(f"🏭 Best Factory: {best_factory}")
    col2.success(f"🍬 Best Product: {best_product}")
    col3.success(f"💰 Avg Profit per Order: ${avg_profit}")


    # ----------------------------------------------------------
    st.subheader("📥 Download Business Report")

    report = df.groupby("Factory_ID").agg({
        "Revenue": "sum",
        "Profit": "sum",
        "Quantity": "sum"
    }).reset_index()

    st.download_button(
        "Download Full Executive Report",
        report.to_csv(index=False),
        "executive_business_report.csv"
    )
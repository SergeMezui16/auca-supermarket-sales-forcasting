import streamlit as st
import pandas as pd
import io
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Kigali Supermarket Sales Forecasting App")

# --- Hide forms when file is uploaded ---
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    # Read uploaded CSV
    df = pd.read_csv(uploaded_file)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]  # Normalize column names

    # 2. Column mapping
    st.sidebar.header("🧩 Column Mapping")
    mapped_columns = {
        "product_id": st.sidebar.selectbox("Product ID column", df.columns),
        "product_name": st.sidebar.selectbox("Product Name column", df.columns),
        "price": st.sidebar.selectbox("Price column", df.columns),
        "quantity": st.sidebar.selectbox("Quantity column", df.columns),
        "total_price": st.sidebar.selectbox("Total Price column", df.columns),
        "date": st.sidebar.selectbox("Date/Hour column", df.columns),
        "category": st.sidebar.selectbox("Category column", df.columns),
    }

    # 3. Rename based on mapping
    df = df.rename(columns={v: k for k, v in mapped_columns.items()})

    # 4. Parse the date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if df.empty or df["quantity"].isna().sum() > len(df) - 2 or len(df.dropna()) < 2:  # Check for valid data
        st.error("Not enough valid data to run forecasting. Please upload more data.")
    else:
        # --- Product Selector ---
        product_selected = st.selectbox("Select a product to analyze", df["product_name"].unique())
        df_product = df[df["product_name"] == product_selected]

        # --- Daily Aggregation ---
        daily_sales = df_product.groupby("date").agg({
            "quantity": "sum",
            "total_price": "sum"
        }).reset_index()

        st.subheader("📈 Daily Sales Trend")
        fig = px.line(daily_sales, x="date", y="quantity", title=f"Daily Quantity Sold — {product_selected}")
        st.plotly_chart(fig, use_container_width=True)

        # --- Forecasting with Prophet ---
        st.subheader("🔮 Sales Forecast (Next 30 Days)")
        prophet_df = daily_sales.rename(columns={"date": "ds", "quantity": "y"})

        model = Prophet()
        model.fit(prophet_df)

        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        st.plotly_chart(plot_plotly(model, forecast), use_container_width=True)

        # --- Forecast Table ---
        st.write("Forecast Table (Last 10 Days):")
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10))

        # --- Inventory Suggestion ---
        avg_daily = prophet_df["y"].mean()
        reorder_point = avg_daily * 7
        safety_stock = avg_daily * 2

        st.subheader("📦 Inventory Suggestion")
        st.markdown(f"""
        - **Average Daily Sales:** {avg_daily:.2f} units  
        - **Recommended Reorder Point:** {reorder_point:.0f} units (7 days lead time)  
        - **Safety Stock:** {safety_stock:.0f} units  
        """)

else:

    st.info("Please upload your sales data CSV to begin analysis.")
    # --- 📥 Example CSV Download ---
    st.subheader("📥 Download Example CSV Template")

    example_data = pd.DataFrame({
        "Product id": ["P001", "P002", "P003"],
        "Product name": ["Ubururu Soap", "Akabanga", "Nido Milk"],
        "Price": [1200, 500, 7500],
        "Quantity": [2, 5, 1],
        "Total Price": [2400, 2500, 7500],
        "date/hour": ["2024-11-01 08:00", "2024-11-01 10:30", "2024-11-01 12:15"],
        "category": ["Hygiene", "Food", "Dairy"]
    })

    csv_buffer = io.StringIO()
    example_data.to_csv(csv_buffer, index=False)
    csv_contents = csv_buffer.getvalue()

    st.download_button(
        label="📄 Download Example CSV",
        data=csv_contents,
        file_name="example_sales_data.csv",
        mime="text/csv",
    )

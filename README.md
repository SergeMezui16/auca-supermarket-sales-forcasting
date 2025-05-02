# 📊 Kigali Supermarket Sales Forecasting App

## Description
The Kigali Supermarket Sales Forecasting App is a Streamlit-based web application designed to help supermarket managers and analysts forecast sales trends and make data-driven decisions. The app allows users to upload sales data in CSV format, visualize daily sales trends, and generate 30-day sales forecasts using the Prophet forecasting model. Additionally, it provides inventory suggestions based on average daily sales.

## Purpose
The primary purpose of this app is to:
- Enable supermarkets to analyze historical sales data.
- Provide accurate sales forecasts for better inventory management.
- Help businesses optimize stock levels and reduce wastage.
- Offer an intuitive and user-friendly interface for data visualization and forecasting.

## Features
- Upload sales data in CSV format.
- Map columns dynamically to match the required format.
- Visualize daily sales trends for selected products.
- Generate 30-day sales forecasts using the Prophet model.
- Provide inventory suggestions, including reorder points and safety stock levels.
- Download an example CSV template for easy data preparation.

## Setting Up the Project

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```
4. Open the app in your browser. By default, it will be available at http://localhost:8501.


### Example CSV Template
If you don't have sales data ready, you can download the example CSV template directly from the app. The template includes the following columns:

- Product id
- Product name
- Price
- Quantity
- Total Price
- date/hour
- category

#### Dependencies
The project uses the following Python libraries:

- streamlit for building the web application.
- pandas for data manipulation.
- prophet for time series forecasting.
- plotly for interactive visualizations.
- Contributing
- Contributions are welcome! Feel free to fork the repository and submit a pull request.

#### License
This project is licensed under the MIT License. See the LICENSE file for details. ```
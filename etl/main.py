import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import logging

# --- SETUP LOGGING ---
logging.basicConfig(
    filename='output/etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- ETL FUNCTIONS ---

def load_data(files):
    """
    Load multi-CSV sales data, add Month column based on filename.
    """
    df_list = []
    for f in files:
        # Extract month from filename (e.g., sales_jan.csv -> Jan)
        month = f.split('_')[1].split('.')[0].capitalize()
        df = pd.read_csv(f)
        df['Month'] = month
        df_list.append(df)
    
    df = pd.concat(df_list, ignore_index=True)
    logging.info("Loaded data from %d files", len(files))
    return df

def clean_sales_column(df):
    """
    Clean Sales column: convert to numeric, remove invalid + outliers.
    """
    # Convert Sales to numeric (errors jadi NaN)
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    
    # Log invalid (NaN) values
    n_invalid = df['Sales'].isna().sum()
    logging.info("Sales conversion: %d invalid rows removed", n_invalid)
    
    # Drop rows with invalid Sales
    df = df.dropna(subset=['Sales'])
    
    # Remove outliers (example: Sales > 1,000,000)
    outliers = df[df['Sales'] > 1_000_000]
    logging.info("Removed %d outlier rows", len(outliers))
    df = df[df['Sales'] <= 1_000_000]
    
    return df

def save_to_db(df, engine):
    """
    Save cleaned data to DB and create index on Product.
    """
    df.to_sql('sales', con=engine, if_exists='replace', index=False)
    
    # Create index for faster queries
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_product ON sales(Product)"))
    
    logging.info("Data saved to DB and index created")

def query_summary(engine):
    """
    Query DB: get total sales per product and month.
    """
    query = """
    SELECT Product, Month, SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Product, Month
    ORDER BY Month, Product
    """
    df_summary = pd.read_sql(query, con=engine)
    logging.info("Queried sales summary (DB)")
    return df_summary

def export_summary(df_summary):
    """
    Export summary DataFrame to CSV.
    """
    out_path = "output/monthly_sales_summary.csv"
    df_summary.to_csv(out_path, index=False)
    logging.info("Exported summary to %s", out_path)
    print(f"✅ Summary saved to {out_path}")

def plot_summary(df_summary):
    """
    Generate bar chart of total sales per month.
    """
    df_plot = df_summary.groupby('Month')['Total_Sales'].sum().reindex(
        ['Jan', 'Feb', 'Mar'], fill_value=0
    )
    df_plot.plot(kind='bar', color='skyblue')
    plt.title('Total Sales per Month')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.tight_layout()
    
    plot_path = "output/sales_per_month.png"
    plt.savefig(plot_path)
    logging.info("Plot saved to %s", plot_path)
    print(f"✅ Plot saved to {plot_path}")
    plt.show()

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # Define source files + DB engine
    files = ["data/sales_jan.csv", "data/sales_feb.csv", "data/sales_mar.csv"]
    engine = create_engine("sqlite:///output/sales_data.db")
    
    # Run ETL pipeline
    df = load_data(files)
    df = clean_sales_column(df)
    save_to_db(df, engine)
    
    # Generate summary + report
    df_summary = query_summary(engine)
    export_summary(df_summary)
    plot_summary(df_summary)
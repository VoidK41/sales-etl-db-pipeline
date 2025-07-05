import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import logging

# Setup logging
logging.basicConfig(
    filename='output/etl.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def load_data(files):
    logging.info("Loading data from files: %s", files)
    df_list = []
    for f in files:
        month = f.split('_')[1].split('.')[0].capitalize()  # Extract month from filename
        df = pd.read_csv(f)
        df['Month'] = month
        df_list.append(df)
    df = pd.concat(df_list, ignore_index=True)
    logging.info("Data loaded with %d rows", len(df))
    return df

def clean_data(df):
    logging.info("Cleaning data")
    df.dropna(inplace=True)
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df.dropna(subset=["Sales"], inplace=True)
    logging.info("Data cleaned; remaining rows: %d", len(df))
    return df

def save_to_db(df, db_path="output/sales_data.db"):
    logging.info("Saving data to DB: %s", db_path)
    engine = create_engine(f'sqlite:///{db_path}')
    df.to_sql("sales", con=engine, if_exists="replace", index=False)
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_product ON sales(Product)"))
        logging.info("Index created on Product column")
    return engine

def query_summary(engine):
    logging.info("Querying summary from DB")
    query = """
    SELECT Product, SUM(Sales) as Total_Sales
    FROM sales
    GROUP BY Product
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        for row in result:
            print(row)

def get_summary_df(engine):
    logging.info("Fetching summary into Pandas DataFrame")
    query = """
    SELECT Product, SUM(Sales) as Total_Sales
    FROM sales
    GROUP BY Product
    """
    df_summary = pd.read_sql(query, con=engine)
    print(df_summary)
    return df_summary

def export_summary(engine):
    logging.info("Exporting summary to CSV")
    query = """
    SELECT Product, SUM(Sales) as Total_Sales
    FROM sales
    GROUP BY Product
    """
    df_summary = pd.read_sql(query, con=engine)
    df_summary.to_csv("output/sales_summary.csv", index=False)
    logging.info("Summary exported to output/sales_summary.csv")

def save_summary_csv(df_summary, path="output/sales_summary_v2.csv"):
    df_summary.to_csv(path, index=False)
    logging.info(f"Summary saved to {path}")

if __name__ == "__main__":
    files = ['data/sales_jan.csv', 'data/sales_feb.csv', 'data/sales_mar.csv']
    df = load_data(files)
    df = clean_data(df)
    engine = save_to_db(df)
    df_summary = get_summary_df(engine)
    save_summary_csv(df_summary)
    query_summary(engine)
    export_summary(engine)
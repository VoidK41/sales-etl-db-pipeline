import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import logging
import os

# Setup logging
logging.basicConfig(filename='output/etl.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(files):
    logging.info(f"Loading files: {files}")
    df_list = []
    for f in files:
        try:
            month = os.path.basename(f).split('_')[1].split('.')[0].capitalize()
            df = pd.read_csv(f)
            df['Month'] = month
            logging.info(f"{f}: {len(df)} rows loaded")
            df_list.append(df)
        except Exception as e:
            logging.error(f"Error loading {f}: {e}")
    df = pd.concat(df_list, ignore_index=True)
    logging.info(f"Total rows after concat: {len(df)}")
    return df

def clean_data(df):
    logging.info("Cleaning data")
    before = len(df)
    df.dropna(inplace=True)
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df.dropna(subset=['Sales'], inplace=True)
    after = len(df)
    logging.info(f"Rows before clean: {before}, after clean: {after}")
    return df

def save_to_db(df, db_path="output/sales_data.db"):
    logging.info(f"Saving data to DB at {db_path}")
    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql('sales', con=engine, if_exists='replace', index=False)
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_product ON sales(Product)"))
    logging.info("Data saved and index created")
    return engine

def query_summary(engine):
    query = """
    SELECT Product, SUM(Sales) as Total_Sales
    FROM sales
    GROUP BY Product
    """
    df_summary = pd.read_sql(query, con=engine)
    logging.info("Summary query completed")
    print(df_summary)
    return df_summary

def export_summary(df_summary):
    out_path = "output/sales_summary.csv"
    df_summary.to_csv(out_path, index=False)
    logging.info(f"Summary exported to {out_path}")

if __name__ == "__main__":
    files = ["data/sales_jan.csv", "data/sales_feb.csv", "data/sales_mar.csv"]
    df = load_data(files)
    df = clean_data(df)
    engine = save_to_db(df)
    df_summary = query_summary(engine)
    export_summary(df_summary)

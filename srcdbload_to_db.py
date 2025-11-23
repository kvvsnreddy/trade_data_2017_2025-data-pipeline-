# src/db/load_to_db.py
from sqlalchemy import create_engine
import pandas as pd

def load_to_database(df, db_url="postgresql+psycopg2://user:password@localhost/trade_analysis"):
    """Load processed data to SQL database"""
    engine = create_engine(db_url)
    
    # Load to database
    df.to_sql('shipments', engine, if_exists='replace', index=False)
    
    print("Data loaded to database successfully!")
    return engine

# Example usage
if __name__ == "__main__":
    # Load processed data
    df = pd.read_csv("data/processed/trade_cleaned.csv")
    
    # Load to database
    engine = load_to_database(df)